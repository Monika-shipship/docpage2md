from docpage2md_app.renderer import render_page_ir_to_markdown


def test_uncertain_latex_environment_renders_as_display_math():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 11,
            "blocks": [
                {
                    "id": "p0011-b002",
                    "type": "uncertain",
                    "text": "\\begin{aligned}\nT_1 &= \\begin{bmatrix}0&-i\\\\i&0\\end{bmatrix}\n\\end{aligned}",
                }
            ],
        },
        11,
    )

    assert "$$" in markdown
    assert "\\begin{aligned}" in markdown


def test_formula_inline_spaced_operator_artifacts_render_as_display_math():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 10,
            "blocks": [
                {
                    "id": "p0010-b012",
                    "type": "formula_inline",
                    "text": "T r\\sigma_{i}=0(无迹)d e t\\sigma_{i}=-1",
                }
            ],
        },
        10,
    )

    assert "$$" in markdown
    assert "\\operatorname{Tr}\\sigma_{i}" in markdown
    assert "\\det \\sigma_{i}" in markdown
    assert "T r" not in markdown
    assert "d e t" not in markdown


def test_figure_json_description_renders_chinese_details_without_raw_keys():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 3,
            "blocks": [
                {
                    "id": "p0003-b010",
                    "type": "figure_note",
                    "description": (
                        '{\n'
                        '  "figure_type": "手绘示意图",\n'
                        '  "labels": ["e"],\n'
                        '  "relations": ["点 e 位于闭合曲线内部"],\n'
                        '  "uncertainties": ["缺少坐标轴"],\n'
                        '  "description": "外层为矩形边框，内部有不规则闭合曲线。"\n'
                        '}'
                    ),
                    "path": "assets/crops/figure.jpg",
                }
            ],
        },
        3,
    )

    assert "<details>\n" in markdown
    assert "<details open>" not in markdown
    assert markdown.index("外层为矩形边框") < markdown.index("<summary>图示识别内容</summary>")
    assert "- 类型：手绘示意图" in markdown
    assert "- 可见标签：e" in markdown
    assert "- 主要关系：点 e 位于闭合曲线内部" in markdown
    assert "- 不确定点：缺少坐标轴" in markdown
    assert "figure_type" not in markdown
    assert "relations" not in markdown
