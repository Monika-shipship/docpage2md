from docpage2md_app.renderer import render_page_ir_to_markdown
from docpage2md_app.validators import validate_slide_markdown


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


def test_formula_block_json_payload_extracts_latex_without_leaking_json():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 12,
            "blocks": [
                {
                    "id": "p0012-b001",
                    "type": "formula_block",
                    "text": (
                        "```json\n"
                        "{\n"
                        '  "latex": "\\\\begin{aligned} A &= B \\\\\\\\ C &= D \\\\end{aligned}",\n'
                        '  "description": "English model explanation should not leak.",\n'
                        '  "figure_type": "formula_block"\n'
                        "}\n"
                        "```"
                    ),
                    "formula_image_path": "assets/crops/formula.jpg",
                }
            ],
        },
        12,
    )

    assert "\\begin{aligned}" in markdown
    assert "```json" not in markdown
    assert '"latex"' not in markdown
    assert "English model explanation" not in markdown
    assert "![formula]" not in markdown
    validation = validate_slide_markdown(markdown, 12)
    assert validation.ok
    assert "structured_payload_inside_formula" not in {issue.code for issue in validation.errors}


def test_formula_block_with_outer_display_math_is_renormalized():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 3,
            "blocks": [
                {
                    "id": "p0003-b001",
                    "type": "formula_block",
                    "text": "$$\n要求： $\\left\\{ A = B \\right.$\n$$",
                }
            ],
        },
        3,
    )

    assert "$\\left" not in markdown
    assert "\\right.$" not in markdown
    assert "要求： \\left\\{ A = B \\right." in markdown
    validation = validate_slide_markdown(markdown, 3)
    assert "nested_inline_math_in_display_math" not in {issue.code for issue in validation.errors}


def test_plain_latex_text_command_renders_as_normal_text():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 11,
            "blocks": [
                {
                    "id": "p0011-b001",
                    "type": "paragraph",
                    "text": "\\text{证：从波函数出发}",
                },
                {
                    "id": "p0011-b002",
                    "type": "formula_block",
                    "text": "\\text{inside math}",
                },
            ],
        },
        11,
    )

    assert "证：从波函数出发" in markdown
    assert "\\text{证" not in markdown
    assert "\\text{inside math}" in markdown


def test_bare_latex_math_in_paragraph_renders_as_inline_math():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 3,
            "blocks": [
                {
                    "id": "p0003-b001",
                    "type": "paragraph",
                    "text": "结论 \\Psi(x_{1},t)=\\hat{H}\\Psi(x_{1},t) .",
                }
            ],
        },
        3,
    )

    assert "结论 $\\Psi" in markdown
    assert "\\hat{H}\\Psi" in markdown
    validation = validate_slide_markdown(markdown, 3)
    assert "bare_latex_math_outside_math" not in {issue.code for issue in validation.errors}


def test_formula_truncated_warning_does_not_render_duplicate_image_when_latex_exists():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 59,
            "blocks": [
                {
                    "id": "p0059-b003",
                    "type": "formula_block",
                    "text": r"|n_k\rangle = \frac{1}{\sqrt{n_k!}}(a_k^\dagger)^{n_k}|0\rangle",
                    "latex": r"|n_k\rangle = \frac{1}{\sqrt{n_k!}}(a_k^\dagger)^{n_k}|0\rangle",
                    "formula_image_path": "assets/crops/page_059_formula.jpg",
                    "formula_quality": {
                        "warnings": [
                            {"code": "formula_truncated", "message": "公式疑似截断。"},
                        ]
                    },
                }
            ],
        },
        59,
    )

    assert "![formula]" not in markdown
    assert r"|n_k\rangle" in markdown
    assert markdown.count("$$") == 2


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


def test_figure_details_merge_adjacent_inline_math_spans():
    markdown = render_page_ir_to_markdown(
        {
            "source_page": 4,
            "blocks": [
                {
                    "id": "p0004-b005",
                    "type": "figure_note",
                    "description": r"右侧为非闭合或有源环路积分不等于零（$\Sigma$$J \neq 0$），并标注有序。",
                    "path": "assets/crops/figure.jpg",
                }
            ],
        },
        4,
    )

    assert r"$\Sigma$$J" not in markdown
    assert r"$\Sigma J \neq 0$" in markdown
    validation = validate_slide_markdown(markdown, 4)
    assert {issue.code for issue in validation.errors}.isdisjoint(
        {"display_math_unbalanced", "inline_math_unbalanced"}
    )
