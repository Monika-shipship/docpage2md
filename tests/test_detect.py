from ppt2md_app.detect import detect_page_suspects, summarize_suspects
from ppt2md_app.ir import build_page_ir


def test_detect_page_suspects_from_validation_quality_and_stage_state():
    suspects = detect_page_suspects(
        slide_no=2,
        stage2={"status": "failed", "error_code": "stage2_failed", "error_message": "Brain Error"},
        validation={
            "ok": True,
            "errors": [],
            "warnings": [
                {
                    "code": "ocr_coverage_low",
                    "severity": "warning",
                    "message": "覆盖率偏低",
                    "evidence": "ratio=0.2",
                }
            ],
        },
        quality={
            "warnings": [
                {
                    "code": "table_quality_warning",
                    "message": "表格结构不可靠。",
                    "details": {"table_format": "markdown"},
                }
            ]
        },
    )

    assert [suspect["id"] for suspect in suspects] == ["p0002-sus001", "p0002-sus002", "p0002-sus003"]
    assert [suspect["source"] for suspect in suspects] == ["stage2", "validation", "block_quality"]
    assert [suspect["op_hint"] for suspect in suspects] == [
        "mark_failed_page",
        "inspect_ocr_coverage",
        "mark_uncertain",
    ]


def test_summarize_suspects_counts_codes_and_severity():
    pages = [
        {"suspects": [{"code": "ocr_coverage_low", "severity": "warning", "op_hint": "inspect_ocr_coverage"}]},
        {
            "suspects": [
                {"code": "ocr_coverage_low", "severity": "warning", "op_hint": "inspect_ocr_coverage"},
                {"code": "stage2_failed", "severity": "error", "op": {"op": "mark_failed_page"}},
            ]
        },
    ]

    summary = summarize_suspects(pages)

    assert summary == {
        "total": 3,
        "actionable_total": 3,
        "by_code": {"ocr_coverage_low": 2, "stage2_failed": 1},
        "by_op": {"inspect_ocr_coverage": 2, "mark_failed_page": 1},
        "by_severity": {"warning": 2, "error": 1},
    }


def test_detect_page_suspects_from_blocks_include_stable_id_and_op_payload():
    page_ir = build_page_ir(
        "### Formula\n"
        "\\frac a}{b\n\n"
        "### Table Analysis\n"
        "| A | B |\n"
        "| --- | --- |\n"
        "| 1 | 2 | 3 |",
        4,
    )

    suspects = detect_page_suspects(slide_no=4, blocks=page_ir["blocks"])

    formula = next(suspect for suspect in suspects if suspect["code"] == "latex_frac_missing_braces")
    table = next(suspect for suspect in suspects if suspect["code"] == "table_quality_warning")
    assert formula["block_id"] == "p0004-b001"
    assert formula["op"] == {"op": "mark_uncertain", "id": "p0004-b001"}
    assert table["block_id"] == "p0004-b002"
    assert table["op"] == {"op": "mark_uncertain", "id": "p0004-b002"}
