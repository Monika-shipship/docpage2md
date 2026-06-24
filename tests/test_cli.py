from docpage2md_app import cli


def test_eval_cli_runs_without_dependency_or_api_checks(monkeypatch, tmp_path, capsys):
    def fail_if_called():
        raise AssertionError("ensure_dependencies should not run for offline eval")

    monkeypatch.setattr(cli, "ensure_dependencies", fail_if_called)

    code = cli.main(
        [
            "--eval-fixtures",
            "tests/fixtures/eval_cases",
            "--eval-output",
            str(tmp_path / "eval_report.json"),
        ]
    )

    captured = capsys.readouterr()
    assert code == 0
    assert "offline eval: 6/6 passed" in captured.out
    assert (tmp_path / "eval_report.json").exists()


def test_cli_build_config_exposes_ocr_confusion_opt_in(tmp_path):
    args = cli.parse_args(["--fix-ocr-confusion", "--output", str(tmp_path)])

    config = cli.build_config(args)

    assert config.fix_ocr_confusion is True
    assert config.output_folder == str(tmp_path.resolve())


def test_cli_build_config_exposes_mineru_multiformat_options(tmp_path):
    args = cli.parse_args(
        [
            "--engine-mode",
            "hybrid",
            "--document-type",
            "handwritten_notes",
            "--model-profile",
            "accurate",
            "--input-file",
            "notes.pdf",
            "--page-ranges",
            "1-5",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.engine_mode == "hybrid"
    assert config.document_type == "handwritten_notes"
    assert config.model_profile == "accurate"
    assert config.mineru_model_version == "vlm"
    assert config.mineru_page_ranges == "1-5"
    assert config.model_brain == "deepseek-v4-pro"
    assert config.brain_provider == "deepseek"


def test_cli_resolves_mineru_folder_batch_inputs(tmp_path):
    keep_pdf = tmp_path / "a.pdf"
    keep_docx = tmp_path / "b.docx"
    ignore_txt = tmp_path / "c.txt"
    nested = tmp_path / "nested"
    nested.mkdir()
    nested_pdf = nested / "d.pdf"
    for path in (keep_pdf, keep_docx, ignore_txt, nested_pdf):
        path.write_bytes(b"x")

    non_recursive = cli.parse_args(["--input-folder", str(tmp_path)])
    recursive = cli.parse_args(["--input-folder", str(tmp_path), "--recursive"])

    assert [path.name for path in cli._resolve_mineru_local_files(non_recursive)] == ["a.pdf", "b.docx"]
    assert [path.name for path in cli._resolve_mineru_local_files(recursive)] == ["a.pdf", "b.docx", "d.pdf"]


def test_cli_rejects_unsupported_explicit_mineru_input(tmp_path):
    bad_file = tmp_path / "notes.txt"
    bad_file.write_text("not a MinerU document", encoding="utf-8")
    args = cli.parse_args(["--input-file", str(bad_file)])

    try:
        cli._resolve_mineru_local_files(args)
    except ValueError as exc:
        assert "Unsupported MinerU input file type" in str(exc)
    else:
        raise AssertionError("Expected unsupported explicit input to fail")


def test_cli_missing_mineru_token_returns_clean_error(monkeypatch, tmp_path, capsys):
    pdf = tmp_path / "notes.pdf"
    pdf.write_bytes(b"%PDF fake")
    monkeypatch.setattr("docpage2md_app.mineru_client.get_env_value", lambda _name: "")

    code = cli.main(["--engine-mode", "hybrid", "--input-file", str(pdf), "--output", str(tmp_path / "out")])

    captured = capsys.readouterr()
    assert code == 1
    assert "MinerU API failed" in captured.out
    assert "MINERU_API_TOKEN" in captured.out
    assert "Traceback" not in captured.out
    assert "Traceback" not in captured.err


def test_interactive_default_starts_with_hybrid_mineru_pdf(monkeypatch):
    args = cli.parse_args([])
    responses = iter(["", "", "", "", "notes.pdf", "1-5"])

    monkeypatch.setattr(cli.sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(responses))

    updated = cli._maybe_prompt_initial_mode(args)

    assert updated.document_type == "handwritten_notes"
    assert updated.engine_mode == "hybrid"
    assert updated.model_profile == "balanced"
    assert updated.input_file == "notes.pdf"
    assert updated.page_ranges == "1-5"
