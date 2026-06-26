import threading
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

from docpage2md_app import cli
from docpage2md_app.config import AppConfig
from docpage2md_app.files import read_json, write_json
from docpage2md_app.input_inspection import build_page_chunks


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


def test_cli_version_prints_app_and_pipeline_versions(capsys):
    code = cli.main(["--version"])

    captured = capsys.readouterr()
    assert code == 0
    assert "DocPage2MD 0.1.0" in captured.out
    assert "pipeline" in captured.out


def test_cli_build_config_exposes_retention_and_scheduler_workers(tmp_path):
    args = cli.parse_args(
        [
            "--output",
            str(tmp_path),
            "--output-retention",
            "debug",
            "--parser-workers",
            "12",
            "--doc-workers",
            "3",
        ]
    )

    config = cli.build_config(args)

    assert config.output_retention == "debug"
    assert config.parser_workers == 12
    assert config.max_docpage_workers == 3
    assert config.output_folder == str(tmp_path.resolve())


def test_cli_paddleocr_evidence_level_controls_visualize(tmp_path):
    args = cli.parse_args(["--output", str(tmp_path), "--paddleocr-evidence-level", "debug"])

    config = cli.build_config(args)

    assert config.paddleocr_evidence_level == "debug"
    assert config.paddleocr_visualize is True
    assert config.paddleocr_visualize_override is None


def test_cli_paddleocr_visualize_overrides_evidence_level(tmp_path):
    args = cli.parse_args(
        [
            "--output",
            str(tmp_path),
            "--paddleocr-evidence-level",
            "audit",
            "--paddleocr-visualize",
            "false",
        ]
    )

    config = cli.build_config(args)

    assert config.paddleocr_evidence_level == "audit"
    assert config.paddleocr_visualize is False
    assert config.paddleocr_visualize_override is False


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


def test_cli_build_config_exposes_dual_hybrid_workflow(tmp_path):
    args = cli.parse_args(
        [
            "--engine-mode",
            "dual_hybrid",
            "--input-file",
            "notes.pdf",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.engine_mode == "dual_hybrid"
    assert config.layout_engine == "dual"
    assert config.refine_mode == "docpage2md"


def test_cli_build_config_exposes_brain_thinking_options(tmp_path):
    args = cli.parse_args(
        [
            "--brain-thinking",
            "enabled",
            "--brain-reasoning-effort",
            "max",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.brain_thinking == "enabled"
    assert config.brain_reasoning_effort == "max"


def test_cli_build_config_exposes_mineru_advanced_options(tmp_path):
    args = cli.parse_args(
        [
            "--input-file",
            "notes.pdf",
            "--mineru-is-ocr",
            "false",
            "--mineru-enable-formula",
            "true",
            "--mineru-enable-table",
            "false",
            "--mineru-language",
            "en",
            "--auto-split-pages",
            "--mineru-page-chunk-size",
            "150",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.mineru_is_ocr is False
    assert config.mineru_enable_formula is True
    assert config.mineru_enable_table is False
    assert config.mineru_language == "en"
    assert config.mineru_auto_split_pages is True
    assert config.mineru_page_chunk_size == 150


def test_cli_explicit_model_overrides_win_over_profile(tmp_path):
    args = cli.parse_args(
        [
            "--model-profile",
            "balanced",
            "--vision-provider",
            "openai_compatible",
            "--vision-model",
            "custom-vision",
            "--vision-base-url",
            "https://vision.example/v1",
            "--vision-api-key-env",
            "VISION_KEY",
            "--brain-provider",
            "openai_compatible",
            "--brain-model",
            "custom-brain",
            "--brain-base-url",
            "https://brain.example/v1",
            "--brain-api-key-env",
            "BRAIN_KEY",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.model_profile == "balanced"
    assert config.vision_provider == "openai_compatible"
    assert config.model_vision == "custom-vision"
    assert config.vision_base_url == "https://vision.example/v1"
    assert config.vision_api_key_env == "VISION_KEY"
    assert config.brain_provider == "openai_compatible"
    assert config.model_brain == "custom-brain"
    assert config.brain_base_url == "https://brain.example/v1"
    assert config.brain_api_key_env == "BRAIN_KEY"


def test_cli_manual_profile_accepts_explicit_model_overrides(tmp_path):
    args = cli.parse_args(
        [
            "--model-profile",
            "manual",
            "--vision-provider",
            "dashscope_openai",
            "--vision-model",
            "qwen3.7-plus",
            "--brain-provider",
            "deepseek",
            "--brain-model",
            "deepseek-v4-pro",
            "--output",
            str(tmp_path),
        ]
    )

    config = cli.build_config(args)

    assert config.model_profile == "manual"
    assert config.vision_provider == "dashscope_openai"
    assert config.model_vision == "qwen3.7-plus"
    assert config.brain_provider == "deepseek"
    assert config.model_brain == "deepseek-v4-pro"


def test_mineru_batch_processing_writes_per_document_process_log(monkeypatch, tmp_path):
    artifact = tmp_path / "artifact"
    artifact.mkdir()
    source = tmp_path / "notes.pdf"
    source.write_bytes(b"%PDF fake")
    args = cli.parse_args(["--input-files", str(source), "--output", str(tmp_path / "out")])
    config = cli.build_config(args)

    class FakeClient:
        def download_zip(self, _url, zip_path):
            zip_path.write_bytes(b"zip")

    class FakeResult:
        full_zip_url = "https://example.com/result.zip"
        task_id = "task-1"
        file_name = "notes.pdf"
        data_id = "data-1"

    monkeypatch.setattr("docpage2md_app.mineru_cache.unzip_mineru_result", lambda _zip, dest: dest.mkdir(parents=True, exist_ok=True))
    monkeypatch.setattr("docpage2md_app.mineru_cache.write_task_manifest", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        "docpage2md_app.mineru_pipeline.process_mineru_artifact_task",
        lambda artifact_dir, config, doc_name, engine_mode, source_path, progress: (
            progress("DocumentIR ready: pages=1, blocks=1") or {
                "page_count": 1,
                "output_dir": str(tmp_path / "out" / "notes"),
            }
        ),
    )
    shared_logger = cli.RunLogger(tmp_path / "out" / "mineru_batch" / "process.log", echo=False)

    cli._download_and_process_mineru_result(
        FakeClient(),
        FakeResult(),
        source=str(source),
        config=config,
        args=args,
        mode="hybrid",
        doc_name=None,
        task_ref={"task_id": "task-1", "batch_id": "batch-1"},
        progress=shared_logger,
    )

    per_doc_log = tmp_path / "out" / "notes" / "process.log"
    assert per_doc_log.exists()
    assert "文档结构已就绪：共 1 页" in per_doc_log.read_text(encoding="utf-8")
    assert "文档结构已就绪：共 1 页" in (tmp_path / "out" / "mineru_batch" / "process.log").read_text(encoding="utf-8")


def test_cli_chunk_merge_renumbers_relative_slides(tmp_path):
    output_dir = tmp_path / "out" / "Deck"
    chunk_dir = tmp_path / "out" / "Deck__chunk_002"
    (chunk_dir / "assets").mkdir(parents=True)
    (chunk_dir / "assets" / "crop.png").write_bytes(b"png")
    (chunk_dir / "ir").mkdir()
    (chunk_dir / "ir" / "page_001_ir.json").write_text("{}", encoding="utf-8")
    (chunk_dir / "mineru_raw").mkdir()
    (chunk_dir / "mineru_raw" / "layout.json").write_text("{}", encoding="utf-8")
    (chunk_dir / "Slide_01.md").write_text("# Slide 1\n\n![图](assets/crop.png)\n", encoding="utf-8")
    write_json(chunk_dir / "Slide_01.meta.json", {"slide_no": 1, "status": "ok"})
    write_json(
        chunk_dir / "run_report.json",
        {
            "doc_name": "Deck__chunk_002",
            "status": "ok",
            "models": {},
            "cost": {"estimated": None, "actual_tokens": None, "note": ""},
            "mineru": {},
            "pages": [
                {
                    "slide_no": 1,
                    "final": {"status": "ok", "included_in_full": True},
                    "validation": {"warnings": []},
                }
            ],
        },
    )
    chunks = build_page_chunks(401, chunk_size=200)

    cli._merge_chunk_outputs(
        output_dir,
        "Deck",
        [{"index": 2, "output_dir": str(chunk_dir)}],
        chunks,
        progress=None,
    )

    merged_slide = output_dir / "Slide_201.md"
    assert merged_slide.exists()
    text = merged_slide.read_text(encoding="utf-8")
    assert text.startswith("# Slide 201")
    assert "assets/chunk_002/crop.png" in text
    assert (output_dir / "assets" / "chunk_002" / "crop.png").exists()
    report = Path(output_dir / "run_report.json")
    assert report.exists()


def test_cli_chunk_merge_slim_cleans_chunk_outputs_and_skips_debug_dirs(tmp_path):
    output_dir = tmp_path / "out" / "Deck"
    chunk_dir = tmp_path / "out" / "Deck__chunk_001"
    (chunk_dir / "assets").mkdir(parents=True)
    (chunk_dir / "assets" / "crop.png").write_bytes(b"png")
    (chunk_dir / "ir").mkdir()
    (chunk_dir / "ir" / "page_001_ir.json").write_text("{}", encoding="utf-8")
    (chunk_dir / "mineru_raw").mkdir()
    (chunk_dir / "mineru_raw" / "layout.json").write_text("{}", encoding="utf-8")
    (chunk_dir / "Slide_01.md").write_text("# Slide 1\n\n![图](assets/crop.png)\n", encoding="utf-8")
    write_json(chunk_dir / "Slide_01.meta.json", {"slide_no": 1, "status": "ok"})
    write_json(
        chunk_dir / "run_report.json",
        {
            "doc_name": "Deck__chunk_001",
            "status": "ok",
            "models": {},
            "cost": {"estimated": None, "actual_tokens": None, "note": ""},
            "mineru": {},
            "pages": [{"slide_no": 1, "final": {"status": "ok", "included_in_full": True}, "validation": {"warnings": []}}],
        },
    )
    chunks = build_page_chunks(2, chunk_size=1)

    cli._merge_chunk_outputs(
        output_dir,
        "Deck",
        [{"index": 1, "output_dir": str(chunk_dir)}],
        chunks,
        progress=None,
        config=AppConfig(output_folder=str(tmp_path / "out"), output_retention="slim"),
    )

    assert (output_dir / "Slide_01.md").exists()
    assert (output_dir / "assets" / "chunk_001" / "crop.png").exists()
    assert not (output_dir / "mineru_raw").exists()
    assert not (output_dir / "ir").exists()
    assert not chunk_dir.exists()


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
    assert "MinerU API 失败" in captured.out
    assert "MINERU_API_TOKEN" in captured.out
    assert "Traceback" not in captured.out
    assert "Traceback" not in captured.err


def test_cli_missing_paddleocr_artifact_returns_clean_error(tmp_path, capsys):
    missing = tmp_path / "missing_artifact"

    code = cli.main(
        [
            "--engine-mode",
            "paddleocr_only",
            "--paddleocr-artifact-dir",
            str(missing),
            "--output",
            str(tmp_path / "out"),
        ]
    )

    captured = capsys.readouterr()
    assert code == 1
    assert "PaddleOCR artifact 处理失败" in captured.out
    assert "Traceback" not in captured.out
    assert "Traceback" not in captured.err


def test_cli_blocks_oversized_paddleocr_url(monkeypatch):
    class _HeadResponse:
        headers = {"Content-Length": str(201 * 1024 * 1024)}

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

    monkeypatch.setattr("urllib.request.urlopen", lambda _req, timeout=15: _HeadResponse())

    try:
        cli._validate_paddleocr_url_size("https://example.com/large.pdf")
    except ValueError as exc:
        assert "200MB" in str(exc)
        assert "large.pdf" in str(exc)
    else:
        raise AssertionError("Expected oversized PaddleOCR URL to fail")


def test_cli_dual_creates_chunk_plan_for_pdf_that_needs_chunking(tmp_path):
    pdf = tmp_path / "long.pdf"
    pdf.write_bytes(b"%PDF\n" + b"\n".join([b"<< /Type /Page >>"] * 251))
    args = cli.parse_args(["--engine-mode", "dual_hybrid", "--input-file", str(pdf), "--output", str(tmp_path / "out")])
    config = cli.build_config(args)

    cli._validate_dual_page_limits([pdf], args, config)
    plans = cli._auto_split_dual_plans_for_local_files([pdf], args, config)

    assert [chunk.page_ranges for chunk in plans[pdf]] == ["1-100", "101-200", "201-251"]


def test_cli_dual_selected_short_range_does_not_chunk_long_pdf(tmp_path):
    pdf = tmp_path / "long.pdf"
    pdf.write_bytes(b"%PDF\n" + b"\n".join([b"<< /Type /Page >>"] * 251))
    args = cli.parse_args(
        [
            "--engine-mode",
            "dual_hybrid",
            "--input-file",
            str(pdf),
            "--page-ranges",
            "1-23",
            "--output",
            str(tmp_path / "out"),
        ]
    )
    config = cli.build_config(args)

    cli._validate_dual_page_limits([pdf], args, config)
    plans = cli._auto_split_dual_plans_for_local_files([pdf], args, config)

    assert plans == {}


def test_cli_merge_dual_chunk_outputs_rewrites_slides_assets_and_report(tmp_path):
    config = AppConfig(output_folder=str(tmp_path / "out"), output_retention="standard")
    output_dir = tmp_path / "out" / "doc"
    chunks = build_page_chunks(122, chunk_size=100)
    chunk_audit = []
    for index, slide_no in [(1, 1), (2, 1)]:
        chunk_dir = tmp_path / "out" / f"doc__chunk_{index:03d}"
        chunk_dir.mkdir(parents=True)
        (chunk_dir / "assets").mkdir()
        (chunk_dir / "assets" / "img.png").write_bytes(b"img")
        (chunk_dir / "ir").mkdir()
        write_json(chunk_dir / "ir" / "document_ir.json", {"chunk": index})
        slide_body = f"# Slide {slide_no}\n\n![x](assets/img.png)\n"
        if index == 2:
            slide_body += (
                "\n<details>\n"
                "    - 可见标签：$\\Sigma$$\n"
                "J \\neq 0$\n"
                "    - 主要关系：$\\Sigma\n"
                "$$J \\neq 0$\n"
                "<summary>图示识别内容</summary>\n\n</details>\n"
            )
        (chunk_dir / f"Slide_{slide_no:02d}.md").write_text(slide_body, encoding="utf-8")
        write_json(chunk_dir / f"Slide_{slide_no:02d}.meta.json", {"slide_no": slide_no, "status": "ok"})
        write_json(
            chunk_dir / "run_report.json",
            {
                "doc_name": f"doc__chunk_{index:03d}",
                "engine_mode": "dual_hybrid",
                "status": "running",
                "pages": [
                    {
                        "slide_no": slide_no,
                        "final": {"status": "ok", "path": str(chunk_dir / f"Slide_{slide_no:02d}.md")},
                        "validation": {"warnings": []},
                    }
                ],
                "dual_parser": {"strategy": "candidate_group_checked_ops"},
                "summary": {},
            },
        )
        chunk_audit.append({"index": index, "page_ranges": chunks[index - 1].page_ranges, "output_dir": str(chunk_dir), "status": "ok"})

    cli._merge_dual_chunk_outputs(output_dir, "doc", chunk_audit, chunks, progress=None, config=config)

    assert (output_dir / "Slide_01.md").exists()
    assert (output_dir / "Slide_101.md").exists()
    merged_markdown = (output_dir / "Slide_101.md").read_text(encoding="utf-8")
    assert "assets/chunk_002/img.png" in merged_markdown
    assert "$\\Sigma$$J" not in merged_markdown
    assert "\n$$J" not in merged_markdown
    assert merged_markdown.count("$\\Sigma J \\neq 0$") == 2
    assert (output_dir / "ir" / "chunk_001" / "document_ir.json").exists()
    report = read_json(output_dir / "run_report.json")
    assert report["engine_mode"] == "dual_hybrid"
    assert report["doc_name"] == "doc"
    assert [page["slide_no"] for page in report["pages"]] == [1, 101]
    assert report["dual_parser"]["chunked_merge"]["copied_slides"] == [1, 101]


def test_cli_run_chunked_dual_pdf_pseudo_long_document_merge(monkeypatch, tmp_path):
    import docpage2md_app.dual_pipeline as dual_pipeline

    pdf = tmp_path / "pseudo_long.pdf"
    pdf.write_bytes(b"%PDF\n" + b"\n".join([b"<< /Type /Page >>"] * 10))
    args = cli.parse_args(["--engine-mode", "dual_hybrid", "--input-file", str(pdf), "--output", str(tmp_path / "out")])
    config = replace(cli.build_config(args), output_retention="slim", parser_workers=2)
    chunks = build_page_chunks(10, chunk_size=5)
    prepare_calls = []

    def fake_prepare_dual_artifacts(_mineru_client, _paddle_client, *, config, args, source, progress):
        prepare_calls.append(args.page_ranges)
        suffix = args.page_ranges.replace("-", "_")
        mineru_artifact = tmp_path / f"mineru_{suffix}"
        paddle_artifact = tmp_path / f"paddle_{suffix}"
        mineru_artifact.mkdir()
        paddle_artifact.mkdir()
        write_json(mineru_artifact / "mineru_task_manifest.json", {"task_id": f"mineru-{suffix}", "batch_id": f"batch-{suffix}"})
        write_json(paddle_artifact / "paddleocr_task_manifest.json", {"job_id": f"paddle-{suffix}", "trace_id": f"trace-{suffix}"})
        return mineru_artifact, paddle_artifact

    def fake_process_dual_artifact_task(_mineru_artifact, _paddle_artifact, config, *, doc_name, source_path, progress):
        chunk_dir = Path(config.output_folder) / doc_name
        chunk_dir.mkdir(parents=True)
        (chunk_dir / "assets").mkdir()
        (chunk_dir / "assets" / "img.png").write_bytes(b"img")
        (chunk_dir / "Slide_01.md").write_text(f"# {doc_name}\n\n![x](assets/img.png)\n", encoding="utf-8")
        write_json(chunk_dir / "Slide_01.meta.json", {"slide_no": 1, "status": "ok"})
        write_json(
            chunk_dir / "run_report.json",
            {
                "doc_name": doc_name,
                "engine_mode": "dual_hybrid",
                "status": "ok",
                "pages": [
                    {
                        "slide_no": 1,
                        "final": {"status": "ok", "path": str(chunk_dir / "Slide_01.md")},
                        "validation": {"warnings": []},
                    }
                ],
                "dual_parser": {"strategy": "pseudo_chunk_fixture"},
                "summary": {},
            },
        )
        return {
            "doc_name": doc_name,
            "output_dir": str(chunk_dir),
            "report_path": str(chunk_dir / "run_report.json"),
            "page_count": 5,
            "status": "ok",
        }

    monkeypatch.setattr(cli, "_prepare_dual_artifacts_for_source", fake_prepare_dual_artifacts)
    monkeypatch.setattr(dual_pipeline, "process_dual_artifact_task", fake_process_dual_artifact_task)

    result = cli._run_chunked_dual_pdf(pdf, chunks, args=args, config=config, doc_name="pseudo_long", progress=None)

    output_dir = Path(result["output_dir"])
    assert sorted(prepare_calls) == ["1-5", "6-10"]
    assert result["status"] == "ok"
    assert (output_dir / "Slide_01.md").exists()
    assert (output_dir / "Slide_06.md").exists()
    assert (output_dir / "pseudo_long_FULL.md").exists()
    assert "assets/chunk_002/img.png" in (output_dir / "Slide_06.md").read_text(encoding="utf-8")
    assert not (Path(config.output_folder) / "pseudo_long__chunk_001").exists()
    assert not (Path(config.output_folder) / "pseudo_long__chunk_002").exists()
    report = read_json(output_dir / "run_report.json")
    assert report["engine_mode"] == "dual_hybrid"
    assert [item["page_ranges"] for item in report["dual_parser"]["chunks"]] == ["1-5", "6-10"]
    assert report["dual_parser"]["chunked_merge"]["enabled"] is True
    assert report["dual_parser"]["chunked_merge"]["selected_page_count"] == 10


def test_cli_dual_prepares_mineru_and_paddleocr_artifacts_in_parallel(monkeypatch, tmp_path):
    pdf = tmp_path / "notes.pdf"
    pdf.write_bytes(b"%PDF")
    args = cli.parse_args(["--engine-mode", "dual_hybrid", "--input-file", str(pdf), "--output", str(tmp_path / "out")])
    config = cli.build_config(args)
    mineru_artifact = tmp_path / "mineru_artifact"
    paddle_artifact = tmp_path / "paddle_artifact"

    mineru_started = threading.Event()
    paddle_started = threading.Event()

    class FakeMinerUClient:
        def submit_local_files(self, files, *, page_ranges=None):
            assert files == [pdf]
            assert page_ranges is None
            mineru_started.set()
            if not paddle_started.wait(timeout=1):
                raise AssertionError("PaddleOCR stage did not start while MinerU was submitting")
            return "batch-1"

        def wait_for_batch_results(self, batch_id, *, expected_count):
            assert batch_id == "batch-1"
            assert expected_count == 1
            return [SimpleNamespace(task_id="task-1", full_zip_url="https://example.com/mineru.zip")]

    class FakePaddleOCRClient:
        def submit_local_file(self, path, *, page_ranges=None):
            assert path == pdf
            assert page_ranges is None
            paddle_started.set()
            if not mineru_started.wait(timeout=1):
                raise AssertionError("MinerU stage did not start while PaddleOCR was submitting")
            return "job-1"

        def wait_for_job(self, job_id):
            assert job_id == "job-1"
            return SimpleNamespace(job_id="job-1", trace_id="trace-1")

    monkeypatch.setattr(cli, "_download_mineru_artifact_only", lambda *_args, **_kwargs: mineru_artifact)
    monkeypatch.setattr(cli, "_download_paddleocr_artifact_only", lambda *_args, **_kwargs: paddle_artifact)

    result = cli._prepare_dual_artifacts_for_source(
        FakeMinerUClient(),
        FakePaddleOCRClient(),
        config=config,
        args=args,
        source=pdf,
        progress=None,
    )

    assert result == (mineru_artifact, paddle_artifact)
    assert mineru_started.is_set()
    assert paddle_started.is_set()


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
