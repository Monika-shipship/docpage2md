from __future__ import annotations

import copy
from typing import Any

from .artifacts import sha256_text
from .mineru_adapter import DOCUMENT_IR_SCHEMA_VERSION


DUAL_ADAPTER_VERSION = "dual-adapter-2026-06-25-v1"


def merge_mineru_paddleocr_ir(
    mineru_ir: dict[str, Any],
    paddleocr_ir: dict[str, Any],
    *,
    engine_mode: str = "dual_hybrid",
) -> dict[str, Any]:
    """Merge two parser IRs into a MinerU-led IR with PaddleOCR as evidence.

    MinerU remains the layout backbone because it already provides stable crops for
    hybrid enrichment. PaddleOCR contributes same-page text/formula/table evidence
    for the Brain refiner and audit report.
    """
    merged = copy.deepcopy(mineru_ir)
    paddle_pages = _pages_by_no(paddleocr_ir)
    pages = []
    for page in merged.get("pages") or []:
        source_page = int(page.get("source_page") or len(pages) + 1)
        paddle_page = paddle_pages.get(source_page)
        pages.append(_merge_page(page, paddle_page, source_page=source_page))

    existing_pages = {int(page.get("source_page") or 0) for page in pages}
    for source_page, paddle_page in sorted(paddle_pages.items()):
        if source_page in existing_pages:
            continue
        pages.append(_paddle_only_page(paddle_page, source_page=source_page))

    merged["schema_version"] = DOCUMENT_IR_SCHEMA_VERSION
    merged["adapter_version"] = DUAL_ADAPTER_VERSION
    merged["engine_mode"] = engine_mode
    merged["pages"] = sorted(pages, key=lambda page: int(page.get("source_page") or 0))
    merged["assets"] = list(mineru_ir.get("assets") or []) + _namespaced_assets(paddleocr_ir)
    merged["metadata"] = dict(merged.get("metadata") or {})
    merged["metadata"]["dual_parser"] = {
        "version": DUAL_ADAPTER_VERSION,
        "primary": "mineru",
        "secondary": "paddleocr",
        "mineru_pages": len(mineru_ir.get("pages") or []),
        "paddleocr_pages": len(paddleocr_ir.get("pages") or []),
        "merged_pages": len(merged["pages"]),
    }
    merged["source"] = {
        "input_path": _first_value((mineru_ir.get("source") or {}).get("input_path"), (paddleocr_ir.get("source") or {}).get("input_path")),
        "input_hash": _first_value((mineru_ir.get("source") or {}).get("input_hash"), (paddleocr_ir.get("source") or {}).get("input_hash")),
        "input_type": _first_value((mineru_ir.get("source") or {}).get("input_type"), (paddleocr_ir.get("source") or {}).get("input_type")),
        "mineru_artifact_root": (mineru_ir.get("source") or {}).get("artifact_root"),
        "paddleocr_artifact_root": (paddleocr_ir.get("source") or {}).get("artifact_root"),
    }
    return merged


def _merge_page(page: dict[str, Any], paddle_page: dict[str, Any] | None, *, source_page: int) -> dict[str, Any]:
    merged = copy.deepcopy(page)
    merged["source_page"] = source_page
    merged["source_engine"] = "dual"
    merged["parser_priority"] = ["mineru", "paddleocr"]
    merged["dual_evidence"] = _dual_evidence(page, paddle_page)
    merged["raw_text"] = _combined_raw_text(page, paddle_page)
    merged["raw_text_sha256"] = sha256_text(merged.get("raw_text") or "")
    for block in merged.get("blocks") or []:
        evidence = block.setdefault("evidence", {})
        evidence["dual_parser"] = {
            "primary": "mineru",
            "secondary": "paddleocr",
            "secondary_available": paddle_page is not None,
        }
    return merged


def _paddle_only_page(paddle_page: dict[str, Any], *, source_page: int) -> dict[str, Any]:
    page = copy.deepcopy(paddle_page)
    page["source_page"] = source_page
    page["source_engine"] = "dual"
    page["parser_priority"] = ["paddleocr"]
    page["dual_evidence"] = _dual_evidence(None, paddle_page)
    page["raw_text_sha256"] = sha256_text(page.get("raw_text") or "")
    return page


def _dual_evidence(mineru_page: dict[str, Any] | None, paddle_page: dict[str, Any] | None) -> dict[str, Any]:
    mineru_blocks = (mineru_page or {}).get("blocks") or []
    paddle_blocks = (paddle_page or {}).get("blocks") or []
    return {
        "version": DUAL_ADAPTER_VERSION,
        "mineru": {
            "available": mineru_page is not None,
            "raw_text": (mineru_page or {}).get("raw_text") or "",
            "block_count": len(mineru_blocks),
            "blocks": [_evidence_block(block) for block in mineru_blocks],
        },
        "paddleocr": {
            "available": paddle_page is not None,
            "raw_text": (paddle_page or {}).get("raw_text") or "",
            "block_count": len(paddle_blocks),
            "blocks": [_evidence_block(block) for block in paddle_blocks],
            "model_settings": ((paddle_page or {}).get("paddleocr") or {}).get("model_settings"),
        },
    }


def _combined_raw_text(mineru_page: dict[str, Any] | None, paddle_page: dict[str, Any] | None) -> str:
    mineru_text = ((mineru_page or {}).get("raw_text") or "").strip()
    paddle_text = ((paddle_page or {}).get("raw_text") or "").strip()
    if mineru_text and paddle_text:
        return f"[MinerU]\n{mineru_text}\n\n[PaddleOCR]\n{paddle_text}"
    return mineru_text or paddle_text


def _evidence_block(block: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": block.get("id"),
        "type": block.get("type"),
        "text": _text_of(block),
        "confidence": block.get("confidence"),
        "bbox": block.get("bbox"),
        "source_engine": block.get("source_engine") or block.get("origin"),
    }


def _text_of(block: dict[str, Any]) -> str:
    return str(block.get("latex") or block.get("text") or block.get("description") or "").strip()


def _pages_by_no(document_ir: dict[str, Any]) -> dict[int, dict[str, Any]]:
    pages = {}
    for index, page in enumerate(document_ir.get("pages") or [], start=1):
        source_page = int(page.get("source_page") or index)
        pages[source_page] = page
    return pages


def _namespaced_assets(document_ir: dict[str, Any]) -> list[dict[str, Any]]:
    assets = []
    for asset in document_ir.get("assets") or []:
        item = dict(asset)
        item["asset_id"] = f"paddleocr::{item.get('asset_id') or item.get('artifact_ref') or len(assets) + 1}"
        item["source_engine"] = "paddleocr"
        assets.append(item)
    return assets


def _first_value(*values):
    for value in values:
        if value not in (None, ""):
            return value
    return None
