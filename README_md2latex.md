# MD2LaTeX Pro 📚

> **学术级 Markdown 转 LaTeX 排版引擎**
> 专为处理由 `ppt2md` 生成的长篇课堂笔记 Markdown 设计，能够智能重构文档结构、修正 OCR 错误并输出符合严格学术规范的 LaTeX 源码。

## 🌟 核心特性

*   **⚡ 智能分块并行 (Smart Chunk Parallelism)**：
    *   **Context-Aware**: 自动将长 Markdown 拆分为适合 LLM 处理的 Chunks（~4000 字符），同时保留 **前文** 和 **后文** 上下文，确保逻辑连贯。
    *   **Nested Concurrency**: 采用 **Nested Parallel** 模式，单章节内部支持 **60+ 并发**，极速完成转录。

*   **🏗️ 文档结构自动重建 (Structure Reconstruction)**：
    *   **Structure Mapping**: 自动分析 Markdown 中的 Slide 边界和摘要信息。
    *   **Intelligent Heading**: 能够识别“内容接续”还是“新话题开始”，自动插入丢失的 `\section`、`\subsection` 标记，拒绝扁平化文档。

*   **💾 断点续传与缓存 (Resume & Cache)**：
    *   **Intermediate Storage**: 所有中间分块结果即时保存到 `latex_output/intermediates/`。
    *   **Metadata Tracking**: 自动提取并保存每个分块中定义的 **公式 Label**、**符号定义** 到 JSON 文件，方便后续索引。
    *   程序中断后，再次运行将自动加载缓存，仅处理未完成的 Chunks。

*   **🔍 交互式过滤 (Interactive Filter)**：
    *   支持按 **章节** 选择，也支持 **精确到页码** (例如: `Slide 1-10, 50-60`) 的细粒度过滤。
    *   内置 **成本预估 (Cost Estimator)**，在运行前自动计算字符数与预估 Token 费用。

## 🛠️ 使用指南

### 1. 启动

```bash
# 默认读取 ./markdown_output 输出到 ./latex_output
python md2latex.py

# 自定义路径
python md2latex.py -i ./my_markdown -o ./my_tex
```

### 2. 交互流程

1.  **扫描目录**: 程序会自动列出 `markdown_output` 下所有可用的章节。
2.  **选择任务**:
    *   `a`: 全选
    *   `1,3-5`: 选择特定章节
3.  **高级过滤 (可选)**:
    *   输入 `y` 进入页码筛选模式。
    *   针对选中的章节，输入范围 (如 `10-20`) 仅重做该部分，或回车处理整章。
4.  **成本确认**: 确认预估价格后开始执行。

## 📂 输出结构

```text
latex_output/
├── 广相笔记第五章.tex         # 最终合并的完整 LaTeX 文件 (Clean, No Markdown fences)
└── intermediates/            # 中间缓存目录 (不要轻易删除)
    └── 广相笔记第五章/
        ├── chunk_000.tex     # 第 1 部分 LaTeX 源码
        ├── chunk_000.json    # 第 1 部分 Metadata (Labels/Terms)
        ├── chunk_001.tex
        └── ...
```

## 🧠 技术细节

*   **上下文窗口**: 每个 Prompt 包含 `Pre-Chunk` (800 chars) + `Current-Chunk` (4000 chars) + `Next-Chunk` (800 chars)。
*   **结构感知**: 利用 `Slide_XX.md` 中的 `<CTX>` 元数据，构建全局目录树，防止在 PPT 分页处重复生成 Section 标题。
*   **Prompt Engineering**: 包含严格的 LaTeX 约束（禁 `$$`，强制 `equation`，强制 `\label`），并内置了 `TikZ` 绘图提示保留逻辑。

---
**依赖**: 需要 `rich` 和 `dashscope` 库。
**模型**: 默认使用 `qwen3-max-preview` (Logic Strong) 以确保 LaTeX 语法准确性。