from docpage2md_app.detect import build_initial_findings_pool, summarize_findings
from docpage2md_app.ir import build_page_ir


def test_build_initial_findings_pool_from_validation_quality_and_stage_state():
    findings = build_initial_findings_pool(
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

    assert [finding["finding_id"] for finding in findings] == ["p0002-f001", "p0002-f002", "p0002-f003"]
    assert [finding["source"] for finding in findings] == ["deterministic_detector", "validator_precheck", "deterministic_detector"]
    assert [finding["op_hint"] for finding in findings] == [
        "mark_failed_page",
        "inspect_ocr_coverage",
        "mark_uncertain",
    ]


def test_summarize_findings_counts_codes_and_severity():
    pages = [
        {"findings": {"initial": [{"kind": "ocr_coverage_low", "severity": "warning", "op_hint": "inspect_ocr_coverage", "source": "validator_precheck"}]}},
        {
            "findings": {
                "initial": [
                    {"kind": "ocr_coverage_low", "severity": "warning", "op_hint": "inspect_ocr_coverage", "source": "validator_precheck"},
                    {"kind": "stage2_failed", "severity": "error", "op": {"op": "mark_failed_page"}, "source": "deterministic_detector"},
                ]
            }
        },
    ]

    summary = summarize_findings(pages)

    assert summary == {
        "total": 3,
        "actionable_total": 3,
        "by_code": {"ocr_coverage_low": 2, "stage2_failed": 1},
        "by_kind": {"ocr_coverage_low": 2, "stage2_failed": 1},
        "by_source": {"validator_precheck": 2, "deterministic_detector": 1},
        "by_op": {"inspect_ocr_coverage": 2, "mark_failed_page": 1},
        "by_severity": {"warning": 2, "error": 1},
    }


def test_build_initial_findings_pool_from_blocks_include_stable_id_and_op_payload():
    page_ir = build_page_ir(
        "### Formula\n"
        "\\frac a}{b\n\n"
        "### Table Analysis\n"
        "| A | B |\n"
        "| --- | --- |\n"
        "| 1 | 2 | 3 |",
        4,
    )

    findings = build_initial_findings_pool(slide_no=4, blocks=page_ir["blocks"])

    formula = next(finding for finding in findings if finding["kind"] == "latex_frac_missing_braces")
    table = next(finding for finding in findings if finding["kind"] == "table_quality_warning")
    assert formula["block_id"] == "p0004-b001"
    assert formula["op"] == {"op": "mark_uncertain", "id": "p0004-b001"}
    assert table["block_id"] == "p0004-b002"
    assert table["op"] == {"op": "mark_uncertain", "id": "p0004-b002"}


def test_build_initial_findings_pool_from_dual_engine_candidate_conflict():
    page_ir = {
        "source_page": 7,
        "blocks": [
            {
                "id": "p0007-b001",
                "type": "paragraph",
                "text": "李群是群论中的基本对象。",
                "evidence": {"fusion": {"group_id": "p0007-g001"}},
                "confidence": 0.61,
            }
        ],
        "fusion": {
            "candidate_groups": [
                {
                    "group_id": "p0007-g001",
                    "type_hint": "paragraph",
                    "match_reason": "bbox_overlap",
                    "match_score": 0.78,
                    "warnings": ["candidate_text_conflict"],
                    "candidates": [
                        {
                            "candidate_id": "mineru:p0007-m001",
                            "source": "mineru",
                            "block_id": "p0007-m001",
                            "type": "paragraph",
                            "text": "李君羊是群论中的基本对象。",
                            "confidence": 0.6,
                            "quality_score": 0.58,
                            "warnings": [],
                        },
                        {
                            "candidate_id": "paddleocr:p0007-p001",
                            "source": "paddleocr",
                            "block_id": "p0007-p001",
                            "type": "paragraph",
                            "text": "李群是群论中的基本对象。",
                            "confidence": 0.74,
                            "quality_score": 0.7,
                            "warnings": [],
                        },
                    ],
                }
            ]
        },
    }

    findings = build_initial_findings_pool(slide_no=7, page_ir=page_ir)

    conflict = next(finding for finding in findings if finding["source"] == "dual_engine_diff")
    assert conflict["kind"] == "ocr_text_conflict"
    assert conflict["block_id"] == "p0007-b001"
    assert conflict["op_hint"] == "replace_text_span_checked"
    assert [candidate["source"] for candidate in conflict["candidates"]] == ["mineru", "paddleocr"]


def test_build_initial_findings_pool_from_vision_crop_evidence():
    page_ir = {
        "source_page": 8,
        "blocks": [
            {
                "id": "p0008-b001",
                "type": "formula_block",
                "text": "\\theta = \\omega t",
                "latex": "\\theta = \\omega t",
                "confidence": 0.68,
                "source_engine": "vision",
                "evidence": {
                    "vision_enrichment": {
                        "changed_fields": ["text", "latex"],
                        "original_text": "θ = ωt",
                        "result_text": "\\theta = \\omega t",
                        "content_sha256": "abc",
                    }
                },
            }
        ],
    }

    findings = build_initial_findings_pool(slide_no=8, page_ir=page_ir)

    vision = next(finding for finding in findings if finding["source"] == "vision_crop_evidence")
    assert vision["kind"] == "vision_crop_low_confidence"
    assert vision["block_id"] == "p0008-b001"
    assert vision["candidates"][0]["source"] == "pre_vision_ocr"
    assert vision["candidates"][1]["source"] == "vision_crop"
