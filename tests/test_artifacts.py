from ppt2md_app.artifacts import (
    build_fail_open_slide_meta,
    build_raw_cache_record,
    build_slide_meta,
    stage1_fingerprint,
    stage2_fingerprint,
    validate_raw_cache_record,
    validate_slide_meta,
)
from ppt2md_app.config import AppConfig


def test_legacy_raw_cache_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    fingerprint = stage1_fingerprint(image, AppConfig())

    valid, reason = validate_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "old"}, 1, fingerprint)

    assert not valid
    assert reason == "legacy_miss"


def test_raw_cache_hits_only_when_fingerprint_matches(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig(model_vision="qwen3-vl-plus")
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    fingerprint = stage1_fingerprint(image, config)

    assert record["page_ir"]["source_page"] == 1
    assert record["page_image_ref"] == str(image)
    assert record["metadata"]["page_image_ref"] == str(image)
    assert record["page_ir"]["page_image_ref"] == str(image)
    assert record["page_ir"]["raw_text"] == "raw text"
    assert record["page_ir"]["raw_text_sha256"] == record["raw_text_sha256"]
    assert record["blocks"][0]["id"] == "p0001-b001"
    assert record["block_refiner"]["version"].startswith("block-refiner-")
    assert record["block_refiner"]["changed"] is False
    assert record["provenance"]["schema_version"] == 3
    assert record["provenance"]["entries"][0]["origin"] == "renderer_template"
    assert record["provenance"]["entries"][1]["id"] == "p0001-b001"
    assert record["provenance"]["entries"][1]["origin"] == "vision_ocr"
    assert record["provenance"]["entries"][1]["page_image_ref"] == str(image)
    assert record["provenance"]["summary"]["origin_counts"] == {"renderer_template": 1, "vision_ocr": 1}
    assert record["provenance"]["summary"]["visual_evidence_count"] == 1
    assert record["ocr_confusion"]["enabled"] is False
    assert record["ocr_confusion"]["status"] == "disabled"

    valid, reason = validate_raw_cache_record(record, 1, fingerprint)
    assert valid
    assert reason == "hit"

    other_fingerprint = stage1_fingerprint(image, AppConfig(model_vision="qwen3-vl-max"))
    valid, reason = validate_raw_cache_record(record, 1, other_fingerprint)
    assert not valid
    assert reason == "invalid"


def test_raw_cache_fingerprint_includes_ocr_confusion_flag(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")

    off = stage1_fingerprint(image, AppConfig(fix_ocr_confusion=False))
    on = stage1_fingerprint(image, AppConfig(fix_ocr_confusion=True))

    assert off["processing"] == {"fix_ocr_confusion": False}
    assert on["processing"] == {"fix_ocr_confusion": True}
    assert off != on


def test_raw_cache_applies_ocr_confusion_only_when_enabled(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")

    off = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "x＝１"}, image, AppConfig())
    on = build_raw_cache_record(
        {"success": True, "slide_no": 1, "raw_text": "x＝１"},
        image,
        AppConfig(fix_ocr_confusion=True),
    )

    assert off["raw_text"] == "x＝１"
    assert off["ocr_confusion"]["status"] == "disabled"
    assert on["raw_text"] == "x=1"
    assert on["ocr_confusion"]["status"] == "applied"
    assert on["ocr_confusion"]["replacement_count"] == 2


def test_raw_cache_without_blocks_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    del record["blocks"]

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_raw_cache_with_top_level_blocks_mismatch_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    record["blocks"] = []

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_raw_cache_with_invalid_page_ir_contract_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    del record["page_ir"]["blocks"][0]["evidence"]

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_raw_cache_without_block_refiner_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    del record["block_refiner"]

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_raw_cache_without_provenance_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    del record["provenance"]

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_raw_cache_with_page_ir_raw_text_mismatch_does_not_hit(tmp_path):
    image = tmp_path / "page.png"
    image.write_bytes(b"fake image")
    config = AppConfig()
    record = build_raw_cache_record({"success": True, "slide_no": 1, "raw_text": "raw text"}, image, config)
    record["page_ir"]["raw_text"] = "different raw"

    valid, reason = validate_raw_cache_record(record, 1, stage1_fingerprint(image, config))

    assert not valid
    assert reason == "invalid"


def test_slide_meta_records_brain_markdown_source():
    config = AppConfig()
    raw_data_map = {1: "raw"}
    markdown = "# Slide 1\n\nraw\n"
    meta = build_slide_meta(1, markdown, {"ok": True, "errors": [], "warnings": []}, raw_data_map, config)

    assert meta["schema_version"] == 2
    assert meta["markdown_source"] == {
        "kind": "brain_refine",
        "source": "stage2_brain",
        "refiner_changed": False,
    }
    valid, reason = validate_slide_meta(meta, 1, markdown, stage2_fingerprint(1, raw_data_map, config))
    assert valid
    assert reason == "hit"


def test_fail_open_slide_meta_records_page_ir_markdown_source():
    config = AppConfig()
    raw_data_map = {1: "raw"}
    markdown = "# Slide 1\n\nraw\n"
    meta = build_fail_open_slide_meta(
        1,
        markdown,
        {"ok": True, "errors": [], "warnings": []},
        raw_data_map,
        config,
        code="stage2_failed",
        message="failed",
        fallback_source="stage1_page_ir",
    )

    assert meta["status"] == "fail_open"
    assert meta["markdown_source"]["kind"] == "stage1_page_ir"
    assert meta["markdown_source"]["source"] == "deterministic_renderer"
    assert meta["markdown_source"]["fallback"] is True


def test_slide_meta_without_markdown_source_is_legacy_miss():
    config = AppConfig()
    raw_data_map = {1: "raw"}
    markdown = "# Slide 1\n\nraw\n"
    meta = build_slide_meta(1, markdown, {"ok": True, "errors": [], "warnings": []}, raw_data_map, config)
    del meta["markdown_source"]

    valid, reason = validate_slide_meta(meta, 1, markdown, stage2_fingerprint(1, raw_data_map, config))

    assert not valid
    assert reason == "legacy_miss"
