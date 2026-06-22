from ppt2md_app.confusion import apply_ocr_confusion_fixes


def test_ocr_confusion_is_disabled_by_default():
    text, audit = apply_ocr_confusion_fixes("x＝１")

    assert text == "x＝１"
    assert audit["enabled"] is False
    assert audit["status"] == "disabled"
    assert audit["applied"] is False


def test_ocr_confusion_applies_whitelisted_low_density_replacements():
    text, audit = apply_ocr_confusion_fixes("令 x＝１，y＝２。", enabled=True)

    assert text == "令 x=1，y=2。"
    assert audit["status"] == "applied"
    assert audit["replacement_count"] == 4
    assert {item["before"] for item in audit["replacements"]} == {"＝", "１", "２"}
    assert audit["text_before_sha256"] != audit["text_after_sha256"]


def test_ocr_confusion_rejects_high_density_replacements():
    text, audit = apply_ocr_confusion_fixes("＝" * 50, enabled=True)

    assert text == "＝" * 50
    assert audit["status"] == "rejected_high_density"
    assert audit["applied"] is False
    assert audit["replacement_count"] == 50
