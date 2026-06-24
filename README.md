# DocPage2MD

把 PDF、Office 文档、图片或旧版文档页图片目录转换成结构化 Markdown 笔记。

`DocPage2MD` 是 `Document Page to Markdown` 的缩写。项目当前主路径是通过 MinerU 精准解析 API 直接处理 PDF、图片、Doc/Docx、Ppt/PPTx、Xls/Xlsx 等多种格式，拿到 layout/json/crop 后再进入 DocPage2MD 的 Markdown-first 渲染、校验和 Brain 精修流程。PDF 尤其是手写矢量笔记 PDF，是 MinerU 路线的核心输入。

当前正式入口是 `docpage2md.py`，正式包名是 `docpage2md_app`，默认图片目录兼容入口是 `doc_pages/`。

当前有两条入口：

- `mineru_only` / `hybrid`：直接处理 PDF、Office 文档、图片，或读取已经下载/解压的 MinerU artifact 目录。这是新主路径。
- `vision_only`：读取旧版图片目录，例如：

```text
doc_pages/
└── 我的课件/
    ├── slide_01.png
    ├── slide_02.png
    └── ...
```

## 最快上手

如果你只是想把一个 PDF 转成 Markdown，推荐按下面做。

1. 把 PDF 放在你顺手的位置。可以放在项目外，也可以放在项目里的 `input_docs/`。`input_docs/` 已经被 Git 忽略，适合临时放自己的 PDF、Word、PPT、图片等私人文件。

```text
input_docs/
└── 我的手写笔记.pdf
```

2. 打开 PowerShell，进入项目目录。

```powershell
cd D:\Repos\lab-python\DocPage2MD
```

3. 转前 5 页先试效果。

```powershell
python docpage2md.py --engine-mode hybrid --input-file ".\input_docs\我的手写笔记.pdf" --page-ranges 1-5
```

4. 如果只想用 MinerU 快速转，不调用后续视觉/Brain 精修：

```powershell
python docpage2md.py --engine-mode mineru_only --input-file ".\input_docs\我的手写笔记.pdf" --page-ranges 1-5
```

5. 转完后看输出目录：

```text
markdown_output/
└── 我的手写笔记/
    ├── Slide_01.md
    ├── Slide_02.md
    ├── 我的手写笔记_FULL.md
    ├── run_report.json
    ├── assets/
    ├── ir/
    └── mineru_raw/
```

最常用的文件是 `Slide_XX.md` 和 `{文档名}_FULL.md`。`run_report.json`、`ir/`、`mineru_raw/` 是排错和审计用的。

## 输入文件放哪

单个 PDF、Word、PPT、Excel 或图片**不要求放在固定目录**。你可以直接传绝对路径：

```powershell
python docpage2md.py --engine-mode hybrid --input-file "D:\Notes\我的手写笔记.pdf" --page-ranges 1-10
```

也可以放进项目里的 `input_docs/`，这样命令短一点：

```powershell
python docpage2md.py --engine-mode hybrid --input-file ".\input_docs\我的手写笔记.pdf" --page-ranges 1-10
```

推荐习惯：

- 私人待处理文件：放 `input_docs/`，不会进 Git。
- 公开测试样本：放 `tests/fixtures/`，并确认内容可公开。
- 私有测试样本：不要提交；`tests/` 根目录下的 PDF/Office 文件默认会被 Git 忽略。
- 已经由 MinerU 客户端/API 解压的结果：用 `--mineru-artifact-dir` 指向那个目录。
- 旧版图片页目录：只在 `vision_only` 时放 `doc_pages/任务名/`。

## 如何选择文件

当前还没有真正的图形界面文件选择器，也没有文件浏览 GUI。可用方式有三种：

1. 直接指定一个文件：

```powershell
python docpage2md.py --engine-mode hybrid --input-file "D:\Notes\我的手写笔记.pdf"
```

2. 指定多个文件：

```powershell
python docpage2md.py --engine-mode mineru_only --input-files "D:\Docs\a.pdf" "D:\Docs\b.pptx" "D:\Docs\c.docx"
```

3. 指定一个文件夹，让程序筛选支持的文件：

```powershell
python docpage2md.py --engine-mode hybrid --input-folder "D:\Docs\待转录" --recursive
```

支持的多格式文件包括：

- `.pdf`
- `.png` / `.jpg` / `.jpeg` / `.webp` / `.bmp` / `.gif`
- `.doc` / `.docx`
- `.ppt` / `.pptx`
- `.xls` / `.xlsx`
- `.html` / `.htm`

Windows 上最快的选文件办法：

- 在资源管理器里选中文件，`Shift + 右键`，选择“复制为路径”。
- 把路径粘贴到 `--input-file` 后面。
- 如果路径外面带双引号，可以直接保留。

直接运行：

```powershell
python docpage2md.py
```

会进入交互式模式，让你选择文档类型、处理模式、模型档位和输入来源。但它目前是终端交互，不是 GUI 文件选择器。

计划中的 GUI 可以做成两层：

- 短期：终端里列出候选文件，让用户输入编号选择。
- 后续：真正的桌面/网页 GUI，支持拖拽 PDF、选择页码范围、选择模式和模型档位。

输出目录结构如下：

```text
markdown_output/
└── 我的文档/
    ├── Slide_01.md
    ├── Slide_02.md
    ├── 我的文档_FULL.md
    ├── run_report.json
    ├── assets/
    │   └── crops/
    ├── ir/
    └── mineru_raw/
```

## 从 0 开始

### 1. 安装 Python

如果你完全不熟悉电脑，先确认电脑里有没有 Python：

```powershell
python --version
```

如果提示找不到命令，请安装 Python 3.10 或更高版本。Windows 用户可以从 Python 官网下载安装包，安装时勾选 `Add python.exe to PATH`。

### 2. 进入项目目录

打开 PowerShell，进入本项目目录：

```powershell
cd D:\Repos\lab-python\DocPage2MD
```

如果你的项目放在其他位置，请把上面的路径替换成你自己的项目文件夹路径。

### 3. 安装依赖

```powershell
pip install -U -r requirements.txt
```

如果网络慢，可以多试一次。依赖主要是：

- `dashscope`：调用阿里云百炼 / 通义千问
- `rich`：终端 UI
- `Pillow`：读取图片尺寸，用于成本估算

### 4. 设置 API Key / Token

如果要直接处理 PDF、PPTX、Docx 等多格式文档，请先准备 MinerU token，并写入环境变量 `MINERU_API_TOKEN`。获取地址：<https://mineru.net/apiManage/token>。

如果要使用 docpage2md 的视觉模型和 Brain 精修，还需要：

- 阿里云百炼 / DashScope：`DASHSCOPE_API_KEY`，获取地址：<https://bailian.console.aliyun.com/cn-beijing?tab=model#/api-key>
- DeepSeek：`DEEPSEEK_API_KEY`，获取地址：<https://platform.deepseek.com/api_keys>

Windows PowerShell 长期设置，推荐：

```powershell
[Environment]::SetEnvironmentVariable("MINERU_API_TOKEN", "你的 MinerU Token", "User")
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-你的阿里云Key", "User")
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-你的DeepSeekKey", "User")
```

CMD 长期设置：

```cmd
setx MINERU_API_TOKEN "你的 MinerU Token"
setx DASHSCOPE_API_KEY "sk-你的阿里云Key"
setx DEEPSEEK_API_KEY "sk-你的DeepSeekKey"
```

Linux / macOS 临时设置：

```bash
export MINERU_API_TOKEN="你的 MinerU Token"
export DASHSCOPE_API_KEY="sk-你的阿里云Key"
export DEEPSEEK_API_KEY="sk-你的DeepSeekKey"
```

临时设置，只对当前 PowerShell 窗口有效：

```powershell
$env:MINERU_API_TOKEN="你的 MinerU Token"
$env:DASHSCOPE_API_KEY="sk-你的阿里云Key"
$env:DEEPSEEK_API_KEY="sk-你的DeepSeekKey"
```

设置后重新打开 PowerShell 更稳妥。

如果你使用 One API、OpenRouter、LiteLLM、自建转发等 OpenAI 兼容服务，也可以先不手动设置。运行程序后在模型选择界面输入 `c`，选择 `openai_compatible`，程序会提示你填写 Base URL、模型 ID、环境变量名，并可把 Key 保存到当前 Windows 用户环境变量。

本项目不会把 API Key / Token 写入仓库文件。模型设置、报告和缓存只保存环境变量名，例如 `MINERU_API_TOKEN`、`DASHSCOPE_API_KEY`、`DEEPSEEK_API_KEY`，不会保存密钥值。

### 5. 准备输入

新主路径可以直接给 MinerU 一个 PDF、PPTX、Docx、Excel 或图片文件，也可以给已经下载/解压好的 MinerU 输出目录。

文件可以放任意位置。为了方便管理，建议在项目根目录新建 `input_docs/`，把待处理 PDF、Word、PPT、图片临时放进去。这个目录已被 `.gitignore` 忽略，不会误提交。

```text
input_docs/
├── 我的手写笔记.pdf
├── 论文.pdf
└── 课件.pptx
```

如果你已经有 MinerU 客户端/API 输出目录，可以直接使用：

```powershell
python docpage2md.py --engine-mode hybrid --mineru-artifact-dir ".\tests\fixtures\mineru_public\minimal_artifact"
```

如果要让程序调用 MinerU API 处理本地 PDF：

```powershell
python docpage2md.py --engine-mode hybrid --input-file ".\我的手写笔记.pdf" --page-ranges 1-10
```

也可以传绝对路径：

```powershell
python docpage2md.py --engine-mode hybrid --input-file "D:\Notes\我的手写笔记.pdf" --page-ranges 1-10
```

如果要批量处理一个文件夹里的 PDF、PPTX、Docx、Excel 或图片：

```powershell
python docpage2md.py --engine-mode hybrid --input-folder ".\待处理文档" --recursive
```

程序会按后缀筛选 MinerU 支持的文件，不会要求你先把 PDF/PPT 拆成图片。

如果要精确指定多个文件：

```powershell
python docpage2md.py --engine-mode mineru_only --input-files ".\论文.pdf" ".\课件.pptx" ".\题目截图.png"
```

如果要处理远程 URL：

```powershell
python docpage2md.py --engine-mode mineru_only --mineru-url "https://example.com/paper.pdf"
```

旧版兼容路径仍然支持图片目录。在默认输入目录 `doc_pages` 下新建一个文件夹，文件夹名就是任务名：

```text
doc_pages/
└── 3.2点群/
    ├── 001.png
    ├── 002.png
    └── 003.png
```

支持的图片格式：

- `.png`
- `.jpg`
- `.jpeg`
- `.bmp`
- `.webp`

文件名建议带数字，程序会自然排序。

只有选择 `vision_only` 旧流程时，才需要自己把 PDF/PPT 导出成图片。新主路径会优先交给 MinerU 处理原文件。

### 6. 启动

```powershell
python docpage2md.py
```

如果需要指定会话名和输出目录：

```powershell
python docpage2md.py -n my_session -o .\markdown_output
```

如果传入 `--mineru-artifact-dir`、`--input-file`、`--input-files`、`--input-folder` 或 `--mineru-url`，程序会直接走 MinerU 多格式路线。没有传这些参数时，程序会进入交互式选择：默认推荐手写笔记 `hybrid`，也可以手动切到论文 PDF 的 `mineru_only`、截图小题的 `vision_only` 或自定义模式。旧版图片目录只是 `vision_only` 的兼容入口，不是项目的新主路径。

## 使用流程

MinerU 多格式路线大致会经历这些步骤：

1. 加载模型目录
2. 读取 MinerU artifact，或通过 MinerU API 提交 PDF / Office / 图片文件
3. 下载并解压 MinerU zip，读取 layout/json/crop 图片
4. 转换为 docpage2md 的 PageIR / BlockIR
5. 复制 crop 到输出目录 `assets/crops/`
6. 渲染干净的 `Slide_XX.md` 和 `{doc_name}_FULL.md`
7. 写入 `run_report.json`、`ir/` 和 `mineru_raw/`

`run_report.json` 会记录每页的 `content_inventory`：每个 MinerU/IR block 是否已经渲染、降级、合并、替换、删除或未渲染。正文 Markdown 不会输出这些诊断文字；如果需要排查遗漏，优先看 report。

旧版 `vision_only` 图片目录流程仍会经历：选择视觉模型、选择 Brain 模型、扫描 `doc_pages`、选择页码范围、成本预估、生成 Markdown。

旧版图片目录页码范围支持：

```text
回车 / all    全部
1-10          第 1 到 10 页
50-end        第 50 页到最后
8             只处理第 8 页
```

## 生成原理：从文档到 Markdown

完整说明见 [文档到 Markdown 的生成原理](docs/architecture/docpage-to-markdown-pipeline.md)。README 这里只放短版。

相关设计文档：

- [Hybrid MinerU + docpage2md 架构](docs/architecture/hybrid-mineru-docpage2md.md)
- [模型管理器架构](docs/architecture/model-manager.md)
- [Markdown 输出契约](docs/architecture/markdown-output-contract.md)
- [MinerU API 配置](docs/architecture/mineru-api-setup.md)
- [当前接手状态](docs/maintenance/current-status.md)
- [Changelog](docs/changelog.md)

当前流程不是让模型直接“看图写 Markdown”后就保存，而是分成识别、结构化、重组、校验和保守回退几层：

```text
PNG/JPG 页面图片
  -> Step 1 Vision 识别 Raw Data
  -> PageIR / BlockIR 结构化中间层
  -> Step 2 Brain 用前后页上下文重组 Markdown
  -> Markdown refiner 做有限格式修复
  -> Validator 检查格式、公式、表格、图示和内容覆盖
  -> 正常写入 Slide_XX.md，或 fail-open 回退到 PageIR 确定性渲染
  -> 合并生成 任务名_FULL.md，并写 run_report.json
```

核心原则是：最终产物仍然是 Markdown，但内部会保留 Raw JSON、PageIR、稳定 block id、provenance 和 run report，用来防止公式、图表、手写文字等内容被静默遗漏。

### Step 1: Vision 识别

对每张图片做 OCR、公式识别、图形结构描述和表格识别，输出 Raw Data。

默认模型：

```text
dashscope:qwen3-vl-plus
```

也可以选择 Qwen3.7-Plus、Qwen3.6-Flash、Qwen3.5-Flash 等视觉模型，或配置自定义 OpenAI-compatible 视觉 API。

Step 1 的结果会写入：

```text
markdown_output/任务名/temp_raw_vision/Raw_XX.json
```

Raw cache 会记录图片 hash、模型身份、prompt 版本、pipeline 版本、PageIR blocks 和质量信息。缓存命中前会校验这些指纹，避免旧版本结果污染新流程。

### PageIR / BlockIR

Raw Data 会被解析成弱结构化 PageIR。每个 block 都有稳定 ID，例如 `p0003-b002`。常见 block 类型包括：

- `heading`
- `paragraph`
- `list`
- `formula_inline`
- `formula_block`
- `table`
- `figure_note`
- `image_ref`
- `uncertain`

这些 block 是后续校验、防遗漏和报告追踪的依据。

### Step 2: Brain 重组

Step 2 使用前后各 2 页 Raw Data，也就是 5 页滑动窗口，把当前页整理成 Markdown。

推荐模型：

```text
deepseek:deepseek-v4-flash
```

它便宜、上下文长，适合做 Markdown 清洗、公式修正、跨页上下文判断。

### Refiner / Validator / Fail-open

Step 2 输出后还会经过两道保护：

1. `refiner` 做有限格式修复，例如补 `# Slide N`、去掉全文代码围栏、清理模型寒暄、规范公式环境，把 `\tag{n}` 移到 `aligned` 外层。
2. `validator` 检查最终 Markdown 是否可信，包括 API 错误文本、公式分隔符、表格结构、邻页泄漏、OCR 覆盖率和目标 block 覆盖率。

目标 block 覆盖率是防遗漏的核心：如果 Step 1 已经识别到文字、公式、表格、图示或不确定内容，但 Step 2 最终 Markdown 没有保留，系统会产生类似下面的 warning：

```text
target_text_block_missing
target_formula_block_missing
target_table_block_missing
target_figure_block_missing
target_uncertain_block_missing
target_image_ref_block_missing
```

这些 warning 会触发 fail-open：程序不把漏内容的 Brain 输出当作正常结果，而是用 Stage 1 PageIR 进行确定性 Markdown 渲染。回退结果可能不如 Brain 输出漂亮，但优先保证已经识别出的内容不被静默删掉。

## 并行是否真实

当前程序是真实并行，但要注意它是“两阶段并行”，不是两个阶段同时交错跑。

具体是：

1. Step 1 对同一个文档页图片任务的所有目标图片用 `ThreadPoolExecutor` 并发调用视觉模型。
2. 等 Step 1 全部完成或命中缓存后，Step 2 再对所有目标页并发调用 Brain 模型。
3. 多个文档页图片任务之间还可以用进程池并行，但默认 `DEFAULT_MAX_DOCPAGE_WORKERS = 1`；默认值为 1 是为了避免同时处理多个大任务导致 API 限流。

这样设计是为了让 Step 2 能看到完整的前后页 Raw Data。

## ETA 是否准确

终端里的剩余时间来自 Rich 进度条，它根据当前完成速度估算。

它不是 API 级精确预测，因为：

- 每页图片大小不同
- 模型响应时间波动很大
- API 可能限流或重试
- 有些页面命中缓存会瞬间完成
- 输出长度不可提前准确知道

所以 ETA 只能作为粗略参考。真实耗时会写入日志，例如：

```text
Step 1 完成，耗时 62.4s，缓存 3，提交 20，失败 0
Step 2 完成，耗时 41.8s，跳过 0，提交 23，失败 0
全部流程结束，总耗时 105.2s
```

## 日志和缓存

日志文件：

```text
log/log_default_YYYYMMDD_HHMMSS.log
```

会话文件：

```text
log/sessions/session_default.json
```

模型偏好：

```text
log/model_settings.json
```

模型目录缓存：

```text
.cache/aliyun_model_catalog.json
```

中间视觉缓存：

```text
markdown_output/任务名/temp_raw_vision/Raw_01.json
```

如果任务中断，直接重新运行。程序会跳过已有的 Raw Data 和已有的 `Slide_XX.md`。

## 模型选择

交互 UI 默认只展示精选主力模型，避免把阿里云文档里抓到的大量旧版、快照、弃用候选都显示出来。

常用选择：

| 阶段 | 便宜 | 平衡 | 强力 |
| --- | --- | --- | --- |
| Step 1 视觉 | qwen3.5-flash / qwen3.5-27b / qwen3-vl-flash | qwen3-vl-plus / qwen3.6-flash / qwen3.7-plus | qwen3.7-max-2026-06-08 / qwen3.7-max / kimi-k2.6 |
| Step 2 Brain | deepseek-v4-flash | deepseek-v4-pro / qwen3.7-plus | qwen3.7-max / kimi-k2.6 |

当前精选 Vision 目录包含：

```text
qwen3-vl-plus
qwen3-vl-flash-2026-01-22
qwen3.7-plus
qwen3.7-plus-2026-05-26
qwen3.7-max
qwen3.7-max-2026-06-08
qwen3.6-plus
qwen3.6-plus-2026-04-02
qwen3.6-flash
qwen3.6-27b
qwen3.5-plus
qwen3.5-plus-2026-04-20
qwen3.5-flash
qwen3.5-27b
kimi-k2.6
```

模型目录命令：

```powershell
# 查看精选模型
python docpage2md.py --list-models

# 从阿里云文档抓取完整候选目录
python docpage2md.py --refresh-models

# 用 API 探针验证模型能力
python docpage2md.py --verify-models --verify-limit 20

# 查看完整缓存目录，仅用于诊断
python docpage2md.py --list-all-models
```

说明：

- DeepSeek 价格可以从官方文档页尽力刷新。
- 阿里云百炼控制台页面是前端渲染页面，不是稳定公开 JSON API，所以 Qwen 价格主要采用本地维护的精选价格表。
- Kimi-K2.6 按 DashScope OpenAI 兼容路径调用，价格采用模型卡中的 `6.5/27 元/百万 tokens`。
- 新模型可以用“自定义模型”录入。

## 自定义 API

在模型选择时输入 `c` 可以配置自定义模型。

支持的 API 类型：

```text
dashscope          阿里云 DashScope 原生接口
dashscope_openai   阿里云 OpenAI 兼容接口
deepseek           DeepSeek OpenAI 兼容接口
openai_compatible  其他 OpenAI 兼容接口
```

自定义 OpenAI-compatible API 需要填写：

```text
Base URL
API Key 环境变量名
模型 ID
输入价格 元/百万 tokens
输出价格 元/百万 tokens
```

示例：OpenRouter

```text
Provider: openai_compatible
Base URL: https://openrouter.ai/api/v1
API Key 环境变量名: OPENROUTER_API_KEY
模型 ID: qwen/qwen3-vl-32b-instruct
```

然后设置环境变量：

```powershell
[Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "你的Key", "User")
```

程序也可以在交互过程中帮你把 key 写入当前用户环境变量，但不会写入仓库文件。

## 成本估算

成本估算现在按每张图片逐页计算，不再只抽样前几张。

它考虑了：

- 每张图片的尺寸不同
- Qwen3-VL 的图像 token 估算
- 输入 token 和输出 token 单价不同
- 本地价格表中的阶梯计费：按输入 token 所在区间选择输入价和输出价
- 自定义模型价格

仍然只能近似，因为：

- 输出 token 数在调用前未知
- 思考 token 数在调用前未知
- 服务商活动折扣、缓存命中、Batch 价格可能变化
- 阿里云控制台价格页不是稳定公开 API

成本表中的 `图片Token均值/范围` 可以帮你判断图片是否过大。如果图片 token 很高，通常说明分辨率很高，成本和耗时都会上升。

## 推荐工作流

### 低成本批处理

```text
Vision: qwen3.5-flash、qwen3.5-27b 或 qwen3-vl-flash
Brain: deepseek-v4-flash
```

适合清晰教材页、普通课件页。

### 质量优先

```text
Vision: qwen3.7-plus、qwen3.6-flash 或 qwen3-vl-plus
Brain: deepseek-v4-pro
```

适合公式较多、图表较复杂的材料。

### 疑难页兜底

```text
Vision: qwen3.7-max-2026-06-08、qwen3.7-max 或 kimi-k2.6
Brain: deepseek-v4-pro、qwen3.7-max 或 kimi-k2.6
```

只建议少量页使用，成本明显更高。

## 常见问题

### 未检测到 API Key

先看报错里提示的是哪个环境变量。默认阿里云是：

```powershell
echo $env:DASHSCOPE_API_KEY
```

DeepSeek 是：

```powershell
echo $env:DEEPSEEK_API_KEY
```

其他自定义服务则检查你在模型选择里填写的环境变量名。如果为空，重新设置，例如：

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-你的Key", "User")
```

重新打开 PowerShell 后再运行。

### 输出目录里已经有文件，会不会重复扣费

程序会跳过：

- 已存在的 `temp_raw_vision/Raw_XX.json`
- 已存在且大小超过 100 字节的 `Slide_XX.md`

所以中断后可以直接重跑。

### 为什么 Step 2 要等 Step 1 全部完成

因为 Step 2 需要前后各 2 页 Raw Data。如果边识别边重组，后文窗口可能不完整，会降低符号一致性和上下文判断质量。

### 能不能直接处理 PDF、PPTX、Docx

可以。新主路径通过 MinerU 精准解析 API 处理 PDF、图片、Doc/Docx、Ppt/PPTx、Xls/Xlsx 等格式，并把 MinerU 输出的 layout/json/crop 图片转换成最终 Markdown。

示例：

```powershell
python docpage2md.py --engine-mode hybrid --input-file ".\我的讲义.pdf" --page-ranges 1-20
python docpage2md.py --engine-mode mineru_only --input-file ".\课件.pptx"
```

只有在选择 `vision_only` 旧流程时，才需要先把 PPT/PDF 导出成图片并放入 `doc_pages/任务名/`。

### 单个 PDF 应该放在哪里

没有强制位置。推荐两种：

- 临时私人文件：放 `input_docs/`，这个目录不会进 Git。
- 任意本地路径：用 `--input-file "完整路径"` 指定。

示例：

```powershell
python docpage2md.py --engine-mode hybrid --input-file ".\input_docs\我的手写笔记.pdf" --page-ranges 1-10
python docpage2md.py --engine-mode hybrid --input-file "D:\Notes\我的手写笔记.pdf" --page-ranges 1-10
```

### 有没有方便筛选文件的 GUI

当前没有图形文件选择器。现在最方便的是：

- 单文件用 `--input-file`。
- 多文件用 `--input-files`。
- 整个文件夹用 `--input-folder`，程序自动筛选 PDF、Office、图片和 HTML。
- 直接运行 `python docpage2md.py` 可以进入终端交互式选择，但不是 GUI。

后续可以把“列出文件夹内候选文件并输入编号选择”作为最近一步改进，再考虑真正的拖拽式桌面/网页 GUI。

### 为什么日志里显示失败，但最终还有 Markdown

如果某页视觉失败，程序会把该页 Raw Data 标为 `[Vision Failed]`，Step 2 仍会继续尝试生成。请优先查看日志和对应 `Slide_XX.md`。

## 目录结构

```text
ProjectRoot/
├── docpage2md.py
├── docpage2md_app/
│   ├── aliyun_catalog.py
│   ├── cli.py
│   ├── config.py
│   ├── cost.py
│   ├── env.py
│   ├── files.py
│   ├── model_catalog.py
│   ├── model_settings.py
│   ├── models.py
│   ├── pipeline.py
│   ├── prompts.py
│   └── session.py
├── input_docs/      # 可选，本地私人输入文件；不会进 Git
├── doc_pages/
├── markdown_output/ # 本地输出；不会进 Git，不应自动删除
├── latex_output/    # 可选 LaTeX 输出；不会进 Git，不应自动删除
├── log/             # 本地日志；不会进 Git，可做轮转
├── .cache/
└── requirements.txt
```

## 费用声明

本工具会调用阿里云 DashScope、DeepSeek 或你配置的第三方 API。运行会产生 token 费用。任务开始前请认真查看成本预估，实际账单以服务商为准。

## 许可证

本项目使用 MIT License，详见 [LICENSE](LICENSE)。
