from ppt2md_app.detect import detect_page_suspects, summarize_suspects


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
        {"suspects": [{"code": "ocr_coverage_low", "severity": "warning"}]},
        {"suspects": [{"code": "ocr_coverage_low", "severity": "warning"}, {"code": "stage2_failed", "severity": "error"}]},
    ]

    summary = summarize_suspects(pages)

    assert summary == {
        "total": 3,
        "by_code": {"ocr_coverage_low": 2, "stage2_failed": 1},
        "by_severity": {"warning": 2, "error": 1},
    }
