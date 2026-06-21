import hashlib
import re
from typing import Any, Dict, List

PAGE_IR_SCHEMA_VERSION = 1


def build_page_ir(raw_text: str, slide_no: int) -> Dict[str, Any]:
    """Build a weakly structured, deterministic IR from Stage 1 raw text."""
    blocks = raw_text_to_blocks(raw_text, slide_no)
    return {
        "schema_version": PAGE_IR_SCHEMA_VERSION,
        "source_page": slide_no,
        "raw_text_sha256": _sha256_text(raw_text or ""),
        "blocks": blocks,
    }


def raw_text_to_blocks(raw_text: str, slide_no: int) -> List[Dict[str, Any]]:
    text = (raw_text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not text:
        return []

    paragraphs = _split_paragraphs(text)
    blocks = []
    for paragraph in paragraphs:
        block_type = _infer_block_type(paragraph)
        blocks.append(
            {
                "id": f"p{slide_no:04d}-b{len(blocks) + 1:03d}",
                "type": block_type,
                "text": paragraph,
                "source_page": slide_no,
                "confidence": _confidence_for_type(block_type),
                "origin": "stage1_raw",
            }
        )
    return blocks


def render_page_ir_to_markdown(page_ir: Dict[str, Any], slide_no: int | None = None) -> str:
    slide = slide_no or page_ir.get("source_page") or 0
    blocks = page_ir.get("blocks") or []
    if blocks:
        return render_blocks_to_markdown(blocks, slide)
    raw_text = page_ir.get("raw_text") or ""
    return _render_raw_text_fallback(raw_text, slide)


def render_page_record_to_markdown(record: Dict[str, Any], slide_no: int | None = None) -> str:
    slide = slide_no or record.get("slide_no") or record.get("page_ir", {}).get("source_page") or 0
    blocks = record.get("blocks") or record.get("page_ir", {}).get("blocks") or []
    if blocks:
        return render_blocks_to_markdown(blocks, slide)
    return _render_raw_text_fallback(record.get("raw_text") or "", slide)


def render_blocks_to_markdown(blocks: List[Dict[str, Any]], slide_no: int) -> str:
    chunks = [f"# Slide {slide_no}"]
    for block in blocks:
        text = (block.get("text") or "").strip()
        if not text:
            continue
        block_type = block.get("type")
        if block_type == "heading":
            chunks.append(f"## {_strip_heading_marks(text)}")
        elif block_type == "figure":
            chunks.append(_render_figure_note(text))
        else:
            chunks.append(text)
    return "\n\n".join(chunks).rstrip() + "\n"


def _split_paragraphs(text: str) -> List[str]:
    paragraphs = []
    current = []
    in_figure = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
            in_figure = False
            continue

        if stripped.lower().startswith("### figure analysis"):
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
            current.append(stripped)
            in_figure = True
            continue

        if in_figure:
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
    if lower.startswith("### figure analysis"):
        return "figure"
    if re.match(r"^#{1,6}\s+", stripped) or (len(stripped) <= 80 and stripped.endswith(":")):
        return "heading"
    if all(_is_list_line(line.strip()) for line in stripped.splitlines() if line.strip()):
        return "list"
    if "$$" in stripped or re.search(r"\\\(|\\\[|[$][^$]+[$]", stripped):
        return "formula"
    if "|" in stripped and "\n" in stripped:
        return "table"
    return "text"


def _confidence_for_type(block_type: str) -> float:
    if block_type in {"figure", "list"}:
        return 0.72
    if block_type in {"heading", "formula", "table"}:
        return 0.62
    return 0.55


def _is_list_line(line: str) -> bool:
    return bool(re.match(r"^([-*+]\s+|\d+[.)]\s+)", line))


def _strip_heading_marks(text: str) -> str:
    return re.sub(r"^#{1,6}\s+", "", text.strip()).rstrip(":").strip()


def _render_figure_note(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if lines and lines[0].lower().startswith("### figure analysis"):
        lines = lines[1:]
    if not lines:
        return "> [!NOTE] Figure 描述"
    return "> [!NOTE] Figure 描述\n" + "\n".join(f"> {line}" for line in lines)


def _render_raw_text_fallback(raw_text: str, slide_no: int) -> str:
    text = (raw_text or "").strip()
    if not text:
        return f"# Slide {slide_no}\n"
    return f"# Slide {slide_no}\n\n{text}\n"


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()
