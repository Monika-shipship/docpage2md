import hashlib
import re
from typing import Any, Dict, List

from .figures import analyze_figure_description
from .formula_quality import assess_formula_text
from .renderer import (
    render_blocks_to_markdown,
    render_page_ir_to_markdown,
    render_page_record_to_markdown,
)
from .table_quality import assess_table, is_probably_aligned_text_table

PAGE_IR_SCHEMA_VERSION = 11

SEMANTIC_ROLE_LABELS = {
    "definition": "定义",
    "theorem": "定理",
    "lemma": "引理",
    "corollary": "推论",
    "proposition": "命题",
    "proof": "证明",
    "example": "例题",
    "exercise": "练习",
    "solution": "解答",
    "remark": "备注",
}


def build_page_ir(raw_text: str, slide_no: int) -> Dict[str, Any]:
    """Build a weakly structured, deterministic IR from Stage 1 raw text."""
    blocks = raw_text_to_blocks(raw_text, slide_no)
    return {
        "schema_version": PAGE_IR_SCHEMA_VERSION,
        "source_page": slide_no,
        "page_image_ref": None,
        "raw_text": raw_text or "",
        "raw_text_sha256": _sha256_text(raw_text or ""),
        "blocks": blocks,
    }


def attach_page_image_evidence(page_ir: Dict[str, Any], image_path: str) -> Dict[str, Any]:
    """Attach page-level visual evidence without requiring true crop extraction."""
    page_image_ref = str(image_path or "")
    if not page_image_ref:
        return page_ir
    page_ir["page_image_ref"] = page_image_ref
    for block in page_ir.get("blocks") or []:
        block["page_image_ref"] = page_image_ref
        if block.get("type") in {"figure_note", "table", "formula_block"}:
            if not block.get("crop_ref"):
                block["crop_ref"] = page_image_ref
            if "crop_ref_is_page" not in block:
                block["crop_ref_is_page"] = True
    return page_ir


def raw_text_to_blocks(raw_text: str, slide_no: int) -> List[Dict[str, Any]]:
    text = (raw_text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []

    paragraphs = _split_paragraphs(text)
    blocks = []
    for paragraph in paragraphs:
        section_role = _section_semantic_role(paragraph)
        block_text = _strip_section_heading(paragraph)
        block_type = _section_block_type(paragraph) or _infer_block_type(block_text)
        if not block_text:
            continue
        block = {
            "id": f"p{slide_no:04d}-b{len(blocks) + 1:03d}",
            "type": block_type,
            "text": block_text,
            "source_page": slide_no,
            "confidence": _confidence_for_type(block_type, block_text),
            "origin": _origin_for_type(block_type),
            "evidence": {"raw_text": paragraph},
            "bbox": None,
        }
        block.update(_semantic_block_fields(section_role, block_text))
        block.update(_extra_block_fields(block_type, block_text))
        blocks.append(block)
    _attach_figure_links(blocks)
    return blocks


def _split_paragraphs(text: str) -> List[str]:
    paragraphs = []
    current = []
    in_section = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
            in_section = False
            continue

        if _is_section_heading(stripped):
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
            current.append(stripped)
            in_section = True
            continue

        if in_section:
            current.append(stripped)
            continue

        if _is_list_line(stripped):
            if current and not all(_is_list_line(item.strip()) for item in current):
                paragraphs.append("\n".join(current).strip())
                current = []
            current.append(stripped)
            continue

        if current and all(_is_list_line(item.strip()) for item in current):
            paragraphs.append("\n".join(current).strip())
            current = []
        current.append(stripped)

    if current:
        paragraphs.append("\n".join(current).strip())
    return paragraphs


def _infer_block_type(text: str) -> str:
    stripped = text.strip()
    lower = stripped.lower()
    if re.match(r"^#{1,6}\s+", stripped) or (len(stripped) <= 80 and stripped.endswith(":")):
        return "heading"
    if all(_is_list_line(line.strip()) for line in stripped.splitlines() if line.strip()):
        return "list"
    if "|" in stripped and "\n" in stripped:
        return "table"
    if re.search(r"<table\b", stripped, flags=re.IGNORECASE):
        return "table"
    if is_probably_aligned_text_table(stripped):
        return "table"
    if re.search(r"\\\(|\\\[|[$][^$]+[$]", stripped):
        return "formula_inline"
    if _looks_like_formula_block(stripped):
        return "formula_block"
    return "paragraph"


def _confidence_for_type(block_type: str, text: str = "") -> float:
    if block_type == "figure_note" and analyze_figure_description(text).unrecognizable:
        return 0.25
    if block_type in {"figure_note", "list"}:
        return 0.72
    if block_type in {"heading", "formula_inline", "formula_block", "table"}:
        return 0.62
    if block_type == "uncertain":
        return 0.25
    return 0.55


def _origin_for_type(block_type: str) -> str:
    if block_type in {"formula_inline", "formula_block"}:
        return "vision_formula"
    if block_type == "figure_note":
        return "vision_description"
    if block_type == "uncertain":
        return "vision_uncertain"
    if block_type == "table":
        return "vision_table"
    return "vision_ocr"


def _extra_block_fields(block_type: str, text: str) -> Dict[str, Any]:
    if block_type == "figure_note":
        return analyze_figure_description(text).to_block_fields()
    if block_type in {"formula_inline", "formula_block"}:
        quality = assess_formula_text(text)
        return {
            "latex": quality.latex,
            "raw_text": text,
            "formula_quality": quality.to_dict(),
            "warnings": [warning.to_dict() for warning in quality.warnings],
        }
    if block_type == "table":
        quality = assess_table(text)
        degrade_reason_codes = [issue.code for issue in quality.errors + quality.warnings] if not quality.reliable else []
        return {
            "table_format": quality.table_format if quality.reliable else "uncertain",
            "table_reliable": quality.reliable,
            "table_render_mode": _table_render_mode(quality),
            "degrade_reason_codes": degrade_reason_codes,
            "rows": quality.row_count,
            "columns": quality.column_counts,
            "raw_text": text,
            "table_quality": quality.to_dict(),
            "image_ref": None,
            "crop_ref": None,
        }
    return {}


def _table_render_mode(quality) -> str:
    if quality.reliable:
        return "normalized_markdown" if quality.normalized_markdown else quality.table_format
    return "degraded_warning"


def _attach_figure_links(blocks: List[Dict[str, Any]]):
    formula_ids = [block["id"] for block in blocks if block.get("type") in {"formula_inline", "formula_block"}]
    semantic_ids = [
        block["id"]
        for block in blocks
        if block.get("type") in {"paragraph", "list", "heading"} and block.get("semantic_role")
    ]
    paragraph_ids = [block["id"] for block in blocks if block.get("type") in {"paragraph", "list"}]
    for index, block in enumerate(blocks):
        if block.get("type") != "figure_note":
            continue
        text = (block.get("description") or block.get("text") or "").lower()
        linked = []
        if any(keyword in text for keyword in ("公式", "方程", "latex", "equation", "函数", "曲线")):
            linked.extend(formula_ids)
        if any(keyword in text for keyword in ("正文关联", "对应", "证明", "定理", "实验", "步骤", "段落")):
            linked.extend(semantic_ids)
            if not linked:
                linked.extend(_nearest_neighbor_ids(blocks, index, paragraph_ids))
        deduped = []
        for block_id in linked:
            if block_id != block.get("id") and block_id not in deduped:
                deduped.append(block_id)
        block["linked_blocks"] = deduped
        figure = block.get("figure")
        if isinstance(figure, dict):
            figure["linked_blocks"] = deduped


def _nearest_neighbor_ids(blocks: List[Dict[str, Any]], index: int, candidates: list[str]) -> list[str]:
    result = []
    for neighbor_index in (index - 1, index + 1):
        if 0 <= neighbor_index < len(blocks):
            block_id = blocks[neighbor_index].get("id")
            if block_id in candidates:
                result.append(block_id)
    return result


def _is_list_line(line: str) -> bool:
    return bool(re.match(r"^([-*+]\s+|\d+[.)]\s+)", line))


def _is_section_heading(line: str) -> bool:
    lower = line.lower()
    return (
        lower.startswith("### ocr text")
        or lower.startswith("### ocr")
        or lower.startswith("### 正文")
        or lower.startswith("### figure analysis")
        or lower.startswith("### formula")
        or lower.startswith("### table analysis")
        or lower.startswith("### uncertain")
        or lower.startswith("### illegible")
        or lower.startswith("### 公式")
        or lower.startswith("### 表格")
        or lower.startswith("### 不确定")
        or _semantic_role_from_section_heading(line) is not None
    )


def _section_block_type(text: str) -> str | None:
    first = (text.strip().splitlines() or [""])[0].strip().lower()
    if first.startswith("### figure analysis"):
        return "figure_note"
    if first.startswith("### formula") or first.startswith("### 公式"):
        return "formula_block"
    if first.startswith("### table analysis") or first.startswith("### 表格"):
        return "table"
    if first.startswith("### uncertain") or first.startswith("### illegible") or first.startswith("### 不确定"):
        return "uncertain"
    return None


def _section_semantic_role(text: str) -> str | None:
    first = (text.strip().splitlines() or [""])[0].strip()
    return _semantic_role_from_section_heading(first)


def _strip_section_heading(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and _is_section_heading(lines[0].strip()):
        lines = lines[1:]
    return "\n".join(line.strip() for line in lines).strip()


def _semantic_block_fields(section_role: str | None, text: str) -> Dict[str, Any]:
    role = section_role or _inline_semantic_role(text)
    if not role:
        return {}
    return {
        "semantic_role": role,
        "semantic_role_label": SEMANTIC_ROLE_LABELS[role],
        "semantic_role_source": "section" if section_role else "inline",
    }


def _semantic_role_from_section_heading(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("#"):
        return None
    title = re.sub(r"^#{1,6}\s*", "", stripped).strip().lower().rstrip(":：")
    role_prefixes = {
        "definition": ("definition", "def.", "定义"),
        "theorem": ("theorem", "定理"),
        "lemma": ("lemma", "引理"),
        "corollary": ("corollary", "推论"),
        "proposition": ("proposition", "命题"),
        "proof": ("proof", "proof steps", "证明", "证明过程"),
        "example": ("example", "examples", "例题", "例子", "例"),
        "exercise": ("exercise", "problem", "练习", "习题"),
        "solution": ("solution", "answer", "解答", "解"),
        "remark": ("remark", "note", "observation", "备注", "注"),
    }
    for role, prefixes in role_prefixes.items():
        if any(_matches_role_prefix(title, prefix) for prefix in prefixes):
            return role
    return None


def _matches_role_prefix(title: str, prefix: str) -> bool:
    return bool(
        title == prefix
        or title.startswith(f"{prefix} ")
        or re.match(rf"^{re.escape(prefix)}[\d一二三四五六七八九十.、:：-]", title)
    )


def _inline_semantic_role(text: str) -> str | None:
    first = (text.strip().splitlines() or [""])[0].strip()
    patterns = [
        ("definition", r"^(定义|Definition)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("theorem", r"^(定理|Theorem)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("lemma", r"^(引理|Lemma)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("corollary", r"^(推论|Corollary)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("proposition", r"^(命题|Proposition)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("proof", r"^(证明|证|Proof)\s*[:：]"),
        ("example", r"^(例题|例子|例|Example)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("exercise", r"^(练习|习题|Exercise|Problem)\s*[\d一二三四五六七八九十.、-]*\s*[:：]"),
        ("solution", r"^(解答|解|Solution|Answer)\s*[:：]"),
        ("remark", r"^(备注|注|Remark|Note|Observation)\s*[:：]"),
    ]
    for role, pattern in patterns:
        if re.match(pattern, first, flags=re.IGNORECASE):
            return role
    return None


def _looks_like_formula_block(text: str) -> bool:
    stripped = text.strip()
    if "$$" in stripped:
        return True
    if re.search(r"[\u4e00-\u9fff]", stripped):
        return False
    if len(stripped.splitlines()) <= 3 and re.search(r"(\\frac|\\sum|\\int|\\lim|\\begin\{|=|≈|≤|≥)", stripped):
        math_chars = sum(1 for ch in stripped if ch in "=+-*/^_{}\\")
        return math_chars >= 2
    return False


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()
