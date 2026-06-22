import re
from dataclasses import dataclass
from typing import Literal


FORMULA_QUALITY_SCHEMA_VERSION = 1
Severity = Literal["warning"]


@dataclass(frozen=True)
class FormulaQualityIssue:
    code: str
    severity: Severity
    message: str
    evidence: str | None = None

    def to_dict(self):
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "evidence": self.evidence,
        }


@dataclass(frozen=True)
class FormulaQualityResult:
    latex: str
    warnings: list[FormulaQualityIssue]
    uncertain: bool

    @property
    def ok(self) -> bool:
        return not self.warnings

    def to_dict(self):
        return {
            "schema_version": FORMULA_QUALITY_SCHEMA_VERSION,
            "ok": self.ok,
            "latex": self.latex,
            "warnings": [warning.to_dict() for warning in self.warnings],
            "uncertain": self.uncertain,
        }


def assess_formula_text(text: str) -> FormulaQualityResult:
    latex = normalize_formula_text(text)
    warnings: list[FormulaQualityIssue] = []
    if not latex:
        warnings.append(_issue("formula_empty", "公式 block 为空。"))
        return FormulaQualityResult(latex, warnings, False)

    if _unbalanced_pair(latex, "{", "}"):
        warnings.append(_issue("formula_brace_unbalanced", "公式中的花括号数量不平衡。", latex[:120]))
    if _unbalanced_pair(latex, "(", ")"):
        warnings.append(_issue("formula_parenthesis_unbalanced", "公式中的圆括号数量不平衡。", latex[:120]))
    if _unbalanced_pair(latex, "[", "]"):
        warnings.append(_issue("formula_bracket_unbalanced", "公式中的方括号数量不平衡。", latex[:120]))
    if len(re.findall(r"\\left\b", latex)) != len(re.findall(r"\\right\b", latex)):
        warnings.append(_issue("latex_left_right_unbalanced", "\\left 与 \\right 数量不匹配。", latex[:120]))
    if re.search(r"\\frac(?!\s*\{)", latex):
        warnings.append(_issue("latex_frac_missing_braces", "\\frac 后缺少花括号参数。", latex[:120]))
    if _looks_truncated(latex):
        warnings.append(_issue("formula_truncated", "公式疑似在运算符或未完成命令处截断。", latex[:120]))
    if _is_isolated_operator_formula(latex):
        warnings.append(_issue("formula_isolated_operator", "公式只有孤立运算符或关系符，无法可靠使用。", latex[:120]))
    if _looks_like_reasoning_without_formula(latex):
        warnings.append(_issue("formula_reasoning_without_latex", "公式 block 疑似包含模型思考说明而不是公式。", latex[:120]))

    uncertain = has_uncertain_formula_marker(latex)
    if uncertain:
        warnings.append(_issue("formula_uncertain_marker", "公式中包含不确定识别标记。", latex[:120]))
    return FormulaQualityResult(latex, _dedupe_issues(warnings), uncertain)


def normalize_formula_text(text: str) -> str:
    stripped = (text or "").strip()
    if stripped.startswith("$$") and stripped.endswith("$$"):
        stripped = stripped[2:-2].strip()
    if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
        stripped = stripped[2:-2].strip()
    if stripped.startswith(r"\(") and stripped.endswith(r"\)"):
        stripped = stripped[2:-2].strip()
    return stripped


def has_uncertain_formula_marker(text: str) -> bool:
    lower = (text or "").lower()
    return (
        "[?]" in text
        or "？" in text
        or "无法确定" in text
        or "看不清" in text
        or "不确定" in text
        or "uncertain" in lower
        or "illegible" in lower
    )


def _looks_truncated(text: str) -> bool:
    stripped = (text or "").strip()
    if not stripped:
        return False
    if re.search(r"(?:[=+\-*/^_,]|\\frac|\\sqrt|\\sum|\\int|\\lim)\s*$", stripped):
        return True
    return bool(re.search(r"\\[A-Za-z]+\\?$", stripped))


def _is_isolated_operator_formula(text: str) -> bool:
    stripped = re.sub(r"\s+", "", text or "")
    if not stripped:
        return False
    return bool(re.fullmatch(r"[=≈≤≥<>+\-*/^_{}()[\],.;:|]+", stripped))


def _looks_like_reasoning_without_formula(text: str) -> bool:
    lower = (text or "").lower()
    markers = (
        "thinking",
        "reasoning",
        "analysis:",
        "思考",
        "推理过程",
        "我将",
        "我们需要",
    )
    has_math_signal = bool(re.search(r"(\\[A-Za-z]+|[=≈≤≥+\-*/^_{}]|\d)", text or ""))
    return any(marker in lower for marker in markers) and not has_math_signal


def _unbalanced_pair(text: str, left: str, right: str) -> bool:
    escaped_left = re.escape(left)
    escaped_right = re.escape(right)
    return len(re.findall(rf"(?<!\\){escaped_left}", text)) != len(re.findall(rf"(?<!\\){escaped_right}", text))


def _dedupe_issues(issues: list[FormulaQualityIssue]) -> list[FormulaQualityIssue]:
    seen = set()
    deduped = []
    for issue in issues:
        key = (issue.code, issue.evidence)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(issue)
    return deduped


def _issue(code: str, message: str, evidence: str | None = None) -> FormulaQualityIssue:
    return FormulaQualityIssue(code=code, severity="warning", message=message, evidence=evidence)
