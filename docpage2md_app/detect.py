from dataclasses import dataclass
import re
from typing import Any, Iterable, Literal

from .table_quality import assess_table


Severity = Literal["error", "warning", "info"]


VALIDATION_OP_HINTS = {
    "api_error_text": "mark_failed_page",
    "vision_failed_target": "mark_failed_page",
    "empty_markdown": "mark_failed_page",
    "heading_missing_or_mismatch": "fix_heading",
    "multiple_slide_headings": "mark_uncertain",
    "ctx_marker_leak": "mark_failed_page",
    "whole_document_code_fence": "strip_fence",
    "whole_document_code_fence_raw": "strip_fence",
    "unclosed_code_fence": "mark_uncertain",
    "display_math_unbalanced": "mark_uncertain",
    "inline_math_unbalanced": "mark_uncertain",
    "formula_brace_unbalanced": "normalize_formula",
    "formula_parenthesis_unbalanced": "normalize_formula",
    "formula_bracket_unbalanced": "normalize_formula",
    "latex_left_right_unbalanced": "normalize_formula",
    "latex_frac_missing_braces": "normalize_formula",
    "formula_markup_needs_normalize": "normalize_formula",
    "formula_uncertain_marker": "mark_uncertain",
    "table_structure_warning": "mark_uncertain",
    "short_body": "inspect_ocr_coverage",
    "ocr_coverage_low": "inspect_ocr_coverage",
    "unrendered_figure_analysis": "convert_figure_note",
    "figure_note_missing": "convert_figure_note",
    "target_text_block_missing": "inspect_ocr_coverage",
    "target_formula_block_missing": "mark_uncertain",
    "target_table_block_missing": "mark_uncertain",
    "target_figure_block_missing": "convert_figure_note",
    "target_uncertain_block_missing": "mark_uncertain",
    "target_image_ref_block_missing": "mark_uncertain",
    "possible_neighbor_leak": "mark_uncertain",
    "chatter_residue": "strip_chatter",
    "control_chars": "strip_control_chars",
    "inline_math_suspicious": "normalize_formula",
}


QUALITY_OP_HINTS = {
    "figure_unrecognizable": "mark_uncertain",
    "formula_empty": "mark_uncertain",
    "formula_brace_unbalanced": "normalize_formula",
    "formula_parenthesis_unbalanced": "normalize_formula",
    "formula_bracket_unbalanced": "normalize_formula",
    "latex_left_right_unbalanced": "normalize_formula",
    "latex_frac_missing_braces": "normalize_formula",
    "formula_uncertain_marker": "mark_uncertain",
    "table_quality_warning": "mark_uncertain",
}


@dataclass(frozen=True)
class Finding:
    finding_id: str
    page: int
    source: str
    kind: str
    severity: Severity
    message: str
    evidence: Any = None
    block_id: str | None = None
    block_type: str | None = None
    confidence: float | None = None
    current_text: str | None = None
    candidates: list[dict[str, Any]] | None = None
    op_hint: str | None = None
    op: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "id": self.finding_id,
            "page": self.page,
            "slide_no": self.page,
            "source": self.source,
            "kind": self.kind,
            "code": self.kind,
            "severity": self.severity,
            "message": self.message,
            "evidence": self.evidence,
            "block_id": self.block_id,
            "block_type": self.block_type,
            "confidence": self.confidence,
            "current_text": self.current_text,
            "candidates": self.candidates or [],
            "op_hint": self.op_hint,
            "op": self.op,
        }


Suspect = Finding


def build_initial_findings_pool(
    *,
    slide_no: int,
    page_ir: dict[str, Any] | None = None,
    stage1: dict[str, Any] | None = None,
    stage2: dict[str, Any] | None = None,
    validation: dict[str, Any] | None = None,
    quality: dict[str, Any] | None = None,
    block_refiner: dict[str, Any] | None = None,
    blocks: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if page_ir is not None and blocks is None:
        blocks = page_ir.get("blocks") if isinstance(page_ir.get("blocks"), list) else None
    findings: list[Finding] = []
    findings.extend(_stage_findings(slide_no, "stage1", stage1 or {}, len(findings)))
    findings.extend(_stage_findings(slide_no, "stage2", stage2 or {}, len(findings)))
    findings.extend(_validation_findings(slide_no, validation or {}, len(findings)))
    block_findings = _block_findings(slide_no, blocks or [], len(findings))
    findings.extend(block_findings)
    findings.extend(_dual_engine_findings(slide_no, page_ir or {}, blocks or [], len(findings)))
    findings.extend(_vision_crop_findings(slide_no, blocks or [], len(findings)))
    if not blocks:
        findings.extend(_quality_findings(slide_no, quality or {}, len(findings)))
    findings.extend(_block_refiner_findings(slide_no, block_refiner or {}, len(findings)))
    return [finding.to_dict() for finding in findings]


def detect_page_suspects(**kwargs: Any) -> list[dict[str, Any]]:
    return build_initial_findings_pool(**kwargs)


def summarize_findings(pages: Iterable[dict[str, Any]]) -> dict[str, Any]:
    by_code: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    by_source: dict[str, int] = {}
    by_op: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    total = 0
    actionable_total = 0
    for page in pages:
        findings = _page_initial_findings(page)
        for finding in findings:
            total += 1
            code = str(finding.get("code") or finding.get("kind") or "unknown")
            kind = str(finding.get("kind") or code)
            source = str(finding.get("source") or "unknown")
            severity = str(finding.get("severity") or "unknown")
            by_code[code] = by_code.get(code, 0) + 1
            by_kind[kind] = by_kind.get(kind, 0) + 1
            by_source[source] = by_source.get(source, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
            op = finding.get("op") if isinstance(finding.get("op"), dict) else None
            op_name = str((op or {}).get("op") or finding.get("op_hint") or "")
            if op_name:
                actionable_total += 1
                by_op[op_name] = by_op.get(op_name, 0) + 1
    return {
        "total": total,
        "actionable_total": actionable_total,
        "by_code": by_code,
        "by_kind": by_kind,
        "by_source": by_source,
        "by_op": by_op,
        "by_severity": by_severity,
    }


def summarize_suspects(pages: Iterable[dict[str, Any]]) -> dict[str, Any]:
    return summarize_findings(pages)


def _page_initial_findings(page: dict[str, Any]) -> list[dict[str, Any]]:
    findings = page.get("findings")
    if isinstance(findings, dict):
        initial = findings.get("initial") or []
        return [item for item in initial if isinstance(item, dict)]
    legacy = page.get("suspects") or []
    return [item for item in legacy if isinstance(item, dict)]


def _stage_findings(slide_no: int, stage: str, state: dict[str, Any], offset: int) -> list[Finding]:
    status = state.get("status")
    if status not in {"failed", "blocked"}:
        return []
    code = str(state.get("error_code") or f"{stage}_{status}")
    message = str(state.get("error_message") or status)
    return [
        Finding(
            finding_id=_finding_id(slide_no, offset + 1),
            page=slide_no,
            source="deterministic_detector",
            kind=code,
            severity="error",
            message=message,
            evidence={"stage": stage, "status": status, "path": state.get("path")},
            op_hint="mark_failed_page",
        )
    ]


def _validation_findings(slide_no: int, validation: dict[str, Any], offset: int) -> list[Finding]:
    findings = []
    issues = list(validation.get("errors") or []) + list(validation.get("warnings") or [])
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        code = str(issue.get("code") or "validation_issue")
        severity = _severity(issue.get("severity") or "warning")
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="validator_precheck",
                kind=code,
                severity=severity,
                message=str(issue.get("message") or code),
                evidence=issue.get("evidence"),
                op_hint=VALIDATION_OP_HINTS.get(code),
            )
        )
    return findings


def _quality_findings(slide_no: int, quality: dict[str, Any], offset: int) -> list[Finding]:
    findings = []
    for warning in quality.get("warnings") or []:
        if not isinstance(warning, dict):
            continue
        code = str(warning.get("code") or "quality_warning")
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="deterministic_detector",
                kind=code,
                severity="warning",
                message=str(warning.get("message") or code),
                evidence=_quality_evidence(warning),
                op_hint=QUALITY_OP_HINTS.get(code),
            )
        )
    return findings


def _block_findings(slide_no: int, blocks: list[dict[str, Any]], offset: int) -> list[Finding]:
    findings = []
    for block in blocks:
        block_id = block.get("id")
        block_type = block.get("type")
        if not block_id or not block_type:
            continue
        if block_type in {"formula_inline", "formula_block"}:
            findings.extend(_formula_block_findings(slide_no, block, offset + len(findings)))
        elif block_type == "table":
            finding = _table_block_finding(slide_no, block, offset + len(findings) + 1)
            if finding:
                findings.append(finding)
        elif block_type == "figure_note" and block.get("unrecognizable"):
            findings.append(
                Finding(
                    finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                    page=slide_no,
                    source="deterministic_detector",
                    kind="figure_unrecognizable",
                    severity="warning",
                    message="图示 block 标记为不可可靠识别。",
                    evidence={"figure_type": block.get("figure_type")},
                    block_id=str(block_id),
                    block_type=str(block_type),
                    op_hint="mark_uncertain",
                    op={"op": "mark_uncertain", "id": block_id},
                )
            )
    return findings


def _formula_block_findings(slide_no: int, block: dict[str, Any], offset: int) -> list[Finding]:
    quality = block.get("formula_quality") if isinstance(block.get("formula_quality"), dict) else {}
    warnings = quality.get("warnings") or []
    findings = []
    for warning in warnings:
        if not isinstance(warning, dict):
            continue
        code = str(warning.get("code") or "formula_quality_warning")
        block_id = str(block.get("id"))
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="deterministic_detector",
                kind=code,
                severity="warning",
                message=str(warning.get("message") or code),
                evidence={"latex": quality.get("latex"), "warning": warning.get("evidence")},
                block_id=block_id,
                block_type=str(block.get("type") or "formula_block"),
                current_text=quality.get("latex") or block.get("latex") or block.get("text"),
                op_hint="mark_uncertain",
                op={"op": "mark_uncertain", "id": block_id},
            )
        )
    return findings


def _table_block_finding(slide_no: int, block: dict[str, Any], index: int) -> Finding | None:
    quality = assess_table(block.get("text") or "")
    if quality.reliable:
        return None
    block_id = str(block.get("id"))
    return Finding(
        finding_id=_finding_id(slide_no, index),
        page=slide_no,
        source="deterministic_detector",
        kind="table_quality_warning",
        severity="warning",
        message="表格结构不可靠。",
        evidence=quality.to_dict(),
        block_id=block_id,
        block_type=str(block.get("type") or "table"),
        current_text=block.get("text"),
        op_hint="mark_uncertain",
        op={"op": "mark_uncertain", "id": block_id},
    )


def _block_refiner_findings(slide_no: int, block_refiner: dict[str, Any], offset: int) -> list[Finding]:
    findings = []
    for item in block_refiner.get("dismissed") or []:
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "block_refiner_dismissed")
        op = item.get("op") if isinstance(item.get("op"), dict) else {}
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="deterministic_detector",
                kind=code,
                severity="info",
                message=str(item.get("reason") or code),
                evidence=item.get("dismissed"),
                block_id=op.get("id") or op.get("a"),
                op_hint=op.get("op"),
                op=op or None,
            )
        )
    return findings


def _dual_engine_findings(slide_no: int, page_ir: dict[str, Any], blocks: list[dict[str, Any]], offset: int) -> list[Finding]:
    fusion = page_ir.get("fusion") if isinstance(page_ir.get("fusion"), dict) else {}
    groups = fusion.get("candidate_groups") if isinstance(fusion.get("candidate_groups"), list) else []
    if not groups:
        return []
    blocks_by_group = _blocks_by_fusion_group(blocks)
    findings: list[Finding] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        candidates = [item for item in group.get("candidates") or [] if isinstance(item, dict)]
        if not candidates:
            continue
        warnings = [str(item) for item in (group.get("warnings") or [])]
        match_reason = str(group.get("match_reason") or "")
        kind = _dual_group_kind(group, candidates, warnings, match_reason)
        if kind is None:
            continue
        group_id = str(group.get("group_id") or "")
        target_blocks = blocks_by_group.get(group_id) or []
        target_block = target_blocks[0] if target_blocks else {}
        severity: Severity = "warning"
        if kind == "engine_unmatched_block" and len(_candidate_texts(candidates)) < 2:
            severity = "info"
        block_id = str(target_block.get("id") or "") or _first_candidate_block_id(candidates)
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="dual_engine_diff",
                kind=kind,
                severity=severity,
                message=_dual_group_message(kind, candidates, match_reason),
                evidence={
                    "group_id": group_id,
                    "match_reason": match_reason,
                    "match_score": group.get("match_score"),
                    "type_hint": group.get("type_hint"),
                    "warnings": warnings,
                    "created_block_ids": [block.get("id") for block in target_blocks if isinstance(block, dict)],
                },
                block_id=block_id,
                block_type=str(target_block.get("type") or group.get("type_hint") or ""),
                confidence=_group_confidence(candidates),
                current_text=_block_text(target_block) if target_block else _safe_text(candidates[0].get("text"), 500),
                candidates=[_public_finding_candidate(candidate) for candidate in candidates],
                op_hint="replace_text_span_checked" if kind in {"ocr_text_conflict", "formula_candidate_conflict"} else "mark_uncertain",
            )
        )
    return findings


def _vision_crop_findings(slide_no: int, blocks: list[dict[str, Any]], offset: int) -> list[Finding]:
    findings: list[Finding] = []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        evidence = block.get("evidence") if isinstance(block.get("evidence"), dict) else {}
        vision = evidence.get("vision_enrichment") if isinstance(evidence.get("vision_enrichment"), dict) else {}
        if not vision:
            continue
        changed_fields = [str(item) for item in (vision.get("changed_fields") or []) if item]
        text = _block_text(block)
        uncertain = _has_uncertain_marker(text) or bool(block.get("unrecognizable"))
        low_confidence = _float_or_none(block.get("confidence")) is not None and float(block.get("confidence")) < 0.72
        if not changed_fields and not uncertain and not low_confidence:
            continue
        if uncertain:
            kind = "vision_crop_uncertain"
            severity: Severity = "warning"
            op_hint = "mark_uncertain"
            message = "Vision 裁剪图证据仍包含不确定识别，需要 Brain 结合上下文审阅。"
        elif low_confidence:
            kind = "vision_crop_low_confidence"
            severity = "warning"
            op_hint = "mark_uncertain"
            message = "Vision 裁剪图结果置信度偏低，需要结合上下文和原 OCR 证据核验。"
        else:
            kind = "vision_crop_changed_block"
            severity = "info"
            op_hint = "replace_text_span_checked"
            message = "Vision 裁剪图结果改写了 block 内容，需要作为证据供 Brain 审阅。"
        block_id = str(block.get("id") or "")
        findings.append(
            Finding(
                finding_id=_finding_id(slide_no, offset + len(findings) + 1),
                page=slide_no,
                source="vision_crop_evidence",
                kind=kind,
                severity=severity,
                message=message,
                evidence={
                    "changed_fields": changed_fields,
                    "original_text": _safe_text(vision.get("original_text"), 500),
                    "result_text": _safe_text(vision.get("result_text"), 500),
                    "content_sha256": vision.get("content_sha256"),
                    "model_request_id": vision.get("model_request_id"),
                    "source_engine": block.get("source_engine"),
                },
                block_id=block_id,
                block_type=str(block.get("type") or ""),
                confidence=_float_or_none(block.get("confidence")),
                current_text=text,
                candidates=[
                    {
                        "source": "pre_vision_ocr",
                        "text": _safe_text(vision.get("original_text"), 500),
                    },
                    {
                        "source": "vision_crop",
                        "text": _safe_text(vision.get("result_text") or text, 500),
                    },
                ],
                op_hint=op_hint,
            )
        )
    return findings


def _quality_evidence(warning: dict[str, Any]) -> Any:
    if "details" in warning:
        return warning.get("details")
    if "latex" in warning:
        return {"latex": warning.get("latex")}
    return None


def _severity(value: str) -> Severity:
    if value == "error":
        return "error"
    if value == "info":
        return "info"
    return "warning"


def _finding_id(slide_no: int, index: int) -> str:
    return f"p{slide_no:04d}-f{index:03d}"


def _suspect_id(slide_no: int, index: int) -> str:
    return _finding_id(slide_no, index)


def _blocks_by_fusion_group(blocks: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for block in blocks:
        if not isinstance(block, dict):
            continue
        evidence = block.get("evidence") if isinstance(block.get("evidence"), dict) else {}
        fusion = evidence.get("fusion") if isinstance(evidence.get("fusion"), dict) else {}
        group_id = str(fusion.get("group_id") or "")
        if group_id:
            grouped.setdefault(group_id, []).append(block)
    return grouped


def _dual_group_kind(
    group: dict[str, Any],
    candidates: list[dict[str, Any]],
    warnings: list[str],
    match_reason: str,
) -> str | None:
    if "candidate_text_conflict" in warnings or _public_candidate_text_conflict(candidates):
        if str(group.get("type_hint") or "") in {"formula_block", "formula_inline"}:
            return "formula_candidate_conflict"
        return "ocr_text_conflict"
    if match_reason.startswith("unmatched"):
        return "engine_unmatched_block"
    if any(_candidate_has_quality_warning(candidate) for candidate in candidates):
        return "candidate_quality_warning"
    return None


def _dual_group_message(kind: str, candidates: list[dict[str, Any]], match_reason: str) -> str:
    sources = " / ".join(sorted({str(candidate.get("source") or "unknown") for candidate in candidates}))
    if kind == "formula_candidate_conflict":
        return f"MinerU/PaddleOCR 对同一区域的公式识别不一致，来源：{sources}。"
    if kind == "ocr_text_conflict":
        return f"MinerU/PaddleOCR 对同一区域的文字识别不一致，来源：{sources}。"
    if kind == "engine_unmatched_block":
        return f"只有一个解析引擎识别到该 block，匹配状态：{match_reason}。"
    return f"双引擎候选包含质量警告，来源：{sources}。"


def _public_candidate_text_conflict(candidates: list[dict[str, Any]]) -> bool:
    texts = _candidate_texts(candidates)
    if len(texts) < 2:
        return False
    if min(len(text) for text in texts) < 8:
        return False
    return len(set(texts)) > 1


def _candidate_texts(candidates: list[dict[str, Any]]) -> list[str]:
    texts = []
    for candidate in candidates:
        text = _normalize_compare_text(str(candidate.get("text") or ""))
        if text:
            texts.append(text)
    return texts


def _candidate_has_quality_warning(candidate: dict[str, Any]) -> bool:
    warnings = {str(item) for item in (candidate.get("warnings") or [])}
    severe = {
        "has_raw_unicode_math",
        "spaced_math_operator_artifact",
        "formula_empty",
        "formula_uncertain_marker",
        "formula_brace_unbalanced",
        "formula_parenthesis_unbalanced",
        "formula_bracket_unbalanced",
        "latex_left_right_unbalanced",
        "latex_frac_missing_braces",
        "table_unreliable",
        "uncertain_marker",
        "empty_candidate",
    }
    return bool(warnings & severe)


def _first_candidate_block_id(candidates: list[dict[str, Any]]) -> str | None:
    for candidate in candidates:
        block_id = str(candidate.get("block_id") or "")
        if block_id:
            return block_id
    return None


def _public_finding_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": candidate.get("source"),
        "candidate_id": candidate.get("candidate_id"),
        "block_id": candidate.get("block_id"),
        "type": candidate.get("type"),
        "text": _safe_text(candidate.get("text"), 500),
        "confidence": candidate.get("confidence"),
        "quality_score": candidate.get("quality_score"),
        "warnings": candidate.get("warnings") or [],
    }


def _group_confidence(candidates: list[dict[str, Any]]) -> float | None:
    values = [_float_or_none(candidate.get("confidence")) for candidate in candidates]
    values = [value for value in values if value is not None]
    if not values:
        return None
    return round(min(values), 4)


def _block_text(block: dict[str, Any]) -> str:
    return str(block.get("latex") or block.get("text") or block.get("description") or "").strip()


def _normalize_compare_text(text: str) -> str:
    text = re.sub(r"\s+", "", text or "")
    return re.sub(r"[^\w\\]+", "", text, flags=re.UNICODE).lower()


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_text(value: Any, limit: int = 500) -> str:
    text = str(value or "").strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def _has_uncertain_marker(text: str) -> bool:
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
