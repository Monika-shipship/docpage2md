from docpage2md_app.formula_quality import (
    assess_formula_text,
    normalize_formula_text,
    normalize_inline_math_text,
    normalize_markdown_formula_blocks,
)


def test_formula_quality_normalizes_display_delimiters():
    result = assess_formula_text("$$\nE = mc^2\n$$")

    assert result.ok
    assert result.latex == "E = mc^2"
    assert normalize_formula_text(r"\[ a + b \]") == "a + b"


def test_formula_quality_normalizes_unicode_math_symbols():
    assert normalize_formula_text("φ + θ = ω") == r"\phi + \theta = \omega"


def test_inline_math_text_wraps_bare_unicode_math_fragment():
    text = normalize_inline_math_text("令 φ, θ, ω 为三个角，且 α+β=γ。")

    assert "$\\phi, \\theta, \\omega$" in text
    assert "$\\alpha + \\beta = \\gamma$" in text
    assert "φ" not in text
    assert "θ" not in text
    assert "ω" not in text


def test_inline_math_text_wraps_compact_arrow_without_swallowing_words():
    text = normalize_inline_math_text("Possible typo: 'G→S' might be 'G→S' or 'GS'.")

    assert text.count("'$G \\to S$'") == 2
    assert "or 'GS'" in text
    assert "$G \\to S or" not in text
    assert "→" not in text


def test_inline_math_text_wraps_arrow_chain_once():
    text = normalize_inline_math_text("Layout suggests a vertical sequence (k→g→?) with lateral connections.")

    assert "($k \\to g \\to ?$)" in text
    assert "$$" not in text
    assert "→" not in text


def test_formula_quality_records_latex_warnings():
    result = assess_formula_text(r"\frac a}{b")

    assert not result.ok
    assert [warning.code for warning in result.warnings] == ["latex_frac_missing_braces"]


def test_formula_quality_records_unbalanced_braces():
    result = assess_formula_text(r"\frac{a}{b")

    assert not result.ok
    assert "formula_brace_unbalanced" in [warning.code for warning in result.warnings]


def test_formula_quality_marks_uncertain_formula():
    result = assess_formula_text("E = [?] mc^2")

    assert result.uncertain
    assert [warning.code for warning in result.warnings] == ["formula_uncertain_marker"]


def test_formula_quality_records_truncated_formula():
    result = assess_formula_text("E =")

    assert not result.ok
    assert "formula_truncated" in [warning.code for warning in result.warnings]


def test_formula_quality_flags_repeated_token_artifact():
    text = (
        r"\begin{array}{c}"
        + r" \\ ".join(["1"] * 10)
        + r" n_{2} n_{3} n_{4} n_{5} n_{6} n_{7} n_{8} n_{9} n_{10} n_{11} n_{12} n_{13} n_{14} n_{15} n_{16} n_{17} n_{18} n_{19}\end{array}"
    )
    result = assess_formula_text(text)

    assert "formula_repeated_token_artifact" in [warning.code for warning in result.warnings]


def test_formula_quality_records_isolated_operator_formula():
    result = assess_formula_text("=")

    assert not result.ok
    assert "formula_isolated_operator" in [warning.code for warning in result.warnings]


def test_formula_quality_warns_on_half_open_interval_without_uncertain_marker():
    result = assess_formula_text("[0,1)")

    assert not result.ok
    assert result.uncertain is False
    assert "formula_bracket_unbalanced" in [warning.code for warning in result.warnings]


def test_formula_quality_moves_tag_outside_aligned_environment():
    source = (
        "\\begin{aligned}\n"
        "S &= k(\\ln Z+\\beta U) \\\\\n"
        "&= \\frac{3}{2}Nk\\ln T \\tag{5}\n"
        "\\end{aligned}"
    )

    normalized = normalize_formula_text(source)

    assert normalized == (
        "\\begin{aligned}\n"
        "S &= k(\\ln Z+\\beta U) \\\\\n"
        "&= \\frac{3}{2}Nk\\ln T\n"
        "\\end{aligned}\n"
        "\\tag{5}"
    )


def test_formula_quality_splits_multiple_tags_inside_aligned_environment():
    source = (
        "\\begin{aligned}\n"
        "& \\begin{cases}\n"
        "a_1 = -1 \\\\\n"
        "a_2 = 0\n"
        "\\end{cases} \\tag{1} \\\\\n"
        "& w+w^* = -1 \\tag{2} \\\\\n"
        "& \\Rightarrow a_3 = 0 \\tag{3}\n"
        "\\end{aligned}"
    )

    normalized = normalize_formula_text(source)

    assert normalized.count("\\begin{aligned}") == 3
    assert normalized.count("\\end{aligned}") == 3
    assert normalized.count("\\tag{") == 3
    assert "\\tag{1} \\\\\n" not in normalized
    assert "\\tag{2} \\\\\n" not in normalized
    assert "\\tag{3}\n\\end{aligned}" not in normalized
    assert "\\end{aligned}\n\\tag{1}" in normalized
    assert "\\end{aligned}\n\\tag{2}" in normalized
    assert "\\end{aligned}\n\\tag{3}" in normalized


def test_markdown_formula_normalization_splits_multiple_tag_display_math():
    markdown = (
        "# Slide 10\n\n"
        "$$\n"
        "\\begin{aligned}\n"
        "& x = 1 \\tag{1} \\\\\n"
        "& y = 2 \\tag{2}\n"
        "\\end{aligned}\n"
        "$$\n"
    )

    normalized = normalize_markdown_formula_blocks(markdown)

    assert normalized.count("$$") == 4
    assert "\\tag{1} \\\\\n" not in normalized
    assert "\\tag{1}\n\\end{aligned}" not in normalized
    assert "\\end{aligned}\n\\tag{1}\n$$" in normalized
    assert "\\end{aligned}\n\\tag{2}\n$$" in normalized


def test_markdown_formula_normalization_merges_multiline_adjacent_inline_math():
    markdown = (
        "标签：$\\Sigma$$\n"
        "J \\neq 0$。\n"
        "关系：$\\Sigma\n"
        "$$J \\neq 0$。"
    )

    normalized = normalize_markdown_formula_blocks(markdown)

    assert "$\\Sigma$$" not in normalized
    assert "\n$$J" not in normalized
    assert normalized.count("$\\Sigma J \\neq 0$") == 2


def test_markdown_formula_normalization_removes_nested_inline_delimiters_in_display_math():
    markdown = "# Slide 3\n\n$$\n要求： $\\left\\{ A = B \\right.$\n$$\n"

    normalized = normalize_markdown_formula_blocks(markdown)

    assert "$\\left" not in normalized
    assert "\\right.$" not in normalized
    assert "要求： \\left\\{ A = B \\right." in normalized
    assert normalized.count("$$") == 2


def test_formula_quality_converts_align_and_trailing_quad_number_to_aligned_tag():
    source = (
        "\\begin{align}\n"
        "A &= B \\\\\n"
        "&= C \\quad (2)\n"
        "\\end{align}"
    )

    normalized = normalize_formula_text(source)

    assert normalized == (
        "\\begin{aligned}\n"
        "A &= B \\\\\n"
        "&= C\n"
        "\\end{aligned}\n"
        "\\tag{2}"
    )


def test_markdown_formula_normalization_skips_code_fences():
    markdown = (
        "# Slide 1\n\n"
        "```text\n"
        "$$\n"
        "\\begin{aligned}\n"
        "x &= y \\tag{raw}\n"
        "\\end{aligned}\n"
        "$$\n"
        "```\n\n"
        "$$\n"
        "\\begin{aligned}\n"
        "x &= y \\tag{1}\n"
        "\\end{aligned}\n"
        "$$\n"
    )

    normalized = normalize_markdown_formula_blocks(markdown)

    assert "\\tag{raw}\n\\end{aligned}" in normalized
    assert "\\begin{aligned}\nx &= y\n\\end{aligned}\n\\tag{1}" in normalized
    assert "\\tag{1}\n\\end{aligned}" not in normalized
