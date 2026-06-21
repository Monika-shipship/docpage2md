import re
from dataclasses import dataclass
from typing import Any, Dict, List

from .validators import ValidationIssue, is_api_error_text, validate_slide_markdown


KNOWN_OPS = {
    "strip_chatter",
    "fix_heading",
    "drop_empty",
    "merge_broken_line",
    "mark_failed_page",
}

SAFE_OPS = {
    "strip_chatter",
    "fix_heading",
    "drop_empty",
    "merge_broken_line",
}


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

    return suspects


def apply_op_checked(
    markdown: str,
    suspect: Suspect,
    slide_no: int,
    *,
    raw_response: str | None = None,
    target_raw: str | None = None,
) -> tuple[str, bool, Dict[str, Any]]:
    if suspect.op not in SAFE_OPS or is_api_error_text(raw_response) or is_api_error_text(markdown):
        return markdown, False, {"reason": "unsafe_or_error_text"}

    before = validate_slide_markdown(markdown, slide_no, raw_response=raw_response, target_raw=target_raw)
    candidate = _apply_op(markdown, suspect.op, slide_no)
    if candidate == markdown:
        return markdown, False, {"reason": "no_change"}

    after = validate_slide_markdown(candidate, slide_no, raw_response=raw_response, target_raw=target_raw)
    if _is_no_worse(before.errors, after.errors):
        return candidate, True, after.to_dict()
    return markdown, False, {"reason": "validation_would_get_worse", "validation": after.to_dict()}


def refine_slide_markdown(
    markdown: str,
    slide_no: int,
    *,
    raw_response: str | None = None,
    target_raw: str | None = None,
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
        )
        if ok:
            item = suspect.to_dict()
            item["validation"] = validation
            applied.append(item)
        else:
            item = suspect.to_dict()
            item["dismissed"] = validation
            dismissed.append(item)

    final_validation = validate_slide_markdown(current, slide_no, raw_response=raw_response, target_raw=target_raw)
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
