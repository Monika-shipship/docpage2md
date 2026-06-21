from ppt2md_app.refiner import KNOWN_OPS, SAFE_OPS, apply_op_checked, detect_markdown_suspects, refine_slide_markdown


def test_refiner_detects_and_applies_safe_heading_fix():
    result = refine_slide_markdown("正文\n", 4)

    assert result.changed
    assert result.markdown.startswith("# Slide 4")
    assert result.validation["ok"] is True
    assert result.applied_ops[0]["op"] == "fix_heading"


def test_refiner_strips_chatter_without_free_rewrite():
    result = refine_slide_markdown("以下是整理结果：\n# Slide 1\n\n正文\n", 1)

    assert result.markdown == "# Slide 1\n\n正文\n"
    assert [op["op"] for op in result.applied_ops] == ["strip_chatter"]


def test_apply_op_checked_does_not_rewrite_api_error_text():
    suspect = detect_markdown_suspects("DeepSeek HTTP Error: 429\n", 1)[0]
    markdown, applied, detail = apply_op_checked(
        "DeepSeek HTTP Error: 429\n",
        suspect,
        1,
        raw_response="DeepSeek HTTP Error: 429",
    )

    assert markdown == "DeepSeek HTTP Error: 429\n"
    assert applied is False
    assert detail["reason"] == "unsafe_or_error_text"


def test_refiner_known_ops_include_failure_and_line_merge_ids():
    assert {"strip_chatter", "fix_heading", "drop_empty", "merge_broken_line", "mark_failed_page"} <= KNOWN_OPS
    assert "mark_failed_page" not in SAFE_OPS


def test_refiner_can_merge_broken_hyphenated_line():
    result = refine_slide_markdown("# Slide 1\n\ninter-\nnal energy\n", 1)

    assert result.changed
    assert "internal energy" in result.markdown
    assert result.validation["ok"] is True
