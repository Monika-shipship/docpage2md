import json
import re
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Callable, Dict, Iterable

from .artifacts import sha256_text
from .config import AppConfig
from .env import get_env_value
from .detect import build_initial_findings_pool
from .figures import analyze_figure_description
from .formula_quality import assess_formula_text, looks_like_latex_display, looks_like_standalone_formula, normalize_inline_math_text
from .models import (
    _run_dashscope_brain,
    _run_deepseek_brain,
    _run_openai_compatible_brain,
    call_aliyun_openai_vision,
)
from .refiner import BLOCK_KNOWN_OPS, BLOCK_REFINER_VERSION, apply_block_op_checked, refine_page_ir
from .run_logger import ProgressCallback, safe_progress
from .table_quality import assess_table
from .validators import first_api_error_prefix, is_api_error_text
from .vision_crop import cleanup_vision_crop_cache, resolve_original_block_image_path, resolve_vision_crop


HYBRID_ENRICHMENT_VERSION = "hybrid-enrichment-2026-06-23-v1"

VisionBackend = Callable[[dict[str, Any], dict[str, Any], Path | None, AppConfig], dict[str, Any]]
BrainBackend = Callable[[dict[str, Any], list[dict[str, Any]], AppConfig], dict[str, Any]]

VISION_ENRICH_BLOCK_TYPES = {"figure_note", "image_ref", "table", "formula_block"}


def enrich_mineru_document_ir(
    document_ir: dict[str, Any],
    config: AppConfig,
    *,
    output_root: str | Path,
    vision_backend: VisionBackend | None = None,
    brain_backend: BrainBackend | None = None,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    """Enrich MinerU IR with crop vision, structured Brain ops, and checked refiner ops.

    The function is deliberately offline-testable: tests can inject mock backends.
    In production, missing API keys cause fail-open reports and keep the MinerU IR.
    """
    enriched = deepcopy(document_ir)
    output_root = Path(output_root)
    vision_backend = vision_backend or default_crop_vision_backend
    brain_backend = brain_backend or default_brain_backend

    pages = enriched.get("pages") or []
    source_pdf = _document_source_pdf(enriched)
    safe_progress(
        progress,
        (
            f"Hybrid enrichment workers: pages={len(pages)}, "
            f"vision={config.vision_batch_workers}, brain={config.brain_batch_workers}"
        ),
    )
    vision_reports = _run_document_crop_vision_enrichment(
        pages,
        config,
        output_root,
        vision_backend,
        source_pdf=source_pdf,
        progress=progress,
    )
    context_pages = deepcopy(pages)
    brain_reports = _run_document_brain_refinement(
        pages,
        context_pages,
        config,
        brain_backend,
        progress=progress,
    )

    page_results: dict[int, dict[str, Any]] = {}
    for page_index, page_ir in enumerate(pages):
        slide_no = int(page_ir.get("source_page") or page_index + 1)
        page_brain = brain_reports[slide_no]
        op_audit = list((page_brain["brain"] or {}).get("op_audit") or []) + list(
            (page_brain["block_refiner"] or {}).get("op_audit") or []
        )
        page_results[slide_no] = {
            "version": HYBRID_ENRICHMENT_VERSION,
            "vision": vision_reports[slide_no],
            "brain": page_brain["brain"],
            "block_refiner": page_brain["block_refiner"],
            "op_audit": op_audit,
        }

    metadata = enriched.setdefault("metadata", {})
    metadata["hybrid_enrichment"] = {
        "version": HYBRID_ENRICHMENT_VERSION,
        "brain_op_review_mode": _brain_op_review_mode(config),
        "pages": _enrichment_summary(page_results.values()),
    }
    return {"document_ir": enriched, "pages": page_results, "summary": metadata["hybrid_enrichment"]}


def _run_document_crop_vision_enrichment(
    pages: list[dict[str, Any]],
    config: AppConfig,
    output_root: Path,
    vision_backend: VisionBackend,
    *,
    source_pdf: str | Path | None = None,
    progress: ProgressCallback | None = None,
) -> dict[int, dict[str, Any]]:
    reports_by_slide: dict[int, dict[str, Any]] = {}
    jobs: list[tuple[int, dict[str, Any], dict[str, Any], Path, dict[str, Any]]] = []
    for page_index, page_ir in enumerate(pages):
        slide_no = int(page_ir.get("source_page") or page_index + 1)
        safe_progress(
            progress,
            f"Hybrid page {page_index + 1}/{len(pages)} start: slide={slide_no}, blocks={len(page_ir.get('blocks') or [])}",
        )
        reports_by_slide[slide_no] = _empty_vision_report()
        for block in page_ir.get("blocks") or []:
            if block.get("type") not in VISION_ENRICH_BLOCK_TYPES:
                continue
            resolved_crop = resolve_vision_crop(page_ir, block, output_root, config, source_pdf=source_pdf)
            if resolved_crop.path is None:
                continue
            jobs.append((slide_no, page_ir, block, resolved_crop.path, resolved_crop.audit))

    if not jobs:
        cleanup_vision_crop_cache(output_root, config)
        return reports_by_slide

    workers = _worker_count(config.vision_batch_workers, len(jobs))
    safe_progress(progress, f"Hybrid crop vision batch start: blocks={len(jobs)}, workers={workers}")
    started = time.monotonic()
    results_by_slide: dict[int, list[dict[str, Any]]] = {slide_no: [] for slide_no in reports_by_slide}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_single_crop_vision_job,
                slide_no,
                page_ir,
                block,
                image_path,
                crop_audit,
                config,
                vision_backend,
                progress,
                output_root=output_root,
                source_pdf=source_pdf,
            ): slide_no
            for slide_no, page_ir, block, image_path, crop_audit in jobs
        }
        for future in as_completed(futures):
            slide_no = futures[future]
            try:
                results_by_slide.setdefault(slide_no, []).append(future.result())
            except Exception as exc:
                safe_progress(progress, f"Crop vision failed: slide={slide_no}, block=<thread>, code=vision_thread_exception")
                results_by_slide.setdefault(slide_no, []).append(
                    {
                        "block_id": None,
                        "type": None,
                        "status": "failed",
                        "error_code": "vision_thread_exception",
                        "error_message": _safe_model_error(str(exc)),
                    }
                )

    for slide_no, block_results in results_by_slide.items():
        reports_by_slide[slide_no] = _vision_report_from_results(block_results)
        report = reports_by_slide[slide_no]
        safe_progress(
            progress,
            (
                f"Hybrid page {slide_no} crop vision: status={report.get('status')}, "
                f"attempted={report.get('attempted_blocks')}, "
                f"succeeded={report.get('succeeded_blocks')}, failed={report.get('failed_blocks')}"
            ),
        )
    elapsed = time.monotonic() - started
    attempted = sum(report.get("attempted_blocks") or 0 for report in reports_by_slide.values())
    succeeded = sum(report.get("succeeded_blocks") or 0 for report in reports_by_slide.values())
    failed = sum(report.get("failed_blocks") or 0 for report in reports_by_slide.values())
    safe_progress(
        progress,
        f"Hybrid crop vision batch done: blocks={attempted}, succeeded={succeeded}, failed={failed}, elapsed={elapsed:.1f}s",
    )
    cleanup_vision_crop_cache(output_root, config)
    return reports_by_slide


def _run_single_crop_vision_job(
    slide_no: int,
    page_ir: dict[str, Any],
    block: dict[str, Any],
    image_path: Path,
    crop_audit: dict[str, Any],
    config: AppConfig,
    vision_backend: VisionBackend,
    progress: ProgressCallback | None,
    *,
    output_root: Path | None = None,
    source_pdf: str | Path | None = None,
) -> dict[str, Any]:
    safe_progress(
        progress,
        (
            f"Crop vision start: slide={slide_no}, block={block.get('id')}, type={block.get('type')}, "
            f"crop={crop_audit.get('crop_strategy')}"
        ),
    )
    attempts: list[dict[str, Any]] = [dict(crop_audit)]
    response = vision_backend(page_ir, block, image_path, config)
    normalized = _normalize_backend_response(response)
    retry_reason = _vision_retry_reason(block, normalized)
    if (
        retry_reason
        and bool(getattr(config, "vision_crop_retry", True))
        and str(getattr(config, "vision_crop_mode", "auto") or "auto") != "original"
        and output_root is not None
    ):
        retry_crop = resolve_vision_crop(
            page_ir,
            block,
            output_root,
            config,
            source_pdf=source_pdf,
            retry=True,
            override_dpi=400,
            override_padding_profile="aggressive",
        )
        retry_audit = dict(retry_crop.audit)
        retry_audit["retry_reason"] = retry_reason
        attempts.append(retry_audit)
        if retry_crop.path is not None:
            safe_progress(
                progress,
                f"Crop vision retry: slide={slide_no}, block={block.get('id')}, reason={retry_reason}, crop={retry_audit.get('crop_strategy')}",
            )
            retry_response = vision_backend(page_ir, block, retry_crop.path, config)
            retry_normalized = _normalize_backend_response(retry_response)
            if _prefer_retry_vision_result(block, normalized, retry_normalized):
                normalized = retry_normalized
                crop_audit = retry_audit
                image_path = retry_crop.path
    if normalized.get("success"):
        normalized["crop_audit"] = crop_audit
        normalized["crop_attempts"] = attempts
        changed_fields = _apply_vision_result(block, normalized)
        safe_progress(
            progress,
            f"Crop vision ok: slide={slide_no}, block={block.get('id')}, changed={','.join(changed_fields) or 'none'}",
        )
        return {
            "block_id": block.get("id"),
            "type": block.get("type"),
            "status": "ok",
            "changed_fields": changed_fields,
            "content_sha256": _response_content_sha256(normalized),
            "crop": crop_audit,
            "crop_attempts": attempts,
            "retry_count": max(0, len(attempts) - 1),
            **_provider_fields(normalized),
        }

    safe_progress(progress, f"Crop vision failed: slide={slide_no}, block={block.get('id')}, code={normalized.get('error_code')}")
    return {
        "block_id": block.get("id"),
        "type": block.get("type"),
        "status": "failed",
        "error_code": normalized.get("error_code"),
        "error_message": _safe_model_error(normalized.get("error_message") or "Vision enrichment failed."),
        "crop": crop_audit,
        "crop_attempts": attempts,
        "retry_count": max(0, len(attempts) - 1),
        **_provider_fields(normalized),
    }


def _run_document_brain_refinement(
    pages: list[dict[str, Any]],
    context_pages: list[dict[str, Any]],
    config: AppConfig,
    brain_backend: BrainBackend,
    *,
    progress: ProgressCallback | None = None,
) -> dict[int, dict[str, Any]]:
    if not pages:
        return {}
    requested_workers = max(1, int(config.brain_batch_workers or 1))
    context_radius = max(0, int(config.brain_context_radius or 0))
    page_jobs = []
    reports_by_slide: dict[int, dict[str, Any]] = {}
    skipped = 0
    for page_index, page_ir in enumerate(pages):
        slide_no = int(page_ir.get("source_page") or page_index + 1)
        skip_reason = _brain_skip_reason(page_ir)
        if skip_reason:
            skipped += 1
            refined_page, report = _skip_brain_and_run_refiner(page_ir, slide_no, skip_reason)
            pages[page_index] = refined_page
            reports_by_slide[slide_no] = report
            continue
        page_jobs.append((page_index, slide_no, page_ir))

    workers = _worker_count(requested_workers, len(page_jobs)) if page_jobs else 0
    safe_progress(
        progress,
        (
            f"Hybrid Brain batch start: pages={len(pages)}, workers={workers}, "
            f"requested_workers={requested_workers}, tasks={len(page_jobs)}, skipped={skipped}, "
            f"thinking={config.brain_thinking}, context_radius={context_radius}"
        ),
    )
    safe_progress(
        progress,
        (
            f"Brain 并发说明：配置并发={requested_workers}，可运行页任务={len(page_jobs)}，"
            f"实际worker={workers}，跳过低价值页={skipped}，Brain上下文=前后{context_radius}页"
        ),
    )
    started = time.monotonic()
    if not page_jobs:
        safe_progress(progress, f"Hybrid Brain batch done: pages={len(pages)}, statuses=skipped:{skipped}, elapsed=0.0s")
        return reports_by_slide

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(
                _run_single_brain_refinement_job,
                page_index,
                slide_no,
                deepcopy(page_ir),
                context_pages,
                context_radius,
                config,
                brain_backend,
                progress,
            ): (page_index, slide_no)
            for page_index, slide_no, page_ir in page_jobs
        }
        for future in as_completed(futures):
            page_index, slide_no = futures[future]
            try:
                refined_page, report = future.result()
            except Exception as exc:
                safe_progress(progress, f"Hybrid page {slide_no} Brain failed: code=brain_thread_exception, error={_safe_model_error(str(exc))}")
                refined_page = pages[page_index]
                brain_report = {
                    "version": HYBRID_ENRICHMENT_VERSION,
                    "status": "failed",
                    "ops_requested": 0,
                    "ops_applied": 0,
                    "ops_rejected": 0,
                    "warnings": [],
                    "op_audit": [],
                    "error_code": "brain_thread_exception",
                    "error_message": _safe_model_error(str(exc)),
                }
                block_refiner = {
                    "changed": False,
                    "applied_ops": [],
                    "dismissed": [],
                    "validation": {},
                    "op_audit": [],
                }
                report = {"brain": brain_report, "block_refiner": block_refiner}
            pages[page_index] = refined_page
            reports_by_slide[slide_no] = report
    elapsed = time.monotonic() - started
    statuses = {}
    for report in reports_by_slide.values():
        status = ((report.get("brain") or {}).get("status") or "unknown")
        statuses[status] = statuses.get(status, 0) + 1
    status_text = ";".join(f"{key}:{value}" for key, value in sorted(statuses.items())) or "none"
    safe_progress(progress, f"Hybrid Brain batch done: pages={len(pages)}, statuses={status_text}, elapsed={elapsed:.1f}s")
    _log_brain_latency_summary(reports_by_slide, progress=progress)
    return reports_by_slide


def _run_single_brain_refinement_job(
    page_index: int,
    slide_no: int,
    page_ir: dict[str, Any],
    pages: list[dict[str, Any]],
    context_radius: int,
    config: AppConfig,
    brain_backend: BrainBackend,
    progress: ProgressCallback | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    context_window = _context_window(pages, page_index, radius=context_radius)
    review_profile = _brain_review_profile(page_ir)
    safe_progress(
        progress,
        (
            f"Hybrid page {slide_no} Brain start: context_pages={len(context_window)}, "
            f"context_radius={context_radius}, findings={review_profile.get('finding_count')}, "
            f"priority_blocks={review_profile.get('priority_block_count')}"
        ),
    )
    brain_started = time.monotonic()
    page_after_brain, brain_report = _run_brain_ops(page_ir, context_window, config, brain_backend)
    brain_elapsed = time.monotonic() - brain_started
    brain_report["elapsed_seconds"] = round(brain_elapsed, 3)
    brain_report["context_window"] = {
        "configured_radius": context_radius,
        "actual_pages": len(context_window),
        "page_numbers": [page.get("source_page") for page in context_window],
        "truncated": True,
        "truncation_note": "上下文字段按固定长度压缩，避免 prompt 过长。",
    }
    safe_progress(
        progress,
        (
            f"Hybrid page {slide_no} Brain done: status={brain_report.get('status')}, "
            f"ops_requested={brain_report.get('ops_requested')}, "
            f"applied={brain_report.get('ops_applied')}, rejected={brain_report.get('ops_rejected')}, "
            f"elapsed={brain_elapsed:.1f}s"
        ),
    )
    rejection_summary = _format_reason_counts_zh(brain_report.get("op_rejection_reasons") or {})
    if rejection_summary:
        safe_progress(progress, f"Brain 第 {slide_no} 页拒绝原因：{rejection_summary}")

    block_refine_result = refine_page_ir(
        page_after_brain,
        slide_no=slide_no,
        target_raw=page_after_brain.get("raw_text"),
    )
    safe_progress(
        progress,
        (
            f"Hybrid page {slide_no} refiner done: changed={block_refine_result.changed}, "
            f"applied={len(block_refine_result.applied_ops)}, dismissed={len(block_refine_result.dismissed)}"
        ),
    )
    return block_refine_result.page_ir, {
        "brain": brain_report,
        "block_refiner": block_refine_result.to_dict(),
    }


def _brain_skip_reason(page_ir: dict[str, Any]) -> str | None:
    blocks = [block for block in page_ir.get("blocks") or [] if isinstance(block, dict)]
    if not blocks:
        return "empty_page"
    profile = _brain_review_profile(page_ir)
    if profile["finding_count"]:
        return None
    if profile["has_dual_evidence"]:
        return None
    if profile["has_visual_or_formula"]:
        return None
    if profile["low_confidence_block_count"]:
        return None
    return "low_value_clean_page"


def _skip_brain_and_run_refiner(page_ir: dict[str, Any], slide_no: int, reason: str) -> tuple[dict[str, Any], dict[str, Any]]:
    block_refine_result = refine_page_ir(page_ir, slide_no=slide_no, target_raw=page_ir.get("raw_text"))
    brain_report = {
        "version": HYBRID_ENRICHMENT_VERSION,
        "status": "skipped",
        "skip_reason": reason,
        "ops_requested": 0,
        "ops_applied": 0,
        "ops_rejected": 0,
        "brain_discovered_count": 0,
        "warnings": [],
        "op_audit": [],
        "usage": None,
        "request_id": None,
        "provider_latency": None,
    }
    return block_refine_result.page_ir, {
        "brain": brain_report,
        "block_refiner": block_refine_result.to_dict(),
    }


def _log_brain_latency_summary(reports_by_slide: dict[int, dict[str, Any]], *, progress: ProgressCallback | None = None) -> None:
    samples: list[tuple[int, float]] = []
    for slide_no, report in sorted(reports_by_slide.items()):
        elapsed = (report.get("brain") or {}).get("elapsed_seconds")
        if isinstance(elapsed, (int, float)) and elapsed >= 0:
            samples.append((slide_no, float(elapsed)))
    if not samples:
        return
    values = sorted(value for _slide_no, value in samples)
    p50 = _percentile_nearest(values, 0.50)
    p90 = _percentile_nearest(values, 0.90)
    max_elapsed = values[-1]
    slowest = sorted(samples, key=lambda item: item[1], reverse=True)[:3]
    slowest_text = ";".join(f"{slide}:{elapsed:.1f}s" for slide, elapsed in slowest)
    tail_ratio = max_elapsed / max(0.1, p50)
    safe_progress(
        progress,
        (
            f"Hybrid Brain latency summary: pages={len(samples)}, p50={p50:.1f}s, "
            f"p90={p90:.1f}s, max={max_elapsed:.1f}s, slowest={slowest_text}, "
            f"tail_ratio={tail_ratio:.2f}"
        ),
    )
    if len(samples) >= 4 and tail_ratio >= 1.7:
        safe_progress(
            progress,
            (
                f"Hybrid Brain latency warning: tail_ratio={tail_ratio:.2f}, "
                "advice=try_brain_workers_3_6_12"
            ),
        )


def _percentile_nearest(sorted_values: list[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0
    index = round((len(sorted_values) - 1) * percentile)
    return sorted_values[max(0, min(len(sorted_values) - 1, index))]


def _empty_vision_report() -> dict[str, Any]:
    return {
        "version": HYBRID_ENRICHMENT_VERSION,
        "status": "skipped",
        "attempted_blocks": 0,
        "succeeded_blocks": 0,
        "failed_blocks": 0,
        "blocks": [],
        "usage": None,
        "request_id": None,
        "provider_latency": None,
    }


def _vision_report_from_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    attempted = len(results)
    succeeded = sum(1 for item in results if item.get("status") == "ok")
    failed = attempted - succeeded
    return {
        "version": HYBRID_ENRICHMENT_VERSION,
        "status": _stage_status(attempted, succeeded, failed),
        "attempted_blocks": attempted,
        "succeeded_blocks": succeeded,
        "failed_blocks": failed,
        "blocks": results,
        "usage": _aggregate_usage(results),
        "request_id": _first_value(results, "request_id"),
        "provider_latency": _sum_provider_latency(results),
    }


def _worker_count(configured: int, jobs: int) -> int:
    try:
        workers = int(configured)
    except (TypeError, ValueError):
        workers = 1
    return max(1, min(max(1, jobs), workers if workers > 0 else 1))


def default_crop_vision_backend(
    page_ir: dict[str, Any],
    block: dict[str, Any],
    image_path: Path | None,
    config: AppConfig,
) -> dict[str, Any]:
    if image_path is None or not image_path.exists():
        return _backend_error("missing_crop_image", "Crop image is not available.")
    api_key = get_env_value(config.vision_api_key_env)
    if not api_key:
        return _backend_error("missing_api_key", f"Missing API key env: {config.vision_api_key_env}.")
    if config.vision_provider not in {"dashscope", "dashscope_openai", "openai_compatible"}:
        return _backend_error("unsupported_vision_provider", f"Unsupported vision provider: {config.vision_provider}.")

    payload = _model_payload(
        call_aliyun_openai_vision(
            model_id=config.model_vision,
            image_path=str(image_path),
            prompt_text=_crop_vision_prompt(page_ir, block),
            api_key=api_key,
            base_url=config.vision_base_url,
            stream=True,
        )
    )
    content = payload["content"].strip()
    if is_api_error_text(content) or content.startswith("OpenAI"):
        return _backend_error(first_api_error_prefix(content) or "vision_api_error", _safe_model_error(content), payload)
    if not content:
        return _backend_error("empty_vision_output", "Vision model returned no content.", payload)

    parsed = _parse_json_object(content) or {"content": content}
    return {"success": True, **parsed, **_provider_fields(payload)}


def default_brain_backend(
    page_ir: dict[str, Any],
    context_pages: list[dict[str, Any]],
    config: AppConfig,
) -> dict[str, Any]:
    if not get_env_value(config.brain_api_key_env):
        return _backend_error("missing_api_key", f"Missing API key env: {config.brain_api_key_env}.")

    prompt = _brain_ops_prompt(page_ir, context_pages)
    last_error = None
    for attempt in range(2):
        raw = _call_brain_model(prompt, config)
        payload = _model_payload(raw)
        content = payload["content"].strip()
        if is_api_error_text(content):
            return _backend_error(first_api_error_prefix(content) or "brain_api_error", _safe_model_error(content), payload)
        if not content:
            last_error = _backend_error("empty_brain_output", "Brain model returned no JSON content.", payload)
            continue

        parsed = _parse_json_object(content)
        if not isinstance(parsed, dict):
            last_error = _backend_error("invalid_brain_json", "Brain output was not valid JSON.", payload)
            continue
        review_payload = _normalize_brain_review_payload(parsed)
        if review_payload.get("error"):
            return _backend_error(str(review_payload["error"]), str(review_payload["message"]), payload)
        return {
            "success": True,
            **review_payload,
            "warnings": review_payload.get("warnings") if isinstance(review_payload.get("warnings"), list) else [],
            "retry_count": attempt,
            **_provider_fields(payload),
        }
    if last_error is not None:
        last_error["retry_count"] = 1
        return last_error
    return _backend_error("empty_brain_output", "Brain model returned no JSON content.")


def _call_brain_model(prompt: str, config: AppConfig):
    if config.brain_provider == "deepseek":
        return _run_deepseek_brain(prompt, config)
    if config.brain_provider in {"dashscope_openai", "openai_compatible"}:
        return _run_openai_compatible_brain(prompt, config)
    return _run_dashscope_brain(prompt, config)


def _run_crop_vision_enrichment(
    page_ir: dict[str, Any],
    config: AppConfig,
    output_root: Path,
    vision_backend: VisionBackend,
    *,
    progress: ProgressCallback | None = None,
    slide_no: int | None = None,
) -> dict[str, Any]:
    blocks = page_ir.get("blocks") or []
    results = []
    attempted = 0
    succeeded = 0
    failed = 0
    for block in blocks:
        if block.get("type") not in VISION_ENRICH_BLOCK_TYPES:
            continue
        resolved_crop = resolve_vision_crop(page_ir, block, output_root, config)
        if resolved_crop.path is None:
            continue
        image_path = resolved_crop.path
        attempted += 1
        safe_progress(
            progress,
            f"Crop vision start: slide={slide_no or page_ir.get('source_page')}, block={block.get('id')}, type={block.get('type')}",
        )
        response = vision_backend(page_ir, block, image_path, config)
        normalized = _normalize_backend_response(response)
        if normalized.get("success"):
            changed_fields = _apply_vision_result(block, normalized)
            succeeded += 1
            safe_progress(
                progress,
                (
                    f"Crop vision ok: slide={slide_no or page_ir.get('source_page')}, "
                    f"block={block.get('id')}, changed={','.join(changed_fields) or 'none'}"
                ),
            )
            results.append(
                {
                    "block_id": block.get("id"),
                    "type": block.get("type"),
                    "status": "ok",
                    "changed_fields": changed_fields,
                    "content_sha256": _response_content_sha256(normalized),
                    "crop": resolved_crop.audit,
                    **_provider_fields(normalized),
                }
            )
        else:
            failed += 1
            safe_progress(
                progress,
                (
                    f"Crop vision failed: slide={slide_no or page_ir.get('source_page')}, "
                    f"block={block.get('id')}, code={normalized.get('error_code')}"
                ),
            )
            results.append(
                {
                    "block_id": block.get("id"),
                    "type": block.get("type"),
                    "status": "failed",
                    "error_code": normalized.get("error_code"),
                    "error_message": _safe_model_error(normalized.get("error_message") or "Vision enrichment failed."),
                    "crop": resolved_crop.audit,
                    **_provider_fields(normalized),
                }
            )
    return {
        "version": HYBRID_ENRICHMENT_VERSION,
        "status": _stage_status(attempted, succeeded, failed),
        "attempted_blocks": attempted,
        "succeeded_blocks": succeeded,
        "failed_blocks": failed,
        "blocks": results,
        "usage": _aggregate_usage(results),
        "request_id": _first_value(results, "request_id"),
        "provider_latency": _sum_provider_latency(results),
    }


def _run_brain_ops(
    page_ir: dict[str, Any],
    context_pages: list[dict[str, Any]],
    config: AppConfig,
    brain_backend: BrainBackend,
) -> tuple[dict[str, Any], dict[str, Any]]:
    response = _normalize_backend_response(brain_backend(page_ir, context_pages, config))
    if not response.get("success"):
        return page_ir, {
            "version": HYBRID_ENRICHMENT_VERSION,
            "status": "failed",
            "ops_requested": 0,
            "ops_applied": 0,
            "ops_rejected": 0,
            "warnings": [],
            "op_audit": [],
            "error_code": response.get("error_code"),
            "error_message": _safe_model_error(response.get("error_message") or "Brain enrichment failed."),
            **_provider_fields(response),
        }

    current = page_ir
    audits = []
    decisions = _normalize_brain_decisions(response.get("decisions") or [])
    new_findings = _normalize_brain_new_findings(response.get("new_findings") or [], int(page_ir.get("source_page") or 0))
    initial_finding_aliases = _brain_initial_finding_alias_map(_brain_initial_findings(page_ir))
    new_finding_aliases = _brain_new_finding_alias_map(new_findings)
    review_mode = _brain_op_review_mode(config)
    ops = _ordered_brain_ops(_normalize_brain_ops(response.get("op_candidates") or response.get("ops") or []))
    applied = 0
    rejected = 0
    repaired_applied = 0
    noop_or_superseded = 0
    resolved_block_ids: set[str] = set()
    slide_no = int(page_ir.get("source_page") or 0)
    for raw_op in ops:
        op = _normalize_brain_op_reference(raw_op)
        if _brain_op_decision(op) == "brain_discovered":
            op.setdefault("new_finding_id", op.get("finding_id"))
        if op.get("op") not in BLOCK_KNOWN_OPS:
            rejected += 1
            audits.append(
                _brain_op_audit(
                    op,
                    "hard_rejected",
                    {"reason": "unknown_or_unsafe_op", **_brain_op_current_preview(current, op)},
                )
            )
            continue
        _resolve_brain_finding_reference(op, initial_finding_aliases, new_finding_aliases)
        op, repair_detail = _repair_brain_op(
            op,
            current,
            initial_finding_aliases,
            new_finding_aliases,
            review_mode=review_mode,
        )
        policy_error = _brain_op_policy_error(op, new_finding_aliases=new_finding_aliases, review_mode=review_mode)
        if policy_error:
            rejected += 1
            policy_error.update(_brain_op_current_preview(current, op))
            policy_error.update(repair_detail)
            audits.append(_brain_op_audit(op, _rejection_status(policy_error.get("reason")), policy_error))
            continue
        target_ids = set(_op_target_block_ids(op))
        if str(op.get("op") or "") == "mark_uncertain" and target_ids & resolved_block_ids:
            noop_or_superseded += 1
            detail = {
                "reason": "mark_uncertain_superseded_by_fix",
                **_brain_op_current_preview(current, op),
                **repair_detail,
            }
            audits.append(_brain_op_audit(op, "superseded_noop", detail))
            continue
        current, ok, detail = apply_block_op_checked(
            current,
            op,
            slide_no=slide_no,
            target_raw=page_ir.get("raw_text"),
        )
        detail.update({key: value for key, value in repair_detail.items() if value not in (None, "", [], {})})
        if ok:
            applied += 1
            if str(op.get("op") or "") in {"replace_text_span_checked", "normalize_formula"}:
                resolved_block_ids.update(_op_target_block_ids(op))
            if repair_detail.get("repair_actions"):
                repaired_applied += 1
                audits.append(_brain_op_audit(op, "repaired_applied", detail))
            else:
                audits.append(_brain_op_audit(op, "applied", detail))
        else:
            status = _detail_status(detail)
            if status == "superseded_noop":
                noop_or_superseded += 1
                if str(detail.get("reason") or "") in {"replacement_same_as_current", "normalized_formula_unchanged"}:
                    resolved_block_ids.update(_op_target_block_ids(op))
            else:
                rejected += 1
            audits.append(_brain_op_audit(op, status, detail))

    rejection_reasons = _count_audit_reasons(audits)
    contract_error_codes = _count_contract_errors(audits)
    return current, {
        "version": HYBRID_ENRICHMENT_VERSION,
        "status": "ok" if rejected == 0 else "partial",
        "brain_op_review_mode": review_mode,
        "ops_requested": len(ops),
        "decisions": decisions,
        "new_findings": new_findings,
        "op_candidates_count": len(ops),
        "ops_applied": applied,
        "ops_rejected": rejected,
        "repair_successes": repaired_applied,
        "noop_or_superseded": noop_or_superseded,
        "brain_discovered_count": len(new_findings),
        "findings": {
            "brain_decisions": decisions,
            "brain_discovered": new_findings,
        },
        "op_rejection_reasons": rejection_reasons,
        "contract_error_codes": contract_error_codes,
        "warnings": response.get("warnings") if isinstance(response.get("warnings"), list) else [],
        "op_audit": audits,
        **_provider_fields(response),
    }


def _brain_op_review_mode(config: AppConfig) -> str:
    mode = str(getattr(config, "brain_op_review_mode", "aggressive") or "aggressive").strip().lower()
    return mode if mode in {"conservative", "standard", "aggressive"} else "aggressive"


def _ordered_brain_ops(ops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority = {
        "replace_text_span_checked": 0,
        "normalize_formula": 1,
        "merge_block": 1,
        "promote_heading": 2,
        "demote_heading": 2,
        "mark_uncertain": 9,
    }
    return [op for _index, op in sorted(enumerate(ops), key=lambda item: (priority.get(str(item[1].get("op") or ""), 5), item[0]))]


def _repair_brain_op(
    op: dict[str, Any],
    page_ir: dict[str, Any],
    initial_aliases: dict[str, dict[str, Any]],
    new_aliases: dict[str, dict[str, Any]],
    *,
    review_mode: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repaired = dict(op)
    detail: dict[str, Any] = {"brain_op_review_mode": review_mode}
    actions: list[str] = []
    if review_mode == "conservative":
        return repaired, detail

    resolved = _resolved_finding_for_op(repaired, initial_aliases, new_aliases)
    finding = resolved.get("finding") if isinstance(resolved, dict) else None
    if isinstance(finding, dict):
        _inherit_missing_op_metadata_from_finding(repaired, finding, actions)

    if _brain_op_decision(repaired) == "brain_discovered":
        if not str(repaired.get("new_finding_id") or repaired.get("finding_id") or "").strip():
            candidate = _unique_finding_for_op(repaired, new_aliases)
            if candidate:
                repaired["new_finding_id"] = candidate.get("new_finding_id") or candidate.get("finding_id")
                repaired["_resolved_finding_id"] = candidate.get("finding_id")
                repaired["_resolved_new_finding_id"] = candidate.get("new_finding_id") or candidate.get("finding_id")
                _attach_resolved_finding_preview(repaired, candidate)
                candidate_finding = candidate.get("finding") if isinstance(candidate, dict) else None
                if isinstance(candidate_finding, dict):
                    _inherit_missing_op_metadata_from_finding(repaired, candidate_finding, actions)
                actions.append("resolve_missing_new_finding_id")
        elif repaired.get("new_finding_id") not in new_aliases:
            candidate = _known_new_finding_alias_from_op(repaired, new_aliases)
            if candidate is None:
                candidate = _unique_finding_for_op(repaired, new_aliases, require_text_evidence=True)
            if candidate:
                repaired["new_finding_id"] = candidate.get("new_finding_id") or candidate.get("finding_id")
                repaired["_resolved_finding_id"] = candidate.get("finding_id")
                repaired["_resolved_new_finding_id"] = candidate.get("new_finding_id") or candidate.get("finding_id")
                _attach_resolved_finding_preview(repaired, candidate)
                candidate_finding = candidate.get("finding") if isinstance(candidate, dict) else None
                if isinstance(candidate_finding, dict):
                    _inherit_missing_op_metadata_from_finding(repaired, candidate_finding, actions)
                actions.append("repair_unknown_new_finding_id")

    if not str(repaired.get("id") or "").strip():
        block_id = _unique_block_id_for_op(page_ir, repaired)
        if block_id:
            repaired["id"] = block_id
            actions.append("resolve_target_block_by_text")
    elif _find_block_by_id(page_ir, repaired.get("id")) is None:
        block_id = _unique_block_id_for_op(page_ir, repaired)
        if block_id:
            repaired["id"] = block_id
            actions.append("repair_missing_target_block")

    if str(repaired.get("op") or "") == "replace_text_span_checked":
        span = _resolve_replace_span(page_ir, repaired, review_mode=review_mode)
        if span:
            actual_old = span.get("actual_old_text")
            if actual_old and actual_old != repaired.get("old_text"):
                repaired["old_text"] = actual_old
                actions.append("repair_old_text_span")
            if span.get("field") and not repaired.get("field"):
                repaired["field"] = span.get("field")
                actions.append("resolve_field")
            repaired["_match_strategy"] = span.get("strategy")
            repaired["_resolved_field"] = span.get("field")
            detail.update(
                {
                    "match_strategy": span.get("strategy"),
                    "resolved_field": span.get("field"),
                    "resolved_span": span.get("span"),
                    "resolved_block_id": repaired.get("id"),
                    "repair_confidence": span.get("confidence"),
                }
            )

    if actions:
        detail["repair_actions"] = actions
    return repaired, detail


def _resolved_finding_for_op(
    op: dict[str, Any],
    initial_aliases: dict[str, dict[str, Any]],
    new_aliases: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if _brain_op_decision(op) == "brain_discovered":
        key = str(op.get("new_finding_id") or op.get("finding_id") or "").strip()
        return new_aliases.get(key) or {}
    key = str(op.get("finding_id") or "").strip()
    return initial_aliases.get(key) or {}


def _inherit_missing_op_metadata_from_finding(op: dict[str, Any], finding: dict[str, Any], actions: list[str]) -> None:
    if not str(op.get("id") or "").strip() and finding.get("block_id"):
        op["id"] = finding.get("block_id")
        actions.append("inherit_block_id_from_finding")
    if not str(op.get("evidence_type") or op.get("evidence") or "").strip():
        op["evidence_type"] = _evidence_type_from_finding(finding)
        actions.append("inherit_evidence_type_from_finding")
    if _safe_float(op.get("confidence"), -1.0) < 0.0:
        confidence = _safe_float(finding.get("confidence"), -1.0)
        op["confidence"] = confidence if 0.0 <= confidence <= 1.0 else 0.78
        actions.append("inherit_confidence_from_finding")


def _known_new_finding_alias_from_op(op: dict[str, Any], aliases: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    for key in ("finding_id", "id"):
        alias = str(op.get(key) or "").strip()
        if alias and alias in aliases:
            return aliases[alias]
    return None


def _attach_resolved_finding_preview(op: dict[str, Any], resolved: dict[str, Any]) -> None:
    finding = resolved.get("finding") if isinstance(resolved, dict) else None
    if isinstance(finding, dict):
        op["_finding_message_preview"] = _finding_message_preview(finding)
        op["_finding_evidence_preview"] = _finding_evidence_preview(finding)


def _unique_finding_for_op(
    op: dict[str, Any],
    aliases: dict[str, dict[str, Any]],
    *,
    require_text_evidence: bool = False,
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    seen = set()
    op_block = str(op.get("id") or op.get("block_id") or "").strip()
    op_old = _compact_for_match(str(op.get("old_text") or ""))
    for resolved in aliases.values():
        finding = resolved.get("finding") if isinstance(resolved, dict) else None
        if not isinstance(finding, dict):
            continue
        key = str(resolved.get("finding_id") or finding.get("finding_id") or id(finding))
        if key in seen:
            continue
        seen.add(key)
        block_ok = op_block and str(finding.get("block_id") or "") == op_block
        text_values = [
            finding.get("current_text"),
            finding.get("suggested_text"),
            finding.get("message"),
            json.dumps(finding.get("evidence"), ensure_ascii=False, default=str) if finding.get("evidence") is not None else "",
        ]
        text_ok = bool(op_old and any(op_old in _compact_for_match(str(value or "")) for value in text_values))
        if text_ok or (block_ok and not require_text_evidence):
            candidates.append(resolved)
    return candidates[0] if len(candidates) == 1 else None


def _evidence_type_from_finding(finding: dict[str, Any]) -> str:
    source = str(finding.get("source") or "")
    if source == "dual_engine_diff":
        return "dual_engine"
    if source == "vision_crop_evidence":
        return "vision_crop"
    if source == "validator_precheck":
        return "validator"
    if source == "brain_discovered":
        return "context"
    return "finding"


def _unique_block_id_for_op(page_ir: dict[str, Any], op: dict[str, Any]) -> str | None:
    old_text = str(op.get("old_text") or "")
    new_text = str(op.get("new_text") or "")
    candidates = []
    for block in page_ir.get("blocks") or []:
        if not isinstance(block, dict) or not block.get("id"):
            continue
        fields = _searchable_block_fields(block, op)
        if old_text and any(old_text in value for _field, value in fields):
            candidates.append(str(block.get("id")))
            continue
        if new_text and any(new_text in value for _field, value in fields):
            candidates.append(str(block.get("id")))
            continue
        if old_text and _resolve_span_in_fields(fields, old_text, review_mode="aggressive"):
            candidates.append(str(block.get("id")))
    unique = sorted(set(candidates))
    return unique[0] if len(unique) == 1 else None


def _resolve_replace_span(page_ir: dict[str, Any], op: dict[str, Any], *, review_mode: str) -> dict[str, Any] | None:
    block = _find_block_by_id(page_ir, op.get("id"))
    if not block:
        return None
    old_text = str(op.get("old_text") or "")
    fields = _searchable_block_fields(block, op)
    structured = _structured_formula_payload_span(fields, old_text, str(op.get("new_text") or ""), block)
    if structured:
        return structured
    return _resolve_span_in_fields(fields, old_text, review_mode=review_mode)


def _find_block_by_id(page_ir: dict[str, Any], block_id: Any) -> dict[str, Any] | None:
    wanted = str(block_id or "").strip()
    if not wanted:
        return None
    for block in page_ir.get("blocks") or []:
        if isinstance(block, dict) and str(block.get("id") or "") == wanted:
            return block
    return None


def _searchable_block_fields(block: dict[str, Any], op: dict[str, Any]) -> list[tuple[str, str]]:
    field = str(op.get("field") or "").strip()
    fields = [field] if field else ["text", "latex", "raw_text", "description"]
    result = []
    for name in fields:
        if name not in {"text", "latex", "raw_text", "description"}:
            continue
        value = block.get(name)
        if isinstance(value, str) and value:
            result.append((name, value))
    return result


def _resolve_span_in_fields(fields: list[tuple[str, str]], old_text: str, *, review_mode: str) -> dict[str, Any] | None:
    if not old_text:
        return None
    exact = []
    for field, value in fields:
        index = value.find(old_text)
        if index >= 0:
            exact.append({"field": field, "actual_old_text": old_text, "span": [index, index + len(old_text)], "strategy": "exact", "confidence": 1.0})
    if len(exact) == 1:
        return exact[0]
    if review_mode == "conservative":
        return None
    for strategy, normalizer, confidence in (
        ("compact_whitespace", _compact_for_match, 0.94),
        ("math_markup_normalized", _math_compact_for_match, 0.90),
    ):
        matches = []
        target = normalizer(old_text)
        if not target:
            continue
        for field, value in fields:
            span = _compact_span(value, target, normalizer)
            if span:
                matches.append({"field": field, "actual_old_text": value[span[0] : span[1]], "span": list(span), "strategy": strategy, "confidence": confidence})
        if len(matches) == 1:
            return matches[0]
    if review_mode != "aggressive":
        return None
    fuzzy = []
    for field, value in fields:
        ratio = SequenceMatcher(None, _math_compact_for_match(old_text), _math_compact_for_match(value), autojunk=False).ratio()
        if ratio >= 0.92 and len(old_text) >= max(12, int(len(value) * 0.35)):
            fuzzy.append({"field": field, "actual_old_text": value, "span": [0, len(value)], "strategy": "whole_field_fuzzy", "confidence": ratio})
    return fuzzy[0] if len(fuzzy) == 1 else None


def _structured_formula_payload_span(
    fields: list[tuple[str, str]],
    old_text: str,
    new_text: str,
    block: dict[str, Any],
) -> dict[str, Any] | None:
    if block.get("type") not in {"formula_block", "formula_inline"}:
        return None
    new_value = new_text.strip()
    if not (looks_like_latex_display(new_value) or looks_like_standalone_formula(new_value) or "\\begin{" in new_value):
        return None
    old_payload = _parse_json_payload(old_text)
    matches = []
    for field, value in fields:
        payload = _parse_json_payload(value)
        if not payload:
            continue
        if old_payload and payload.get("latex") and old_payload.get("latex"):
            if _math_compact_for_match(str(payload.get("latex"))) != _math_compact_for_match(str(old_payload.get("latex"))):
                continue
        matches.append({"field": field, "actual_old_text": value, "span": [0, len(value)], "strategy": "structured_formula_payload", "confidence": 0.96})
    return matches[0] if len(matches) == 1 else None


def _parse_json_payload(text: str) -> dict[str, Any] | None:
    value = str(text or "").strip()
    if not value:
        return None
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", value, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        value = fence.group(1).strip()
    start = value.find("{")
    end = value.rfind("}")
    if 0 <= start < end:
        value = value[start : end + 1]
    if not value.startswith("{"):
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _compact_span(value: str, normalized_target: str, normalizer: Callable[[str], str]) -> tuple[int, int] | None:
    chars: list[str] = []
    mapping: list[int] = []
    for index, char in enumerate(value):
        normalized = normalizer(char)
        if not normalized:
            continue
        for item in normalized:
            chars.append(item)
            mapping.append(index)
    haystack = "".join(chars)
    start = haystack.find(normalized_target)
    if start < 0:
        return None
    if haystack.find(normalized_target, start + 1) >= 0:
        return None
    end = start + len(normalized_target) - 1
    return mapping[start], mapping[end] + 1


def _compact_for_match(text: str) -> str:
    value = unicodedata.normalize("NFKC", str(text or ""))
    return re.sub(r"\s+", "", value).lower()


def _math_compact_for_match(text: str) -> str:
    value = unicodedata.normalize("NFKC", str(text or ""))
    value = normalize_inline_math_text(value)
    value = re.sub(r"```(?:json)?|```", "", value, flags=re.IGNORECASE)
    value = re.sub(r"(?<!\\)\$+", "", value)
    return re.sub(r"[\s{}，,。.;；:：]+", "", value).lower()


def _rejection_status(reason: Any) -> str:
    reason_text = str(reason or "")
    if reason_text in {"brain_op_low_confidence_replace"}:
        return "soft_rejected"
    return "hard_rejected"


def _detail_status(detail: dict[str, Any]) -> str:
    reason = str(detail.get("reason") or "")
    if reason in {"already_uncertain", "replacement_same_as_current", "normalized_formula_unchanged", "mark_uncertain_no_effect"}:
        return "superseded_noop"
    return _rejection_status(reason)


def _apply_vision_result(block: dict[str, Any], result: dict[str, Any]) -> list[str]:
    changed = []
    block_type = block.get("type")
    evidence = block.setdefault("evidence", {})
    original_text = str(block.get("latex") or block.get("text") or block.get("description") or "").strip()
    evidence["vision_enrichment"] = {
        "version": HYBRID_ENRICHMENT_VERSION,
        "content_sha256": _response_content_sha256(result),
        "model_request_id": result.get("request_id"),
        "original_text": _truncate(original_text, 1200),
    }
    if isinstance(result.get("crop_audit"), dict):
        evidence["vision_enrichment"]["crop"] = result["crop_audit"]
    if isinstance(result.get("crop_attempts"), list):
        evidence["vision_enrichment"]["crop_attempts"] = result["crop_attempts"]
        evidence["vision_enrichment"]["retry_count"] = max(0, len(result["crop_attempts"]) - 1)

    if block_type in {"figure_note", "image_ref"}:
        description = _first_text(result, "description", "vision_summary", "content", "text")
        if description:
            if block.get("type") == "image_ref":
                block["type"] = "figure_note"
                changed.append("type")
            block["description"] = description
            block["text"] = description
            figure = block.setdefault("figure", {})
            figure["vision_summary"] = description
            for key in ("figure_type", "labels", "relations", "linked_blocks", "uncertainties"):
                if key in result and result.get(key) not in (None, ""):
                    if key == "figure_type":
                        block["figure_type"] = result[key]
                    else:
                        block[key] = result[key]
                    figure[key] = result[key]
            analysis = analyze_figure_description(description)
            fields = analysis.to_block_fields()
            figure.update({key: value for key, value in fields.get("figure", {}).items() if key not in figure or not figure[key]})
            changed.append("description")
        block["origin"] = "vision_description"
        block["source_engine"] = "vision"

    elif block_type == "formula_block":
        latex = _first_text(result, "latex", "formula", "content", "text")
        if latex:
            quality = assess_formula_text(latex)
            block["text"] = quality.latex
            block["latex"] = quality.latex
            block["raw_text"] = result.get("raw_text") or latex
            block["formula_quality"] = quality.to_dict()
            block["warnings"] = [warning.to_dict() for warning in quality.warnings]
            block["origin"] = "vision_formula"
            block["source_engine"] = "vision"
            changed.extend(["text", "latex", "formula_quality"])

    elif block_type == "table":
        table_text = _first_text(result, "markdown", "table_markdown", "raw_text", "content", "text")
        if table_text:
            quality = assess_table(table_text)
            block["text"] = quality.normalized_markdown or table_text
            block["raw_text"] = table_text
            block["table_format"] = quality.table_format if quality.reliable else "uncertain"
            block["table_reliable"] = quality.reliable
            block["table_render_mode"] = "normalized_markdown" if quality.reliable else "degraded_warning"
            block["degrade_reason_codes"] = [issue.code for issue in quality.errors + quality.warnings] if not quality.reliable else []
            block["rows"] = quality.row_count
            block["columns"] = quality.column_counts
            block["table_quality"] = quality.to_dict()
            block["origin"] = "vision_table"
            block["source_engine"] = "vision"
            changed.extend(["text", "table_quality"])

    changed = sorted(set(changed))
    result_text = str(block.get("latex") or block.get("text") or block.get("description") or "").strip()
    evidence["vision_enrichment"]["result_text"] = _truncate(result_text, 1200)
    evidence["vision_enrichment"]["changed_fields"] = changed
    evidence["vision_enrichment"]["text_changed"] = original_text != result_text
    return changed


def _brain_op_audit(op: dict[str, Any], status: str, detail: dict[str, Any]) -> dict[str, Any]:
    return {
        "op": op.get("op"),
        "decision": _brain_op_decision(op),
        "finding_id": op.get("finding_id"),
        "new_finding_id": op.get("new_finding_id"),
        "resolved_finding_id": detail.get("resolved_finding_id") or op.get("_resolved_finding_id"),
        "resolved_new_finding_id": detail.get("resolved_new_finding_id") or op.get("_resolved_new_finding_id"),
        "evidence_type": op.get("evidence_type") or op.get("evidence"),
        "confidence": op.get("confidence"),
        "op_payload_summary": _brain_op_payload_summary(op),
        "target_block_ids": _op_target_block_ids(op),
        "old_text_preview": detail.get("old_text_preview") or _preview_for_audit(str(op.get("old_text") or "")),
        "new_text_preview": detail.get("new_text_preview") or _preview_for_audit(str(op.get("new_text") or "")),
        "current_text_preview": detail.get("current_text_preview"),
        "reason_preview": detail.get("reason_preview") or _preview_for_audit(op.get("reason") or detail.get("reason")),
        "finding_message_preview": detail.get("finding_message_preview") or op.get("_finding_message_preview"),
        "finding_evidence_preview": detail.get("finding_evidence_preview") or op.get("_finding_evidence_preview"),
        "target_block_type": detail.get("target_block_type"),
        "target_block_origin": detail.get("target_block_origin"),
        "target_block_confidence": detail.get("target_block_confidence"),
        "brain_op_review_mode": detail.get("brain_op_review_mode"),
        "repair_actions": detail.get("repair_actions", []),
        "match_strategy": detail.get("match_strategy") or op.get("_match_strategy"),
        "resolved_field": detail.get("resolved_field") or op.get("_resolved_field"),
        "resolved_span": detail.get("resolved_span"),
        "resolved_block_id": detail.get("resolved_block_id"),
        "repair_confidence": detail.get("repair_confidence"),
        "before_block_ids": detail.get("before_block_ids", []),
        "after_block_ids": detail.get("after_block_ids", []),
        "before_blocks": detail.get("before_blocks", []),
        "after_blocks": detail.get("after_blocks", []),
        "before_text_sha256": detail.get("before_text_sha256"),
        "after_text_sha256": detail.get("after_text_sha256"),
        "removed_spans": detail.get("removed_spans", []),
        "removed_text_hashes": detail.get("removed_text_hashes", []),
        "created_block_ids": detail.get("created_block_ids", []),
        "degraded": bool(detail.get("degraded") or op.get("op") == "mark_uncertain"),
        "reason": detail.get("reason") or op.get("reason"),
        "policy_error_detail": detail.get("policy_error_detail"),
        "errors": detail.get("errors", []),
        "status": status,
        "validator_before": detail.get("validator_before"),
        "validator_after": detail.get("validator_after") or detail.get("validation"),
        "validator_delta": detail.get("validator_delta"),
    }


def _normalize_brain_review_payload(parsed: dict[str, Any]) -> dict[str, Any]:
    warnings = parsed.get("warnings") if isinstance(parsed.get("warnings"), list) else []
    decisions = parsed.get("decisions") or []
    new_findings = parsed.get("new_findings") or []
    op_candidates = parsed.get("op_candidates")
    legacy_ops = parsed.get("ops") or parsed.get("operations")
    if op_candidates is None and legacy_ops is not None:
        op_candidates = legacy_ops
        warnings = list(warnings) + [{"code": "legacy_brain_ops_schema", "message": "Brain returned legacy ops schema."}]
    if op_candidates is None:
        op_candidates = []
    if not isinstance(decisions, list):
        return {"error": "invalid_brain_decisions", "message": "Brain JSON field 'decisions' must be a list."}
    if not isinstance(new_findings, list):
        return {"error": "invalid_brain_new_findings", "message": "Brain JSON field 'new_findings' must be a list."}
    if not isinstance(op_candidates, list):
        return {"error": "invalid_brain_op_candidates", "message": "Brain JSON field 'op_candidates' must be a list."}
    return {
        "decisions": [item for item in decisions if isinstance(item, dict)],
        "new_findings": [item for item in new_findings if isinstance(item, dict)],
        "op_candidates": [item for item in op_candidates if isinstance(item, dict)],
        "warnings": warnings,
    }


def _normalize_brain_decisions(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    decisions: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        normalized = dict(item)
        if "finding_id" not in normalized and normalized.get("suspect_id"):
            normalized["finding_id"] = normalized.get("suspect_id")
        normalized.pop("suspect_id", None)
        decision = str(normalized.get("decision") or "").strip()
        if decision == "suspect_confirmed":
            normalized["decision"] = "finding_confirmed"
        decisions.append(normalized)
    return decisions


def _normalize_brain_new_findings(value: Any, slide_no: int) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    findings: list[dict[str, Any]] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            continue
        finding = dict(item)
        raw_aliases = _unique_nonempty_strings(
            [
                finding.get("new_finding_id"),
                finding.get("finding_id"),
                finding.get("id"),
                *(finding.get("aliases") if isinstance(finding.get("aliases"), list) else []),
            ]
        )
        finding_id = str(finding.get("finding_id") or finding.get("id") or f"p{slide_no:04d}-bf{index:03d}")
        finding["finding_id"] = finding_id
        aliases = _unique_nonempty_strings([*raw_aliases, finding.get("new_finding_id"), finding_id])
        if aliases:
            finding["aliases"] = aliases
        finding.pop("id", None)
        finding.pop("suspect_id", None)
        finding["source"] = "brain_discovered"
        finding["page"] = int(finding.get("page") or slide_no)
        finding["kind"] = str(finding.get("kind") or finding.get("code") or "brain_discovered")
        finding["severity"] = str(finding.get("severity") or "warning")
        findings.append(finding)
    return findings


def _normalize_brain_ops(value: Any) -> list[dict[str, Any]]:
    ops = []
    if not isinstance(value, list):
        return ops
    for item in value:
        if not isinstance(item, dict):
            continue
        op = dict(item)
        ops.append(op)
    return ops


def _normalize_brain_op_reference(op: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(op)
    if "id" not in normalized and normalized.get("block_id"):
        normalized["id"] = normalized.get("block_id")
    if "finding_id" not in normalized and normalized.get("suspect_id"):
        normalized["finding_id"] = normalized.get("suspect_id")
    normalized.pop("suspect_id", None)
    decision = str(normalized.get("decision") or "").strip()
    if decision == "suspect_confirmed":
        normalized["decision"] = "finding_confirmed"
    if "new_finding_id" not in normalized and normalized.get("source") == "brain_discovered":
        normalized["new_finding_id"] = normalized.get("finding_id")
    return normalized


def _brain_op_decision(op: dict[str, Any]) -> str:
    decision = str(op.get("decision") or op.get("source") or "").strip()
    if decision == "suspect_confirmed":
        return "finding_confirmed"
    if decision in {"finding_confirmed", "brain_discovered"}:
        return decision
    return "finding_confirmed" if op.get("finding_id") and not op.get("new_finding_id") else "brain_discovered"


def _brain_op_policy_error(
    op: dict[str, Any],
    *,
    new_finding_ids: set[str] | None = None,
    new_finding_aliases: dict[str, dict[str, Any]] | None = None,
    review_mode: str = "aggressive",
) -> dict[str, Any] | None:
    new_finding_ids = new_finding_ids or set()
    new_finding_aliases = new_finding_aliases or {}
    if not str(op.get("decision") or op.get("source") or "").strip():
        return {"reason": "brain_op_missing_or_invalid_decision"}
    decision = _brain_op_decision(op)
    if decision not in {"finding_confirmed", "brain_discovered"}:
        return {"reason": "brain_op_missing_or_invalid_decision"}
    if decision == "brain_discovered":
        new_finding_id = str(op.get("new_finding_id") or op.get("finding_id") or "").strip()
        if not new_finding_id:
            return {"reason": "brain_op_missing_new_finding_reference"}
        if new_finding_aliases and new_finding_id not in new_finding_aliases:
            return {
                "reason": "brain_op_unknown_new_finding_reference",
                "policy_error_detail": {
                    "provided_new_finding_id": new_finding_id,
                    "known_alias_count": len(new_finding_aliases),
                    "known_aliases_sample": sorted(new_finding_aliases)[:12],
                },
            }
        if new_finding_ids and new_finding_id not in new_finding_ids:
            return {
                "reason": "brain_op_unknown_new_finding_reference",
                "policy_error_detail": {
                    "provided_new_finding_id": new_finding_id,
                    "known_alias_count": len(new_finding_ids),
                    "known_aliases_sample": sorted(new_finding_ids)[:12],
                },
            }
    elif not str(op.get("finding_id") or "").strip():
        return {"reason": "brain_op_missing_finding_reference"}

    evidence_type = str(op.get("evidence_type") or op.get("evidence") or "").strip()
    if not evidence_type:
        return {"reason": "brain_op_missing_evidence_type"}

    confidence = _safe_float(op.get("confidence"), -1.0)
    if confidence < 0.0 or confidence > 1.0:
        return {"reason": "brain_op_missing_or_invalid_confidence"}

    op_name = str(op.get("op") or "")
    if op_name == "replace_text_span_checked":
        if confidence < 0.75 and not _low_confidence_replace_allowed(op, review_mode=review_mode):
            return {"reason": "brain_op_low_confidence_replace"}
        if not str(op.get("id") or "").strip():
            return {"reason": "brain_op_missing_target_block"}
        if not str(op.get("old_text") or "") or not str(op.get("new_text") or ""):
            return {"reason": "brain_op_missing_checked_span"}
        if (
            _looks_like_whole_markdown_rewrite(str(op.get("old_text") or ""))
            or _looks_like_whole_markdown_rewrite(str(op.get("new_text") or ""))
        ) and not _structured_formula_rewrite_allowed(op):
            return {"reason": "brain_op_whole_markdown_rewrite"}
    elif op_name in {"normalize_formula", "mark_uncertain", "promote_heading", "demote_heading"}:
        if not str(op.get("id") or "").strip():
            return {"reason": "brain_op_missing_target_block"}
    elif op_name == "merge_block":
        if not str(op.get("a") or "").strip() or not str(op.get("b") or "").strip():
            return {"reason": "brain_op_missing_target_block"}
    return None


def _low_confidence_replace_allowed(op: dict[str, Any], *, review_mode: str) -> bool:
    if review_mode != "aggressive":
        return False
    old_text = str(op.get("old_text") or "")
    new_text = str(op.get("new_text") or "")
    if not old_text or not new_text:
        return False
    if len(old_text) > 180 or len(new_text) > len(old_text) + 120:
        return False
    return str(op.get("match_strategy") or op.get("_match_strategy") or op.get("resolved_field") or "").strip() != ""


def _structured_formula_rewrite_allowed(op: dict[str, Any]) -> bool:
    strategy = str(op.get("match_strategy") or op.get("_match_strategy") or "")
    if strategy == "structured_formula_payload":
        return True
    old_payload = _parse_json_payload(str(op.get("old_text") or ""))
    if not old_payload:
        return False
    new_text = str(op.get("new_text") or "").strip()
    return bool(new_text and (looks_like_latex_display(new_text) or looks_like_standalone_formula(new_text) or "\\begin{" in new_text))


def _brain_initial_finding_alias_map(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return _brain_finding_alias_map(findings, include_new_id=False)


def _brain_new_finding_alias_map(new_findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return _brain_finding_alias_map(new_findings, include_new_id=True)


def _brain_finding_alias_map(findings: list[dict[str, Any]], *, include_new_id: bool) -> dict[str, dict[str, Any]]:
    aliases: dict[str, dict[str, Any]] = {}
    for finding in findings:
        if not isinstance(finding, dict):
            continue
        alias_values = _brain_finding_alias_values(finding, include_new_id=include_new_id)
        if not alias_values:
            continue
        resolved = {
            "finding_id": str(finding.get("finding_id") or alias_values[0]),
            "new_finding_id": str(finding.get("new_finding_id") or finding.get("finding_id") or alias_values[0])
            if include_new_id
            else None,
            "aliases": alias_values,
            "finding": finding,
        }
        for alias in alias_values:
            aliases[alias] = resolved
    return aliases


def _brain_finding_alias_values(finding: dict[str, Any], *, include_new_id: bool) -> list[str]:
    values: list[Any] = [finding.get("finding_id"), finding.get("id"), finding.get("suspect_id")]
    if include_new_id:
        values.insert(0, finding.get("new_finding_id"))
    aliases = finding.get("aliases")
    if isinstance(aliases, list):
        values.extend(aliases)
    return _unique_nonempty_strings(values)


def _resolve_brain_finding_reference(
    op: dict[str, Any],
    initial_aliases: dict[str, dict[str, Any]],
    new_aliases: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    decision = _brain_op_decision(op)
    if decision == "brain_discovered":
        reference = str(op.get("new_finding_id") or op.get("finding_id") or "").strip()
        resolved = new_aliases.get(reference) if reference else None
    else:
        reference = str(op.get("finding_id") or "").strip()
        resolved = initial_aliases.get(reference) if reference else None
    if not reference:
        return None
    if not resolved:
        return None
    op["_resolved_finding_id"] = resolved.get("finding_id")
    op["_resolved_new_finding_id"] = resolved.get("new_finding_id")
    finding = resolved.get("finding")
    if isinstance(finding, dict):
        op["_finding_message_preview"] = _finding_message_preview(finding)
        op["_finding_evidence_preview"] = _finding_evidence_preview(finding)
    return resolved


def _unique_nonempty_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if text and text not in result:
            result.append(text)
    return result


def _finding_message_preview(finding: dict[str, Any]) -> str | None:
    message = (
        finding.get("message")
        or finding.get("reason")
        or finding.get("description")
        or finding.get("kind")
        or finding.get("code")
    )
    return _preview_for_audit(message)


def _finding_evidence_preview(finding: dict[str, Any]) -> str | None:
    evidence = finding.get("evidence")
    if evidence in (None, "", [], {}):
        evidence = {
            key: finding.get(key)
            for key in ("current_text", "suggested_text", "candidates", "op_hint", "block_id", "severity")
            if finding.get(key) not in (None, "", [], {})
        }
    return _preview_for_audit(evidence)


def _looks_like_whole_markdown_rewrite(text: str) -> bool:
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


def _brain_op_payload_summary(op: dict[str, Any]) -> dict[str, Any]:
    old_text = str(op.get("old_text") or "")
    new_text = str(op.get("new_text") or "")
    return {
        "op": op.get("op"),
        "field": op.get("field"),
        "decision": _brain_op_decision(op),
        "finding_id": op.get("finding_id"),
        "new_finding_id": op.get("new_finding_id"),
        "target_block_ids": _op_target_block_ids(op),
        "old_text_len": len(old_text) if old_text else 0,
        "new_text_len": len(new_text) if new_text else 0,
        "old_text_sha256": sha256_text(old_text) if old_text else None,
        "new_text_sha256": sha256_text(new_text) if new_text else None,
        "evidence_type": op.get("evidence_type") or op.get("evidence"),
        "confidence": op.get("confidence"),
        "reason": _preview_for_audit(op.get("reason"), limit=180),
    }


def _count_audit_reasons(audits: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for audit in audits:
        if audit.get("status") not in {"rejected", "hard_rejected", "soft_rejected"}:
            continue
        reason = str(audit.get("reason") or "unknown")
        counts[reason] = counts.get(reason, 0) + 1
    return counts


def _count_contract_errors(audits: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for audit in audits:
        if audit.get("status") not in {"rejected", "hard_rejected", "soft_rejected"}:
            continue
        for error in audit.get("errors") or []:
            code = str(error or "unknown")
            counts[code] = counts.get(code, 0) + 1
    return counts


def _format_reason_counts_zh(counts: dict[str, int]) -> str:
    if not counts:
        return ""
    labels = {
        "page_ir_contract_failed": "IR合同失败",
        "no_change": "无变化",
        "validation_would_get_worse": "校验变差",
        "unknown_or_unsafe_op": "未知或不安全操作",
        "brain_op_unknown_new_finding_reference": "Brain新疑点引用不存在",
        "brain_op_missing_new_finding_reference": "Brain新疑点引用缺失",
        "old_text_not_found": "原文片段未命中",
        "replacement_same_as_current": "替换后与当前一致",
        "already_uncertain": "已是不确定块",
        "normalized_formula_unchanged": "公式规范化无变化",
        "mark_uncertain_no_effect": "标记不确定无效果",
        "replacement_growth_unsafe": "替换增长过大",
        "replacement_too_broad": "替换范围过大",
        "drop_block_not_allowed_nonempty": "非空块禁止删除",
    }
    parts = []
    for reason, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        parts.append(f"{labels.get(reason, reason)}={count}")
    return "，".join(parts)


def _op_target_block_ids(op: dict[str, Any]) -> list[str]:
    ids = []
    for key in ("id", "a", "b", "table_id", "title_block_id", "caption_block_id"):
        value = op.get(key)
        if value and value not in ids:
            ids.append(str(value))
    value = op.get("target_block_ids")
    if isinstance(value, list):
        for item in value:
            if item and str(item) not in ids:
                ids.append(str(item))
    return ids


def _brain_op_current_preview(page_ir: dict[str, Any], op: dict[str, Any]) -> dict[str, Any]:
    target_ids = set(_op_target_block_ids(op))
    texts = []
    first_block: dict[str, Any] | None = None
    for block in page_ir.get("blocks") or []:
        if not isinstance(block, dict) or str(block.get("id") or "") not in target_ids:
            continue
        if first_block is None:
            first_block = block
        text = str(block.get("text") or block.get("latex") or block.get("description") or block.get("raw_text") or "")
        if text:
            texts.append(text)
    result: dict[str, Any] = {}
    if texts:
        result["current_text_preview"] = _preview_for_audit("\n".join(texts))
    if first_block:
        result.update(
            {
                "target_block_type": first_block.get("type"),
                "target_block_origin": first_block.get("origin") or first_block.get("source_engine"),
                "target_block_confidence": first_block.get("confidence"),
            }
        )
    return result


def _preview_for_audit(value: Any, limit: int = 200) -> str | None:
    if value in (None, "", [], {}):
        return None
    if isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)
        except (TypeError, ValueError):
            text = str(value)
    compact = " ".join(str(text or "").split())
    if not compact:
        return None
    compact = _redact_sensitive_preview(compact)
    if len(compact) <= limit:
        return compact
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


def _resolve_block_image_path(block: dict[str, Any], output_root: Path) -> Path | None:
    return resolve_original_block_image_path(block, output_root)


def _document_source_pdf(document_ir: dict[str, Any]) -> Path | None:
    source = document_ir.get("source") if isinstance(document_ir.get("source"), dict) else {}
    for key in ("input_path", "source_path", "pdf_path", "path"):
        value = str(source.get(key) or "").strip()
        if not value:
            continue
        path = Path(value)
        if path.exists() and path.suffix.lower() == ".pdf":
            return path
    return None


def _vision_retry_reason(block: dict[str, Any], normalized: dict[str, Any]) -> str | None:
    if not normalized.get("success"):
        return None
    block_type = str(block.get("type") or "")
    if block_type == "formula_block":
        latex = _first_text(normalized, "latex", "formula", "content", "text")
        if not latex:
            return "formula_empty"
        if _looks_like_json_payload_text(latex):
            return "formula_json_payload"
        quality = assess_formula_text(latex)
        hard_codes = {
            "formula_empty",
            "formula_brace_unbalanced",
            "formula_parenthesis_unbalanced",
            "formula_bracket_unbalanced",
            "latex_left_right_unbalanced",
            "latex_frac_missing_braces",
            "formula_truncated",
            "formula_isolated_operator",
            "formula_reasoning_without_latex",
            "formula_repeated_token_artifact",
        }
        for warning in quality.warnings:
            if warning.code in hard_codes:
                return warning.code
        return None
    if block_type == "table":
        table_text = _first_text(normalized, "markdown", "table_markdown", "raw_text", "content", "text")
        if not table_text:
            return "table_empty"
        if _looks_like_json_payload_text(table_text):
            return "table_json_payload"
    if block_type in {"figure_note", "image_ref"}:
        description = _first_text(normalized, "description", "vision_summary", "content", "text")
        if not description:
            return "figure_description_empty"
        if _looks_like_json_payload_text(description):
            return "figure_json_payload"
    return None


def _prefer_retry_vision_result(block: dict[str, Any], original: dict[str, Any], retry: dict[str, Any]) -> bool:
    if not retry.get("success"):
        return False
    if not original.get("success"):
        return True
    original_reason = _vision_retry_reason(block, original)
    retry_reason = _vision_retry_reason(block, retry)
    if original_reason and not retry_reason:
        return True
    if retry_reason:
        return False
    block_type = str(block.get("type") or "")
    if block_type == "formula_block":
        return len(_first_text(retry, "latex", "formula", "content", "text")) > len(
            _first_text(original, "latex", "formula", "content", "text")
        )
    if block_type == "table":
        return len(_first_text(retry, "markdown", "table_markdown", "raw_text", "content", "text")) > len(
            _first_text(original, "markdown", "table_markdown", "raw_text", "content", "text")
        )
    if block_type in {"figure_note", "image_ref"}:
        return len(_first_text(retry, "description", "vision_summary", "content", "text")) > len(
            _first_text(original, "description", "vision_summary", "content", "text")
        )
    return False


def _looks_like_json_payload_text(text: str) -> bool:
    value = str(text or "").strip()
    if not value:
        return False
    if value.startswith("```") and "json" in value[:16].lower():
        return True
    if value.startswith("{") and any(key in value[:300] for key in ('"latex"', '"description"', '"figure_type"', '"markdown"')):
        return True
    return False


def _context_window(pages: list[dict[str, Any]], page_index: int, radius: int = 2) -> list[dict[str, Any]]:
    start = max(0, page_index - radius)
    end = min(len(pages), page_index + radius + 1)
    return [pages[index] for index in range(start, end)]


def _crop_vision_prompt(page_ir: dict[str, Any], block: dict[str, Any]) -> str:
    block_type = block.get("type")
    if block_type in {"figure_note", "image_ref"}:
        task = "识别这个图示或手绘图。必须用中文返回图类型、可见标签、主要关系、与正文或公式的可能关联、不确定点。"
    elif block_type == "table":
        task = "识别这个表格。优先返回可靠 Markdown 表格；如果结构不可靠，返回 raw_text 并说明不确定。"
    elif block_type == "formula_block":
        task = "识别这个公式裁剪图。返回可渲染 LaTeX，不要把 \\tag{} 放进 aligned 环境内部。"
    else:
        task = "识别这个文档裁剪块。"
    context = _crop_vision_context(page_ir, block)
    return (
        f"{task}\n"
        "页面上下文只用于判读裁剪图，不要把上下文里不存在于裁剪图的内容编进结果。\n"
        f"页面上下文 JSON：{json.dumps(context, ensure_ascii=False)}\n"
        "只返回 JSON，不要返回思考过程，不要返回 Markdown 代码围栏。可用字段："
        "description, figure_type, labels, relations, uncertainties, latex, markdown, raw_text, warnings。"
    )


def _crop_vision_context(page_ir: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    target_id = block.get("id")
    compact_blocks = []
    for item in page_ir.get("blocks") or []:
        if not isinstance(item, dict):
            continue
        text = str(item.get("latex") or item.get("text") or item.get("description") or "").strip()
        if not text:
            continue
        compact_blocks.append(
            {
                "id": item.get("id"),
                "role": "target_crop" if item.get("id") == target_id else "nearby_page_block",
                "type": item.get("type"),
                "text": _truncate(text, 180),
            }
        )
    return {
        "page": page_ir.get("source_page"),
        "target_block_id": target_id,
        "target_block_type": block.get("type"),
        "nearby_blocks": compact_blocks[:40],
    }


def _brain_ops_prompt(page_ir: dict[str, Any], context_pages: list[dict[str, Any]]) -> str:
    page_no = int(page_ir.get("source_page") or 0)
    context = [_brain_context_page(page, target_page_no=page_no) for page in context_pages]
    review_profile = _brain_review_profile(page_ir)
    dual_note = ""
    if page_ir.get("dual_evidence"):
        dual_note = (
            "当前页包含 MinerU 与 PaddleOCR 两份解析证据。MinerU 是主版面骨架，"
            "PaddleOCR 是交叉核验证据；只有当 PaddleOCR 对公式、手写字词或段落明显更完整/更符合上下文时，"
            "才使用 checked op 修正对应 MinerU block。\n"
        )
    return (
        "你是 DocPage2MD 的 Brain 证据审阅器。只能输出 JSON，不得输出 Markdown，不得输出思考过程。\n"
        "任务：结合当前页、可配置前后页上下文、initial findings、MinerU/PaddleOCR 双引擎证据和 Vision 裁剪图结果，审阅明显 OCR/LaTeX 错误。\n"
        "你可以主动发现新疑点，但不能自由重写整页；每条修改必须绑定具体 block_id 和 old_text/new_text，且 old_text 必须是目标字段中真实存在的短 span。\n"
        "上下文中每个 block 会提供 fields 快照。replace_text_span_checked 应优先从 fields.text/fields.latex/fields.raw_text/fields.description 复制原文短 span，避免凭记忆改写。\n"
        "已有 finding 的审核写入 decisions，decision 使用 accept/reject/uncertain，并填写 finding_id。自主发现的新疑点写入 new_findings，source 必须是 brain_discovered。\n"
        "所有修改只能写入 op_candidates。已有 finding 的 op 使用 decision=finding_confirmed 并填写 finding_id；自主发现的 op 使用 decision=brain_discovered 并填写 new_finding_id。\n"
        "每条 op 应填写 block_id、evidence_type 和 confidence；如果无法确定 evidence_type，就根据证据写 context/dual_engine/vision_crop/finding。不要因为格式字段不确定而放弃明显正确的短 span 修正。\n"
        "公式和数学符号必须使用 LaTeX；即使符号混在 paragraph/text block 中，也要改成 $...$ 内的 \\phi、\\theta、\\omega 等命令，不能保留裸 φ、θ、ω。\n"
        f"{dual_note}"
        "允许 ops：replace_text_span_checked, normalize_formula, mark_uncertain, merge_block, promote_heading, demote_heading。\n"
        "replace_text_span_checked 格式："
        '{"op":"replace_text_span_checked","block_id":"p0001-b001","old_text":"...","new_text":"...","field":"text","decision":"brain_discovered","new_finding_id":"p0001-bf001","evidence_type":"context|dual_engine|vision_crop|formula_quality|finding","confidence":0.86,"reason":"..."}\n'
        "禁止输出整页 Markdown、禁止输出未绑定 block 的修改、禁止输出 [mineru]/[paddleocr] 二选一残留。\n"
        f"当前页：{page_no}\n"
        f"审阅配置 JSON：{json.dumps(review_profile, ensure_ascii=False)}\n"
        f"上下文 JSON：{json.dumps(context, ensure_ascii=False)}\n"
        '返回格式：{"decisions":[],"new_findings":[],"op_candidates":[],"warnings":[]}'
    )


def _brain_context_page(page: dict[str, Any], *, target_page_no: int) -> dict[str, Any]:
    page_no = int(page.get("source_page") or 0)
    is_target = page_no == target_page_no
    block_limit = 80 if is_target else 32
    raw_limit = 1600 if is_target else 360
    text_limit = 420 if is_target else 120
    context = {
        "page": page.get("source_page"),
        "role": "target" if is_target else "neighbor",
        "raw_text": _truncate(page.get("raw_text") or "", raw_limit),
        "blocks": [
            {
                "id": block.get("id"),
                "type": block.get("type"),
                "text": _truncate(block.get("latex") or block.get("text") or block.get("description") or "", text_limit),
                "fields": _brain_block_fields_snapshot(block, text_limit),
                "confidence": block.get("confidence"),
                "origin": block.get("origin"),
                "source_engine": block.get("source_engine"),
            }
            for block in (page.get("blocks") or [])[:block_limit]
            if _brain_context_block_text(block)
        ],
    }
    if is_target:
        findings = _brain_initial_findings(page)
        context["initial_findings"] = _brain_findings_context(findings)
        context["priority_blocks"] = _brain_priority_blocks(page, findings)
    dual_evidence = page.get("dual_evidence")
    if is_target and isinstance(dual_evidence, dict):
        context["dual_evidence"] = _brain_dual_evidence_context(dual_evidence)
    return context


def _brain_review_profile(page_ir: dict[str, Any]) -> dict[str, Any]:
    findings = _brain_initial_findings(page_ir)
    priority_blocks = _brain_priority_blocks(page_ir, findings)
    blocks = [block for block in page_ir.get("blocks") or [] if isinstance(block, dict)]
    low_confidence_count = sum(1 for block in blocks if _safe_float(block.get("confidence"), 1.0) < 0.72)
    has_visual_or_formula = any(block.get("type") in VISION_ENRICH_BLOCK_TYPES or block.get("type") in {"formula_inline"} for block in blocks)
    dual = page_ir.get("dual_evidence")
    return {
        "mode": "standard_evidence_review",
        "policy": "findings_first_but_brain_may_discover_high_confidence_span_errors",
        "block_count": len(blocks),
        "finding_count": len(findings),
        "priority_block_count": len(priority_blocks),
        "low_confidence_block_count": low_confidence_count,
        "has_dual_evidence": isinstance(dual, dict) and bool((dual.get("paddleocr") or {}).get("available")),
        "has_visual_or_formula": has_visual_or_formula,
        "accepted_decisions": ["finding_confirmed", "brain_discovered"],
        "required_op_fields": ["op", "id", "old_text", "new_text", "field", "decision", "evidence_type", "confidence", "reason"],
    }


def _brain_initial_findings(page_ir: dict[str, Any]) -> list[dict[str, Any]]:
    findings = page_ir.get("findings")
    if isinstance(findings, dict) and isinstance(findings.get("initial"), list):
        return [item for item in findings.get("initial") or [] if isinstance(item, dict)]
    slide_no = int(page_ir.get("source_page") or 0)
    return build_initial_findings_pool(slide_no=slide_no, page_ir=page_ir, blocks=page_ir.get("blocks") or [])


def _brain_findings_context(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact = []
    for finding in findings[:40]:
        if not isinstance(finding, dict):
            continue
        compact.append(
            {
                "finding_id": finding.get("finding_id") or finding.get("id"),
                "source": finding.get("source"),
                "kind": finding.get("kind") or finding.get("code"),
                "severity": finding.get("severity"),
                "block_id": finding.get("block_id"),
                "block_type": finding.get("block_type"),
                "current_text": _truncate(str(finding.get("current_text") or ""), 180) if finding.get("current_text") else None,
                "candidates": _brain_finding_candidates_context(finding.get("candidates") or []),
                "op_hint": finding.get("op_hint"),
                "locator": {
                    "block_id": finding.get("block_id"),
                    "preferred_field": (finding.get("op") or {}).get("field") if isinstance(finding.get("op"), dict) else None,
                    "candidate_old_text": _truncate(str(finding.get("current_text") or ""), 160) if finding.get("current_text") else None,
                },
                "message": _truncate(str(finding.get("message") or ""), 180),
                "evidence": _truncate(json.dumps(finding.get("evidence"), ensure_ascii=False, default=str), 240)
                if finding.get("evidence") is not None
                else None,
            }
        )
    return compact


def _brain_finding_candidates_context(candidates: Any) -> list[dict[str, Any]]:
    compact = []
    if not isinstance(candidates, list):
        return compact
    for candidate in candidates[:4]:
        if not isinstance(candidate, dict):
            continue
        compact.append(
            {
                "source": candidate.get("source"),
                "block_id": candidate.get("block_id"),
                "type": candidate.get("type"),
                "text": _truncate(str(candidate.get("text") or ""), 160),
                "confidence": candidate.get("confidence"),
            }
        )
    return compact


def _brain_priority_blocks(page_ir: dict[str, Any], findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    finding_block_ids = {str(finding.get("block_id")) for finding in findings if finding.get("block_id")}
    priority = []
    for block in page_ir.get("blocks") or []:
        if not isinstance(block, dict):
            continue
        block_id = str(block.get("id") or "")
        block_type = str(block.get("type") or "")
        confidence = _safe_float(block.get("confidence"), 1.0)
        has_vision = isinstance(block.get("evidence"), dict) and isinstance(block["evidence"].get("vision_enrichment"), dict)
        if block_id not in finding_block_ids and confidence >= 0.72 and block_type not in {"formula_inline", "formula_block", "table", "figure_note", "image_ref", "uncertain"} and not has_vision:
            continue
        priority.append(
            {
                "id": block_id,
                "type": block_type,
                "confidence": block.get("confidence"),
                "origin": block.get("origin"),
                "source_engine": block.get("source_engine"),
                "text": _truncate(block.get("latex") or block.get("text") or block.get("description") or "", 360),
                "finding_ids": [finding.get("finding_id") or finding.get("id") for finding in findings if str(finding.get("block_id") or "") == block_id],
                "has_vision_evidence": has_vision,
            }
        )
    return priority[:48]


def _brain_context_block_text(block: dict[str, Any]) -> str:
    return str(block.get("latex") or block.get("text") or block.get("description") or "").strip()


def _brain_block_fields_snapshot(block: dict[str, Any], limit: int) -> dict[str, str]:
    fields = {}
    for key in ("text", "latex", "raw_text", "description"):
        value = block.get(key)
        if isinstance(value, str) and value.strip():
            fields[key] = _truncate(value, limit)
    return fields


def _brain_dual_evidence_context(dual_evidence: dict[str, Any]) -> dict[str, Any]:
    def compact(engine: str) -> dict[str, Any]:
        payload = dual_evidence.get(engine) if isinstance(dual_evidence.get(engine), dict) else {}
        return {
            "available": bool(payload.get("available")),
            "raw_text": _truncate(payload.get("raw_text") or "", 1200),
            "blocks": [
                {
                    "id": block.get("id"),
                    "type": block.get("type"),
                    "text": _truncate(block.get("text") or "", 220),
                    "confidence": block.get("confidence"),
                }
                for block in (payload.get("blocks") or [])[:80]
                if isinstance(block, dict) and str(block.get("text") or "").strip()
            ],
        }

    return {"mineru": compact("mineru"), "paddleocr": compact("paddleocr")}


def _parse_json_object(text: str) -> dict[str, Any] | None:
    stripped = (text or "").strip()
    if not stripped:
        return None
    fence = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        stripped = fence.group(1).strip()
    try:
        value = json.loads(stripped)
        return value if isinstance(value, dict) else None
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end > start:
        try:
            value = json.loads(stripped[start : end + 1])
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def _model_payload(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return {
            "content": str(value.get("content") or ""),
            "reasoning": str(value.get("reasoning") or value.get("reasoning_content") or ""),
            "usage": value.get("usage"),
            "request_id": value.get("request_id"),
            "provider_latency": value.get("provider_latency"),
        }
    if isinstance(value, tuple):
        return {
            "content": str(value[0] if len(value) > 0 else ""),
            "reasoning": str(value[1] if len(value) > 1 else ""),
            "usage": value[2] if len(value) > 2 else None,
            "request_id": value[3] if len(value) > 3 else None,
            "provider_latency": value[4] if len(value) > 4 else None,
        }
    return {"content": str(value or ""), "reasoning": "", "usage": None, "request_id": None, "provider_latency": None}


def _normalize_backend_response(response: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(response, dict):
        return _backend_error("invalid_backend_response", "Backend did not return a dict.")
    if response.get("success") is True:
        return response
    if response.get("success") is False:
        return response
    if any(key in response for key in ("ops", "op_candidates", "decisions", "new_findings")) or any(
        key in response for key in ("description", "latex", "markdown", "content")
    ):
        response["success"] = True
        return response
    return _backend_error("invalid_backend_response", "Backend response lacked success/content fields.", response)


def _backend_error(code: str, message: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    return {
        "success": False,
        "error_code": code,
        "error_message": _safe_model_error(message),
        **_provider_fields(payload),
    }


def _provider_fields(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "usage": source.get("usage"),
        "request_id": source.get("request_id"),
        "provider_latency": source.get("provider_latency"),
    }


def _safe_model_error(message: Any) -> str:
    text = str(message or "")
    text = re.sub(r"Trace:\s*.*$", "Trace omitted.", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"reasoning_content\s*[:=]\s*.*$", "reasoning_content omitted.", text, flags=re.DOTALL | re.IGNORECASE)
    return _truncate(text.strip(), 300)


def _first_text(source: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = source.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _response_content_sha256(source: dict[str, Any]) -> str | None:
    content = _first_text(source, "description", "vision_summary", "latex", "markdown", "table_markdown", "raw_text", "content", "text")
    return sha256_text(content) if content else None


def _stage_status(attempted: int, succeeded: int, failed: int) -> str:
    if attempted == 0:
        return "skipped"
    if succeeded and not failed:
        return "ok"
    if succeeded and failed:
        return "partial"
    return "failed"


def _aggregate_usage(items: Iterable[dict[str, Any]]) -> dict[str, int] | None:
    total_prompt = 0
    total_completion = 0
    total = 0
    seen = False
    for item in items:
        usage = item.get("usage")
        if not isinstance(usage, dict):
            continue
        prompt = _first_int(usage, "input_tokens", "prompt_tokens", "promptTokenCount")
        completion = _first_int(usage, "output_tokens", "completion_tokens", "completionTokenCount")
        usage_total = _first_int(usage, "total_tokens", "totalTokenCount")
        if prompt is None and completion is None and usage_total is None:
            continue
        seen = True
        total_prompt += int(prompt or 0)
        total_completion += int(completion or 0)
        total += int(usage_total if usage_total is not None else int(prompt or 0) + int(completion or 0))
    if not seen:
        return None
    return {"prompt_tokens": total_prompt, "completion_tokens": total_completion, "total_tokens": total}


def _first_int(source: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = source.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _first_value(items: Iterable[dict[str, Any]], key: str):
    for item in items:
        value = item.get(key)
        if value:
            return value
    return None


def _sum_provider_latency(items: Iterable[dict[str, Any]]) -> float | None:
    total = 0.0
    seen = False
    for item in items:
        value = item.get("provider_latency")
        if value is None:
            continue
        try:
            total += float(value)
            seen = True
        except (TypeError, ValueError):
            continue
    return round(total, 3) if seen else None


def _enrichment_summary(page_results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    results = list(page_results)
    return {
        "page_count": len(results),
        "vision_attempted_blocks": sum(int((item.get("vision") or {}).get("attempted_blocks") or 0) for item in results),
        "vision_succeeded_blocks": sum(int((item.get("vision") or {}).get("succeeded_blocks") or 0) for item in results),
        "brain_ops_requested": sum(int((item.get("brain") or {}).get("ops_requested") or 0) for item in results),
        "brain_ops_applied": sum(int((item.get("brain") or {}).get("ops_applied") or 0) for item in results),
        "brain_repair_successes": sum(int((item.get("brain") or {}).get("repair_successes") or 0) for item in results),
        "brain_noop_or_superseded": sum(int((item.get("brain") or {}).get("noop_or_superseded") or 0) for item in results),
        "brain_discovered_count": sum(int((item.get("brain") or {}).get("brain_discovered_count") or 0) for item in results),
        "refiner_ops_applied": sum(len((item.get("block_refiner") or {}).get("applied_ops") or []) for item in results),
    }


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."
