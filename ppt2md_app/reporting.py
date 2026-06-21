from pathlib import Path
from typing import Any, Dict, Iterable

from .artifacts import (
    RUN_REPORT_SCHEMA_VERSION,
    now_iso,
    report_model_identity,
    report_prompt_identity,
)
from .config import AppConfig
from .versioning import PNG2MD_PIPELINE_VERSION


def build_run_report(
    ppt_name: str,
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
                "stage1": _stage_state(),
                "stage2": _stage_state(),
                "validation": {"ok": None, "errors": [], "warnings": []},
                "refiner": {"changed": False, "applied_ops": [], "dismissed": []},
                "final": {
                    "status": "pending",
                    "included_in_full": False,
                    "reason": None,
                },
            }
        )

    report = {
        "schema_version": RUN_REPORT_SCHEMA_VERSION,
        "pipeline_version": PNG2MD_PIPELINE_VERSION,
        "ppt_name": ppt_name,
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
    pages_failed = sum(1 for page in pages if page.get("final", {}).get("status") in ("failed", "fail_open"))
    stage1_cache_hits = sum(1 for page in pages if page.get("stage1", {}).get("cache") == "hit")
    stage2_cache_hits = sum(1 for page in pages if page.get("stage2", {}).get("cache") == "hit")
    warnings = sum(len(page.get("validation", {}).get("warnings") or []) for page in pages)

    report["summary"] = {
        "pages_total": len(pages),
        "pages_ok": pages_ok,
        "pages_failed": pages_failed,
        "stage1_cache_hits": stage1_cache_hits,
        "stage2_cache_hits": stage2_cache_hits,
        "fail_open_pages": sum(1 for page in pages if page.get("final", {}).get("status") == "fail_open"),
        "validation_warnings": warnings,
    }
    if pages_ok == len(pages):
        report["status"] = "ok"
    elif pages_ok > 0:
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


def _stage_state():
    return {
        "status": "pending",
        "cache": None,
        "path": None,
        "elapsed_seconds": None,
        "sha256": None,
        "error_code": None,
        "error_message": None,
        "warnings": [],
    }
