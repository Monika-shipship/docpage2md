# DocPage2MD Current Status

Last updated: 2026-06-24

## Project Identity

- Product name: `DocPage2MD`
- Main entrypoint: `python docpage2md.py`
- Importable package: `docpage2md_app`
- Main branch under active work: `codex/mineru-refine-inspired`
- Legacy image-folder input directory: `doc_pages/`
- Optional local private input directory: `input_docs/`
- Primary output directory: `markdown_output/`

New work should use `docpage2md.py` and `docpage2md_app`. Historical entrypoint files have been removed from the working tree and are tracked by Git as deletions.

Internal code should use DocPage2MD naming only: `process_single_docpage_task`, `scan_docpage_folders`, `max_docpage_workers`, `doc_name`, and `doc_root`.

## Current Architecture

DocPage2MD has three processing modes:

- `mineru_only`: call or read MinerU output, render clean Markdown from MinerU layout/json/crops.
- `vision_only`: legacy image-folder flow for page images.
- `hybrid`: MinerU layout/crops first, then crop vision + Brain JSON ops + checked refiner + deterministic renderer.

User-facing Markdown remains:

- `Slide_XX.md`
- `{doc_name}_FULL.md`

Diagnostics and audit data belong in:

- `run_report.json`
- `process.log`
- `ir/`
- `mineru_raw/`

Do not put stack traces, API errors, model reasoning, coverage diagnostics, or validator dumps into user Markdown.

Local output directories are useful user assets, not disposable trash:

- Keep `markdown_output/` and `latex_output/` out of Git.
- Do not automatically delete them during cleanup.
- `log/` can be rotated or compressed by an explicit command, but should not be silently deleted.

Recommended future log cleanup behavior:

- Add an explicit command such as `python docpage2md.py --cleanup-logs`.
- Compress logs older than 7 days into `log/archive/`.
- Delete archived logs only when they are older than a documented threshold, such as 60 or 90 days.
- Never delete `markdown_output/`, `latex_output/`, `input_docs/` or user-provided source files from cleanup code.

## Key Docs

- User quickstart: `README.md`
- Pipeline explanation: `docs/architecture/docpage-to-markdown-pipeline.md`
- Hybrid design: `docs/architecture/hybrid-mineru-docpage2md.md`
- Model management: `docs/architecture/model-manager.md`
- Markdown contract: `docs/architecture/markdown-output-contract.md`
- MinerU setup: `docs/architecture/mineru-api-setup.md`
- Change history: `docs/changelog.md`
- Research comparison: `docs/research/comparison-and-docpage2md-roadmap.md`

## Secrets

API keys and tokens must stay out of the repository.

Expected environment variables:

- `MINERU_API_TOKEN`
- `DASHSCOPE_API_KEY`
- `DEEPSEEK_API_KEY`

Logs and reports may record env var names, providers, models, task IDs and trace IDs. They must not record actual token values.

## Verification Commands

Run these after code changes:

```powershell
python docpage2md.py --help
python -m docpage2md_app --help
python -m pytest
git diff --check
```

Useful offline smoke using an existing MinerU artifact:

```powershell
python docpage2md.py --engine-mode mineru_only --mineru-artifact-dir ".\tests\fixtures\mineru_public\minimal_artifact" --output ".\markdown_output\smoke" --name "public_mineru_fixture"
```

Useful real API smoke, when keys are configured and cost/time are acceptable:

```powershell
python docpage2md.py --engine-mode hybrid --model-profile cheap --input-file ".\input_docs\我的手写笔记.pdf" --page-ranges 1-2 --output ".\markdown_output\real_smoke" --name "private_api_smoke_1_2"
```

## Latest Verified Results

- `python -m pytest`: 198 passed.
- `python docpage2md.py --help`: passed.
- `python -m docpage2md_app --help`: passed.
- `git diff --check`: no whitespace errors, CRLF warnings only.
- Historical alias search: no working-tree matches.
- Public fixture artifact smoke can run without network or private data.
- Private real API smoke should use ignored files under `input_docs/` or another local path; do not commit those inputs or outputs.

## Handoff Notes

- Keep README, architecture docs, changelog and this status file synchronized with code changes.
- If a public command changes, update README and `docs/maintenance/current-status.md`.
- If schema names, output layout or report fields change, update architecture docs and tests together.
- If a real API smoke reveals a quality issue, summarize it in `docs/changelog.md` and keep detailed diagnostics in `run_report.json`, not Markdown.
