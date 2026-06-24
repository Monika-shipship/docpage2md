from docpage2md_app.invariant import page_ir_contract_errors, valid_block_id, valid_source_page
from docpage2md_app.ir import build_page_ir


def test_page_ir_contract_accepts_generated_ir():
    page_ir = build_page_ir("标题:\n\n正文。", 1)

    assert page_ir_contract_errors(page_ir, expected_slide_no=1) == []


def test_page_ir_contract_reports_slide_and_block_errors():
    page_ir = build_page_ir("标题:\n\n正文。", 2)
    page_ir["source_page"] = 3
    page_ir["blocks"][0]["source_page"] = 4
    page_ir["blocks"][1]["id"] = "p0002-b001"
    page_ir["blocks"].append({**page_ir["blocks"][1]})

    errors = page_ir_contract_errors(page_ir, expected_slide_no=2)

    assert "source_page_mismatch" in errors
    assert "block_0_invalid_id" in errors
    assert "block_0_source_page_mismatch" in errors
    assert "block_1_invalid_id" in errors
    assert "block_1_source_page_mismatch" in errors
    assert "block_2_invalid_id" in errors
    assert "block_2_duplicate_id" in errors


def test_page_ir_contract_reports_non_dict_block():
    page_ir = build_page_ir("正文。", 3)
    page_ir["blocks"].append("bad block")

    errors = page_ir_contract_errors(page_ir, expected_slide_no=3)

    assert "block_1_not_dict" in errors


def test_valid_source_page_and_block_id_reject_bools_and_cross_page_ids():
    assert valid_source_page(1) is True
    assert valid_source_page(True) is False
    assert valid_source_page(0) is False
    assert valid_block_id("p0001-b001", 1) is True
    assert valid_block_id("p0002-b001", 1) is False
