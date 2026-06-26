import re
from dataclasses import dataclass
from copy import deepcopy
from typing import Any, Dict, List

from .figures import analyze_figure_description
from .formula_quality import (
    assess_formula_text,
    formula_markup_needs_normalize,
    markdown_formula_markup_needs_normalize,
    normalize_formula_text,
    normalize_markdown_formula_blocks,
)
from .invariant import page_ir_contract_errors, valid_source_page
from .renderer import render_page_ir_to_markdown
from .validators import ValidationIssue, is_api_error_text, validate_slide_markdown


KNOWN_OPS = {
    "strip_chatter",
    "fix_heading",
    "drop_empty",
    "merge_broken_line",
    "mark_failed_page",
    "normalize_formula",
}

SAFE_OPS = {
    "strip_chatter",
    "fix_heading",
    "drop_empty",
    "merge_broken_line",
    "normalize_formula",
}

BLOCK_REFINER_VERSION = "block-refiner-2026-06-22-formula-markup"

BLOCK_KNOWN_OPS = {
    "merge_block",
    "drop_block",
    "promote_heading",
    "demote_heading",
    "convert_figure_note",
    "mark_uncertain",
    "normalize_formula",
    "replace_text_span_checked",
}

BLOCK_SAFE_OPS = set(BLOCK_KNOWN_OPS)

@dataclass(frozen=True)
class Suspect:
    id: str
    code: str
    op: str
    reason: str
    evidence: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "op": self.op,
            "reason": self.reason,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class RefineResult:
    markdown: str
    applied_ops: List[Dict[str, Any]]
    dismissed: List[Dict[str, Any]]
    validation: Dict[str, Any]

    @property
    def changed(self) -> bool:
        return bool(self.applied_ops)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "changed": self.changed,
            "applied_ops": self.applied_ops,
            "dismissed": self.dismissed,
            "validation": self.validation,
        }


@dataclass(frozen=True)
class BlockSuspect:
    id: str
    code: str
    op: Dict[str, Any]
    reason: str
    evidence: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "code": self.code,
            "op": self.op,
            "reason": self.reason,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class BlockRefineResult:
    page_ir: Dict[str, Any]
    applied_ops: List[Dict[str, Any]]
    dismissed: List[Dict[str, Any]]
    validation: Dict[str, Any]
    op_audit: List[Dict[str, Any]]

    @property
    def changed(self) -> bool:
        return bool(self.applied_ops)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": BLOCK_REFINER_VERSION,
            "changed": self.changed,
            "applied_ops": self.applied_ops,
            "dismissed": self.dismissed,
            "op_audit": self.op_audit,
            "validation": self.validation,
        }


def detect_markdown_suspects(markdown: str, slide_no: int) -> List[Suspect]:
    text = markdown or ""
    suspects: List[Suspect] = []
    lines = text.splitlines()
    first_nonempty = next((line.strip() for line in lines if line.strip()), "")

    if first_nonempty and _is_chatter_line(first_nonempty):
        suspects.append(
            Suspect(
                id=f"p{slide_no:04d}-s001",
                code="leading_chatter",
                op="strip_chatter",
                reason="输出开头包含模型寒暄或处理说明。",
                evidence=first_nonempty,
            )
        )

    heading = re.match(r"^#\s*Slide\s+0*(\d+)\b", first_nonempty, flags=re.IGNORECASE)
    if not heading or int(heading.group(1)) != slide_no:
        suspects.append(
            Suspect(
                id=f"p{slide_no:04d}-s002",
                code="heading_missing_or_mismatch",
                op="fix_heading",
                reason=f"输出没有以 # Slide {slide_no} 作为第一页标题。",
                evidence=first_nonempty,
            )
        )

    if re.search(r"\n{3,}", text):
        suspects.append(
            Suspect(
                id=f"p{slide_no:04d}-s003",
                code="excess_blank_lines",
                op="drop_empty",
                reason="输出包含连续空行，可压缩为空白段落。",
            )
        )

    if re.search(r"(?m)[A-Za-z]-\n[A-Za-z]", text):
        suspects.append(
            Suspect(
                id=f"p{slide_no:04d}-s004",
                code="broken_hyphenated_line",
                op="merge_broken_line",
                reason="英文单词疑似被换行断开。",
            )
        )

    if markdown_formula_markup_needs_normalize(text):
        suspects.append(
            Suspect(
                id=f"p{slide_no:04d}-s005",
                code="formula_markup_needs_normalize",
                op="normalize_formula",
                reason="公式含不稳定 Markdown/LaTeX 标记，应移动编号并统一行间公式环境。",
                evidence=_formula_markup_evidence(text),
            )
        )

    return suspects


def detect_block_suspects(page_ir: Dict[str, Any]) -> List[BlockSuspect]:
    blocks = page_ir.get("blocks") or []
    suspects: List[BlockSuspect] = []
    for index, block in enumerate(blocks):
        block_id = block.get("id")
        block_type = block.get("type")
        text = (block.get("text") or block.get("description") or "").strip()
        if not block_id:
            continue
        suspect_no = len(suspects) + 1

        if not text:
            if _empty_text_block_has_nontext_payload(block):
                continue
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "empty_block",
                    {"op": "drop_block", "id": block_id, "reason": "empty"},
                    "block 内容为空，应删除。",
                )
            )
            continue

        if block_type == "heading" and _looks_like_body_text(text):
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "heading_looks_like_body",
                    {"op": "demote_heading", "id": block_id},
                    "heading block 更像正文，应降级为 paragraph。",
                    text,
                )
            )
            continue

        if block_type == "paragraph" and _looks_like_heading_text(text):
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "paragraph_looks_like_heading",
                    {"op": "promote_heading", "id": block_id},
                    "paragraph block 更像标题，应升级为 heading。",
                    text,
                )
            )
            continue

        if block_type == "paragraph" and _looks_like_figure_description(text):
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "paragraph_looks_like_figure",
                    {"op": "convert_figure_note", "id": block_id},
                    "paragraph block 更像图示说明，应转为 figure_note。",
                    text,
                )
            )
            continue

        if block_type in {"paragraph", "list"} and _has_uncertain_marker(text):
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "text_contains_uncertain_marker",
                    {"op": "mark_uncertain", "id": block_id},
                    "block 含不确定识别标记，应转为 uncertain。",
                    text,
                )
            )
            continue

        if block_type in {"formula_inline", "formula_block"} and _formula_needs_normalize(text):
            suspects.append(
                _block_suspect(
                    page_ir,
                    suspect_no,
                    "formula_needs_normalize",
                    {"op": "normalize_formula", "id": block_id},
                    "公式 block 含外层分隔符或不稳定公式编号位置，应规范为可渲染 LaTeX 文本。",
                    text,
                )
            )
            continue

        if index + 1 < len(blocks) and block_type == "paragraph":
            next_block = blocks[index + 1]
            if next_block.get("type") == "paragraph" and text.endswith("-"):
                suspects.append(
                    _block_suspect(
                        page_ir,
                        suspect_no,
                        "broken_hyphenated_block",
                        {"op": "merge_block", "a": block_id, "b": next_block.get("id")},
                        "相邻 paragraph 疑似英文单词被跨 block 断开。",
                        text,
                    )
                )
    return suspects


def _empty_text_block_has_nontext_payload(block: Dict[str, Any]) -> bool:
    block_type = block.get("type")
    if block_type in {"image_ref", "figure_note"}:
        if any(str(block.get(key) or "").strip() for key in ("path", "image_path", "crop_ref", "image_ref")):
            return True
        figure = block.get("figure") if isinstance(block.get("figure"), dict) else {}
        if any(figure.get(key) not in (None, "", [], {}) for key in ("figure_type", "labels", "relations", "uncertainties")):
            return True
    if block_type == "table":
        if any(str(block.get(key) or "").strip() for key in ("table_image_path", "image_path", "crop_ref", "image_ref")):
            return True
        if block.get("rows") or block.get("columns"):
            return True
    return False


def apply_block_op_checked(
    page_ir: Dict[str, Any],
    op: Dict[str, Any],
    *,
    slide_no: int | None = None,
    target_raw: str | None = None,
) -> tuple[Dict[str, Any], bool, Dict[str, Any]]:
    op_name = op.get("op")
    if op_name not in BLOCK_SAFE_OPS:
        return page_ir, False, {"reason": "unknown_or_unsafe_op", "op": op_name}

    slide = _resolve_slide_no(page_ir, slide_no)
    before_validation = validate_slide_markdown(
        render_page_ir_to_markdown(page_ir, slide),
        slide,
        target_raw=target_raw,
    )
    text_previews = _op_text_previews(page_ir, op)
    no_change_reason = _block_no_change_reason(page_ir, op)
    before_ids = _block_ids(page_ir)
    before_summaries = _block_summaries(page_ir)
    candidate = deepcopy(page_ir)
    changed = _apply_block_op(candidate, op)
    after_ids = _block_ids(candidate)
    after_summaries = _block_summaries(candidate)
    if not changed:
        return page_ir, False, {
            "reason": no_change_reason or "no_change",
            "before_block_ids": before_ids,
            "after_block_ids": before_ids,
            "before_blocks": before_summaries,
            "after_blocks": before_summaries,
            "removed_spans": [],
            "removed_text_hashes": [],
            "before_text_sha256": _target_text_sha256(before_summaries, op),
            "after_text_sha256": _target_text_sha256(before_summaries, op),
            "validator_before": before_validation.to_dict(),
            "validator_after": before_validation.to_dict(),
            **text_previews,
        }

    contract_errors = page_ir_contract_errors(candidate, expected_slide_no=slide if slide > 0 else None)
    if contract_errors:
        return page_ir, False, {
            "reason": "page_ir_contract_failed",
            "errors": contract_errors,
            "before_block_ids": before_ids,
            "after_block_ids": after_ids,
            "before_blocks": before_summaries,
            "after_blocks": after_summaries,
            "removed_spans": _removed_spans(before_summaries, after_summaries),
            "removed_text_hashes": _removed_text_hashes(before_summaries, after_summaries),
            "before_text_sha256": _target_text_sha256(before_summaries, op),
            "after_text_sha256": _target_text_sha256(after_summaries, op),
            "validator_before": before_validation.to_dict(),
            **text_previews,
        }

    after_markdown = render_page_ir_to_markdown(candidate, slide)
    after_validation = validate_slide_markdown(after_markdown, slide, target_raw=target_raw)
    if not _is_no_worse(before_validation.errors, after_validation.errors):
        return page_ir, False, {
            "reason": "validation_would_get_worse",
            "validation": after_validation.to_dict(),
            "validator_before": before_validation.to_dict(),
            "validator_after": after_validation.to_dict(),
            "before_block_ids": before_ids,
            "after_block_ids": after_ids,
            "before_blocks": before_summaries,
            "after_blocks": after_summaries,
            "removed_spans": _removed_spans(before_summaries, after_summaries),
            "removed_text_hashes": _removed_text_hashes(before_summaries, after_summaries),
            "before_text_sha256": _target_text_sha256(before_summaries, op),
            "after_text_sha256": _target_text_sha256(after_summaries, op),
            **text_previews,
        }

    return candidate, True, {
        "validation": after_validation.to_dict(),
        "validator_before": before_validation.to_dict(),
        "validator_after": after_validation.to_dict(),
        "before_block_ids": before_ids,
        "after_block_ids": after_ids,
        "before_blocks": before_summaries,
        "after_blocks": after_summaries,
        "removed_spans": _removed_spans(before_summaries, after_summaries),
        "removed_text_hashes": _removed_text_hashes(before_summaries, after_summaries),
        "before_text_sha256": _target_text_sha256(before_summaries, op),
        "after_text_sha256": _target_text_sha256(after_summaries, op),
        "degraded": op_name == "mark_uncertain",
        **text_previews,
    }


def refine_page_ir(
    page_ir: Dict[str, Any],
    *,
    slide_no: int | None = None,
    target_raw: str | None = None,
) -> BlockRefineResult:
    current = deepcopy(page_ir)
    applied = []
    dismissed = []
    op_audit = []
    for suspect in detect_block_suspects(current):
        current, ok, detail = apply_block_op_checked(
            current,
            suspect.op,
            slide_no=slide_no,
            target_raw=target_raw,
        )
        item = suspect.to_dict()
        if ok:
            item.update(detail)
            applied.append(item)
            op_audit.append(_block_op_audit(suspect, "applied", detail))
        else:
            item["dismissed"] = detail
            dismissed.append(item)
            op_audit.append(_block_op_audit(suspect, "rejected", detail))

    slide = _resolve_slide_no(current, slide_no)
    validation = validate_slide_markdown(render_page_ir_to_markdown(current, slide), slide, target_raw=target_raw)
    return BlockRefineResult(current, applied, dismissed, validation.to_dict(), op_audit)


def apply_op_checked(
    markdown: str,
    suspect: Suspect,
    slide_no: int,
    *,
    raw_response: str | None = None,
    target_raw: str | None = None,
    target_blocks: list[dict] | None = None,
) -> tuple[str, bool, Dict[str, Any]]:
    if suspect.op not in SAFE_OPS or is_api_error_text(raw_response) or is_api_error_text(markdown):
        return markdown, False, {"reason": "unsafe_or_error_text"}

    before = validate_slide_markdown(
        markdown,
        slide_no,
        raw_response=raw_response,
        target_raw=target_raw,
        target_blocks=target_blocks,
    )
    candidate = _apply_op(markdown, suspect.op, slide_no)
    if candidate == markdown:
        return markdown, False, {"reason": "no_change"}

    after = validate_slide_markdown(
        candidate,
        slide_no,
        raw_response=raw_response,
        target_raw=target_raw,
        target_blocks=target_blocks,
    )
    if _is_no_worse(before.errors, after.errors):
        return candidate, True, after.to_dict()
    return markdown, False, {"reason": "validation_would_get_worse", "validation": after.to_dict()}


def refine_slide_markdown(
    markdown: str,
    slide_no: int,
    *,
    raw_response: str | None = None,
    target_raw: str | None = None,
    target_blocks: list[dict] | None = None,
) -> RefineResult:
    current = markdown
    applied = []
    dismissed = []
    for suspect in detect_markdown_suspects(current, slide_no):
        current, ok, validation = apply_op_checked(
            current,
            suspect,
            slide_no,
            raw_response=raw_response,
            target_raw=target_raw,
            target_blocks=target_blocks,
        )
        if ok:
            item = suspect.to_dict()
            item["validation"] = validation
            applied.append(item)
        else:
            item = suspect.to_dict()
            item["dismissed"] = validation
            dismissed.append(item)

    final_validation = validate_slide_markdown(
        current,
        slide_no,
        raw_response=raw_response,
        target_raw=target_raw,
        target_blocks=target_blocks,
    )
    return RefineResult(
        markdown=current,
        applied_ops=applied,
        dismissed=dismissed,
        validation=final_validation.to_dict(),
    )


def _apply_op(markdown: str, op: str, slide_no: int) -> str:
    if op == "strip_chatter":
        return _strip_leading_chatter(markdown)
    if op == "fix_heading":
        return _fix_heading(markdown, slide_no)
    if op == "drop_empty":
        return re.sub(r"\n{3,}", "\n\n", markdown).strip() + "\n"
    if op == "merge_broken_line":
        return re.sub(r"(?m)([A-Za-z])-\n([A-Za-z])", r"\1\2", markdown).strip() + "\n"
    if op == "normalize_formula":
        return normalize_markdown_formula_blocks(markdown).rstrip() + "\n"
    return markdown


def _strip_leading_chatter(markdown: str) -> str:
    lines = markdown.splitlines()
    while lines and (not lines[0].strip() or _is_chatter_line(lines[0])):
        lines.pop(0)
    return "\n".join(lines).strip() + "\n"


def _fix_heading(markdown: str, slide_no: int) -> str:
    text = markdown.strip()
    lines = text.splitlines()
    if lines and re.match(r"^#\s*Slide\s+\d+\b", lines[0], flags=re.IGNORECASE):
        lines[0] = f"# Slide {slide_no}"
        return "\n".join(lines).strip() + "\n"
    return f"# Slide {slide_no}\n\n{text}".strip() + "\n"


def _is_chatter_line(line: str) -> bool:
    normalized = line.strip().lstrip("> ").strip()
    prefixes = (
        "好的",
        "当然",
        "以下是",
        "下面是",
        "根据您提供",
        "基于您提供",
        "我将",
        "我已经",
    )
    return normalized.startswith(prefixes)


def _is_no_worse(before: List[ValidationIssue], after: List[ValidationIssue]) -> bool:
    before_codes = {issue.code for issue in before}
    after_codes = {issue.code for issue in after}
    return after_codes.issubset(before_codes)


def _block_suspect(
    page_ir: Dict[str, Any],
    suspect_no: int,
    code: str,
    op: Dict[str, Any],
    reason: str,
    evidence: str | None = None,
) -> BlockSuspect:
    page = int(page_ir.get("source_page") or 0)
    return BlockSuspect(
        id=f"p{page:04d}-bs{suspect_no:03d}",
        code=code,
        op=op,
        reason=reason,
        evidence=evidence,
    )


def _block_op_audit(suspect: BlockSuspect, status: str, detail: Dict[str, Any]) -> Dict[str, Any]:
    op = suspect.op if isinstance(suspect.op, dict) else {}
    target_ids = []
    for key in ("id", "a", "b"):
        value = op.get(key)
        if value and value not in target_ids:
            target_ids.append(value)
    return {
        "suspect_id": suspect.id,
        "code": suspect.code,
        "op": op.get("op"),
        "target_block_ids": target_ids,
        "before_block_ids": detail.get("before_block_ids", []),
        "after_block_ids": detail.get("after_block_ids", []),
        "before_blocks": detail.get("before_blocks", []),
        "after_blocks": detail.get("after_blocks", []),
        "before_text_sha256": detail.get("before_text_sha256"),
        "after_text_sha256": detail.get("after_text_sha256"),
        "removed_spans": detail.get("removed_spans", []),
        "removed_text_hashes": detail.get("removed_text_hashes", []),
        "degraded": bool(detail.get("degraded") or op.get("op") == "mark_uncertain"),
        "reason": detail.get("reason") or suspect.reason,
        "status": status,
        "validator_before": detail.get("validator_before"),
        "validator_after": detail.get("validator_after") or detail.get("validation"),
    }


def _apply_block_op(page_ir: Dict[str, Any], op: Dict[str, Any]) -> bool:
    op_name = op.get("op")
    if op_name == "merge_block":
        return _op_merge_block(page_ir, op.get("a"), op.get("b"))
    if op_name == "drop_block":
        return _op_drop_block(page_ir, op.get("id"), op.get("reason"))
    if op_name == "promote_heading":
        return _op_set_block_type(page_ir, op.get("id"), "heading")
    if op_name == "demote_heading":
        return _op_set_block_type(page_ir, op.get("id"), "paragraph")
    if op_name == "convert_figure_note":
        return _op_convert_figure_note(page_ir, op.get("id"))
    if op_name == "mark_uncertain":
        return _op_mark_uncertain(page_ir, op.get("id"))
    if op_name == "normalize_formula":
        return _op_normalize_formula(page_ir, op.get("id"))
    if op_name == "replace_text_span_checked":
        return _op_replace_text_span_checked(page_ir, op)
    return False


def _block_no_change_reason(page_ir: Dict[str, Any], op: Dict[str, Any]) -> str | None:
    op_name = op.get("op")
    blocks = page_ir.get("blocks") or []
    if op_name == "replace_text_span_checked":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        old_text = str(op.get("old_text") or "")
        new_text = str(op.get("new_text") or "")
        if not old_text or not new_text:
            return "missing_checked_span"
        if old_text == new_text:
            return "replacement_same_as_current"
        if is_api_error_text(new_text):
            return "unsafe_or_error_text"
        if not _replacement_growth_is_safe(old_text, new_text):
            return "replacement_growth_unsafe"
        if _replace_text_span_is_too_broad(block, old_text, new_text):
            return "replacement_too_broad"
        fields = [str(op.get("field"))] if op.get("field") else ["text", "latex", "raw_text", "description"]
        searchable_values = [
            str(block.get(field) or "")
            for field in fields
            if field in {"text", "latex", "raw_text", "description"} and isinstance(block.get(field), str)
        ]
        if not any(old_text in value for value in searchable_values):
            if new_text and any(new_text in value for value in searchable_values):
                return "replacement_same_as_current"
            return "old_text_not_found"
        return "no_change"
    if op_name == "mark_uncertain":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        if block.get("type") == "uncertain":
            return "already_uncertain"
        return "mark_uncertain_no_effect"
    if op_name == "normalize_formula":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        if block.get("type") not in {"formula_inline", "formula_block"}:
            return "normalize_formula_not_applicable"
        text = (block.get("text") or "").strip()
        if _normalize_formula_text(text) == text:
            return "normalized_formula_unchanged"
        return "no_change"
    if op_name == "promote_heading":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        if block.get("type") == "heading":
            return "already_heading"
        return "promote_heading_no_effect"
    if op_name == "demote_heading":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        if block.get("type") == "paragraph":
            return "already_paragraph"
        return "demote_heading_no_effect"
    if op_name == "drop_block":
        block = _find_block(blocks, op.get("id"))
        if not block:
            return "target_block_not_found"
        text = (block.get("text") or block.get("description") or "").strip()
        if text and op.get("reason") not in {"empty", "page_artifact"}:
            return "drop_block_not_allowed_nonempty"
        return "drop_block_no_effect"
    return None


def _op_text_previews(page_ir: Dict[str, Any], op: Dict[str, Any]) -> Dict[str, Any]:
    target_ids = {str(value) for value in (op.get("id"), op.get("a"), op.get("b")) if value}
    current_texts: list[str] = []
    first_block: Dict[str, Any] | None = None
    for block in page_ir.get("blocks") or []:
        if not isinstance(block, dict) or str(block.get("id") or "") not in target_ids:
            continue
        if first_block is None:
            first_block = block
        text = _longest_block_text(block)
        if text:
            current_texts.append(text)
    result = {
        "old_text_preview": _text_preview(str(op.get("old_text") or ""), limit=180),
        "new_text_preview": _text_preview(str(op.get("new_text") or ""), limit=180),
        "current_text_preview": _text_preview("\n".join(current_texts), limit=180),
        "reason_preview": _text_preview(str(op.get("reason") or ""), limit=200),
    }
    if first_block:
        result.update(
            {
                "target_block_type": first_block.get("type"),
                "target_block_origin": first_block.get("origin") or first_block.get("source_engine"),
                "target_block_confidence": first_block.get("confidence"),
            }
        )
    return result


def _op_merge_block(page_ir: Dict[str, Any], a_id: str | None, b_id: str | None) -> bool:
    blocks = page_ir.get("blocks") or []
    a_index = _find_block_index(blocks, a_id)
    b_index = _find_block_index(blocks, b_id)
    if a_index is None or b_index is None or b_index != a_index + 1:
        return False
    a = blocks[a_index]
    b = blocks[b_index]
    if a.get("type") != b.get("type"):
        return False
    a_text = (a.get("text") or "").rstrip()
    b_text = (b.get("text") or "").lstrip()
    if not a_text and not b_text:
        return False
    if a_text.endswith("-") and b_text:
        merged_text = a_text[:-1] + b_text
    else:
        merged_text = f"{a_text}\n{b_text}".strip()
    before_ids = [a.get("id"), b.get("id")]
    a["text"] = merged_text
    _mark_refiner_origin(a, "merge_block", before_ids=before_ids)
    del blocks[b_index]
    return True


def _op_drop_block(page_ir: Dict[str, Any], block_id: str | None, reason: str | None) -> bool:
    blocks = page_ir.get("blocks") or []
    index = _find_block_index(blocks, block_id)
    if index is None:
        return False
    block = blocks[index]
    text = (block.get("text") or block.get("description") or "").strip()
    if text and reason not in {"empty", "page_artifact"}:
        return False
    del blocks[index]
    return True


def _op_set_block_type(page_ir: Dict[str, Any], block_id: str | None, block_type: str) -> bool:
    block = _find_block(page_ir.get("blocks") or [], block_id)
    if not block or block.get("type") == block_type:
        return False
    block["type"] = block_type
    if block_type == "heading":
        block["confidence"] = max(float(block.get("confidence") or 0.0), 0.62)
    _mark_refiner_origin(block, f"set_{block_type}")
    return True


def _op_convert_figure_note(page_ir: Dict[str, Any], block_id: str | None) -> bool:
    block = _find_block(page_ir.get("blocks") or [], block_id)
    if not block or block.get("type") == "figure_note":
        return False
    text = (block.get("text") or "").strip()
    if not text:
        return False
    analysis = analyze_figure_description(text)
    block["type"] = "figure_note"
    block.update(analysis.to_block_fields())
    block["confidence"] = 0.25 if analysis.unrecognizable else max(float(block.get("confidence") or 0.0), 0.72)
    _mark_refiner_origin(block, "convert_figure_note")
    return True


def _op_mark_uncertain(page_ir: Dict[str, Any], block_id: str | None) -> bool:
    block = _find_block(page_ir.get("blocks") or [], block_id)
    if not block or block.get("type") == "uncertain":
        return False
    block["type"] = "uncertain"
    block["confidence"] = min(float(block.get("confidence") or 0.25), 0.25)
    _mark_refiner_origin(block, "mark_uncertain")
    return True


def _op_normalize_formula(page_ir: Dict[str, Any], block_id: str | None) -> bool:
    block = _find_block(page_ir.get("blocks") or [], block_id)
    if not block or block.get("type") not in {"formula_inline", "formula_block"}:
        return False
    text = (block.get("text") or "").strip()
    normalized = _normalize_formula_text(text)
    if normalized == text:
        return False
    block["text"] = normalized
    block["type"] = "formula_block"
    _update_formula_fields(block)
    _mark_refiner_origin(block, "normalize_formula")
    return True


def _op_replace_text_span_checked(page_ir: Dict[str, Any], op: Dict[str, Any]) -> bool:
    block = _find_block(page_ir.get("blocks") or [], op.get("id"))
    if not block:
        return False
    old_text = str(op.get("old_text") or "")
    new_text = str(op.get("new_text") or "")
    if not old_text or not new_text or old_text == new_text:
        return False
    if is_api_error_text(new_text):
        return False
    if not _replacement_growth_is_safe(old_text, new_text):
        return False
    if _replace_text_span_is_too_broad(block, old_text, new_text):
        return False

    fields = [str(op.get("field"))] if op.get("field") else ["text", "latex", "raw_text", "description"]
    changed_fields = []
    for field in fields:
        if field not in {"text", "latex", "raw_text", "description"}:
            continue
        value = block.get(field)
        if not isinstance(value, str) or old_text not in value:
            continue
        block[field] = value.replace(old_text, new_text, 1)
        changed_fields.append(field)

    if not changed_fields:
        return False

    if block.get("type") in {"formula_inline", "formula_block"}:
        if "text" not in changed_fields and isinstance(block.get("text"), str) and old_text in block["text"]:
            block["text"] = block["text"].replace(old_text, new_text, 1)
            changed_fields.append("text")
        _update_formula_fields(block)

    evidence = block.setdefault("evidence", {})
    evidence["brain_op"] = "replace_text_span_checked"
    evidence["replace_text_span_checked"] = {
        "old_text_sha256": _sha256_text(old_text),
        "new_text_sha256": _sha256_text(new_text),
        "fields": changed_fields,
        "reason": op.get("reason"),
    }
    block["origin"] = "brain_refine"
    block["source_engine"] = "brain"
    return True


def _replacement_growth_is_safe(old_text: str, new_text: str) -> bool:
    if len(new_text) <= len(old_text) + 80:
        return True
    if len(old_text) >= 8 and len(new_text) <= len(old_text) * 4:
        return True
    return False


def _replace_text_span_is_too_broad(block: Dict[str, Any], old_text: str, new_text: str) -> bool:
    if _looks_like_markdown_document(old_text) or _looks_like_markdown_document(new_text):
        return True
    block_text = _longest_block_text(block)
    if len(block_text) >= 600 and len(old_text) >= max(420, int(len(block_text) * 0.70)):
        return True
    return False


def _looks_like_markdown_document(text: str) -> bool:
    value = (text or "").strip()
    if not value:
        return False
    if re.search(r"(?im)^\s*#\s*Slide\s+\d+\b", value):
        return True
    if re.search(r"(?im)^\s*\[(?:mineru|paddleocr)\]\s+", value):
        return True
    if "```" in value:
        return True
    if len(value) > 1200:
        return True
    if value.count("\n") >= 16:
        return True
    return False


def _longest_block_text(block: Dict[str, Any]) -> str:
    texts = [
        str(block.get(field) or "")
        for field in ("text", "latex", "raw_text", "description")
        if isinstance(block.get(field), str)
    ]
    return max(texts, key=len, default="")


def _mark_refiner_origin(block: Dict[str, Any], op: str, *, before_ids: list[str | None] | None = None):
    evidence = block.setdefault("evidence", {})
    evidence["refiner_op"] = op
    if before_ids:
        evidence["before_block_ids"] = before_ids
    block["origin"] = "refiner_op"


def _update_formula_fields(block: Dict[str, Any]):
    quality = assess_formula_text(block.get("text") or "")
    block["latex"] = quality.latex
    block["formula_quality"] = quality.to_dict()


def _find_block(blocks: List[Dict[str, Any]], block_id: str | None) -> Dict[str, Any] | None:
    index = _find_block_index(blocks, block_id)
    return blocks[index] if index is not None else None


def _find_block_index(blocks: List[Dict[str, Any]], block_id: str | None) -> int | None:
    if not block_id:
        return None
    for index, block in enumerate(blocks):
        if block.get("id") == block_id:
            return index
    return None


def _block_ids(page_ir: Dict[str, Any]) -> list[str]:
    return [str(block.get("id")) for block in page_ir.get("blocks") or [] if block.get("id")]


def _block_summaries(page_ir: Dict[str, Any]) -> list[Dict[str, Any]]:
    summaries = []
    for block in page_ir.get("blocks") or []:
        text = block.get("text") or block.get("description") or block.get("raw_text") or ""
        summaries.append(
            {
                "id": block.get("id"),
                "type": block.get("type"),
                "origin": block.get("origin"),
                "confidence": block.get("confidence"),
                "text_sha256": _sha256_text(text),
                "text_preview": _text_preview(text),
            }
        )
    return summaries


def _removed_spans(before: list[Dict[str, Any]], after: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    after_ids = {item.get("id") for item in after}
    return [
        {
            "block_id": item.get("id"),
            "type": item.get("type"),
            "text_sha256": item.get("text_sha256"),
            "text_preview": item.get("text_preview"),
        }
        for item in before
        if item.get("id") not in after_ids
    ]


def _removed_text_hashes(before: list[Dict[str, Any]], after: list[Dict[str, Any]]) -> list[str]:
    return [
        str(item.get("text_sha256"))
        for item in _removed_spans(before, after)
        if item.get("text_sha256")
    ]


def _target_text_sha256(summaries: list[Dict[str, Any]], op: Dict[str, Any]) -> str | None:
    target_ids = [op.get("id"), op.get("a"), op.get("b")]
    hashes = [item.get("text_sha256") for item in summaries if item.get("id") in target_ids and item.get("text_sha256")]
    if not hashes:
        return None
    return _sha256_text("|".join(str(value) for value in hashes))


def _text_preview(text: str, limit: int = 120) -> str | None:
    compact = " ".join(str(text or "").split())
    if len(compact) <= limit:
        return _redact_sensitive_preview(compact) if compact else None
    compact = _redact_sensitive_preview(compact)
    head_len = max(20, (limit - 3) // 2)
    tail_len = max(20, limit - 3 - head_len)
    return compact[:head_len].rstrip() + "..." + compact[-tail_len:].lstrip()


def _redact_sensitive_preview(text: str) -> str:
    redacted = re.sub(
        r"(?i)\b(api[_-]?key|token|secret|authorization|bearer)\b\s*[:=]\s*['\"]?([A-Za-z0-9._\-]{12,})",
        lambda match: f"{match.group(1)}=[REDACTED]",
        text,
    )
    redacted = re.sub(r"(?i)\bBearer\s+[A-Za-z0-9._\-]{12,}", "Bearer [REDACTED]", redacted)
    redacted = re.sub(r"\b(?:sk|ak|tk)-[A-Za-z0-9._\-]{16,}\b", "[REDACTED_TOKEN]", redacted)
    redacted = re.sub(r"\b[a-fA-F0-9]{40,}\b", "[REDACTED_HEX]", redacted)
    redacted = re.sub(r"\b[A-Za-z0-9_-]{48,}\b", "[REDACTED_TOKEN]", redacted)
    return redacted


def _sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _resolve_slide_no(page_ir: Dict[str, Any], slide_no: int | None) -> int:
    if slide_no is not None:
        return slide_no
    source_page = page_ir.get("source_page")
    if valid_source_page(source_page):
        return source_page
    return 0


def _looks_like_body_text(text: str) -> bool:
    stripped = text.strip()
    return len(stripped) > 120 or bool(re.search(r"[。.!?]\s*$", stripped))


def _looks_like_heading_text(text: str) -> bool:
    stripped = text.strip()
    return 1 <= len(stripped) <= 80 and stripped.endswith(":")


def _looks_like_figure_description(text: str) -> bool:
    stripped = text.strip()
    return (
        ("图示" in stripped or "图中" in stripped or "坐标图" in stripped or "流程图" in stripped)
        and ("左侧" in stripped or "右侧" in stripped or "节点" in stripped or "箭头" in stripped or "坐标轴" in stripped)
    )


def _formula_needs_normalize(text: str) -> bool:
    return formula_markup_needs_normalize(text)


def _normalize_formula_text(text: str) -> str:
    return normalize_formula_text(text)


def _formula_markup_evidence(text: str) -> str | None:
    match = re.search(r"\$\$(.*?)\$\$", text or "", flags=re.DOTALL)
    if not match:
        match = re.search(r"\\\[(.*?)\\\]", text or "", flags=re.DOTALL)
    if not match:
        return None
    return _text_preview(match.group(0), limit=160)


def _has_uncertain_marker(text: str) -> bool:
    lower = text.lower()
    return (
        "[?]" in text
        or "？" in text
        or "无法确定" in text
        or "看不清" in text
        or "不确定" in text
        or "uncertain" in lower
        or "illegible" in lower
    )
