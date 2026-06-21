# png2md / PPT2MD-V10 项目研究报告

生成时间：2026-06-19  
研究者角色：Subagent B  
工作区：`D:\Repos\lab-python\png2md`  
当前分支：`codex/mineru-refine-inspired`  
报告目标文件：`D:\Repos\lab-python\png2md\docs\research\png2md-research.md`

## 0. 研究边界与已验证事实

本报告基于当前工作区源码与运行产物的只读研究结果编写。除创建本报告所在目录与本 Markdown 文件外，未修改业务代码。

需要先说明一个命名事实：仓库目录名是 `png2md`，README 标题与入口脚本描述的是 `PPT2MD-V10`，实际 Python 包名是 `ppt2md_app`。当前仓库中没有 `png2md_app` 目录；用户要求研究的 `cli.py`、`pipeline.py`、`models.py`、`prompts.py`、`config.py`、`cost.py`、`files.py`、`model_settings.py`、`third_party_models.py` 实际都位于 `ppt2md_app\` 下。

当前 `git status --short --untracked-files=all` 验证到以下未提交改动：

```text
 M ppt2md_app/config.py
 M ppt2md_app/model_settings.py
?? ppt2md_app/third_party_models.py
```

其中 `third_party_models.py` 是未跟踪的新文件；`config.py` 和 `model_settings.py` 已修改。`git diff --stat` 显示已跟踪文件的差异为：

```text
 ppt2md_app/config.py         |   4 +
 ppt2md_app/model_settings.py | 476 +++++++++++++++++++++++++++++++++++++------
 2 files changed, 415 insertions(+), 65 deletions(-)
```

未跟踪文件 `ppt2md_app/third_party_models.py` 不在上述 diff stat 中，但已被当前 `model_settings.py` import，因此它是当前运行形态的一部分，不能只按已提交版本理解项目。

当前仓库未发现 `tests/` 目录；对仓库执行 `rg -n "unittest|pytest|def test_|class Test|assert " .` 没有匹配。当前也没有 `docs/` 目录，报告写入前由本次任务创建了 `docs\research`。

## 1. 项目当前目标与定位

项目目标是把一组已经导出的 PPT 截图、扫描页、论文图片或类似页面图片批量转换为结构化 Markdown 笔记。README 明确说明它不是读取 `.pptx` 文件，而是读取图片目录，例如 `ppt_images\某个任务\001.png`、`002.png` 等，然后输出单页 Markdown、视觉中间缓存和汇总 Markdown。

当前产品形态更接近一个交互式本地 CLI 批处理工具，而不是库或服务：

- 入口是仓库根目录的 `ppt2md.py`，它只负责调用 `ppt2md_app.cli.main()`。
- 主交互流程在 `ppt2md_app\cli.py:208` 的 `main()` 中编排。
- 用户通过 `python ppt2md.py` 启动，随后在终端中选择模型、选择图片任务、选择页码范围、查看成本预估并确认执行。
- 模型目录管理命令也是同一入口提供，例如 `--list-models`、`--refresh-models`、`--verify-models`。

该项目目前的核心价值不是“完美 OCR”，而是把视觉模型的页面理解能力与文本模型的 Markdown 整理能力组合起来，给用户一个端到端、可断点续跑、可预估成本、可选择模型的图片转 Markdown 工作流。

## 2. 使用流程

### 2.1 安装与启动

`requirements.txt` 只有三项依赖：

```text
dashscope
rich
Pillow
```

`ppt2md_app\cli.py:35` 的 `ensure_dependencies()` 会检查 `rich`、`PIL`、`dashscope` 是否可 import，缺少时直接提示安装包名。没有检测 Python 版本，也没有检测网络连通性、API Key 有效性或模型权限；API Key 和模型可用性在后续步骤处理。

普通启动方式：

```powershell
python ppt2md.py
```

支持指定会话名与输出目录：

```powershell
python ppt2md.py -n my_session -o .\markdown_output
```

`ppt2md_app\cli.py:12` 的 `parse_args()` 定义了以下主要参数：

- `-n / --name`：会话名称，默认 `default`。
- `-o / --output`：输出目录，默认 `./markdown_output`。
- `--list-models`：列出可用模型后退出。
- `--list-all-models`：列出完整缓存模型目录，包含未验证候选。
- `--refresh-models`：从阿里云文档刷新候选模型列表并缓存。
- `--verify-models`：用 API 验证模型可用性。
- `--region`：阿里云地域，默认 `cn-beijing`。
- `--base-url`：OpenAI 兼容端点，默认 DashScope compatible endpoint。
- `--model-cache`：模型缓存文件路径，默认 `.cache/aliyun_model_catalog.json`。
- `--verify-limit` 和 `--verify-sleep`：控制模型验证数量和间隔。

### 2.2 主流程顺序

`ppt2md_app\cli.py:208` 的 `main()` 是主流程入口。按源码顺序，普通转换模式执行：

1. `configure_stdio()` 设置 stdout/stderr 为 UTF-8。
2. `parse_args()` 解析 CLI 参数。
3. `ensure_dependencies()` 检查依赖。
4. `build_config()` 把参数转换成 frozen dataclass `AppConfig`。
5. 如果是模型目录命令，则进入 `_handle_model_commands()` 后退出。
6. `ensure_input_folder(config)` 检查 `ppt_images`，不存在则创建并要求用户放入图片后重跑。
7. `configure_models(console, config)` 交互选择 Vision 和 Brain 模型。
8. `check_runtime_env(config)` 检查所选模型需要的 API Key 环境变量。
9. `setup_logger(config)` 创建日志文件。
10. `interactive_setup(console, final_key, config)` 扫描图片任务、处理断点会话、选择 PPT 文件夹和页码范围。
11. `show_cost_estimation(console, tasks_config, config)` 做成本预估。
12. 用户确认开始。
13. 创建 `multiprocessing.Manager().Queue()` 和 Rich `Progress`。
14. 用 `ProcessPoolExecutor(max_workers=config.max_ppt_workers)` 对多个 PPT 文件夹并行提交 `process_single_ppt_task()`。
15. 主进程持续消费 worker 发来的 `init_task`、`advance`、`status`、`log` 消息，更新进度条和日志。

这个流程说明当前程序的交互体验已经覆盖了从模型选择到成本确认再到处理进度的完整闭环。

## 3. 输入、输出与运行时目录

### 3.1 默认目录

默认路径在 `ppt2md_app\config.py` 中定义：

- `DEFAULT_INPUT_FOLDER = "./ppt_images"`，见 `ppt2md_app\config.py:11`。
- `DEFAULT_OUTPUT_FOLDER = "./markdown_output"`，见 `ppt2md_app\config.py:12`。
- `DEFAULT_LOG_FOLDER = "./log"`，见 `ppt2md_app\config.py:13`。
- `DEFAULT_MODEL_CACHE_PATH = ".cache/aliyun_model_catalog.json"`，见 `ppt2md_app\config.py:14`。

`AppConfig` 是 frozen dataclass，定义于 `ppt2md_app\config.py:41`。由于它是 frozen，模型选择和配置变更通常通过 `dataclasses.replace()` 返回新配置对象，而不是原地修改。

### 3.2 输入结构

输入扫描逻辑在 `ppt2md_app\files.py:123` 的 `scan_ppt_folders(root_folder)`：

- 只扫描输入根目录下的一级子目录。
- 每个子目录代表一个 PPT 或图片任务。
- 支持扩展名集合为 `.jpg`、`.jpeg`、`.png`、`.bmp`、`.webp`。
- 图片按 `natural_sort_key()` 排序，避免 `10.png` 排在 `2.png` 前面。
- 返回结构是 `{任务名: [图片绝对路径列表]}`。

这意味着当前不支持：

- 直接读取 `.pptx`。
- 递归扫描多级目录。
- 单文件输入。
- PDF 直接输入。

README 中也明确要求先把 PPT/PDF 导出成图片后放入 `ppt_images\任务名\`。

### 3.3 输出结构

单个任务的输出根目录由 `ppt2md_app\pipeline.py:25` 计算：

```text
{config.output_folder}\{ppt_name}
```

在该目录下，`process_single_ppt_task()` 会创建：

- `temp_raw_vision\`：Step 1 视觉模型 Raw Data 缓存目录。
- `Slide_XX.md`：Step 2 Brain 模型整理后的单页 Markdown。
- `{ppt_name}_FULL.md`：由 `files.merge_markdowns()` 生成的汇总 Markdown。

Step 1 缓存文件名格式由 `ppt2md_app\pipeline.py:82` 定义：

```text
temp_raw_vision\Raw_01.json
temp_raw_vision\Raw_02.json
...
```

Step 2 输出文件名格式由 `ppt2md_app\pipeline.py:158` 定义：

```text
Slide_01.md
Slide_02.md
...
```

汇总逻辑在 `ppt2md_app\files.py:150` 的 `merge_markdowns()`：

- 查找输出目录下所有 `Slide_*.md`。
- 按自然排序读取。
- 写入 `{ppt_name}_FULL.md`。
- 文件头包含任务名、生成时间和 `V10 (Parallel Brain)` 引擎标识。
- 单页之间用 Markdown 分隔线 `---` 隔开。

### 3.4 日志、会话、模型设置与缓存

运行时状态分布在多个位置：

- 日志：`log\log_{session_name}_{YYYYMMDD_HHMMSS}.log`，由 `ppt2md_app\files.py:13` 的 `setup_logger()` 创建。
- 会话：`log\sessions\session_{session_name}.json`，由 `ppt2md_app\config.py:77` 和 `ppt2md_app\session.py:24` 控制。
- 旧会话兼容路径：仓库根目录下的 `session_{session_name}.json`，见 `ppt2md_app\config.py:85` 和 `ppt2md_app\session.py:7`。
- 模型偏好：`log\model_settings.json`，见 `ppt2md_app\config.py:105` 与 `ppt2md_app\model_settings.py:687`。
- 第三方模型注册表：`log\third_party_models.json`，这是当前未提交改动新增的路径，见 `ppt2md_app\config.py:109` 与 `ppt2md_app\third_party_models.py:20`。
- 阿里云模型目录缓存：`.cache\aliyun_model_catalog.json`，见 `ppt2md_app\config.py:14`、`ppt2md_app\aliyun_catalog.py:745`。

本次研究实际观察到：

- `log\model_settings.json` 存在，当前保存 Vision 为 `dashscope:qwen3.5-plus-2026-04-20`，Brain 为 `deepseek:deepseek-v4-flash`。
- `log\third_party_models.json` 存在，保存了第三方模型条目，例如 `openai_compatible` provider、Base URL、API Key 环境变量名、模型 ID、roles、价格字段和验证字段；该文件不保存 API Key 明文。
- `log\sessions` 下已有多个 session JSON 文件。
- `.cache\aliyun_model_catalog.json` 存在。
- `markdown_output` 下已有大量历史输出。

## 4. 两阶段 Pipeline

当前项目最核心的设计是 Vision/Brain 双阶段 pipeline。控制器位于 `ppt2md_app\pipeline.py:10` 的 `process_single_ppt_task()`。

### 4.1 Stage 1: Vision 视觉提取

Stage 1 的调度函数是 `ppt2md_app\pipeline.py:71` 的 `_run_vision_stage()`。它对当前任务选中的图片页执行视觉模型调用，产出 Raw Data。

核心行为：

- 目标页由 `images_paths[start_idx:end_idx]` 决定。
- 对每页计算实际页码 `actual_slide_no = start_idx + i + 1`。
- 如果 `temp_raw_vision\Raw_XX.json` 已存在，则尝试读取并从 JSON 中取 `data["raw_text"]` 作为缓存命中。
- 如果缓存不存在或读取失败，则提交线程任务 `run_stage_1_vision(img_path, actual_slide_no, ppt_name, msg_queue, config)`。
- 成功后把完整 result 写入 `Raw_XX.json`。
- 失败时把 `raw_data_map[slide_no]` 设置为字符串 `[Vision Failed]`，并继续流程。

真正调用视觉模型的函数是 `ppt2md_app\models.py:246` 的 `run_stage_1_vision()`：

- DashScope 原生路径使用 `dashscope.MultiModalConversation.call()`。
- 对 `dashscope_openai` 或 `openai_compatible` provider，转到 `_run_openai_compatible_vision()`。
- 原生 DashScope 请求中开启 `enable_thinking=True`，`thinking_budget=config.thinking_budget_vision`，`stream=True`，`incremental_output=True`。
- 视觉 prompt 来自 `ppt2md_app\prompts.py:1` 的 `PROMPT_STAGE_1_VISION`。

Stage 1 prompt 的目标很明确：

- 逐字 OCR 文本并保留换行结构。
- 把公式转换为 LaTeX。
- 对有信息量的 Figure 生成 `### Figure Analysis` 区块，描述布局、节点、连接、箭头、标签等。
- 不要求整理成 Markdown。

这说明 Stage 1 的输出是“面向后续重组的自然语言 Raw Data”，而不是结构化 JSON 或可验证 AST。

### 4.2 Stage 2: Brain 重组

Stage 2 的调度函数是 `ppt2md_app\pipeline.py:139` 的 `_run_brain_stage()`。它把每一页的 Raw Data 与前后上下文送入 Brain 模型，生成最终 Markdown。

核心行为：

- 对每个目标页计算输出路径 `Slide_XX.md`。
- 如果输出文件已存在且大小大于 100 字节，则跳过该页。
- 否则提交线程任务 `run_stage_2_brain_parallel(actual_slide_no, raw_data_map, config)`。
- 线程完成后直接把返回字符串写入 `Slide_XX.md`。

真正构造 Brain prompt 的函数是 `ppt2md_app\models.py:395` 的 `run_stage_2_brain_parallel()`。它把五页滑动窗口填入 `PROMPT_STAGE_2_BRAIN`：

- `[P-2]`：前前页 Raw Data。
- `[P-1]`：前一页 Raw Data。
- `[Target]`：当前页 Raw Data。
- `[N+1]`：后一页 Raw Data。
- `[N+2]`：后两页 Raw Data。

窗口内容通过 `ppt2md_app\models.py:387` 的 `get_raw_content()` 获取，超过 3000 个字符会截断为前 3000 字符并追加 `...(truncated)`。

Brain prompt 定义于 `ppt2md_app\prompts.py:26`，其关键约束是：

- 只能输出当前页 `[Target]` 中实际出现的内容。
- 前后两页只允许作为 OCR 错字、符号一致性、术语一致性的后台参考。
- 严禁把前后页正文、标题、例子、结论、下一节内容写入当前页。
- 最终答案必须从 `# Slide {slide_no}` 开始。
- 不允许输出 `<CTX>` 元数据、寒暄、解释、处理过程或 Markdown 代码围栏包裹全文。

Brain provider 路由在 `run_stage_2_brain_parallel()` 中：

- `deepseek`：调用 `_run_deepseek_brain()`，见 `ppt2md_app\models.py:525`。
- `dashscope_openai` 或 `openai_compatible`：调用 `_run_openai_compatible_brain()`，见 `ppt2md_app\models.py:501`。
- 其他默认走 DashScope 原生文本 API `_run_dashscope_brain()`，见 `ppt2md_app\models.py:464`。

最终结果会经过 `ppt2md_app\models.py:417` 的 `sanitize_stage_2_markdown()`：

- 去掉包裹全文的 Markdown 代码围栏。
- 删除 `<CTX>...</CTX>`。
- 尝试定位 `# Slide {slide_no}` 标题，如果存在则从该标题开始截取。
- 如果没有标题，则去掉一些常见中文寒暄开场，并强制补 `# Slide {slide_no}`。

这个 sanitize 是轻量清洗，不是内容正确性校验。它无法证明模型没有引用前后页内容，也无法验证公式是否正确。

## 5. 并发模型

### 5.1 多任务进程并发

顶层并发在 `ppt2md_app\cli.py:274` 使用 `ProcessPoolExecutor(max_workers=config.max_ppt_workers)`。每个 PPT 图片文件夹作为一个独立任务提交给子进程执行 `process_single_ppt_task()`。

默认 `max_ppt_workers` 来自 `ppt2md_app\config.py:16`：

```text
DEFAULT_MAX_PPT_WORKERS = 1
```

这意味着默认不会同时处理多个 PPT 文件夹。README 也解释这是为了避免多个大任务同时调用 API 导致限流。

进程与主进程之间用 `multiprocessing.Manager().Queue()` 传递消息。worker 发送：

- `init_task`：初始化进度条总数。
- `advance`：推进进度。
- `status`：更新当前状态文字。
- `log`：交给主进程 logger 写日志。

### 5.2 单任务内线程并发

单个 PPT 任务内部，Stage 1 和 Stage 2 都使用 `ThreadPoolExecutor`：

- Stage 1：`ppt2md_app\pipeline.py:81`，`max_workers=config.vision_batch_workers`。
- Stage 2：`ppt2md_app\pipeline.py:153`，`max_workers=config.brain_batch_workers`。

默认 worker 数在 `ppt2md_app\config.py:17` 和 `ppt2md_app\config.py:18`：

```text
DEFAULT_VISION_BATCH_WORKERS = 60
DEFAULT_BRAIN_BATCH_WORKERS = 60
```

并发模型是“两阶段并行”，不是流水线交错执行：

1. 先对所有目标页并发执行 Stage 1，或读取 Stage 1 缓存。
2. Stage 1 全部完成后，得到完整 `raw_data_map`。
3. 再对所有目标页并发执行 Stage 2。

这种设计服务于五页窗口：Stage 2 需要当前页前后各两页的 Raw Data，因此必须等 Stage 1 全部完成或命中缓存。

### 5.3 并发风险

当前默认 60 个 Vision worker 和 60 个 Brain worker 对本地 CPU 不是主要压力，真正压力在远端 API 并发、速率限制和账号配额。项目有一些重试逻辑，但覆盖不一致：

- `ppt2md_app\models.py:26` 定义了 `retry_with_backoff()` 装饰器，但从当前源码看，主要 API 调用路径并未系统性套用该装饰器。
- `run_stage_1_vision()` 内部有三次手写 retry。
- `_run_deepseek_brain()`、`_run_dashscope_brain()`、`_run_openai_compatible_brain()` 主要返回错误字符串或异常信息，没有统一退避策略。

因此在高并发、服务商限流或网络抖动下，Stage 2 的稳定性可能弱于用户从“并发已实现”这句话直觉期待的水平。

## 6. 缓存与断点续跑

### 6.1 Vision Raw Data 缓存

Stage 1 缓存存在于输出目录的 `temp_raw_vision\Raw_XX.json`。`_run_vision_stage()` 的缓存判断非常直接：

- 文件存在就尝试 `read_json()`。
- 成功读取 `data["raw_text"]` 就认为缓存命中。
- 失败则忽略缓存并重新调用模型。

优点：

- 中断后重跑不会重复调用已完成页的 Vision 模型。
- 对长任务非常实用，因为 Vision 阶段通常最贵或最慢。

限制：

- 缓存没有记录或校验模型 ID、provider、base_url、prompt 版本、图片文件 hash、图片修改时间、thinking budget、代码版本等指纹。
- 如果用户更换 Vision 模型、改了 prompt、替换了图片、调整了 OCR 要求，旧 Raw JSON 仍会被使用。
- Raw JSON 的最小 schema 依赖 `raw_text` 字段，缺少显式版本。

### 6.2 Slide Markdown 跳过策略

Stage 2 的断点判断在 `ppt2md_app\pipeline.py:160`：

```text
output_path.exists() and output_path.stat().st_size > 100
```

优点：

- 已生成的 `Slide_XX.md` 可以跳过，避免重复调用 Brain 模型。
- 文件过小则视为不可靠，允许重新生成。

限制：

- 同样没有模型、prompt、Raw Data、代码版本、输出 schema 指纹。
- `>100 字节` 是启发式判断，不能证明内容完整或正确。
- 如果之前生成了错误 Markdown，只要长度超过 100 字节就会被跳过。

### 6.3 会话恢复

会话逻辑在 `ppt2md_app\session.py`：

- `load_session()` 见 `ppt2md_app\session.py:7`，先查 `log\sessions\session_{name}.json`，再查旧路径。
- 如果读取到旧路径且新路径不存在，会调用 `save_session()` 迁移。
- `interactive_setup()` 见 `ppt2md_app\session.py:50`，扫描到旧会话后询问是否继续。
- `save_session()` 见 `ppt2md_app\session.py:24`，保存 `tasks_config`，包含 images 列表、range_start、range_end、task_id。

会话恢复和文件级跳过共同构成当前“断点续跑”能力：

- 会话恢复让用户不用重新选择 PPT 和页码范围。
- Raw JSON 缓存避免重复 Vision 调用。
- Slide 文件跳过避免重复 Brain 调用。

限制：

- session 中保存的是图片绝对路径列表；如果目录移动、文件重命名、图片替换，缺少一致性检查。
- `task_id` 会保存在 JSON 里，但新的运行会在 `cli.main()` 中覆盖为 Rich progress task id。
- 没有 session schema 版本，也没有校验 session 是否匹配当前模型和输出目录。

## 7. 日志模型

日志创建在 `ppt2md_app\files.py:13` 的 `setup_logger()`：

- 创建 `log` 目录。
- 日志文件名包含 session name 和时间戳。
- logger 名称是 `PPT2MD_{session_name}`。
- 格式包含时间、进程名、level 和消息。
- `logger.propagate = False` 避免重复传播。

worker 子进程并不直接写该 logger，而是通过消息队列发送 `("log", message)`，主进程在 `cli.main()` 的 Live loop 中收到后执行 `logger.info(message)`。这样可以避免多个进程直接写同一日志文件造成的简单竞争。

当前日志覆盖内容包括：

- 任务启动时的模型和 worker 数。
- 每页 Vision 缓存命中。
- 每页 Vision 失败或异常。
- Stage 1 完成耗时、缓存数、提交数、失败数。
- Stage 2 开始。
- 每页重组完成或异常。
- Stage 2 完成耗时、跳过数、提交数、失败数。
- 全流程总耗时。

限制：

- API 请求 payload、响应 token usage、服务商 request id 未记录。
- 失败页只记录摘要，无法直接关联原始响应。
- logger handler 只在 `if not logger.handlers` 时添加；同一 Python 进程内多次调用相同 session 的 `main()` 时，新 log 文件路径会返回，但 logger 仍可能使用旧 handler。普通 CLI 每次新进程运行时影响较小。

## 8. 成本估算

成本估算位于 `ppt2md_app\cost.py`，入口是 `show_cost_estimation()`，见 `ppt2md_app\cost.py:141`。

### 8.1 图片 token 估算

`calculate_image_tokens()` 见 `ppt2md_app\cost.py:4`。它使用 Qwen3-VL 规则近似计算图片 token：

```text
Token = (H_bar * W_bar) / (32 * 32) + 2
```

其中 `H_bar` 和 `W_bar` 是把图片高宽 round 到 32 的倍数。读取图片尺寸使用 Pillow。读取失败时 fallback 为 `2000` tokens。

### 8.2 模型价格估算

`estimate_text_cost()` 见 `ppt2md_app\cost.py:59`：

- 输入价格、输出价格来自 `ModelRecord`。
- 支持 `price_tiers`，用输入 tokens 所在区间选择输入价和输出价。
- 支持 `cached_input_price`，但当前 `show_cost_estimation()` 没有传入 cache hit tokens，因此通常按未命中估算。
- 价格单位是元/百万 tokens。

如果找不到 `ModelRecord` 或价格，`show_cost_estimation()` 会 fallback 到 `estimate_price()`，见 `ppt2md_app\cost.py:24`。该 fallback 只覆盖少数旧模型，例如 `qwen3-vl-plus` 和 `qwen-plus`。

第三方或自定义模型价格通过 `config.vision_input_price_per_million`、`config.vision_output_price_per_million`、`config.brain_input_price_per_million`、`config.brain_output_price_per_million` 进入 `_find_model_record()`，见 `ppt2md_app\cost.py:246`。

### 8.3 估算假设

`show_cost_estimation()` 的当前固定假设：

- Stage 1 每页 prompt tokens 约 `300`。
- Stage 1 每页输出 tokens 约 `500`。
- Stage 2 每页输入 tokens 约 `3500`。
- Stage 2 每页输出 tokens 约 `800`。
- 图片 token 按每张图片逐页计算，而不是抽样。

优点：

- 会按真实图片尺寸逐页估算 Vision 输入。
- 会显示图片 token 均值和范围，有助于发现高分辨率图片导致的成本异常。
- 能使用本地静态价格表、动态模型目录价格或第三方自定义价格。

限制：

- Stage 1 输出 token、Stage 2 输入 token、Stage 2 输出 token都只是经验值。
- thinking/reasoning tokens 不一定被准确计入。
- 服务商上下文缓存、批处理价格、活动折扣、账号级计费策略无法准确预测。
- 如果第三方模型价格未知，则成本会偏低或显示不完整。

## 9. 模型选择与模型目录

模型相关逻辑横跨 `model_catalog.py`、`aliyun_catalog.py`、`model_settings.py` 和当前未提交的 `third_party_models.py`。

### 9.1 官方/内置模型目录

`ppt2md_app\model_catalog.py` 定义静态精选目录：

- `ModelPrice` 见 `ppt2md_app\model_catalog.py:12`。
- `ModelSpec` 见 `ppt2md_app\model_catalog.py:22`。
- `get_default_catalog()` 见 `ppt2md_app\model_catalog.py:45`。
- `static_to_records()` 见 `ppt2md_app\model_catalog.py:368`，把静态目录转换成 `aliyun_catalog.ModelRecord`。
- `merge_static_and_dynamic()` 见 `ppt2md_app\model_catalog.py:471`，合并静态目录和动态缓存。
- `load_model_catalog()` 见 `ppt2md_app\model_catalog.py:575`，作为模型目录统一入口。

静态目录包含 Vision 与 Brain 候选，例如：

- Vision：`qwen3-vl-plus`、`qwen3-vl-flash-2026-01-22`、`qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash`、`qwen3.5-flash`、`kimi-k2.6` 等。
- Brain：`qwen-plus`、`deepseek-v4-flash`、`deepseek-v4-pro`，以及部分多模态模型也可作为 Brain。

`ppt2md_app\aliyun_catalog.py` 负责动态抓取和验证：

- `ModelRecord` 数据结构见 `ppt2md_app\aliyun_catalog.py:227`。
- `fetch_model_ids_from_docs()` 见 `ppt2md_app\aliyun_catalog.py:274`，从公开阿里云文档页面提取模型 ID 并合并价格。
- `verify_openai_chat_model()` 见 `ppt2md_app\aliyun_catalog.py:510`。
- `verify_dashscope_multimodal_model()` 见 `ppt2md_app\aliyun_catalog.py:566`。
- `verify_all_capabilities()` 见 `ppt2md_app\aliyun_catalog.py:604`，更新 OpenAI text、OpenAI vision、DashScope multimodal 能力矩阵。
- `load_cache()` 与 `save_cache()` 分别见 `ppt2md_app\aliyun_catalog.py:745` 和 `ppt2md_app\aliyun_catalog.py:759`。

`cli.py` 中的模型目录命令由 `_handle_model_commands()` 处理，见 `ppt2md_app\cli.py:73`：

- `--refresh-models`：抓取候选并写入 `.cache\aliyun_model_catalog.json`。
- `--verify-models`：读取目录并用 API Key 探测模型能力，然后回写缓存。
- `--list-models` 和 `--list-all-models`：用 `_display_models_table()` 展示模型表，见 `ppt2md_app\cli.py:147`。

### 9.2 交互式模型选择

`ppt2md_app\model_settings.py:30` 的 `configure_models()` 是模型选择入口：

1. 调用 `load_model_catalog(prefer_cache=True, cache_path=config.model_cache_path)`。
2. 读取 `log\model_settings.json`。
3. 如果存在历史配置，询问是否沿用。
4. 如果不沿用，分别调用 `choose_model()` 选择 Vision 和 Brain。
5. 如果 Brain 默认可使用 DeepSeek 且检测到 `DEEPSEEK_API_KEY`，优先给出 `deepseek-v4-flash`。
6. 检查或提示保存所需 API Key。
7. 保存最终模型设置到 `log\model_settings.json`。

官方模型候选展示：

- Vision 展示由 `_print_vision_candidates()` 实现，见 `ppt2md_app\model_settings.py:156`。它使用 REC/CAN/FAIL 分层，并展示 OpenAI vision 与 DashScope multimodal 状态。
- Brain 展示由 `_print_brain_candidates()` 实现，见 `ppt2md_app\model_settings.py:199`。它展示 text 状态、价格、价格来源和 provider。

`_apply_record()` 见 `ppt2md_app\model_settings.py:263`，把 `ModelRecord` 应用到 `AppConfig`，包括 provider、model_id、base_url、api_key_env 和价格字段。

API Key 处理：

- `ppt2md_app\env.py` 通过 `get_env_value()` 读取环境变量。
- Windows 下优先读当前用户环境变量注册表，见 `ppt2md_app\env.py:12`。
- `_prompt_and_save_api_key()` 见 `ppt2md_app\model_settings.py:664`，可把用户粘贴的 key 写入当前用户环境变量；不写入仓库文件。
- `check_runtime_env()` 见 `ppt2md_app\files.py:44`，按当前 Vision/Brain provider 和 env 名称检查是否缺 key。

## 10. 未提交的第三方模型管理改动

这是当前分支最重要的未提交功能变化。必须按当前工作区内容研究，不能只看已提交版本。

### 10.1 config.py 新增第三方模型注册表路径

`ppt2md_app\config.py` 当前新增：

```text
third_party_models_path -> log\third_party_models.json
```

该属性位于 `ppt2md_app\config.py:109`，返回 `self.log_path / "third_party_models.json"`。

### 10.2 model_settings.py 从“自定义一次性模型”扩展为“第三方模型注册表”

当前 `ppt2md_app\model_settings.py` import 了 `third_party_models.py` 中的多项函数：

- `discover_openai_compatible_models`
- `filter_registry_models`
- `load_third_party_models`
- `parse_bulk_models_text`
- `upsert_third_party_model`
- `delete_third_party_model`

这说明第三方模型管理已经被接入交互式模型选择流程。

`choose_model()` 当前菜单从旧的 `c=自定义` 扩展为：

```text
默认编号
t = 第三方模型
c = 新增第三方模型
m = 管理第三方模型
```

相关入口：

- `choose_model()`：`ppt2md_app\model_settings.py:93`。
- `_print_third_party_candidates()`：`ppt2md_app\model_settings.py:230`。
- `_select_third_party_model()`：`ppt2md_app\model_settings.py:319`。
- `_manage_third_party_models()`：`ppt2md_app\model_settings.py:339`。
- `_create_third_party_model_wizard()`：`ppt2md_app\model_settings.py:386`。
- `_bulk_import_third_party_models()`：`ppt2md_app\model_settings.py:425`。
- `_discover_and_import_models()`：`ppt2md_app\model_settings.py:454`。
- `_edit_third_party_model()`：`ppt2md_app\model_settings.py:514`。
- `_delete_third_party_model()`：`ppt2md_app\model_settings.py:558`。
- `_verify_registry_item()`：`ppt2md_app\model_settings.py:584`。
- `_apply_registry_item()`：`ppt2md_app\model_settings.py:286`。

管理菜单支持：

- `a` 新增。
- `b` 批量导入。
- `d` 自动发现 OpenAI-compatible `/models`。
- `e` 编辑。
- `x` 删除。
- `s` 选择。
- `q` 返回。

### 10.3 third_party_models.py 注册表模型

`ppt2md_app\third_party_models.py` 是未跟踪新文件，当前职责是：

- 从 `log\third_party_models.json` 读取第三方模型。
- 保存第三方模型列表。
- upsert/delete 模型。
- 把注册表 item 转换为 `ModelRecord`。
- 按 role 过滤 Vision/Brain 模型。
- 解析批量导入文本。
- 调 OpenAI-compatible `/models` 自动发现模型。
- 规范化字段、roles、价格和去重 key。

关键函数：

- `load_third_party_models()`：`ppt2md_app\third_party_models.py:20`。
- `save_third_party_models()`：`ppt2md_app\third_party_models.py:36`。
- `upsert_third_party_model()`：`ppt2md_app\third_party_models.py:47`。
- `delete_third_party_model()`：`ppt2md_app\third_party_models.py:63`。
- `registry_item_to_model_record()`：`ppt2md_app\third_party_models.py:72`。
- `filter_registry_models()`：`ppt2md_app\third_party_models.py:101`。
- `parse_bulk_models_text()`：`ppt2md_app\third_party_models.py:105`。
- `discover_openai_compatible_models()`：`ppt2md_app\third_party_models.py:148`。
- `_normalize_registry_item()`：`ppt2md_app\third_party_models.py:193`。
- `_parse_roles()`：`ppt2md_app\third_party_models.py:216`。
- `_dedupe_key()`：`ppt2md_app\third_party_models.py:259`。

注册表支持的 provider 集合：

```text
dashscope
dashscope_openai
deepseek
openai_compatible
```

支持 role：

```text
vision
brain
both
```

`both` 会被规范化为 `[vision, brain]`。

### 10.4 第三方模型注册表 JSON 形态

`save_third_party_models()` 会写出如下顶层结构：

```json
{
  "version": 1,
  "updated_at": "2026-06-12T16:28:02Z",
  "models": []
}
```

每个模型条目由 `_normalize_registry_item()` 规范化，包含：

- `id`
- `name`
- `provider`
- `base_url`
- `api_key_env`
- `model_id`
- `roles`
- `supports_vision`
- `supports_thinking`
- `input_price`
- `output_price`
- `price_source`
- `note`
- `verification`
- `created_at`
- `updated_at`

当前实际存在的 `log\third_party_models.json` 保存了两个示例/实际条目：

- `vision-model`，provider 为 `openai_compatible`，roles 为 `vision`，模型 ID 为 `my-vision-model`，Base URL 为 `https://example.com/v1`。
- `gpt-5.4-mini`，provider 为 `openai_compatible`，roles 为 `vision` 和 `brain`，Base URL 为 `https://vip.lcodex.cn/v1`，API Key 环境变量名为 `VIP_LCODEX_API_KEY`。

该文件保存的是环境变量名，不保存 API Key 明文。

### 10.5 第三方模型管理的当前风险

第三方模型管理功能尚处在未提交状态，风险集中在以下方面：

1. `ppt2md_app\third_party_models.py` 是 untracked 文件。如果只提交 `config.py` 和 `model_settings.py`，运行时会因为 import 缺失而直接失败。
2. 该功能没有测试覆盖。新增的解析、upsert、delete、角色过滤、批量导入、自动发现和交互分支都依赖手工验证。
3. 自动发现只调用 OpenAI-compatible `/models`，并根据模型 ID 里的 `vision`、`vl`、`omni`、`image`、`multimodal` 推断视觉能力。这是启发式，不能证明模型真的支持图片输入。
4. 验证是可选操作；用户可以保存未经验证的模型。
5. 批量导入支持 JSON 或逗号分隔文本，但没有严格 schema 报错机制；无效字段会被 normalize 或忽略。
6. `registry_item_to_model_record()` 当前存在，但从已读 `model_settings.py` 看，交互选择第三方模型时直接用 `_apply_registry_item()`，并没有把第三方模型融合进官方模型表排序和能力矩阵中。第三方列表是单独展示的。
7. 第三方模型价格可以为空；成本估算会受影响。
8. Base URL、模型 ID、roles 都是用户输入，缺少 URL 格式校验和 provider-specific 能力约束。

## 11. 核心文件职责

### 11.1 `ppt2md.py`

根入口脚本，只做两件事：

- 从 `ppt2md_app.cli` import `main`。
- 调用 `main()`，捕获 `KeyboardInterrupt` 后返回 130。

这是薄入口，业务逻辑都在 `ppt2md_app`。

### 11.2 `ppt2md_app\cli.py`

职责：CLI 参数、依赖检查、配置构造、模型目录命令、主交互流程、Rich 进度条、多 PPT 任务进程调度。

关键位置：

- `parse_args()`：`ppt2md_app\cli.py:12`。
- `ensure_dependencies()`：`ppt2md_app\cli.py:35`。
- `build_config()`：`ppt2md_app\cli.py:50`。
- `configure_stdio()`：`ppt2md_app\cli.py:66`。
- `_handle_model_commands()`：`ppt2md_app\cli.py:73`。
- `_display_models_table()`：`ppt2md_app\cli.py:147`。
- `main()`：`ppt2md_app\cli.py:208`。

设计特点：

- 把模型目录命令和普通转换流程合在一个入口。
- 使用 Rich `Live` 和 `Progress` 展示所有任务的进度。
- 使用 `ProcessPoolExecutor` 支持多个 PPT 文件夹并行，但默认 worker 为 1。
- 通过 Manager Queue 汇总子进程消息。

风险点：

- `main()` 较长，聚合了启动、交互、成本预估、进程池和进度循环，未来维护复杂度会增长。
- 模型目录刷新和验证涉及网络，但没有专门的超时/错误 UI 分层。
- 主循环依赖 `msg_queue.empty()`，多进程队列的 empty 语义通常不适合做严格同步依据；当前结合 future done 轮询使用，实际可用但不是最强保证。

### 11.3 `ppt2md_app\pipeline.py`

职责：单个 PPT 任务的双阶段 pipeline 控制器。

关键函数：

- `process_single_ppt_task()`：`ppt2md_app\pipeline.py:10`。
- `_run_vision_stage()`：`ppt2md_app\pipeline.py:71`。
- `_run_brain_stage()`：`ppt2md_app\pipeline.py:139`。

设计特点：

- 明确先 Vision 后 Brain。
- 两个阶段各自用线程池并发。
- Vision 结果保存为 Raw JSON。
- Brain 结果保存为 Markdown。
- 最后调用 `merge_markdowns()` 汇总。

风险点：

- Raw cache 和 Slide skip 都是文件存在式判断，没有版本指纹。
- Stage 1 失败页以 `[Vision Failed]` 继续进入 Stage 2，可能生成质量不可控的 Markdown。
- Stage 2 写文件直接写最终路径，没有先写临时文件再原子 rename；进程中断可能留下部分文件，而下次运行若超过 100 字节会被跳过。

### 11.4 `ppt2md_app\models.py`

职责：API 调用、流式响应收集、Vision/Brain worker、Markdown 清洗、API Key 设置。

关键函数：

- `retry_with_backoff()`：`ppt2md_app\models.py:26`。
- `call_aliyun_openai_chat()`：`ppt2md_app\models.py:81`。
- `call_aliyun_openai_vision()`：`ppt2md_app\models.py:125`。
- `_collect_openai_stream()`：`ppt2md_app\models.py:198`。
- `_collect_openai_sync()`：`ppt2md_app\models.py:228`。
- `run_stage_1_vision()`：`ppt2md_app\models.py:246`。
- `_run_openai_compatible_vision()`：`ppt2md_app\models.py:357`。
- `get_raw_content()`：`ppt2md_app\models.py:387`。
- `run_stage_2_brain_parallel()`：`ppt2md_app\models.py:395`。
- `sanitize_stage_2_markdown()`：`ppt2md_app\models.py:417`。
- `_run_dashscope_brain()`：`ppt2md_app\models.py:464`。
- `_run_openai_compatible_brain()`：`ppt2md_app\models.py:501`。
- `_run_deepseek_brain()`：`ppt2md_app\models.py:525`。
- `set_dashscope_api_key()`：`ppt2md_app\models.py:589`。

设计特点：

- 同时支持 DashScope 原生 Vision、DashScope/OpenAI compatible Vision、DashScope 原生 Brain、OpenAI-compatible Brain 和 DeepSeek Brain。
- OpenAI-compatible Vision 会把本地图片读入并转为 base64 data URL。
- 流式响应解析会累积 `content` 和 `reasoning_content`。
- Brain 输出统一经过 `sanitize_stage_2_markdown()`。

风险点：

- 直接使用 `urllib.request` 手写 OpenAI-compatible streaming 解析，缺少 SDK 层封装和 token usage 信息。
- API 错误很多情况下被转成字符串返回，调用方可能把错误字符串写进 Markdown。
- `retry_with_backoff()` 定义了但没有系统应用。
- `sanitize_stage_2_markdown()` 只处理格式噪声，不验证内容真实性。
- Stage 2 的五页窗口虽然 prompt 约束严格，但没有程序化防止跨页内容泄漏。

### 11.5 `ppt2md_app\prompts.py`

职责：集中存放两阶段 prompt。

关键常量：

- `PROMPT_STAGE_1_VISION`：`ppt2md_app\prompts.py:1`。
- `PROMPT_STAGE_2_BRAIN`：`ppt2md_app\prompts.py:26`。

Stage 1 prompt 要求视觉模型做：

- OCR。
- 公式转 LaTeX。
- 判断 Figure 是否有知识信息量。
- 对有价值 Figure 输出详细自然语言几何描述。

Stage 2 prompt 要求 Brain 模型做：

- 只整理当前页。
- 用前后页只做 OCR 和符号校正。
- 输出从 `# Slide {slide_no}` 开始。
- 对 Figure Analysis 转成 `> [!NOTE] Figure 描述`。
- 必要时输出 `> [!WARNING] 原文勘误`。

风险点：

- 关键质量边界依赖 prompt，而不是程序约束。
- 没有 prompt 版本号，缓存无法判断 Raw Data 或 Markdown 是否来自旧 prompt。
- Stage 1 “不需要整理成 Markdown”，但 Stage 2 强依赖自然语言 Raw Data 的稳定性，缺少中间 schema。

### 11.6 `ppt2md_app\config.py`

职责：默认值与不可变配置对象。

关键内容：

- 默认模型和 provider：`ppt2md_app\config.py:6` 到 `ppt2md_app\config.py:9`。
- 默认输入/输出/log/cache 目录：`ppt2md_app\config.py:11` 到 `ppt2md_app\config.py:14`。
- 默认并发：`ppt2md_app\config.py:16` 到 `ppt2md_app\config.py:18`。
- 默认 thinking budget：`ppt2md_app\config.py:20` 到 `ppt2md_app\config.py:21`。
- API retry 默认值：`ppt2md_app\config.py:24` 到 `ppt2md_app\config.py:26`。
- API endpoint 和 env 名称：`ppt2md_app\config.py:29` 到 `ppt2md_app\config.py:33`。
- `AppConfig`：`ppt2md_app\config.py:41`。
- `model_settings_path`：`ppt2md_app\config.py:105`。
- `third_party_models_path`：`ppt2md_app\config.py:109`，当前未提交改动新增。

设计特点：

- dataclass frozen，减少意外原地修改。
- 路径通过 property 统一转换为 `Path`。

风险点：

- 并发默认值 60/60 较激进。
- retry 参数存在于 config，但主要模型调用未统一使用。
- session/model/cache 等路径没有版本命名空间；不同模型配置共享同一输出缓存。

### 11.7 `ppt2md_app\cost.py`

职责：图片 token 估算、文本 token 成本估算、Rich 成本表展示。

关键函数：

- `calculate_image_tokens()`：`ppt2md_app\cost.py:4`。
- `estimate_price()`：`ppt2md_app\cost.py:24`。
- `estimate_text_cost()`：`ppt2md_app\cost.py:59`。
- `_resolve_tier_price()`：`ppt2md_app\cost.py:112`。
- `estimate_flat_price()`：`ppt2md_app\cost.py:132`。
- `show_cost_estimation()`：`ppt2md_app\cost.py:141`。
- `_find_model_record()`：`ppt2md_app\cost.py:246`。

设计特点：

- 不只是按页数估算，而是逐图读取尺寸估算图片 token。
- 支持模型目录中的阶梯价格。
- 支持第三方/自定义模型的输入输出单价。

风险点：

- Stage 2 token 使用固定经验值。
- usage 不从真实 API 响应回填，因此无法形成实际成本审计。
- 对未知价格模型 fallback 可能低估。

### 11.8 `ppt2md_app\files.py`

职责：日志、输入目录检查、环境变量检查、文件扫描、自然排序、Markdown 合并、JSON 读写。

关键函数：

- `setup_logger()`：`ppt2md_app\files.py:13`。
- `ensure_input_folder()`：`ppt2md_app\files.py:33`。
- `check_runtime_env()`：`ppt2md_app\files.py:44`。
- `_required_api_envs()`：`ppt2md_app\files.py:80`。
- `natural_sort_key()`：`ppt2md_app\files.py:118`。
- `scan_ppt_folders()`：`ppt2md_app\files.py:123`。
- `extract_context()`：`ppt2md_app\files.py:139`。
- `merge_markdowns()`：`ppt2md_app\files.py:150`。
- `read_json()`：`ppt2md_app\files.py:169`。
- `write_json()`：`ppt2md_app\files.py:174`。

设计特点：

- 文件工具简单直接。
- 输入扫描规则清晰。
- runtime env 检查按实际 provider/env 组合去重。

风险点：

- `extract_context()` 还保留 `<CTX>` 解析能力，但当前 prompt 禁止 `<CTX>`，主流程也不依赖它；可能是遗留逻辑。
- `write_json()` 不带 indent，Raw 缓存可读性一般。
- JSON 写入没有临时文件和原子替换。

### 11.9 `ppt2md_app\model_settings.py`

职责：模型选择交互、模型设置持久化、API Key 辅助保存、第三方模型管理入口。

关键函数已在第 9 和第 10 节列出。

设计特点：

- 用户体验上比硬编码模型强很多：官方模型、历史模型配置、第三方模型、API Key 保存、价格字段都在同一流程里。
- 对 DeepSeek Brain 有便利默认：检测到 `DEEPSEEK_API_KEY` 时可优先使用 `deepseek-v4-flash`。
- 保存的是 API Key 环境变量名，不保存密钥。

风险点：

- 文件已经增长到较大体量，交互 UI、数据持久化、验证、第三方管理都在一个模块里。
- 大量 `input()` 分支难以自动测试。
- 第三方模型新增后，`model_settings.py` 强依赖未跟踪的 `third_party_models.py`。

### 11.10 `ppt2md_app\third_party_models.py`

职责：第三方模型注册表的数据层与 OpenAI-compatible discovery。详见第 10 节。

设计特点：

- 提供可持久化的第三方模型注册表，而不是一次性临时输入。
- 支持批量导入和 `/models` 发现。
- 有去重 key：provider、base_url、api_key_env、model_id。
- 不保存 API Key 明文。

风险点：

- 当前未提交。
- 缺少 tests。
- discovery 能力推断偏启发式。
- registry schema 没有迁移机制。
- `registry_item_to_model_record()` 尚未充分接入模型目录统一展示。

## 12. 现有优势

### 12.1 端到端可用性强

从 README、CLI 和源码看，项目已经覆盖真实用户批量处理所需的关键路径：

- 检查输入目录。
- 扫描任务。
- 选择页码范围。
- 选择模型。
- 检查 API Key。
- 成本预估。
- 并发调用模型。
- 保存中间缓存。
- 生成单页 Markdown。
- 合并汇总 Markdown。
- 日志记录。
- 断点续跑。

这比一个单纯“调用视觉模型生成 Markdown”的脚本成熟很多。

### 12.2 模型选择体验较完整

当前模型体验有三个层次：

1. 静态精选模型目录保证常用模型可用且有价格。
2. 动态缓存/验证支持从阿里云文档发现并验证新模型。
3. 当前未提交改动引入第三方模型注册表，支持 OpenAI-compatible 服务、批量导入和自动发现。

用户不必改源码就能切换 provider、model_id、base_url、api_key_env 和价格。

### 12.3 成本预估有实际价值

成本估算不是简单按页数乘固定值，而是逐图片读取尺寸估算图片 token，并按当前模型价格计算。它还能展示图片 token 均值和范围，对用户判断图片是否过大很有帮助。

### 12.4 断点续跑实用

断点续跑来自三层机制：

- session JSON 保存任务选择。
- Raw JSON 缓存 Stage 1。
- Slide Markdown 跳过 Stage 2。

对长文档、多页 PPT 或 API 不稳定环境，这个能力非常关键。

### 12.5 Vision/Brain 双阶段架构合理

把视觉识别和 Markdown 重组拆成两阶段，有几个实际优势：

- Vision 模型专注 OCR、公式识别和 Figure 描述。
- Brain 模型专注清洗、结构化、符号一致性和 Markdown 输出。
- Stage 2 可以使用前后页上下文修正当前页 OCR。
- Stage 1 Raw Data 可缓存，便于换 Brain 模型重新整理。

这个设计比单阶段“让视觉模型直接输出最终 Markdown”更可控，虽然当前仍缺少结构化中间表示。

## 13. 当前主要风险

### 13.1 LLM 直接生成 Markdown

当前最终 `Slide_XX.md` 由 Brain 模型直接生成，程序只做轻量 sanitize。风险包括：

- 模型可能把前后页内容带入当前页。
- 模型可能省略当前页内容。
- 模型可能改写公式、符号或表格。
- 模型可能生成看似合理但原图不存在的解释。
- 模型可能输出 Markdown 语法错误或 LaTeX 错误。

虽然 `PROMPT_STAGE_2_BRAIN` 对单页边界有非常明确的限制，但这仍是 prompt 约束，不是程序化保证。

### 13.2 缓存缺少版本指纹

当前 Raw JSON 缓存和 Slide Markdown 跳过都不校验版本。

缺失的关键指纹包括：

- 图片内容 hash。
- 图片路径和修改时间。
- Vision provider/model/base_url。
- Brain provider/model/base_url。
- Stage 1 prompt hash。
- Stage 2 prompt hash。
- thinking budget。
- 代码版本或 pipeline schema 版本。
- 输出格式 schema 版本。

后果是：用户改变模型或 prompt 后可能继续复用旧缓存，得到混合版本结果。

### 13.3 缺少结构化中间表示

Stage 1 输出是自然语言 Raw Data 字符串。它没有把内容拆成稳定字段，例如：

- 页面标题。
- 文本块。
- 公式块。
- 表格。
- Figure objects。
- 坐标或阅读顺序。
- OCR 置信度。
- 原始视觉模型 metadata。

这会导致：

- Stage 2 只能重新解释自然语言 Raw Data。
- 无法稳定验证“当前页内容是否全部被保留”。
- 无法做 deterministic Markdown renderer。
- 无法对公式、表格、Figure 分别做校验或重试。
- 无法局部修复某个块，只能整页再生成。

### 13.4 缺少系统性校验

当前校验主要是：

- 依赖 prompt 要求。
- `sanitize_stage_2_markdown()` 去掉代码围栏、`<CTX>`、寒暄并补标题。
- 文件大小大于 100 字节视为可跳过。

缺少的校验包括：

- Markdown parse/lint。
- LaTeX 公式语法检查。
- 当前页标题格式检查以外的结构检查。
- 禁止跨页内容泄漏的相似度或引用检查。
- Raw Data 与最终 Markdown 的覆盖率检查。
- Figure Analysis 是否正确变成 note block 的检查。
- 错误字符串是否被写入最终 Markdown 的检查。
- 输出为空、输出过短、输出包含 API error 的 fail-fast 机制。

### 13.5 缺少测试

当前仓库没有 `tests/` 目录，也没有匹配 `pytest`、`unittest` 或 `def test_` 的测试文件。风险尤其集中在：

- 页码范围解析。
- 自然排序。
- session 迁移与恢复。
- Raw cache 命中与损坏 fallback。
- Slide skip 策略。
- Markdown sanitize。
- OpenAI-compatible stream parser。
- 第三方模型 registry normalize/upsert/delete。
- 批量导入解析。
- 成本估算。
- provider/env 选择。

由于很多逻辑是交互式 `input()`，后续补测试时需要先把纯逻辑与交互层拆开，或对 `input()` 做 monkeypatch。

### 13.6 第三方模型管理未提交

这是当前分支的直接工程风险：

- `model_settings.py` 已 import `third_party_models.py`。
- `third_party_models.py` 仍是 untracked。
- 如果当前分支被切换、打包、提交或交给 CI 时漏掉该文件，应用会在导入阶段失败。
- 该功能同时修改了用户交互路径和持久化文件格式，但没有测试或迁移说明。

### 13.7 高默认并发与 API 限流风险

默认单阶段 60 线程并发对 API 服务商是强压力。虽然 README 说明多个 PPT 文件夹默认不并行，但单个 PPT 的页级并发仍可能触发：

- 429 限流。
- 连接超时。
- 服务商短时失败。
- 账号级并发限制。

当前 retry 策略不统一，失败页可能进入 `[Vision Failed]` 或错误字符串进入 Markdown。

### 13.8 错误字符串可能污染输出

多个模型调用函数在异常时返回字符串，例如：

- `OpenAI Stream Error: ...`
- `OpenAI Sync Error: ...`
- `Brain Error: ...`
- `DeepSeek Error: ...`
- `DeepSeek HTTP Error: ...`
- `DeepSeek Exception: ...`

Stage 2 调度层把 `future.result()` 视作 `final_markdown` 写入文件。虽然异常会被捕获并记录，但返回错误字符串并不是异常，因此可能被 sanitize 后写成 `Slide_XX.md`。

## 14. 建议改进方向

### 14.1 引入结构化中间表示

建议新增 Stage 1 输出 schema，例如：

```json
{
  "version": 1,
  "slide_no": 1,
  "source_image": {
    "path": "...",
    "sha256": "...",
    "width": 1920,
    "height": 1080
  },
  "model": {
    "provider": "dashscope",
    "id": "qwen3-vl-plus",
    "prompt_hash": "..."
  },
  "blocks": [
    {
      "type": "text",
      "text": "...",
      "order": 1
    },
    {
      "type": "formula",
      "latex": "...",
      "display": true,
      "order": 2
    },
    {
      "type": "figure",
      "description": "...",
      "order": 3
    }
  ],
  "warnings": []
}
```

不一定一步到位做复杂版；哪怕先把 Raw Text、Formula、Figure Analysis 分字段，也能显著提高可验证性。

### 14.2 为缓存增加指纹

Raw JSON 和 Slide Markdown 旁边应记录或内嵌 metadata：

- 输入图片 hash。
- Stage prompt hash。
- provider/model/base_url。
- thinking budget。
- code version。
- schema version。

重跑时只有指纹匹配才命中缓存。否则提示用户可选择复用、重建或只重建某阶段。

### 14.3 输出校验与失败隔离

建议至少增加以下校验：

- 最终 Markdown 必须以 `# Slide XX` 开始。
- 不允许包含明显 API error 前缀。
- 不允许包含 `<CTX>`。
- 不允许全文代码围栏。
- 公式 delimiter 基础平衡检查。
- 输出长度低于阈值时标记为失败，而不是缓存跳过。
- 如果 Stage 1 是 `[Vision Failed]`，Stage 2 输出应带明确 warning 或默认跳过，避免伪装成正常页。

### 14.4 测试优先级

建议先补不需要真实 API 的单元测试：

1. `session.parse_range_string()`。
2. `files.natural_sort_key()` 和 `scan_ppt_folders()`。
3. `models.sanitize_stage_2_markdown()`。
4. `cost.calculate_image_tokens()`。
5. `cost.estimate_text_cost()` 的阶梯价格。
6. `third_party_models._parse_roles()`、`parse_bulk_models_text()`、`upsert_third_party_model()`、`delete_third_party_model()`。
7. `model_settings.apply_model_settings()` 和 `_apply_registry_item()`。

然后再补 mock API 的集成测试，覆盖 Stage 1/Stage 2 缓存与跳过行为。

### 14.5 第三方模型管理先完成提交边界

第三方模型管理改动应作为一个完整变更提交，至少包含：

- `ppt2md_app\third_party_models.py`。
- `ppt2md_app\config.py` 中的 `third_party_models_path`。
- `ppt2md_app\model_settings.py` 中的交互流程修改。
- README 中对 `t/c/m` 菜单和 `log\third_party_models.json` 的说明更新。
- registry 相关单元测试。

如果短期不提交，则应避免在共享分支中保留 `model_settings.py` 对 untracked 文件的硬依赖。

### 14.6 降低默认并发或做自适应限流

建议把默认页级并发调低，或至少按 provider/model 提供并发档位：

- 低风险默认：5 到 10。
- 高并发模式：用户显式开启。
- 对 429/503 做指数退避和全局限流。
- 对不同 provider 使用独立 semaphore。

### 14.7 实际成本回填

如果 API 响应能拿到 token usage，建议把真实 usage 写入：

- `Raw_XX.json` metadata。
- `Slide_XX.md` sidecar metadata。
- `log`。
- 汇总成本报告。

这样成本估算可以逐步校准，而不是长期依赖经验值。

## 15. 总结

当前 `png2md` 工作区实际实现的是 `PPT2MD-V10`：一个基于图片目录输入、Vision/Brain 双阶段 LLM pipeline 的本地 CLI 工具。它已经具备端到端可用性、模型选择体验、成本预估、断点续跑、并发处理和日志记录。设计上最有价值的部分是把视觉提取和 Markdown 重组拆开，并用 Raw Data 缓存支撑长任务恢复。

当前最大风险也很清晰：最终 Markdown 仍由 LLM 直接生成，缺少结构化中间表示和系统性校验；缓存命中不带版本指纹，容易复用过期结果；测试体系为空；第三方模型管理改动已经接入主流程但仍未提交，其中 `third_party_models.py` 是 untracked 文件，必须作为当前功能的一部分处理。

如果后续目标是借鉴 MinerU 或类似文档解析系统的可靠性，优先方向应是：结构化 IR、缓存指纹、输出校验、错误隔离和测试覆盖，而不是继续只强化 prompt。

