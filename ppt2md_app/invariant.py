import hashlib
import re
from typing import Any, Dict

from .ir import PAGE_IR_SCHEMA_VERSION


BLOCK_ALLOWED_ORIGINS = {
    "vision_ocr",
    "vision_formula",
    "vision_description",
    "vision_table",
    "vision_uncertain",
    "brain_refine",
    "renderer_template",
    "refiner_op",
}

BLOCK_ALLOWED_TYPES = {
    "heading",
    "paragraph",
    "list",
    "formula_inline",
    "formula_block",
    "figure_note",
    "table",
    "image_ref",
    "uncertain",
}

BLOCK_VISION_ORIGINS = {
    "vision_ocr",
    "vision_formula",
    "vision_description",
    "vision_table",
    "vision_uncertain",
}


def page_ir_contract_errors(page_ir: Dict[str, Any], *, expected_slide_no: int | None = None) -> list[str]:
    errors = []
    if not isinstance(page_ir, dict):
        return ["page_ir_not_dict"]
    schema_version = page_ir.get("schema_version")
    if "schema_version" not in page_ir:
        errors.append("schema_version_missing")
    elif isinstance(schema_version, bool) or not isinstance(schema_version, int):
        errors.append("schema_version_not_int")
    elif schema_version != PAGE_IR_SCHEMA_VERSION:
        errors.append("schema_version_mismatch")
    source_page = page_ir.get("source_page")
    if "source_page" not in page_ir:
        errors.append("source_page_missing")
    elif not valid_source_page(source_page):
        errors.append("source_page_not_positive_int")
    elif expected_slide_no is not None and source_page != expected_slide_no:
        errors.append("source_page_mismatch")
    raw_text = page_ir.get("raw_text")
    if "raw_text" not in page_ir:
        errors.append("raw_text_missing")
    elif not isinstance(raw_text, str):
        errors.append("raw_text_not_string")
    if "raw_text_sha256" not in page_ir:
        errors.append("raw_text_sha256_missing")
    elif not isinstance(page_ir.get("raw_text_sha256"), str):
        errors.append("raw_text_sha256_not_string")
    elif isinstance(raw_text, str) and page_ir.get("raw_text_sha256") != _sha256_text(raw_text):
        errors.append("raw_text_sha256_mismatch")
    if "page_image_ref" in page_ir and page_ir.get("page_image_ref") is not None and not isinstance(page_ir.get("page_image_ref"), str):
        errors.append("page_image_ref_not_string")
    blocks = page_ir.get("blocks")
    if not isinstance(blocks, list):
        errors.append("blocks_not_list")
        return errors
    seen = set()
    for index, block in enumerate(blocks):
        if not isinstance(block, dict):
            errors.append(f"block_{index}_not_dict")
            continue
        block_id = block.get("id")
        if not block_id:
            errors.append(f"block_{index}_missing_id")
        else:
            if not valid_block_id(block_id, page_ir.get("source_page")):
                errors.append(f"block_{index}_invalid_id")
            if block_id in seen:
                errors.append(f"block_{index}_duplicate_id")
            seen.add(block_id)
        block_type = block.get("type")
        if not block_type:
            errors.append(f"block_{index}_missing_type")
        elif block_type not in BLOCK_ALLOWED_TYPES:
            errors.append(f"block_{index}_unknown_type")
        if "text" not in block and block_type != "image_ref":
            errors.append(f"block_{index}_missing_text")
        if block.get("source_page") != page_ir.get("source_page"):
            errors.append(f"block_{index}_source_page_mismatch")
        if "confidence" not in block:
            errors.append(f"block_{index}_missing_confidence")
        elif not valid_confidence(block.get("confidence")):
            errors.append(f"block_{index}_invalid_confidence")
        if "bbox" not in block:
            errors.append(f"block_{index}_missing_bbox")
        elif not valid_bbox(block.get("bbox")):
            errors.append(f"block_{index}_invalid_bbox")
        origin = block.get("origin")
        if not origin:
            errors.append(f"block_{index}_missing_origin")
        elif origin not in BLOCK_ALLOWED_ORIGINS:
            errors.append(f"block_{index}_unknown_origin")
        if "evidence" not in block:
            errors.append(f"block_{index}_missing_evidence")
        elif not isinstance(block.get("evidence"), dict):
            errors.append(f"block_{index}_invalid_evidence")
        else:
            errors.extend(_block_evidence_errors(index, block))
    return errors


def valid_block_id(value, source_page) -> bool:
    if not isinstance(value, str):
        return False
    if not valid_source_page(source_page):
        return False
    return bool(re.fullmatch(rf"p{source_page:04d}-b\d{{3}}", value))


def valid_source_page(value) -> bool:
    return not isinstance(value, bool) and isinstance(value, int) and value > 0


def valid_bbox(value) -> bool:
    if value is None:
        return True
    if not isinstance(value, list) or len(value) != 4:
        return False
    return all(isinstance(item, (int, float)) for item in value)


def valid_confidence(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return 0.0 <= float(value) <= 1.0


def _block_evidence_errors(index: int, block: Dict[str, Any]) -> list[str]:
    evidence = block.get("evidence") or {}
    origin = block.get("origin")
    errors = []
    if origin in BLOCK_VISION_ORIGINS and not isinstance(evidence.get("raw_text"), str):
        errors.append(f"block_{index}_missing_raw_text_evidence")
    if origin == "refiner_op" and not isinstance(evidence.get("refiner_op"), str):
        errors.append(f"block_{index}_missing_refiner_op_evidence")
    return errors


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()
