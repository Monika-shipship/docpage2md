from docpage2md_app.config import AppConfig
from docpage2md_app.reporting import build_run_report, finalize_run_report


def test_finalize_report_summarizes_usage_and_op_audit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    report, page_reports = build_run_report("Deck", [str(image)], 0, AppConfig())
    page = page_reports[1]
    page["stage1"]["status"] = "ok"
    page["stage1"]["usage"] = {"prompt_tokens": 10, "completion_tokens": 5}
    page["stage2"]["status"] = "ok"
    page["stage2"]["usage"] = {"input_tokens": 20, "output_tokens": 7}
    page["final"].update({"status": "ok", "included_in_full": True})
    page["op_audit"] = [
        {
            "status": "applied",
            "op": "mark_uncertain",
            "decision": "brain_discovered",
            "degraded": True,
            "removed_spans": [{"block_id": "p0001-b002"}],
        },
        {
            "status": "rejected",
            "op": "replace_text_span_checked",
            "reason": "page_ir_contract_failed",
            "errors": ["block_2_unknown_origin"],
        }
    ]
    page["brain"] = {"brain_discovered_count": 1}

    finalize_run_report(report)

    assert report["summary"]["op_audit"]["by_status"] == {"applied": 1, "rejected": 1}
    assert report["summary"]["op_audit"]["rejection_reasons"] == {"page_ir_contract_failed": 1}
    assert report["summary"]["op_audit"]["contract_error_codes"] == {"block_2_unknown_origin": 1}
    assert report["summary"]["op_rejection_reasons"] == {"page_ir_contract_failed": 1}
    assert report["summary"]["contract_error_codes"] == {"block_2_unknown_origin": 1}
    assert report["summary"]["brain_discovered_count"] == 1
    assert "findings" in report["summary"]
    assert "suspects" not in report["summary"]
    assert "suspects" not in page
    assert report["summary"]["op_audit"]["removed_spans"] == 1
    assert report["summary"]["op_audit"]["degraded"] == 1
    assert report["cost"]["actual_tokens"]["input_tokens"] == 30
    assert report["cost"]["actual_tokens"]["output_tokens"] == 12
    assert report["cost"]["actual_tokens"]["total_tokens"] == 42


def test_finalize_report_keeps_actual_usage_null_when_provider_does_not_return_usage(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    report, page_reports = build_run_report("Deck", [str(image)], 0, AppConfig())
    page_reports[1]["final"].update({"status": "ok", "included_in_full": True})

    finalize_run_report(report)

    assert report["cost"]["actual_tokens"] is None
