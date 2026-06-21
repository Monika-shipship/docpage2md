from ppt2md_app.table_quality import assess_table_markdown


def test_reliable_markdown_table_passes_quality_gate():
    result = assess_table_markdown("| A | B |\n| --- | --- |\n| 1 | 2 |")

    assert result.reliable
    assert result.errors == []
    assert result.warnings == []


def test_ragged_markdown_table_is_unreliable():
    result = assess_table_markdown("| A | B |\n| --- | --- |\n| 1 | 2 | 3 |")

    assert not result.reliable
    assert [issue.code for issue in result.errors] == ["table_column_mismatch"]


def test_table_shell_is_warning_and_unreliable():
    result = assess_table_markdown("| A | B |\n| --- | --- |")

    assert not result.reliable
    assert [issue.code for issue in result.warnings] == ["table_shell"]
