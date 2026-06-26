from pathlib import Path
from typing import Any, Dict, Iterable

from .artifacts import (
    RUN_REPORT_SCHEMA_VERSION,
    now_iso,
    report_model_identity,
    report_prompt_identity,
)
from .config import AppConfig
from .content_inventory import merge_content_inventory_summaries
from .detect import build_initial_findings_pool, summarize_findings
from .provenance import merge_provenance_summaries
from .table_quality import assess_table
from .versioning import DOCPAGE2MD_PIPELINE_VERSION


def build_run_report(
    doc_name: str,
    target_images: Iterable[str],
    start_idx: int,
    config: AppConfig,
) -> tuple[Dict[str, Any], Dict[int, Dict[str, Any]]]:
    pages = []
    for offset, image_path in enumerate(target_images):
        slide_no = start_idx + offset + 1
        pages.append(
            {
                "slide_no": slide_no,
                "image_path": str(Path(image_path)),
                "image_sha256": None,
                "page_image_ref": None,
                "stage1": _stage_state(),
                "stage2": _stage_state(),
                "validation": {"ok": None, "errors": [], "warnings": []},
                "quality": _empty_quality_summary(),
                "findings": _empty_findings(),
                "provenance": {"schema_version": None, "entries": [], "summary": {}},
                "content_inventory": {"schema_version": None, "entries": [], "summary": {}},
                "block_refiner": {
                    "version": None,
                    "changed": False,
                    "applied_ops": [],
                    "dismissed": [],
                    "op_audit": [],
                    "validation": None,
                },
                "op_audit": [],
                "refiner": {"changed": False, "applied_ops": [], "dismissed": []},
                "final": {
                    "status": "pending",
                    "included_in_full": False,
                    "reason": None,
                    "markdown_source": None,
                },
            }
        )

    report = {
        "schema_version": RUN_REPORT_SCHEMA_VERSION,
        "pipeline_version": DOCPAGE2MD_PIPELINE_VERSION,
        "doc_name": doc_name,
        "started_at": now_iso(),
        "finished_at": None,
        "status": "running",
        "models": report_model_identity(config),
        "prompts": report_prompt_identity(),
        "summary": {},
        "cost": {
            "estimated": None,
            "actual_tokens": None,
            "note": "Per-request token usage is not available from the current streaming API wrappers.",
        },
        "pages": pages,
    }
    return report, {page["slide_no"]: page for page in pages}


def finalize_run_report(report: Dict[str, Any]) -> Dict[str, Any]:
    report["finished_at"] = now_iso()
    pages = report.get("pages") or []
    pages_ok = sum(1 for page in pages if page.get("final", {}).get("status") == "ok")
    fail_open_pages = sum(1 for page in pages if page.get("final", {}).get("status") == "fail_open")
    pages_failed = sum(1 for page in pages if page.get("final", {}).get("status") in ("failed", "fail_open"))
    markdown_pages = sum(1 for page in pages if page.get("final", {}).get("included_in_full"))
    stage1_cache_hits = sum(1 for page in pages if page.get("stage1", {}).get("cache") == "hit")
    stage2_cache_hits = sum(1 for page in pages if page.get("stage2", {}).get("cache") == "hit")
    warnings = sum(len(page.get("validation", {}).get("warnings") or []) for page in pages)
    block_refiner_applied_ops = sum(len(page.get("block_refiner", {}).get("applied_ops") or []) for page in pages)
    op_audit_status_counts = _op_audit_status_counts(pages)
    op_rejection_reasons = _op_audit_rejection_reasons(pages)
    contract_error_codes = _op_audit_contract_error_codes(pages)
    formula_warning_count = sum(
        _count_validation_codes(page, ("formula_", "latex_"))
        + int(page.get("quality", {}).get("formula_warning_count") or 0)
        for page in pages
    )
    table_warning_count = sum(
        _count_validation_codes(page, ("table_",)) + int(page.get("quality", {}).get("table_warning_count") or 0)
        for page in pages
    )
    ocr_coverage_warning_count = sum(_count_validation_codes(page, ("ocr_coverage_",)) for page in pages)
    block_counts = _sum_block_counts(pages)
    provenance_summary = merge_provenance_summaries(pages)
    content_inventory_summary = merge_content_inventory_summaries(pages)

    report["summary"] = {
        "pages_total": len(pages),
        "pages_ok": pages_ok,
        "pages_failed": pages_failed,
        "stage1_cache_hits": stage1_cache_hits,
        "stage2_cache_hits": stage2_cache_hits,
        "fail_open_pages": fail_open_pages,
        "markdown_pages": markdown_pages,
        "validation_warnings": warnings,
        "block_refiner_changed_pages": sum(1 for page in pages if page.get("block_refiner", {}).get("changed")),
        "block_refiner_applied_ops": block_refiner_applied_ops,
        "op_audit": {
            "total": sum(op_audit_status_counts.values()),
            "by_status": op_audit_status_counts,
            "rejection_reasons": op_rejection_reasons,
            "contract_error_codes": contract_error_codes,
            "removed_spans": _op_audit_removed_span_count(pages),
            "degraded": _op_audit_degraded_count(pages),
        },
        "op_rejection_reasons": op_rejection_reasons,
        "contract_error_codes": contract_error_codes,
        "brain_discovered_count": _brain_discovered_count(pages),
        "block_counts": block_counts,
        "semantic_role_counts": _sum_semantic_role_counts(pages),
        "provenance": provenance_summary,
        "content_inventory": content_inventory_summary,
        "uncertain_block_count": block_counts.get("uncertain", 0),
        "figure_count": block_counts.get("figure_note", 0),
        "figure_warning_count": sum(int(page.get("quality", {}).get("figure_warning_count") or 0) for page in pages),
        "formula_warning_count": formula_warning_count,
        "table_warning_count": table_warning_count,
        "ocr_coverage_warning_count": ocr_coverage_warning_count,
        "markdown_source_counts": _markdown_source_counts(pages),
        "findings": summarize_findings(pages),
    }
    report["cost"]["actual_tokens"] = _actual_token_usage(pages)
    report["cost"]["note"] = (
        "Actual token usage is recorded only when the provider wrapper returns usage; "
        "unsupported providers remain null."
    )
    if pages_ok == len(pages):
        report["status"] = "ok"
    elif pages_ok + fail_open_pages == len(pages) and fail_open_pages:
        report["status"] = "fail_open"
    elif pages_ok > 0 or fail_open_pages > 0:
        report["status"] = "partial_failed"
    else:
        report["status"] = "failed"
    return report


def stage_failed(page: Dict[str, Any], stage: str, code: str, message: str):
    page[stage].update(
        {
            "status": "failed",
            "error_code": code,
            "error_message": message,
        }
    )


def stage_blocked(page: Dict[str, Any], stage: str, code: str, message: str):
    page[stage].update(
        {
            "status": "blocked",
            "error_code": code,
            "error_message": message,
        }
    )


def summarize_blocks(blocks: Iterable[Dict[str, Any]] | None) -> Dict[str, Any]:
    summary = _empty_quality_summary()
    for block in blocks or []:
        block_type = block.get("type") or "unknown"
        summary["block_counts"][block_type] = summary["block_counts"].get(block_type, 0) + 1
        role = block.get("semantic_role")
        if role:
            summary["semantic_role_counts"][role] = summary["semantic_role_counts"].get(role, 0) + 1
        if block_type == "uncertain":
            summary["uncertain_block_count"] += 1
        elif block_type == "figure_note":
            summary["figure_count"] += 1
            if block.get("unrecognizable"):
                summary["figure_warning_count"] += 1
                summary["warnings"].append(
                    {
                        "code": "figure_unrecognizable",
                        "message": "图示 block 标记为不可可靠识别。",
                        "figure_type": block.get("figure_type"),
                    }
                )
        elif block_type in {"formula_inline", "formula_block"}:
            warnings = _formula_block_warnings(block)
            if warnings:
                summary["formula_warning_count"] += 1
                summary["warnings"].extend(warnings)
        elif block_type == "table":
            quality = assess_table(block.get("text") or "")
            if quality.errors or quality.warnings:
                summary["table_warning_count"] += 1
                summary["warnings"].append(
                    {
                        "code": "table_quality_warning",
                        "message": "表格存在质量警告。" if quality.reliable else "表格结构不可靠。",
                        "details": quality.to_dict(),
                    }
                )
    return summary


def refresh_page_findings(
    page: Dict[str, Any],
    blocks: list[Dict[str, Any]] | None = None,
    page_ir: Dict[str, Any] | None = None,
) -> list[Dict[str, Any]]:
    findings = build_initial_findings_pool(
        slide_no=int(page.get("slide_no") or 0),
        page_ir=page_ir,
        stage1=page.get("stage1") or {},
        stage2=page.get("stage2") or {},
        validation=page.get("validation") or {},
        quality=page.get("quality") or {},
        block_refiner=page.get("block_refiner") or {},
        blocks=blocks,
    )
    page_findings = page.get("findings") if isinstance(page.get("findings"), dict) else _empty_findings()
    page_findings["initial"] = findings
    page.setdefault("findings", page_findings)
    page["findings"] = page_findings
    page.pop("suspects", None)
    return findings


def refresh_page_suspects(
    page: Dict[str, Any],
    blocks: list[Dict[str, Any]] | None = None,
    page_ir: Dict[str, Any] | None = None,
) -> list[Dict[str, Any]]:
    return refresh_page_findings(page, blocks, page_ir)


def _stage_state():
    return {
        "status": "pending",
        "cache": None,
        "path": None,
        "elapsed_seconds": None,
        "sha256": None,
        "usage": None,
        "request_id": None,
        "provider_latency": None,
        "error_code": None,
        "error_message": None,
        "warnings": [],
    }


def _empty_quality_summary() -> Dict[str, Any]:
    return {
        "block_counts": {},
        "semantic_role_counts": {},
        "uncertain_block_count": 0,
        "figure_count": 0,
        "figure_warning_count": 0,
        "formula_warning_count": 0,
        "table_warning_count": 0,
        "warnings": [],
    }


def _empty_findings() -> Dict[str, Any]:
    return {
        "initial": [],
        "brain_decisions": [],
        "brain_discovered": [],
    }


def _count_validation_codes(page: Dict[str, Any], prefixes: tuple[str, ...]) -> int:
    warnings = page.get("validation", {}).get("warnings") or []
    return sum(1 for issue in warnings if str(issue.get("code") or "").startswith(prefixes))


def _sum_block_counts(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for page in pages:
        for block_type, count in (page.get("quality", {}).get("block_counts") or {}).items():
            counts[block_type] = counts.get(block_type, 0) + count
    return counts


def _sum_semantic_role_counts(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for page in pages:
        for role, count in (page.get("quality", {}).get("semantic_role_counts") or {}).items():
            counts[role] = counts.get(role, 0) + count
    return counts


def _markdown_source_counts(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for page in pages:
        source = page.get("final", {}).get("markdown_source")
        if not isinstance(source, dict):
            continue
        kind = str(source.get("kind") or "unknown")
        counts[kind] = counts.get(kind, 0) + 1
    return counts


def _op_audit_status_counts(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for page in pages:
        audits = page.get("op_audit")
        if not isinstance(audits, list):
            audits = page.get("block_refiner", {}).get("op_audit") or []
        for audit in audits:
            if not isinstance(audit, dict):
                continue
            status = str(audit.get("status") or "unknown")
            counts[status] = counts.get(status, 0) + 1
    return counts


def _op_audit_removed_span_count(pages: list[Dict[str, Any]]) -> int:
    total = 0
    for audit in _iter_op_audits(pages):
        total += len(audit.get("removed_spans") or [])
    return total


def _op_audit_degraded_count(pages: list[Dict[str, Any]]) -> int:
    return sum(1 for audit in _iter_op_audits(pages) if audit.get("degraded"))


def _op_audit_rejection_reasons(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for audit in _iter_op_audits(pages):
        if audit.get("status") != "rejected":
            continue
        reason = str(audit.get("reason") or "unknown")
        counts[reason] = counts.get(reason, 0) + 1
    return counts


def _op_audit_contract_error_codes(pages: list[Dict[str, Any]]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for audit in _iter_op_audits(pages):
        if audit.get("status") != "rejected":
            continue
        for error in audit.get("errors") or []:
            code = str(error or "unknown")
            counts[code] = counts.get(code, 0) + 1
    return counts


def _brain_discovered_count(pages: list[Dict[str, Any]]) -> int:
    total = 0
    for page in pages:
        brain = page.get("brain") if isinstance(page.get("brain"), dict) else {}
        total += int(brain.get("brain_discovered_count") or 0)
        if brain.get("brain_discovered_count") is not None:
            continue
        for audit in page.get("op_audit") or []:
            if isinstance(audit, dict) and audit.get("decision") == "brain_discovered":
                total += 1
    return total


def _iter_op_audits(pages: list[Dict[str, Any]]):
    for page in pages:
        audits = page.get("op_audit")
        if not isinstance(audits, list):
            audits = page.get("block_refiner", {}).get("op_audit") or []
        for audit in audits:
            if isinstance(audit, dict):
                yield audit


def _actual_token_usage(pages: list[Dict[str, Any]]) -> Dict[str, Any] | None:
    stages = {}
    total_input = 0
    total_output = 0
    total = 0
    seen = False
    for stage_name in ("stage1", "stage2", "vision", "brain"):
        stage_usage = []
        for page in pages:
            usage = page.get(stage_name, {}).get("usage")
            if not isinstance(usage, dict):
                continue
            normalized = _normalize_usage(usage)
            if not normalized:
                continue
            seen = True
            stage_usage.append({"slide_no": page.get("slide_no"), **normalized})
            total_input += int(normalized.get("input_tokens") or 0)
            total_output += int(normalized.get("output_tokens") or 0)
            total += int(normalized.get("total_tokens") or 0)
        stages[stage_name] = stage_usage
    if not seen:
        return None
    return {
        "input_tokens": total_input or None,
        "output_tokens": total_output or None,
        "total_tokens": total or None,
        "by_stage": stages,
    }


def _normalize_usage(usage: Dict[str, Any]) -> Dict[str, int | None] | None:
    input_tokens = _first_int(usage, "input_tokens", "prompt_tokens", "promptTokenCount")
    output_tokens = _first_int(usage, "output_tokens", "completion_tokens", "completionTokenCount")
    total_tokens = _first_int(usage, "total_tokens", "totalTokenCount")
    if total_tokens is None and (input_tokens is not None or output_tokens is not None):
        total_tokens = int(input_tokens or 0) + int(output_tokens or 0)
    if input_tokens is None and output_tokens is None and total_tokens is None:
        return None
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }


def _first_int(source: Dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = source.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _formula_block_warnings(block: Dict[str, Any]) -> list[Dict[str, Any]]:
    quality = block.get("formula_quality")
    if isinstance(quality, dict):
        warnings = quality.get("warnings") or []
        return [
            {
                "code": warning.get("code"),
                "message": warning.get("message"),
                "latex": quality.get("latex"),
            }
            for warning in warnings
            if isinstance(warning, dict)
        ]
    warning = _legacy_formula_block_warning(block.get("text") or "")
    return [warning] if warning else []


def _legacy_formula_block_warning(text: str) -> Dict[str, Any] | None:
    lower = (text or "").lower()
    if (
        "[?]" in text
        or "？" in text
        or "无法确定" in text
        or "看不清" in text
        or "不确定" in text
        or "uncertain" in lower
        or "illegible" in lower
    ):
        return {"code": "formula_uncertain_marker", "message": "公式 block 包含不确定识别标记。"}
    return None
