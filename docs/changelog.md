# Changelog

## 2026-06-24

### Changed

- README now has a beginner-oriented quick start for single PDF conversion, explains where to put private input files, and clarifies that there is no GUI file picker yet.
- Added `input_docs/` as the recommended local ignored directory for private PDFs, Office files and images.
- Clarified that `markdown_output/` and `latex_output/` are local user assets and must not be automatically deleted by cleanup work.
- 统一项目命名为 `DocPage2MD`：
  - 正式入口为 `docpage2md.py`。
  - 正式 Python 包名为 `docpage2md_app`。
  - 历史入口文件已从工作树移除，删除记录由 Git 跟踪。
  - 默认文档页图片目录为 `doc_pages/`。
- 文档、测试、schema、provenance 和版本常量统一改为 `docpage2md` 命名：
  - `DOCPAGE2MD_PIPELINE_VERSION`
  - `docpage2md-docir-v1`
  - `docpage2md-provenance`
- 清理内部历史命名残留：
  - `process_single_docpage_task`
  - `scan_docpage_folders`
  - `DEFAULT_MAX_DOCPAGE_WORKERS`
  - `max_docpage_workers`
  - `doc_name` / `doc_root`
- 增强 MinerU / hybrid 运行日志：
  - 终端实时输出关键阶段。
  - 每个任务输出目录写入 `process.log`。
  - 日志覆盖提交、上传、轮询、下载、解压、IR 适配、crop 复制、crop vision、Brain、refiner、逐页渲染和 report 写入。
  - 日志只记录环境变量名，不记录真实 token。
- 修正 `content_inventory` 的误报：
  - 不再把全页 `before_block_ids` / `after_block_ids` 误归因到每个 block。
  - inline formula 因空白规范化造成的假 `unrendered` 已修正。
- 新增接手状态文档：`docs/maintenance/current-status.md`。

### Verified

- `python docpage2md.py --help`：通过。
- `python -m docpage2md_app --help`：通过。
- `python -m pytest`：198 passed。
- `git diff --check`：无 whitespace error，仅有 CRLF 提示。
- 旧入口、旧包名、旧项目别名和旧内部函数/变量名搜索无匹配；删除记录由 Git 跟踪。
- 使用正式入口对公开 MinerU fixture 做无网络 smoke，确认 artifact adapter、IR、Markdown、assets 和 report 输出路径可用。
- 真实手写 PDF API smoke 应使用 `input_docs/` 或仓库外路径中的私有样本；这些输入、输出和日志不进入 Git。

### Known Gaps

- 完整 11 页真实 hybrid 已跑通一次，但那次是在日志增强前完成；带详细日志的真实 API smoke 当前只跑了 1-2 页。

## 2026-06-23

### Added

- 新增 MinerU 多格式主路径设计和实现，支持通过 MinerU artifact/API 将 PDF、Office、图片等输入转换为内部 IR。
- 新增 MinerU artifact 读取、图片 crop 复制、`assets/crops` 相对路径渲染。
- 新增 `mineru_only` / `vision_only` / `hybrid` 处理模式。
- 新增模型档位 `cheap`、`balanced`、`accurate`、`manual`，Brain 默认 `deepseek-v4-flash`，accurate 使用 `deepseek-v4-pro`。
- 新增 `hybrid_enrichment.py`，支持 crop vision enrichment、Brain JSON ops、受限 refiner、op audit，并可通过 mock backend 离线测试。
- 新增 `replace_text_span_checked` block op，用于 Brain 做局部 OCR/公式识别修正。
- 新增 `content_inventory`，记录每个 source block 是否 rendered、replaced、merged、degraded、dropped 或 unrendered。
- 新增 `run_report.json` 中的 `vision`、`brain`、`op_audit`、`content_inventory` 汇总。
- 新增架构文档：
  - `docs/architecture/hybrid-mineru-docpage2md.md`
  - `docs/architecture/model-manager.md`
  - `docs/architecture/markdown-output-contract.md`
  - `docs/architecture/mineru-api-setup.md`

### Changed

- README 定位从“图片目录转 Markdown”调整为“MinerU 多格式文档输入 -> Markdown-first 输出”，PDF 是核心输入。
- `vision_only` 被保留为旧图片目录兼容路径，不再是项目主定位。
- 图示 Markdown 输出改为 crop 图片 + 默认折叠 `<details>` 说明。
- 公式规范化要求 `\tag{}` 位于 `aligned` 环境外。
- 不再把 coverage、validator 诊断、API 错误、模型思考过程写进用户 Markdown。

### Verified

- `python -m pytest`：193 passed。
- `python -m docpage2md_app --help`：通过。
- `git diff --check`：无 whitespace error，仅有 CRLF 提示。

### Known Gaps

- `hybrid` 的默认 production backend 已接入接口形态；真实模型效果需要用本地私有手写 PDF 样本持续验证。
- 完整的第三方 provider/model registry 仍可继续扩展；当前已有 profile/role binding 基础。
