from pathlib import Path

from PIL import Image

from docpage2md_app.config import AppConfig
from docpage2md_app import vision_crop
from docpage2md_app.vision_crop import cleanup_vision_crop_cache, expand_bbox, map_bbox_to_image, resolve_vision_crop


def test_map_bbox_to_image_and_expand_clamps_with_min_padding():
    mapped = map_bbox_to_image([25, 25, 50, 50], page_size=[100, 100], image_size=(400, 400))

    assert mapped == [100, 100, 200, 200]
    assert expand_bbox(mapped, image_size=(220, 220), block_type="formula_block", profile="normal") == [76, 76, 220, 220]


def test_handwritten_padding_is_larger_than_normal():
    bbox = [100, 100, 200, 140]

    normal = expand_bbox(bbox, image_size=(500, 500), block_type="formula_block", profile="normal")
    handwritten = expand_bbox(bbox, image_size=(500, 500), block_type="formula_block", profile="handwritten")

    assert normal is not None
    assert handwritten is not None
    assert handwritten[0] < normal[0]
    assert handwritten[1] < normal[1]
    assert handwritten[2] > normal[2]
    assert handwritten[3] > normal[3]


def test_page_image_ref_is_preferred_over_pdf_render(tmp_path, monkeypatch):
    output_root = tmp_path / "out"
    page_dir = output_root / "assets" / "pages"
    crop_dir = output_root / "assets" / "crops"
    page_dir.mkdir(parents=True)
    crop_dir.mkdir(parents=True)
    page_image = page_dir / "page-1.png"
    original_crop = crop_dir / "formula.png"
    Image.new("RGB", (400, 400), "white").save(page_image)
    Image.new("RGB", (40, 20), "white").save(original_crop)
    page_ir = {"source_page": 1, "page_image_ref": "assets/pages/page-1.png", "page_size": [100, 100]}
    block = {
        "id": "p0001-b001",
        "type": "formula_block",
        "bbox": [30, 30, 50, 40],
        "crop_ref": "assets/crops/formula.png",
    }
    monkeypatch.setattr(vision_crop, "_render_pdf_page_cached", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("pdf render should not run")))

    resolved = resolve_vision_crop(page_ir, block, output_root, AppConfig(document_type="handwritten_notes"), source_pdf=tmp_path / "missing.pdf")

    assert resolved.path is not None
    assert resolved.path.exists()
    assert resolved.path != original_crop
    assert resolved.audit["crop_strategy"] == "expanded_from_page_image"
    assert resolved.audit["render_backend"] == "page_image_ref"
    assert resolved.audit["padding_profile"] == "handwritten"


def test_missing_bbox_falls_back_to_original_crop(tmp_path):
    output_root = tmp_path / "out"
    crop_dir = output_root / "assets" / "crops"
    crop_dir.mkdir(parents=True)
    original_crop = crop_dir / "formula.png"
    Image.new("RGB", (40, 20), "white").save(original_crop)
    block = {"id": "p0001-b001", "type": "formula_block", "crop_ref": "assets/crops/formula.png"}

    resolved = resolve_vision_crop({"source_page": 1}, block, output_root, AppConfig())

    assert resolved.path == original_crop
    assert resolved.audit["fallback_used"] is True
    assert resolved.audit["fallback_reason"] == "missing_bbox"


def test_pdf_page_render_cache_reuses_same_rendered_page(tmp_path, monkeypatch):
    output_root = tmp_path / "out"
    source_pdf = tmp_path / "source.pdf"
    source_pdf.write_bytes(b"%PDF")
    calls = {"count": 0}

    def fake_render(_pdf_path: Path, _source_page: int, *, dpi: int, output_path: Path):
        calls["count"] += 1
        Image.new("RGB", (300, 300), "white").save(output_path)
        return vision_crop._RenderedPage(output_path, "fake")

    monkeypatch.setattr(vision_crop, "_render_pdf_page", fake_render)
    page_ir = {"source_page": 1, "page_size": [100, 100]}
    block_a = {"id": "p0001-b001", "type": "formula_block", "bbox": [10, 10, 30, 20]}
    block_b = {"id": "p0001-b002", "type": "formula_block", "bbox": [40, 40, 60, 50]}

    first = resolve_vision_crop(page_ir, block_a, output_root, AppConfig(), source_pdf=source_pdf)
    second = resolve_vision_crop(page_ir, block_b, output_root, AppConfig(), source_pdf=source_pdf)

    assert first.path and first.path.exists()
    assert second.path and second.path.exists()
    assert calls["count"] == 1
    assert second.audit["render_backend"] == "cache"


def test_vision_crop_cache_cleanup_respects_retention(tmp_path):
    slim_root = tmp_path / "slim"
    debug_root = tmp_path / "debug"
    (slim_root / ".vision_crop_cache").mkdir(parents=True)
    (debug_root / ".vision_crop_cache").mkdir(parents=True)

    cleanup_vision_crop_cache(slim_root, AppConfig(output_retention="slim"))
    cleanup_vision_crop_cache(debug_root, AppConfig(output_retention="debug"))

    assert not (slim_root / ".vision_crop_cache").exists()
    assert (debug_root / ".vision_crop_cache").exists()
