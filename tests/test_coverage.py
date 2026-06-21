from ppt2md_app.coverage import assess_ocr_coverage


def test_ocr_coverage_passes_when_markdown_keeps_ocr_text():
    blocks = [
        {
            "type": "paragraph",
            "origin": "vision_ocr",
            "text": "热力学第一定律描述内能、热量和功之间的关系。",
        }
    ]

    result = assess_ocr_coverage("# Slide 1\n\n热力学第一定律描述内能、热量和功之间的关系。\n", blocks)

    assert result.checked
    assert result.warning is False
    assert result.ratio == 1.0


def test_ocr_coverage_warns_when_most_ocr_text_is_missing():
    blocks = [
        {
            "type": "paragraph",
            "origin": "vision_ocr",
            "text": "热力学第一定律描述内能、热量和功之间的关系。孤立系统的总能量保持守恒。",
        }
    ]

    result = assess_ocr_coverage("# Slide 1\n\n热力学第一定律。\n", blocks)

    assert result.checked
    assert result.warning
    assert result.missing_snippets


def test_ocr_coverage_ignores_generated_figure_descriptions():
    blocks = [
        {
            "type": "figure_note",
            "origin": "vision_description",
            "text": "坐标图中横轴为 t，纵轴为 v，曲线逐渐上升。",
        }
    ]

    result = assess_ocr_coverage("# Slide 1\n\n> [!NOTE] 图示说明\n> 坐标图中横轴为 t。\n", blocks)

    assert not result.checked
    assert result.reason == "no_ocr_segments"
