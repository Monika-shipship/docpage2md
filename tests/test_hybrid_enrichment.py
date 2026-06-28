import json
import threading
import time
from pathlib import Path

from PIL import Image

from docpage2md_app.artifacts import sha256_text
from docpage2md_app.config import AppConfig
from docpage2md_app import hybrid_enrichment
from docpage2md_app.hybrid_enrichment import _brain_op_audit, _brain_ops_prompt, default_brain_backend, enrich_mineru_document_ir
from docpage2md_app.ir import PAGE_IR_SCHEMA_VERSION
from docpage2md_app.renderer import render_page_ir_to_markdown


def test_hybrid_enrichment_applies_crop_vision_and_checked_brain_ops(tmp_path):
    output_root = tmp_path / "HybridDoc"
    crop_dir = output_root / "assets" / "crops"
    crop_dir.mkdir(parents=True)
    (crop_dir / "figure.jpg").write_bytes(b"fake figure")
    (crop_dir / "formula.jpg").write_bytes(b"fake formula")

    document_ir = _document_ir(
        [
            _block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr"),
            _block("p0001-b002", "figure_note", "", crop_ref="assets/crops/figure.jpg", origin="vision_description"),
            _block(
                "p0001-b003",
                "formula_block",
                "\\begin{aligned}\nS &= k(\\ln Z+\\beta U) \\tag{5}\n\\end{aligned}",
                crop_ref="assets/crops/formula.jpg",
                origin="vision_formula",
            ),
        ]
    )

    def vision_backend(page_ir, block, image_path: Path | None, config):
        assert image_path and image_path.exists()
        if block["type"] == "figure_note":
            return {
                "success": True,
                "description": "手绘坐标图，横轴为 t，纵轴为 x，曲线随时间上升。",
                "figure_type": "coordinate_plot",
                "labels": ["t", "x"],
                "usage": {"prompt_tokens": 3, "completion_tokens": 5},
                "request_id": "vision-1",
            }
        return {
            "success": True,
            "latex": "\\begin{aligned}\nS &= k(\\ln Z+\\beta U) \\tag{5}\n\\end{aligned}",
            "usage": {"prompt_tokens": 2, "completion_tokens": 4},
        }

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                    "current_text": "配分函教",
                    "suggested_text": "配分函数",
                    "confidence": 0.91,
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.91,
                    "reason": "上下文显示为配分函数。",
                }
            ],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7},
            "request_id": "brain-1",
            "reasoning": "this private reasoning must not be persisted",
        }

    result = enrich_mineru_document_ir(
        document_ir,
        AppConfig(engine_mode="hybrid"),
        output_root=output_root,
        vision_backend=vision_backend,
        brain_backend=brain_backend,
    )

    page = result["document_ir"]["pages"][0]
    markdown = render_page_ir_to_markdown(page, 1)

    assert page["blocks"][0]["text"] == "配分函数为 Z。"
    assert page["blocks"][0]["origin"] == "brain_refine"
    assert page["blocks"][1]["figure"]["figure_type"] == "coordinate_plot"
    assert "横轴为 t" in markdown
    assert "\\tag{5}\n\\end{aligned}" not in markdown
    assert "\\end{aligned}\n\\tag{5}" in markdown
    assert result["pages"][1]["brain"]["ops_applied"] == 1
    assert result["pages"][1]["brain"]["brain_discovered_count"] == 1
    assert result["pages"][1]["op_audit"][0]["op"] == "replace_text_span_checked"
    assert result["pages"][1]["op_audit"][0]["decision"] == "brain_discovered"
    assert "private reasoning" not in json.dumps(result, ensure_ascii=False)


def test_default_brain_backend_retries_empty_or_invalid_json(monkeypatch):
    page = _document_ir([_block("p0001-b001", "paragraph", "正文。", origin="vision_ocr")])["pages"][0]
    calls = iter(
        [
            {"content": "not json", "reasoning": "hidden first reasoning"},
            {"content": '{"decisions": [], "new_findings": [], "op_candidates": [], "warnings": []}', "usage": {"prompt_tokens": 2, "completion_tokens": 1}},
        ]
    )

    monkeypatch.setenv("DEEPSEEK_API_KEY", "test-key")
    monkeypatch.setattr(hybrid_enrichment, "_call_brain_model", lambda prompt, config: next(calls))

    result = default_brain_backend(page, [page], AppConfig(engine_mode="hybrid"))

    assert result["success"] is True
    assert result["retry_count"] == 1
    assert result["op_candidates"] == []
    assert "hidden first reasoning" not in json.dumps(result, ensure_ascii=False)


def test_hybrid_enrichment_runs_vision_and_brain_in_parallel(tmp_path):
    output_root = tmp_path / "HybridDoc"
    crop_dir = output_root / "assets" / "crops"
    crop_dir.mkdir(parents=True)
    for index in range(1, 5):
        (crop_dir / f"formula-{index}.jpg").write_bytes(b"fake formula")

    document_ir = _document_ir_pages(
        [
            [_block("p0001-b001", "formula_block", "x_1", crop_ref="assets/crops/formula-1.jpg", origin="vision_formula")],
            [_block("p0002-b001", "formula_block", "x_2", crop_ref="assets/crops/formula-2.jpg", origin="vision_formula", source_page=2)],
            [_block("p0003-b001", "formula_block", "x_3", crop_ref="assets/crops/formula-3.jpg", origin="vision_formula", source_page=3)],
            [_block("p0004-b001", "formula_block", "x_4", crop_ref="assets/crops/formula-4.jpg", origin="vision_formula", source_page=4)],
        ]
    )
    vision_counter = _ConcurrencyCounter()
    brain_counter = _ConcurrencyCounter()

    def vision_backend(page_ir, block, image_path: Path | None, config):
        with vision_counter:
            time.sleep(0.02)
            return {"success": True, "latex": block["text"]}

    def brain_backend(page_ir, context_pages, config):
        assert len(context_pages) >= 3
        with brain_counter:
            time.sleep(0.02)
            return {"success": True, "decisions": [], "new_findings": [], "op_candidates": []}

    result = enrich_mineru_document_ir(
        document_ir,
        AppConfig(engine_mode="hybrid", vision_batch_workers=4, brain_batch_workers=4),
        output_root=output_root,
        vision_backend=vision_backend,
        brain_backend=brain_backend,
    )

    assert vision_counter.max_active > 1
    assert brain_counter.max_active > 1
    assert result["summary"]["pages"]["page_count"] == 4


def test_hybrid_enrichment_sends_expanded_crop_to_vision_backend(tmp_path):
    output_root = tmp_path / "HybridDoc"
    page_dir = output_root / "assets" / "pages"
    crop_dir = output_root / "assets" / "crops"
    page_dir.mkdir(parents=True)
    crop_dir.mkdir(parents=True)
    Image.new("RGB", (400, 400), "white").save(page_dir / "page-1.png")
    Image.new("RGB", (30, 20), "white").save(crop_dir / "formula.jpg")
    document_ir = _document_ir(
        [_block("p0001-b001", "formula_block", "x=", crop_ref="assets/crops/formula.jpg", origin="vision_formula")]
    )
    page = document_ir["pages"][0]
    page["page_image_ref"] = "assets/pages/page-1.png"
    page["page_size"] = [100, 100]
    page["blocks"][0]["bbox"] = [40, 40, 60, 48]
    seen_paths: list[Path] = []

    def vision_backend(page_ir, block, image_path: Path | None, config):
        assert image_path and image_path.exists()
        seen_paths.append(image_path)
        assert ".vision_crop_cache" in image_path.parts
        assert image_path.name != "formula.jpg"
        return {"success": True, "latex": "x=1"}

    result = enrich_mineru_document_ir(
        document_ir,
        AppConfig(engine_mode="hybrid", document_type="handwritten_notes"),
        output_root=output_root,
        vision_backend=vision_backend,
        brain_backend=lambda page_ir, context_pages, config: {"success": True, "decisions": [], "new_findings": [], "op_candidates": []},
    )

    report = result["pages"][1]["vision"]["blocks"][0]
    evidence = result["document_ir"]["pages"][0]["blocks"][0]["evidence"]["vision_enrichment"]
    assert seen_paths
    assert report["crop"]["crop_strategy"] == "expanded_from_page_image"
    assert report["crop"]["padding_profile"] == "handwritten"
    assert evidence["crop"]["expanded_bbox"]
    assert not (output_root / ".vision_crop_cache").exists()


def test_hybrid_enrichment_retries_formula_crop_when_vision_returns_empty_latex(tmp_path):
    output_root = tmp_path / "HybridDoc"
    page_dir = output_root / "assets" / "pages"
    crop_dir = output_root / "assets" / "crops"
    page_dir.mkdir(parents=True)
    crop_dir.mkdir(parents=True)
    Image.new("RGB", (500, 500), "white").save(page_dir / "page-1.png")
    Image.new("RGB", (30, 20), "white").save(crop_dir / "formula.jpg")
    document_ir = _document_ir(
        [_block("p0001-b001", "formula_block", "", crop_ref="assets/crops/formula.jpg", origin="vision_formula")]
    )
    page = document_ir["pages"][0]
    page["page_image_ref"] = "assets/pages/page-1.png"
    page["page_size"] = [100, 100]
    page["blocks"][0]["bbox"] = [35, 35, 65, 45]
    calls: list[Path] = []

    def vision_backend(page_ir, block, image_path: Path | None, config):
        assert image_path and image_path.exists()
        calls.append(image_path)
        if len(calls) == 1:
            return {"success": True, "latex": ""}
        return {"success": True, "latex": "E=mc^2"}

    result = enrich_mineru_document_ir(
        document_ir,
        AppConfig(engine_mode="hybrid", document_type="handwritten_notes"),
        output_root=output_root,
        vision_backend=vision_backend,
        brain_backend=lambda page_ir, context_pages, config: {"success": True, "decisions": [], "new_findings": [], "op_candidates": []},
    )

    block = result["document_ir"]["pages"][0]["blocks"][0]
    report = result["pages"][1]["vision"]["blocks"][0]
    assert len(calls) == 2
    assert block["latex"] == "E=mc^2"
    assert report["retry_count"] == 1
    assert report["crop"]["render_dpi"] == 400
    assert report["crop"]["padding_profile"] == "aggressive"
    assert report["crop_attempts"][1]["retry_reason"] == "formula_empty"


def test_brain_context_window_uses_configured_radius(tmp_path):
    output_root = tmp_path / "HybridDoc"
    document_ir = _document_ir_pages(
        [
            [_block("p0001-b001", "formula_inline", "x_1", origin="vision_ocr")],
            [_block("p0002-b001", "formula_inline", "x_2", origin="vision_ocr", source_page=2)],
            [_block("p0003-b001", "formula_inline", "x_3", origin="vision_ocr", source_page=3)],
            [_block("p0004-b001", "formula_inline", "x_4", origin="vision_ocr", source_page=4)],
            [_block("p0005-b001", "formula_inline", "x_5", origin="vision_ocr", source_page=5)],
        ]
    )
    seen_windows: dict[int, list[int]] = {}

    def brain_backend(page_ir, context_pages, config):
        seen_windows[int(page_ir["source_page"])] = [int(page["source_page"]) for page in context_pages]
        return {"success": True, "decisions": [], "new_findings": [], "op_candidates": []}

    enrich_mineru_document_ir(
        document_ir,
        AppConfig(engine_mode="hybrid", brain_context_radius=1),
        output_root=output_root,
        vision_backend=lambda page_ir, block, image_path, config: {"success": True},
        brain_backend=brain_backend,
    )

    assert seen_windows[1] == [1, 2]
    assert seen_windows[3] == [2, 3, 4]
    assert seen_windows[5] == [4, 5]


def test_brain_prompt_keeps_target_detail_and_compresses_neighbors():
    long_neighbor = "邻页上下文" * 300
    long_target = "目标页正文" * 300
    document_ir = _document_ir_pages(
        [
            [_block("p0001-b001", "paragraph", long_neighbor, origin="vision_ocr")],
            [_block("p0002-b001", "paragraph", long_target, origin="vision_ocr", source_page=2)],
            [_block("p0003-b001", "paragraph", long_neighbor, origin="vision_ocr", source_page=3)],
        ]
    )

    prompt = _brain_ops_prompt(document_ir["pages"][1], document_ir["pages"])

    assert '"role": "target"' in prompt
    assert '"role": "neighbor"' in prompt
    assert "initial_findings" in prompt
    assert "priority_blocks" in prompt
    assert "不能自由重写整页" in prompt
    assert "decision" in prompt
    assert long_target[:400] in prompt
    assert long_neighbor not in prompt


def test_brain_prompt_includes_dual_and_vision_findings():
    page_ir = {
        "schema_version": PAGE_IR_SCHEMA_VERSION,
        "source_page": 1,
        "raw_text": "MinerU 与 PaddleOCR 候选不一致。",
        "blocks": [
            {
                "id": "p0001-b001",
                "type": "paragraph",
                "text": "李群",
                "confidence": 0.68,
                "evidence": {
                    "fusion": {"group_id": "p0001-g001"},
                    "vision_enrichment": {
                        "changed_fields": ["text"],
                        "original_text": "李君羊",
                        "result_text": "李群",
                    },
                },
            }
        ],
        "fusion": {
            "candidate_groups": [
                {
                    "group_id": "p0001-g001",
                    "type_hint": "paragraph",
                    "match_reason": "bbox_overlap",
                    "warnings": ["candidate_text_conflict"],
                    "candidates": [
                        {"source": "mineru", "block_id": "m1", "type": "paragraph", "text": "李君羊", "confidence": 0.62},
                        {"source": "paddleocr", "block_id": "p1", "type": "paragraph", "text": "李群", "confidence": 0.74},
                    ],
                }
            ]
        },
        "dual_evidence": {
            "mineru": {"available": True, "raw_text": "李君羊", "blocks": []},
            "paddleocr": {"available": True, "raw_text": "李群", "blocks": []},
        },
    }

    prompt = _brain_ops_prompt(page_ir, [page_ir])

    assert "dual_engine_diff" in prompt
    assert "vision_crop_evidence" in prompt
    assert "ocr_text_conflict" in prompt
    assert "李君羊" in prompt


def test_brain_audit_keeps_contract_errors_and_payload_summary():
    audit = _brain_op_audit(
        {
            "op": "replace_text_span_checked",
            "id": "p0001-b001",
            "old_text": "错字",
            "new_text": "正字",
            "field": "text",
            "decision": "finding_confirmed",
            "finding_id": "p0001-f001",
            "evidence_type": "finding",
            "confidence": 0.9,
        },
        "rejected",
        {"reason": "page_ir_contract_failed", "errors": ["block_2_unknown_origin"]},
    )

    assert audit["errors"] == ["block_2_unknown_origin"]
    assert audit["decision"] == "finding_confirmed"
    assert audit["finding_id"] == "p0001-f001"
    assert audit["op_payload_summary"]["old_text_sha256"]
    assert audit["old_text_preview"] == "错字"
    assert audit["new_text_preview"] == "正字"


def test_brain_ops_inherit_missing_evidence_policy_fields_in_aggressive_mode():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                    "message": "上下文显示这里应为配分函数。",
                    "evidence": {
                        "current_text": "配分函教",
                        "token": "fake_test_token_1234567890abcdef1234567890abcdef",
                    },
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "confidence": 0.91,
                    "reason": "上下文显示为配分函数。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_applied"] == 1
    assert report["ops_rejected"] == 0
    assert report["repair_successes"] == 1
    audit = report["op_audit"][0]
    assert audit["status"] == "repaired_applied"
    assert audit["evidence_type"] == "context"
    assert "inherit_evidence_type_from_finding" in audit["repair_actions"]
    assert audit["old_text_preview"] == "配分函教"
    assert audit["new_text_preview"] == "配分函数"
    assert audit["current_text_preview"] == "配分函教为 Z。"
    assert audit["reason_preview"] == "上下文显示为配分函数。"
    assert audit["finding_message_preview"] == "上下文显示这里应为配分函数。"
    assert "配分函教" in audit["finding_evidence_preview"]
    assert "fake_test_token" not in audit["finding_evidence_preview"]
    assert audit["target_block_type"] == "paragraph"
    assert audit["target_block_origin"] == "vision_ocr"
    assert audit["target_block_confidence"] == 0.75


def test_brain_ops_conservative_mode_still_rejects_missing_evidence_policy_fields():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                    "message": "上下文显示这里应为配分函数。",
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "confidence": 0.91,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(
        page,
        [page],
        AppConfig(engine_mode="hybrid", brain_op_review_mode="conservative"),
        brain_backend,
    )

    assert refined["blocks"][0]["text"] == "配分函教为 Z。"
    assert report["ops_rejected"] == 1
    assert report["op_audit"][0]["status"] == "hard_rejected"
    assert report["op_audit"][0]["reason"] == "brain_op_missing_evidence_type"


def test_brain_audit_previews_redact_secrets_and_truncate_middle():
    secret = "sk-" + "a" * 60
    audit = _brain_op_audit(
        {
            "op": "replace_text_span_checked",
            "id": "p0001-b001",
            "old_text": f"开头 api_key={secret} 结尾",
            "new_text": "新文本" * 120,
            "field": "text",
            "decision": "finding_confirmed",
            "finding_id": "p0001-f001",
            "evidence_type": "finding",
            "confidence": 0.9,
            "reason": "因为上下文一致。" * 30,
        },
        "rejected",
        {"reason": "old_text_not_found"},
    )

    encoded = json.dumps(audit, ensure_ascii=False)
    assert secret not in encoded
    assert "[REDACTED" in encoded
    assert audit["new_text_preview"].startswith("新文本")
    assert "..." in audit["new_text_preview"]
    assert "..." in audit["reason_preview"]


def test_brain_ops_accept_block_id_alias_for_checked_op():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "block_id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.91,
                    "reason": "上下文显示为配分函数。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_applied"] == 1
    assert report["op_audit"][0]["target_block_ids"] == ["p0001-b001"]


def test_brain_ops_accept_new_finding_id_alias_for_brain_discovered_op():
    page = _document_ir([_block("p0001-b001", "paragraph", "在之余中", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "new_finding_id": "p0001-nf001",
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "block_id": "p0001-b001",
                    "old_text": "在之余中",
                    "new_text": "在$\\Sigma$系中",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-nf001",
                    "evidence_type": "context",
                    "confidence": 0.91,
                    "reason": "上下文显示为 Sigma 系。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "在$\\Sigma$系中"
    assert report["ops_applied"] == 1
    audit = report["op_audit"][0]
    assert audit["resolved_new_finding_id"] == "p0001-nf001"
    assert audit["resolved_finding_id"] == "p0001-bf001"
    assert audit["old_text_preview"] == "在之余中"
    assert audit["new_text_preview"] == "在$\\Sigma$系中"
    assert audit["current_text_preview"] == "在之余中"


def test_brain_ops_accept_finding_id_alias_for_brain_discovered_op():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "new_finding_id": "p0001-nf001",
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "block_id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.91,
                    "reason": "上下文显示为配分函数。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_applied"] == 1
    audit = report["op_audit"][0]
    assert audit["resolved_new_finding_id"] == "p0001-nf001"
    assert audit["resolved_finding_id"] == "p0001-bf001"


def test_brain_ops_repair_unknown_new_finding_alias_when_text_evidence_matches():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "new_finding_id": "p0001-nf001",
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                    "current_text": "配分函教",
                    "suggested_text": "配分函数",
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "block_id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-missing",
                    "evidence_type": "context",
                    "confidence": 0.91,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_applied"] == 1
    audit = report["op_audit"][0]
    assert audit["status"] == "repaired_applied"
    assert "repair_unknown_new_finding_id" in audit["repair_actions"]
    assert audit["resolved_new_finding_id"] == "p0001-nf001"
    assert audit["resolved_finding_id"] == "p0001-bf001"


def test_brain_ops_reject_unknown_new_finding_alias_with_detail():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [
                {
                    "new_finding_id": "p0001-nf001",
                    "finding_id": "p0001-bf001",
                    "page": 1,
                    "block_id": "p0001-b001",
                    "kind": "contextual_ocr_error",
                }
            ],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "block_id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-missing",
                    "evidence_type": "context",
                    "confidence": 0.91,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函教为 Z。"
    assert report["ops_rejected"] == 1
    audit = report["op_audit"][0]
    assert audit["reason"] == "brain_op_unknown_new_finding_reference"
    assert audit["policy_error_detail"]["provided_new_finding_id"] == "p0001-missing"
    assert "p0001-nf001" in audit["policy_error_detail"]["known_aliases_sample"]


def test_brain_ops_allow_low_confidence_exact_short_span_in_aggressive_mode():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.61,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_applied"] == 1
    assert report["op_audit"][0]["match_strategy"] == "exact"


def test_brain_ops_reject_low_confidence_replace_in_conservative_mode():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.61,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(
        page,
        [page],
        AppConfig(engine_mode="hybrid", brain_op_review_mode="conservative"),
        brain_backend,
    )

    assert refined["blocks"][0]["text"] == "配分函教为 Z。"
    assert report["ops_rejected"] == 1
    assert report["op_audit"][0]["status"] == "soft_rejected"
    assert report["op_audit"][0]["reason"] == "brain_op_low_confidence_replace"


def test_brain_ops_repair_old_text_whitespace_mismatch():
    page = _document_ir([_block("p0001-b001", "paragraph", "配 分 函 数为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函数",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.88,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    audit = report["op_audit"][0]
    assert audit["status"] == "repaired_applied"
    assert audit["match_strategy"] == "compact_whitespace"
    assert "repair_old_text_span" in audit["repair_actions"]


def test_brain_ops_repair_old_text_unicode_width_mismatch():
    page = _document_ir([_block("p0001-b001", "paragraph", "ＡＢＣ 表示常数。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "unicode_width"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "ABC",
                    "new_text": "ABC",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.9,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "ABC 表示常数。"
    assert report["op_audit"][0]["match_strategy"] == "compact_whitespace"


def test_brain_ops_extract_json_formula_payload_to_latex():
    json_formula = '```json\n{"latex":"E = mc^2","description":"formula"}\n```'
    page = _document_ir([_block("p0001-b001", "formula_block", json_formula, origin="vision_formula")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "formula_json_payload"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": json_formula,
                    "new_text": "E = mc^2",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "validator",
                    "confidence": 0.96,
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "E = mc^2"
    assert refined["blocks"][0]["latex"] == "E = mc^2"
    assert report["ops_applied"] == 1
    audit = report["op_audit"][0]
    assert audit["reason"] != "brain_op_whole_markdown_rewrite"
    assert audit["match_strategy"] == "structured_formula_payload"


def test_brain_ops_classify_redundant_noops_as_superseded():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函数为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.9,
                },
                {
                    "op": "mark_uncertain",
                    "id": "p0001-b001",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.9,
                },
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函数为 Z。"
    assert report["ops_rejected"] == 0
    assert report["noop_or_superseded"] == 2
    assert report["op_audit"][0]["status"] == "superseded_noop"
    assert report["op_audit"][0]["reason"] == "replacement_same_as_current"
    assert report["op_audit"][1]["status"] == "superseded_noop"
    assert report["op_audit"][1]["reason"] == "mark_uncertain_superseded_by_fix"


def test_legacy_brain_ops_are_audited_and_rejected_without_required_schema():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "ops": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "配分函数",
                    "field": "text",
                    "reason": "旧格式缺少 finding/decision/evidence/confidence。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函教为 Z。"
    assert report["ops_requested"] == 1
    assert report["ops_rejected"] == 1
    assert report["op_audit"][0]["reason"] == "brain_op_missing_or_invalid_decision"


def test_brain_ops_reject_whole_markdown_rewrite():
    page = _document_ir([_block("p0001-b001", "paragraph", "配分函教为 Z。", origin="vision_ocr")])["pages"][0]

    def brain_backend(page_ir, context_pages, config):
        return {
            "success": True,
            "new_findings": [{"finding_id": "p0001-bf001", "page": 1, "block_id": "p0001-b001", "kind": "contextual_ocr_error"}],
            "op_candidates": [
                {
                    "op": "replace_text_span_checked",
                    "id": "p0001-b001",
                    "old_text": "配分函教",
                    "new_text": "# Slide 1\n\n配分函数为 Z。",
                    "field": "text",
                    "decision": "brain_discovered",
                    "new_finding_id": "p0001-bf001",
                    "evidence_type": "context",
                    "confidence": 0.95,
                    "reason": "模拟整页 Markdown 改写。",
                }
            ],
        }

    refined, report = hybrid_enrichment._run_brain_ops(page, [page], AppConfig(engine_mode="hybrid"), brain_backend)

    assert refined["blocks"][0]["text"] == "配分函教为 Z。"
    assert report["ops_rejected"] == 1
    assert report["op_audit"][0]["reason"] == "brain_op_whole_markdown_rewrite"


def _document_ir(blocks):
    return _document_ir_pages([blocks])


def _document_ir_pages(pages_blocks):
    pages = []
    for page_index, blocks in enumerate(pages_blocks, start=1):
        raw_text = "\n\n".join(block.get("text") or block.get("description") or "" for block in blocks)
        for block in blocks:
            block["source_page"] = page_index
        pages.append(
            {
                "schema_version": PAGE_IR_SCHEMA_VERSION,
                "source_page": page_index,
                "page_image_ref": None,
                "raw_text": raw_text,
                "raw_text_sha256": sha256_text(raw_text),
                "blocks": blocks,
                "mineru": {"page_idx": page_index - 1, "page_size": [100, 100], "artifact_refs": {}},
            }
        )
    return {
        "schema_version": "docpage2md-docir-v1",
        "engine_mode": "hybrid",
        "source": {"input_path": "notes.pdf", "input_type": "pdf"},
        "pages": pages,
        "assets": [],
        "metadata": {},
    }


def _block(block_id, block_type, text, *, crop_ref=None, origin, source_page=1):
    block = {
        "id": block_id,
        "type": block_type,
        "text": text,
        "source_page": source_page,
        "confidence": 0.75,
        "origin": origin,
        "source_engine": "mineru",
        "evidence": {"raw_text": text, "provider": "mineru"},
        "bbox": None,
    }
    if crop_ref:
        block["crop_ref"] = crop_ref
        block["image_ref"] = crop_ref
    if block_type == "formula_block":
        block["latex"] = text
        block["raw_text"] = text
    return block


class _ConcurrencyCounter:
    def __init__(self):
        self.lock = threading.Lock()
        self.active = 0
        self.max_active = 0

    def __enter__(self):
        with self.lock:
            self.active += 1
            self.max_active = max(self.max_active, self.active)

    def __exit__(self, *_exc):
        with self.lock:
            self.active -= 1
