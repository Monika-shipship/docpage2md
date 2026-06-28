from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from .config import AppConfig, normalize_vision_crop_dpi, normalize_vision_crop_mode, normalize_vision_crop_padding_profile


VISION_CROP_CACHE_DIR = ".vision_crop_cache"


@dataclass(frozen=True)
class ResolvedVisionCrop:
    path: Path | None
    audit: dict[str, Any]


def resolve_vision_crop(
    page_ir: dict[str, Any],
    block: dict[str, Any],
    output_root: str | Path,
    config: AppConfig,
    *,
    source_pdf: str | Path | None = None,
    retry: bool = False,
    override_dpi: int | None = None,
    override_padding_profile: str | None = None,
) -> ResolvedVisionCrop:
    """Resolve the image sent to crop Vision.

    The resolver prefers recropping from a full page image or the original PDF
    because parser-provided block crops are often too tight for handwritten
    formulas. It does not mutate the block asset refs used by Markdown output.
    """
    output_root = Path(output_root)
    original_path = resolve_original_block_image_path(block, output_root)
    mode = normalize_vision_crop_mode(getattr(config, "vision_crop_mode", None))
    profile = _effective_padding_profile(config, block, override_padding_profile)
    dpi = _effective_dpi(config, block, profile, override_dpi)
    source_page = _source_page(page_ir, block)
    audit = {
        "crop_strategy": "original_crop" if mode == "original" else "expanded_from_page",
        "source_page": source_page,
        "render_dpi": dpi,
        "original_bbox": _bbox_from_block(block),
        "expanded_bbox": None,
        "padding_profile": profile,
        "padding_ratio": _padding_ratio(block.get("type"), profile),
        "fallback_used": False,
        "fallback_reason": None,
        "render_backend": None,
        "retry": bool(retry),
    }

    if mode == "original":
        audit["crop_strategy"] = "original_crop"
        audit["fallback_used"] = False
        return ResolvedVisionCrop(original_path, audit)

    expanded = _try_expanded_crop(
        page_ir,
        block,
        output_root,
        source_pdf=source_pdf,
        source_page=source_page,
        dpi=dpi,
        profile=profile,
        retry=retry,
        audit=audit,
    )
    if expanded.path is not None:
        return expanded

    fallback_audit = dict(expanded.audit)
    fallback_audit["crop_strategy"] = "fallback_original_crop"
    fallback_audit["fallback_used"] = True
    if not fallback_audit.get("fallback_reason"):
        fallback_audit["fallback_reason"] = "expanded_crop_unavailable"
    return ResolvedVisionCrop(original_path, fallback_audit)


def resolve_original_block_image_path(block: dict[str, Any], output_root: str | Path) -> Path | None:
    output_root = Path(output_root)
    for key in ("crop_ref", "image_ref", "table_image_path", "formula_image_path", "path", "image_path"):
        value = str(block.get(key) or "").strip()
        if not value:
            continue
        path = Path(value)
        if not path.is_absolute():
            path = output_root / path
        return path
    return None


def map_bbox_to_image(
    bbox: list[float],
    *,
    page_size: Any,
    image_size: tuple[int, int],
) -> list[float] | None:
    if len(bbox) != 4:
        return None
    img_w, img_h = image_size
    if img_w <= 0 or img_h <= 0:
        return None
    page_w, page_h = _page_size_pair(page_size)
    x1, y1, x2, y2 = [float(value) for value in bbox]
    if page_w and page_h:
        return [x1 / page_w * img_w, y1 / page_h * img_h, x2 / page_w * img_w, y2 / page_h * img_h]
    max_x = max(x1, x2)
    max_y = max(y1, y2)
    if max_x <= img_w * 1.05 and max_y <= img_h * 1.05:
        return [x1, y1, x2, y2]
    return None


def expand_bbox(
    bbox: list[float],
    *,
    image_size: tuple[int, int],
    block_type: str | None,
    profile: str,
) -> list[int] | None:
    if len(bbox) != 4:
        return None
    img_w, img_h = image_size
    x1, y1, x2, y2 = [float(value) for value in bbox]
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    if x2 <= x1 or y2 <= y1:
        return None
    ratio = _padding_ratio(block_type, profile)
    min_px = _min_padding_px(profile)
    pad_x = max(min_px, (x2 - x1) * float(ratio["x"]))
    pad_y = max(min_px, (y2 - y1) * float(ratio["y"]))
    left = max(0, int(round(x1 - pad_x)))
    top = max(0, int(round(y1 - pad_y)))
    right = min(img_w, int(round(x2 + pad_x)))
    bottom = min(img_h, int(round(y2 + pad_y)))
    if right <= left or bottom <= top:
        return None
    return [left, top, right, bottom]


def should_keep_vision_crop_cache(config: AppConfig) -> bool:
    return str(getattr(config, "output_retention", "slim") or "slim").strip().lower() == "debug"


def cleanup_vision_crop_cache(output_root: str | Path, config: AppConfig) -> None:
    if should_keep_vision_crop_cache(config):
        return
    cache_dir = Path(output_root) / VISION_CROP_CACHE_DIR
    if not cache_dir.exists():
        return
    import shutil

    shutil.rmtree(cache_dir, ignore_errors=True)


def _try_expanded_crop(
    page_ir: dict[str, Any],
    block: dict[str, Any],
    output_root: Path,
    *,
    source_pdf: str | Path | None,
    source_page: int | None,
    dpi: int,
    profile: str,
    retry: bool,
    audit: dict[str, Any],
) -> ResolvedVisionCrop:
    bbox = _bbox_from_block(block)
    if bbox is None:
        audit["fallback_reason"] = "missing_bbox"
        return ResolvedVisionCrop(None, audit)

    page_image = _resolve_page_image_ref(page_ir, output_root)
    render_backend = None
    if page_image is not None and page_image.exists():
        image_path = page_image
        render_backend = "page_image_ref"
    else:
        rendered = _render_pdf_page_cached(source_pdf, source_page, dpi=dpi, output_root=output_root)
        image_path = rendered.path
        render_backend = rendered.backend
        if image_path is None:
            audit["fallback_reason"] = rendered.error or "missing_page_image_and_source_pdf"
            audit["render_backend"] = rendered.backend
            return ResolvedVisionCrop(None, audit)

    try:
        with Image.open(image_path) as image:
            image_size = image.size
            mapped = map_bbox_to_image(bbox, page_size=_page_size(page_ir, block), image_size=image_size)
            if mapped is None:
                audit["fallback_reason"] = "bbox_coordinate_mapping_failed"
                audit["render_backend"] = render_backend
                return ResolvedVisionCrop(None, audit)
            expanded_bbox = expand_bbox(mapped, image_size=image_size, block_type=block.get("type"), profile=profile)
            if expanded_bbox is None:
                audit["fallback_reason"] = "expanded_bbox_invalid"
                audit["render_backend"] = render_backend
                return ResolvedVisionCrop(None, audit)
            crop_dir = output_root / VISION_CROP_CACHE_DIR / "crops"
            crop_dir.mkdir(parents=True, exist_ok=True)
            crop_path = crop_dir / _crop_file_name(block, source_page, dpi, profile, retry)
            image.crop(tuple(expanded_bbox)).save(crop_path)
    except Exception as exc:  # pragma: no cover - exercised through fallback tests with monkeypatches.
        audit["fallback_reason"] = f"crop_failed:{type(exc).__name__}"
        audit["render_backend"] = render_backend
        return ResolvedVisionCrop(None, audit)

    audit["crop_strategy"] = "expanded_from_page_image" if render_backend == "page_image_ref" else "expanded_from_pdf_page"
    audit["expanded_bbox"] = expanded_bbox
    audit["render_backend"] = render_backend
    audit["fallback_used"] = False
    audit["fallback_reason"] = None
    return ResolvedVisionCrop(crop_path, audit)


@dataclass(frozen=True)
class _RenderedPage:
    path: Path | None
    backend: str | None
    error: str | None = None


def _render_pdf_page_cached(source_pdf: str | Path | None, source_page: int | None, *, dpi: int, output_root: Path) -> _RenderedPage:
    pdf_path = Path(str(source_pdf or "")).expanduser()
    if not source_pdf or not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        return _RenderedPage(None, None, "missing_source_pdf")
    if not source_page or source_page < 1:
        return _RenderedPage(None, None, "invalid_source_page")
    page_dir = output_root / VISION_CROP_CACHE_DIR / "pages"
    page_dir.mkdir(parents=True, exist_ok=True)
    out_path = page_dir / f"{_safe_stem(pdf_path.stem)}_p{source_page:04d}_{dpi}dpi.png"
    if out_path.exists():
        return _RenderedPage(out_path, "cache")
    return _render_pdf_page(pdf_path, source_page, dpi=dpi, output_path=out_path)


def _render_pdf_page(pdf_path: Path, source_page: int, *, dpi: int, output_path: Path) -> _RenderedPage:
    try:
        import fitz  # type: ignore

        doc = fitz.open(str(pdf_path))
        try:
            if source_page < 1 or source_page > doc.page_count:
                return _RenderedPage(None, "pymupdf", "source_page_out_of_range")
            scale = dpi / 72.0
            pix = doc.load_page(source_page - 1).get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
            pix.save(str(output_path))
            return _RenderedPage(output_path, "pymupdf")
        finally:
            doc.close()
    except Exception as fitz_exc:
        fallback = _render_pdf_page_with_pdf2image(pdf_path, source_page, dpi=dpi, output_path=output_path)
        if fallback.path is not None:
            return fallback
        return _RenderedPage(None, fallback.backend or "pymupdf", fallback.error or f"pymupdf_failed:{type(fitz_exc).__name__}")


def _render_pdf_page_with_pdf2image(pdf_path: Path, source_page: int, *, dpi: int, output_path: Path) -> _RenderedPage:
    try:
        from pdf2image import convert_from_path  # type: ignore
    except Exception:
        return _RenderedPage(None, "pdf2image", "pdf2image_unavailable")
    try:
        images = convert_from_path(str(pdf_path), dpi=dpi, first_page=source_page, last_page=source_page)
        if not images:
            return _RenderedPage(None, "pdf2image", "pdf2image_empty")
        images[0].save(output_path)
        return _RenderedPage(output_path, "pdf2image")
    except Exception as exc:
        return _RenderedPage(None, "pdf2image", f"pdf2image_failed:{type(exc).__name__}")


def _resolve_page_image_ref(page_ir: dict[str, Any], output_root: Path) -> Path | None:
    for key in ("page_image_ref", "image_ref", "path"):
        value = str(page_ir.get(key) or "").strip()
        if not value:
            continue
        path = Path(value)
        if not path.is_absolute():
            path = output_root / path
        return path
    return None


def _bbox_from_block(block: dict[str, Any]) -> list[float] | None:
    polygon = block.get("polygon")
    if polygon:
        points = _polygon_points(polygon)
        if points:
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            return [min(xs), min(ys), max(xs), max(ys)]
    bbox = block.get("bbox")
    if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        return None
    try:
        return [float(item) for item in bbox]
    except (TypeError, ValueError):
        return None


def _polygon_points(value: Any) -> list[tuple[float, float]]:
    raw_points: list[Any]
    if isinstance(value, (list, tuple)) and value and all(isinstance(item, (int, float)) for item in value):
        raw_points = list(zip(value[0::2], value[1::2]))
    elif isinstance(value, (list, tuple)):
        raw_points = list(value)
    else:
        raw_points = []
    points: list[tuple[float, float]] = []
    for point in raw_points:
        if isinstance(point, dict):
            x, y = point.get("x"), point.get("y")
        elif isinstance(point, (list, tuple)) and len(point) >= 2:
            x, y = point[0], point[1]
        else:
            continue
        try:
            points.append((float(x), float(y)))
        except (TypeError, ValueError):
            continue
    return points


def _page_size(page_ir: dict[str, Any], block: dict[str, Any]) -> Any:
    return block.get("page_size") or page_ir.get("page_size")


def _page_size_pair(value: Any) -> tuple[float | None, float | None]:
    if isinstance(value, dict):
        width = value.get("width") or value.get("w")
        height = value.get("height") or value.get("h")
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        width, height = value[0], value[1]
    else:
        return None, None
    try:
        width_f = float(width)
        height_f = float(height)
    except (TypeError, ValueError):
        return None, None
    if width_f <= 0 or height_f <= 0:
        return None, None
    return width_f, height_f


def _source_page(page_ir: dict[str, Any], block: dict[str, Any]) -> int | None:
    for source in (block, page_ir):
        try:
            value = int(source.get("source_page") or source.get("page") or 0)
        except (TypeError, ValueError):
            value = 0
        if value > 0:
            return value
    return None


def _effective_dpi(config: AppConfig, block: dict[str, Any], profile: str, override_dpi: int | None) -> int:
    dpi = normalize_vision_crop_dpi(override_dpi if override_dpi is not None else getattr(config, "vision_crop_dpi", None))
    if dpi:
        return dpi
    doc_type = str(getattr(config, "document_type", "") or "").strip()
    if doc_type in {"handwritten_notes", "complex_ppt"} or profile in {"handwritten", "aggressive"}:
        return 300
    if block.get("type") in {"formula_block", "formula_inline"} and doc_type == "custom":
        return 300
    return 200


def _effective_padding_profile(config: AppConfig, block: dict[str, Any], override_profile: str | None) -> str:
    profile = normalize_vision_crop_padding_profile(
        override_profile if override_profile is not None else getattr(config, "vision_crop_padding_profile", None)
    )
    if profile != "auto":
        return profile
    doc_type = str(getattr(config, "document_type", "") or "").strip()
    if doc_type in {"handwritten_notes", "complex_ppt"}:
        return "handwritten"
    return "normal"


def _padding_ratio(block_type: Any, profile: str) -> dict[str, float]:
    block_type = str(block_type or "")
    if block_type in {"formula_block", "formula_inline"}:
        if profile == "aggressive":
            return {"x": 0.30, "y": 0.45}
        if profile == "handwritten":
            return {"x": 0.20, "y": 0.35}
        return {"x": 0.10, "y": 0.15}
    if block_type == "table":
        return {"x": 0.10, "y": 0.12}
    if block_type in {"figure_note", "image_ref", "image"}:
        return {"x": 0.15, "y": 0.15}
    if profile == "aggressive":
        return {"x": 0.20, "y": 0.25}
    if profile == "handwritten":
        return {"x": 0.15, "y": 0.20}
    return {"x": 0.10, "y": 0.10}


def _min_padding_px(profile: str) -> int:
    if profile == "aggressive":
        return 72
    if profile == "handwritten":
        return 48
    return 24


def _crop_file_name(block: dict[str, Any], source_page: int | None, dpi: int, profile: str, retry: bool) -> str:
    block_id = _safe_stem(str(block.get("id") or "block"))
    retry_suffix = "_retry" if retry else ""
    return f"p{int(source_page or 0):04d}_{block_id}_{dpi}dpi_{profile}{retry_suffix}.png"


def _safe_stem(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")
    return safe[:80] or "item"


def crop_audit_preview(value: Any, max_chars: int = 240) -> str | None:
    if value in (None, "", [], {}):
        return None
    if isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            text = str(value)
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3].rstrip() + "..."
