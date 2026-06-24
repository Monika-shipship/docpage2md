# mineru-refine 与 docpage2md 对比及 docpage2md 精进路线图

研究对象：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine`
- `D:\Repos\lab-python\docpage2md`

本报告依赖的既有研究报告：

- `D:\Repos\lab-python\docpage2md\docs\research\mineru-refine-research.md`
- `D:\Repos\lab-python\docpage2md\docs\research\docpage2md-research.md`

本报告只对比两份报告已经建立的事实，并针对少数关键点回看源码核对。没有重新做泛泛项目介绍，没有运行真实模型调用，也没有运行测试。当前正式项目名是 `DocPage2MD`，实际包名是 `docpage2md_app`。

## 0. 研究边界与已验证事实

本报告写入目标是：

- `D:\Repos\lab-python\docpage2md\docs\research\comparison-and-docpage2md-roadmap.md`

本次只允许创建或写入这一份报告文件。当前主工作区已有未提交改动：

- `docpage2md_app\config.py`
- `docpage2md_app\model_settings.py`
- `docpage2md_app\third_party_models.py`
- `docs\research\mineru-refine-research.md`
- `docs\research\docpage2md-research.md`

本报告不会建议把这些未提交改动当作已经稳定发布的能力；只把它们视为当前分支中已经接入或正在接入的工程事实。

额外核对过的关键源码点包括：

- `docpage2md_app\pipeline.py`：`process_single_docpage_task()`、`_run_vision_stage()`、`_run_brain_stage()`。
- `docpage2md_app\models.py`：`run_stage_1_vision()`、`run_stage_2_brain_parallel()`、`sanitize_stage_2_markdown()`、错误字符串返回路径。
- `docpage2md_app\prompts.py`：两阶段 prompt 对单页边界、Figure 描述和 Markdown 输出的约束。
- `docpage2md_app\config.py`：默认并发、默认模型、`model_settings_path`、`third_party_models_path`。
- `docpage2md_app\model_settings.py` 与 `docpage2md_app\third_party_models.py`：第三方模型注册表已经被模型选择流程 import。
- `mineru-refine\crates\mineru-refine\src\types.rs`：`MineruItem`、`RefItem`、`SuspectKind`、`OpCall`、`RefineResult`、`RefineReport`。
- `mineru-refine\crates\mineru-refine\src\id.rs`：稳定内部 ID 分配与出口剥离。
- `mineru-refine\crates\mineru-refine\src\ops.rs`：`apply_op_checked()` 单一操作入口、reject 与 fidelity rollback。
- `mineru-refine\crates\mineru-refine\src\invariant.rs`：字符子集、表格主体、几何保真检查。
- `mineru-refine\crates\mineru-refine\src\agent_loop.rs`：suspect worklist、固定工具集、observe/dismiss/op loop、视觉裁决分支。
- `mineru-refine\crates\mineru-refine\src\refine.rs`：fail-open、cache key、opt-in OCR confusion、opt-in garbled table rewrite/degrade。
- `mineru-refine\crates\mineru-refine\src\markdown.rs`：结构化 items 到 Markdown 的确定性渲染。

## 1. 总体结论

`mineru-refine` 和当前 `docpage2md` 都在解决“模型参与的文档到 Markdown 转换质量问题”，但两者所处抽象层和对 LLM 的授权边界完全不同。

`mineru-refine` 的核心不是端到端 OCR，而是对 MinerU 已产出的 `content_list` 做结构化后处理。它的输入已经是 item 数组，输出仍是同 schema 的 item 数组。LLM 不直接重写全文，只能面对 detector 生成的局部 suspect，在固定工具集中选择 observe、受限 op 或 dismiss。所有 op 都经 `apply_op_checked()` 执行，并通过字符、表格和几何保真闸门。失败时 fail-open，返回原输入或已安全产物，并在 `report` 中记录。

当前 `docpage2md` 的核心是端到端本地 CLI 工作流：读取图片目录，Stage 1 Vision 生成自然语言 Raw Data，Stage 2 Brain 用五页窗口直接生成 `Slide_XX.md`，最后合并成 `{doc_name}_FULL.md`。它已经有模型选择、成本估算、并发、日志和断点续跑，但结构化中间层较弱，最终 Markdown 的正确性主要依赖 prompt 与 `sanitize_stage_2_markdown()`，程序侧尚不能证明没有跨页泄漏、遗漏、误改或 API 错误字符串污染。

因此，`docpage2md` 不应该短期照搬 `mineru-refine` 的 Rust core、多语言绑定或 MinerU 字段规则。真正应迁移的是工程契约：

- 结构化中间层。
- 稳定内部 ID。
- detector 先定位疑点。
- LLM 只裁决有限操作。
- 操作单入口落地。
- 保真、覆盖率、边界和结构质量闸门。
- fail-open 与错误隔离。
- cache key 版本指纹。
- report、provenance、token/cost 审计。
- mock 模型测试和 golden fixture。

路线图建议按四阶段推进：

- v1 最小改造：不改变主流程形态，先补缓存指纹、错误隔离、运行报告、原子写入、第三方模型管理边界和基础测试。
- v2 结构化中间层：在 Raw Data 之外新增 Page IR / Block IR，并把最终 Markdown 渲染逐步改为确定性 renderer。
- v3 linter/refiner：引入 detector、suspect、受限 op、`apply_op_checked`、LLM 裁决和 Markdown/LaTeX/跨页泄漏 linter。
- v4 测试与质量闸门：用 mock 模型、golden fixtures、幂等测试、缓存失效测试和 CI 质量门把 v1-v3 固化。

## 2. 两项目共同点

两项目的共同点不是实现语言或输入 schema，而是问题空间：

1. 都把 LLM/VLM 放进文档转换链路。
   - `mineru-refine` 使用文本 LLM 裁决结构疑点，特定表格问题使用视觉裁决或视觉重转写。
   - `docpage2md` 使用 Vision 模型做 OCR/公式/Figure 描述，再使用 Brain 模型生成 Markdown。

2. 都面对长文档和批处理。
   - `mineru-refine` 用 worklist、进度回调、cache key 和 report 支撑可审计长任务。
   - `docpage2md` 用图片目录扫描、页级并发、日志、Raw JSON 缓存、Slide 文件跳过和 session 恢复支撑长任务。

3. 都需要模型配置管理。
   - `mineru-refine` cache key 会把 refine logic version、模型、prompt version 和 opt-in flags 纳入输出身份。
   - `docpage2md` 当前已经有官方模型目录、阿里云模型缓存、DeepSeek 便利路径，以及未提交的第三方模型注册表。

4. 都需要错误可恢复。
   - `mineru-refine` 通过 fail-open 保守返回。
   - `docpage2md` 当前遇到 Vision 失败会给该页填入 `[Vision Failed]` 并继续，Stage 2 出错路径也多以字符串返回；这保证流程不中断，但还缺少“失败输出不可伪装成正常 Markdown”的闸门。

5. 都有输出 Markdown 的目标。
   - `mineru-refine` 的 Markdown 是从结构化 item 确定性渲染出来的派生产物。
   - `docpage2md` 的 Markdown 是 Brain 模型直接生成后轻量 sanitize 的主产物。

6. 都已经有“分阶段处理”的雏形。
   - `mineru-refine` 分为机械清洗、agent loop、opt-in garbled rewrite/degrade、opt-in confusion。
   - `docpage2md` 分为 Stage 1 Vision 和 Stage 2 Brain。

共同点说明：`docpage2md` 不需要推翻当前两阶段 pipeline，而是应该在两阶段之间和 Stage 2 之后补上结构化契约、报告、缓存指纹和质量闸门。

## 3. 核心差异

| 维度 | mineru-refine | 当前 DocPage2MD | 对 DocPage2MD 的含义 |
|---|---|---|---|
| 输入 | MinerU `content_list` item 数组 | MinerU 多格式 artifact/API、PDF/Office/图片文件，以及兼容图片目录 | DocPage2MD 必须同时处理 MinerU layout/crop 和 OCR/视觉理解源头，不能直接套 MinerU 的 item schema |
| 输出主合同 | 输入输出同 schema，返回 `items/provenance/report` | `Raw_XX.json`、`Slide_XX.md`、`FULL.md` | docpage2md 需要新增中间合同，不能只靠文件存在 |
| 中间表示 | `MineruItem` + `RefItem` + stable id | `raw_data_map: {slide_no: raw_text}`，Raw Data 是自然语言字符串 | docpage2md 的局部修复能力受限，应建立 Page IR / Block IR |
| Markdown 生成 | `render_markdown(items)` 确定性渲染 | Brain 模型直接生成整页 Markdown | 应逐步把 Markdown 变成 IR 的派生产物 |
| LLM 权力 | LLM 只能裁决固定工具和有限 op | Brain 可直接改写、组织、生成整页 Markdown | LLM 权力边界需要缩小到“裁决/建议”，至少对 OCR 文本和跨页内容如此 |
| 保真机制 | 字符子集、表格主体、几何检查和回滚 | prompt 约束 + `sanitize_stage_2_markdown()` | 需要程序化验证覆盖率、边界、错误字符串、Markdown/LaTeX 结构 |
| 失败策略 | fail-open，report 标记 `failOpen` | 失败页可能继续进入 Stage 2，错误字符串可能写入 Markdown | 应把失败页和错误字符串隔离为失败产物，不缓存为成功 |
| 缓存身份 | `sha256 + logic version + model + prompt version + flags` | Raw cache 看 `Raw_XX.json`，Slide skip 看文件大小 `>100` | 需要 manifest/fingerprint，否则换模型或 prompt 会误用旧缓存 |
| 测试体系 | detector、ops、invariant、loop、refine、confusion、garbled、markdown 测试 | 当前报告未发现 `tests/` 和 pytest/unittest 测试 | 精进路线不能只改 prompt，必须先补可离线测试层 |
| 产品形态 | Rust core + CLI/HTTP/Python/JS/plugin 多形态 | 本地交互式 Python CLI | 短期继续 Python CLI 更现实，不应优先引入 Rust/PyO3 |

## 4. 抽象层级差异

### 4.1 mineru-refine 的抽象层级

`mineru-refine` 的抽象层级从低到高是：

1. 原始 JSON item：`MineruItem(pub Map<String, Value>)`，未知字段原样透传。
2. 内部 item：`RefItem { id, item }`，处理期间有稳定 ID，出口剥离。
3. 疑点：`SuspectKind` / `WorkItem`，由确定性 detector 产生。
4. 操作：`OpCall`，包括 `merge`、`split`、`demote`、`promote`、`reorder`、`drop`、`strip`、`deleteChar`、`mergeTable`、`mergeList`、`extractCaption`、`dropCaption`。
5. 操作执行：`apply_op_checked()`，统一校验参数、执行、保真检查、reject 或落地。
6. 结果：`RefineResult { items, provenance, report }`。
7. Markdown：`render_markdown(items)`，从结构化 item 确定性派生。

这个层级让每一步都可以被测试、回滚和审计。

### 4.2 当前 docpage2md 的抽象层级

当前 `docpage2md` 的抽象层级从低到高是：

1. 图片任务：`scan_docpage_folders()` 返回 `{任务名: [图片路径]}`。
2. 运行配置：`AppConfig` 保存模型、provider、base_url、API key env、并发、目录等。
3. Stage 1 Raw Data：`Raw_XX.json` 中主要使用 `raw_text`。
4. Stage 2 Prompt：五页 Raw Data 窗口被填入 `PROMPT_STAGE_2_BRAIN`。
5. Markdown 文件：`Slide_XX.md` 直接由 Brain 模型输出，经 `sanitize_stage_2_markdown()` 清理。
6. 汇总：`merge_markdowns()` 合并 `Slide_*.md` 为 `{doc_name}_FULL.md`。

这个层级缺少中间结构。程序知道“第几页有一段 Raw Text”和“第几页有一份 Markdown”，但不知道 Markdown 中哪些段落来自哪个 OCR 块、哪个公式、哪个表格、哪个 Figure 描述，也不知道某个修复是否只是移动/删除，还是模型新增。

### 4.3 直接后果

抽象层级差异导致两类工程后果：

1. 局部修复能力不同。
   - `mineru-refine` 能只修一个 item、一个 caption、一处 OCR 衍字或两个相邻表格。
   - 当前 `docpage2md` 如果发现一页 Markdown 有问题，通常只能重跑整页 Stage 2，甚至重跑 Stage 1。

2. 质量验证能力不同。
   - `mineru-refine` 可以在 op 落地时判断是否新增字符、破坏表格主体或产生非法几何。
   - 当前 `docpage2md` 只能做表层 sanitize，无法稳定判断“Target 页内容是否全部保留且没有混入前后页”。

因此，`docpage2md` 的优先精进方向不是继续强化 prompt，而是降低最终输出对“整页自由生成”的依赖。

## 5. LLM 权力边界差异

### 5.1 mineru-refine 的 LLM 边界

`mineru-refine` 的 LLM 权力边界非常窄：

- detector 先定位 suspect，LLM 不负责全局寻找问题。
- 每个 suspect 只给局部上下文。
- LLM 可以 observe，但 observe 也是固定工具。
- LLM 最终只能给一个固定 op 或 dismiss。
- op 参数必须引用稳定 ID。
- 程序执行 op，而不是 LLM 返回修改后的全文。
- `apply_op_checked()` 失败时 reject，原 items 不动。
- 出口还有异常数不单调、保真闸门和 fail-open。
- OCR confusion 和 garbled table rewrite 被放在 opt-in 层，并进入 provenance。

这意味着 LLM 是“裁判”和“建议器”，不是“写入者”。

### 5.2 当前 docpage2md 的 LLM 边界

当前 `docpage2md` 的 LLM 权力边界更宽：

- Stage 1 Vision 负责 OCR、公式 LaTeX、Figure Analysis，输出自然语言 Raw Data。
- Stage 2 Brain 接收五页窗口后直接生成当前页完整 Markdown。
- prompt 明确禁止跨页补写，但程序没有结构化证据证明模型遵守。
- `sanitize_stage_2_markdown()` 只去掉代码围栏、`<CTX>`、寒暄，并补 `# Slide {slide_no}`。
- `_run_dashscope_brain()`、`_run_openai_compatible_brain()`、`_run_deepseek_brain()` 的一些错误路径会返回字符串，调度层会把 `future.result()` 当成最终 Markdown 写入文件。

这意味着 Brain 模型当前是“作者”和“结构编辑器”，程序只做轻度收尾。

### 5.3 docpage2md 需要的分层授权模型

`docpage2md` 不能简单采用 `mineru-refine` 的“核心层不新增字符”作为全局规则，因为它的输入是图片，图像理解本身会产生文本化描述，尤其 Figure Analysis 不是原图里的逐字文本。但可以按内容来源分层授权：

- OCR 文本块：应尽量满足覆盖率和不跨页新增合同。允许清理空白、修正少量 OCR 混淆，但必须有 provenance。
- 公式块：允许从图像转写为 LaTeX，但必须通过语法和平衡检查，且保留原 Raw/截图引用。
- 表格块：允许结构化为 Markdown/HTML 表格，但应有行列一致性和来源截图或 Raw evidence。
- Figure 描述块：允许生成自然语言描述，但必须标记为 `origin: "vision_description"`，不能与 OCR 正文混在同一保真合同里。
- 最终 Markdown：尽量由确定性 renderer 生成。LLM 可以建议 block 顺序、标题层级、OCR 混淆修正或 Figure 描述整理，但不应无边界重写整页。

## 6. 应迁移到 docpage2md 的 mineru-refine 设计

以下设计应迁移，迁移的是思想和合同，不是照抄 Rust 代码。

### 6.1 稳定内部 ID

应迁移。`docpage2md` 的页、块、表格、公式、Figure 描述都应有稳定 ID，例如 `pg_0001`、`blk_0001_0003`、`tbl_0001_0001`。所有 refiner op 都引用 ID，而不是数组下标或 Markdown 行号。

迁移价值：

- merge/split/drop/reorder 后仍能定位对象。
- report/provenance 可回溯。
- 缓存、测试和 UI 定位更稳定。

### 6.2 结构化中间层

应迁移。`docpage2md` 需要 Page IR / Block IR。即使 Stage 1 仍保留 Raw Text，也应并行产出或后处理出结构化 blocks。

迁移价值：

- Markdown renderer 可确定性。
- linter 可按 block 类型检查。
- Stage 2 可从“整页生成”降权为“结构整理与局部裁决”。

### 6.3 detector 先生成 suspect

应迁移。`docpage2md` 应先用规则发现疑点，例如空页、过短输出、API error 字符串、跨页内容泄漏、疑似标题误判、公式 delimiter 不平衡、Figure Analysis 未转为 note、表格行列异常，再决定是否调用 LLM。

迁移价值：

- 节省 token。
- 疑点可单测。
- LLM 不负责盲搜全局问题。

### 6.4 有限 op 与统一执行入口

应迁移。`docpage2md` 应定义 `DocPage2MDOp`，由 `apply_op_checked()` 或同等函数统一执行。最小 op 可包括：

- `dropBlock`
- `stripText`
- `mergeBlocks`
- `splitBlock`
- `setHeadingLevel`
- `reorderBlocks`
- `replaceOcrChar`
- `markGenerated`
- `markFailed`
- `convertFigureAnalysisToNote`
- `normalizeFormula`

迁移价值：

- LLM 不能直接改全文。
- 每类修改都有 reject 条件和测试。
- 所有删除、替换、生成都能审计。

### 6.5 保真与质量闸门

应迁移，但要按来源分层。`docpage2md` 不应照搬“输出字符必须是输入字符子集”到所有块，而应定义：

- OCR 文本覆盖率闸门。
- 当前页边界闸门。
- Markdown 结构闸门。
- LaTeX 基础语法闸门。
- API error 污染闸门。
- cache manifest 版本闸门。
- 表格结构闸门。
- 生成内容 provenance 闸门。

迁移价值：

- 错误不会静默变成成功缓存。
- 可以明确区分“安全削减”“OCR 替换”“视觉生成描述”。

### 6.6 fail-open 与失败隔离

应迁移。`docpage2md` 的 fail-open 不应表现为把错误字符串写成 `Slide_XX.md`。更合适的是：

- 保留上一阶段安全产物。
- 生成 `.failed.json` 或在 page report 中标记失败。
- 对最终 Markdown 写入明确 warning 或跳过该页。
- 失败页不满足成功缓存条件。

### 6.7 report 与 provenance

应迁移。`docpage2md` 应新增任务级和页级 report：

- 每页 Stage 1/Stage 2/refine 状态。
- 使用的 provider/model/base_url/prompt hash。
- input image hash。
- token usage 或估算。
- op counts。
- removed spans。
- generated spans。
- OCR replacement provenance。
- linter violations。
- fail-open 状态。

### 6.8 cache key 版本指纹

应迁移。当前 Raw cache 和 Slide skip 只看文件存在或大小，风险很高。应迁移 `mineru-refine` 的 cache key 思想，把输入 hash、模型身份、prompt version/hash、logic version、schema version、flags、thinking budget 纳入缓存身份。

### 6.9 mock 模型测试

应迁移。`mineru-refine` 的测试价值不在 Rust，而在 mock chat、mock vision、golden input、idempotence、fail-open 和 reject 测试。`docpage2md` 的模型调用必须抽象到可 mock，否则后续 refiner 无法稳定测试。

## 7. 不应迁移或不应立即迁移的设计

### 7.1 不应短期迁移 Rust core 与多语言绑定

当前 `docpage2md` 是 Python CLI 项目，主要模块都在 `docpage2md_app`。短期改成 Rust core 或 PyO3/napi 会增加构建、发布、调试和 Windows 环境复杂度。除非未来有明确多语言 SDK 或性能瓶颈，否则应先在 Python 中迁移架构契约。

### 7.2 不应照搬 MinerU 字段和 detector

`mineru-refine` 规则依赖 `type`、`text_level`、`table_body`、`table_caption`、`img_path`、`page_idx`、`bbox`、`list_items` 等 MinerU 字段。当前 `docpage2md` 没有这些字段。直接翻译 `detect.rs` 会产生错配。应先定义 `docpage2md` 自己的 Page IR，再设计 detector。

### 7.3 不应把“no new character”作为全局合同

`docpage2md` 的输入是图片，模型需要把图像转成文字、公式和 Figure 描述。Figure 描述本质是视觉解释，无法要求字符来自 Raw OCR。应把 no-new-char 改成来源分层合同，而不是全局规则。

### 7.4 不应一开始引入完整 agent loop

`mineru-refine` 的 agent loop 有 observe、多轮、并发、矛盾裁决、视觉裁决和振荡保护。`docpage2md` 当前没有结构化 IR 和 op executor，过早引入完整 loop 会把复杂度压在薄弱基础上。应先做 single-pass detector + op executor + mock tests，再考虑多轮 observe。

### 7.5 不应默认开启 OCR confusion 和视觉表格重转写

OCR 混淆、乱码表视觉重转写和降级在 `mineru-refine` 中都是 opt-in。`docpage2md` 的基础结构尚未稳定，不应默认打开高风险生成式修复。应先做审计和闸门，再以显式开关启用。

### 7.6 不应把 HTTP server、plugin、多语言分发作为近期重点

当前用户价值主要来自本地 CLI 批处理。HTTP/server/plugin 可以以后做，但 v1-v4 的基础可靠性比部署形态更关键。

## 8. 当前 docpage2md 风险清单

以下风险来自 `docpage2md-research.md` 和本次源码核对。

1. Stage 1 Raw cache 没有版本指纹。
   - `_run_vision_stage()` 命中 `Raw_XX.json` 后读取 `data["raw_text"]` 即复用。
   - 没有校验图片 hash、Vision model、prompt、thinking budget 或 schema version。

2. Stage 2 Slide skip 没有版本指纹。
   - `_run_brain_stage()` 对 `Slide_XX.md` 只判断存在且大小大于 100 字节。
   - 换 Brain model、prompt 或 Raw Data 后仍可能跳过旧输出。

3. Stage 2 直接生成整页 Markdown。
   - `run_stage_2_brain_parallel()` 把五页 Raw Data 填进 prompt。
   - Prompt 限制强，但程序无法证明没有跨页泄漏。

4. 错误字符串可能污染 Markdown。
   - `_run_dashscope_brain()`、`_run_openai_compatible_brain()`、`_run_deepseek_brain()` 有返回 `Brain Error:`、`OpenAI Brain Error:`、`DeepSeek Error:` 等字符串的路径。
   - `_run_brain_stage()` 把 `future.result()` 直接写入 `Slide_XX.md`。

5. Vision 失败页继续进入 Brain 阶段。
   - `_run_vision_stage()` 失败时给 `raw_data_map[slide_no] = "[Vision Failed]"`。
   - Stage 2 仍可能为该页生成一份看似正常的 Markdown。

6. 缺少结构化中间表示。
   - Stage 1 prompt 要求“直接输出提取到的内容，不需要整理成 Markdown 格式”。
   - Raw Data 是自然语言字符串，不是可验证 blocks。

7. 缺少测试体系。
   - 既有研究报告未发现 `tests/` 目录，也未发现 pytest/unittest 测试。

8. 第三方模型管理处于未提交但已接入状态。
   - `model_settings.py` 已 import `third_party_models.py`。
   - `third_party_models.py` 是当前未提交的新文件。
   - 若漏提交或回滚该文件，模型选择流程存在导入失败风险。

## 9. v1 最小改造路线图

v1 目标：不重写业务主流程，不引入大规模 IR，不改变用户操作路径。先把现有两阶段 pipeline 的“成功/失败/缓存/模型身份/报告”变得可验证。

### v1.1 增加运行 manifest 与缓存指纹

目标：

- 让 Raw cache 和 Slide skip 不再只看文件存在或大小。
- 防止换图片、模型、prompt、provider、base_url、thinking budget 后复用旧产物。

涉及模块：

- `docpage2md_app\pipeline.py`
- `docpage2md_app\models.py`
- `docpage2md_app\prompts.py`
- `docpage2md_app\config.py`
- `docpage2md_app\files.py`
- 可新增 `docpage2md_app\manifest.py`

推荐接口/数据结构：

```python
DOCPAGE2MD_PIPELINE_VERSION = "docpage2md-pipeline-v1"
PROMPT_STAGE_1_VERSION = "stage1-p1"
PROMPT_STAGE_2_VERSION = "stage2-p1"

@dataclass(frozen=True)
class ModelIdentity:
    role: str
    provider: str
    model: str
    base_url: str
    api_key_env: str
    thinking_budget: int | None

@dataclass(frozen=True)
class PageCacheFingerprint:
    slide_no: int
    image_sha256: str
    image_size: tuple[int, int] | None
    pipeline_version: str
    stage1_prompt_hash: str
    stage2_prompt_hash: str | None
    vision_model: ModelIdentity | None
    brain_model: ModelIdentity | None
    flags: dict
```

Raw cache 文件可扩展为：

```json
{
  "schema_version": 1,
  "status": "ok",
  "fingerprint": {},
  "raw_text": "...",
  "usage": null,
  "error": null
}
```

Slide 可增加 sidecar：

```text
Slide_01.md
Slide_01.meta.json
```

失败模式：

- manifest 生成失败：不使用缓存，重新计算，并在任务 report 中记录 `cacheFingerprintError`。
- 旧 Raw JSON 没有 manifest：默认视为 legacy cache，可以提示或按配置选择复用；建议 v1 默认不命中，避免混版本污染。
- prompt hash 计算不稳定：统一从 `PROMPT_STAGE_1_VISION`、`PROMPT_STAGE_2_BRAIN` 原始字符串 SHA256 得到。
- base_url 含尾斜杠差异导致缓存错失：fingerprint 前做规范化，例如 `rstrip("/")`。

测试方案：

- 单元测试：同一图片、同一配置生成相同 fingerprint。
- 单元测试：换 model、base_url、prompt、thinking budget、image hash 后 fingerprint 改变。
- 集成测试：存在 legacy `Raw_01.json` 时不会被误判为新缓存。
- 集成测试：`Slide_01.md` 存在但 meta 不匹配时会重建而不是跳过。

### v1.2 错误隔离与 fail-open 输出合同

目标：

- 防止 `Brain Error:`、`OpenAI Brain Error:`、`DeepSeek Error:`、`[Vision Failed]` 被当成成功 Markdown。
- 让失败页可见、可重试、不可污染成功缓存。

涉及模块：

- `docpage2md_app\pipeline.py`
- `docpage2md_app\models.py`
- `docpage2md_app\files.py`
- 可新增 `docpage2md_app\status.py`

推荐接口/数据结构：

```python
@dataclass(frozen=True)
class StageResult:
    ok: bool
    slide_no: int
    content: str = ""
    error: str = ""
    provider: str = ""
    model: str = ""
    usage: dict | None = None
```

Brain worker 不应返回裸字符串，可返回：

```python
StageResult(ok=True, slide_no=1, content=markdown)
StageResult(ok=False, slide_no=1, error="DeepSeek HTTP Error: ...")
```

页级状态可写入：

```json
{
  "slide_no": 1,
  "stage1": {"status": "ok|failed|cache_hit"},
  "stage2": {"status": "ok|failed|skipped|cache_hit"},
  "final": {"status": "ok|failed|fail_open"}
}
```

失败模式：

- Stage 1 失败：Stage 2 默认跳过该页，写 `Slide_XX.failed.md` 或 `Slide_XX.error.json`，不写成功 `Slide_XX.md`。
- Stage 2 返回错误：保留 Raw cache，写 error sidecar，不写成功 Markdown。
- sanitize 后输出过短或只包含错误前缀：标记失败。
- 中断导致半写 Markdown：通过临时文件和原子替换规避。

测试方案：

- mock Stage 1 失败，断言不生成成功 `Slide_XX.md`。
- mock Brain 返回 `DeepSeek Error:`，断言写 error sidecar 且不缓存成功。
- mock sanitize 后空内容，断言 page status 为 failed。
- 模拟中断前临时文件存在，断言下次运行不会把 `.tmp` 当成功输出。

### v1.3 原子写入与成功标记

目标：

- 避免进程中断留下半个 `Slide_XX.md`，下次因为大于 100 字节而跳过。
- 把“文件写完”与“内容通过基础校验”绑定。

涉及模块：

- `docpage2md_app\pipeline.py`
- `docpage2md_app\files.py`

推荐接口/数据结构：

```python
def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    ...

def atomic_write_json(path: Path, data: dict) -> None:
    ...

def is_successful_slide(output_path: Path, meta_path: Path, expected_fingerprint: dict) -> bool:
    ...
```

成功 meta 至少包含：

```json
{
  "schema_version": 1,
  "status": "ok",
  "fingerprint": {},
  "validated_at": "..."
}
```

失败模式：

- 写入 meta 成功但 Markdown 写失败：成功判断必须要求两者都存在且 fingerprint 匹配。
- Markdown 写成功但 meta 写失败：下次不跳过，重新生成或校验。
- 文件系统 rename 失败：保留 `.tmp` 并记录 error，不把 `.tmp` 纳入 merge。

测试方案：

- 单元测试 `atomic_write_text()` 不留下成功文件之外的半成品。
- 集成测试 `Slide_01.md` 存在但 `Slide_01.meta.json` 缺失时不会跳过。
- 集成测试 meta status 为 `failed` 时不会跳过。

### v1.4 最小 Markdown 与 LaTeX 输出校验

目标：

- 在仍由 Brain 直接生成 Markdown 的阶段，先建立最低质量闸门。
- 防止显而易见的坏输出进入成功路径。

涉及模块：

- `docpage2md_app\models.py`
- `docpage2md_app\pipeline.py`
- 可新增 `docpage2md_app\validators.py`

推荐接口/数据结构：

```python
@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    message: str
    location: dict | None = None

def validate_slide_markdown(markdown: str, slide_no: int) -> list[ValidationIssue]:
    ...
```

v1 最小规则：

- 必须以 `# Slide {slide_no}` 开始。
- 不允许包含 `<CTX>`。
- 不允许全文被代码围栏包裹。
- 不允许以 `Brain Error:`、`OpenAI Brain Error:`、`DeepSeek Error:`、`DeepSeek HTTP Error:`、`OpenAI Stream Error:` 等错误前缀作为正文。
- 输出正文长度低于阈值时标记 warning 或 failure。
- `$...$`、`$$...$$` 做基础平衡检查。

失败模式：

- 校验 false positive：v1 可以把部分规则设为 warning，不阻断；但错误前缀必须阻断。
- 公式中合法 `$` 被误判：基础检查只做 delimiter 数量和平衡，不做复杂 LaTeX parse。
- 模型输出 `# Slide 001`：允许前导零。

测试方案：

- 对 `sanitize_stage_2_markdown()` 和 `validate_slide_markdown()` 加单元测试。
- 覆盖代码围栏、`<CTX>`、寒暄、错误前缀、缺标题、空输出、公式不平衡。
- 使用参数化测试覆盖 `Slide 1`、`Slide 01`、`Slide 001`。

### v1.5 任务级 report

目标：

- 让一次运行的输入、模型、缓存命中、失败页、估算成本和实际输出状态可复盘。
- 为 v2-v4 的 provenance 和质量闸门提供承载格式。

涉及模块：

- `docpage2md_app\pipeline.py`
- `docpage2md_app\cost.py`
- `docpage2md_app\files.py`
- 可新增 `docpage2md_app\report.py`

推荐接口/数据结构：

```json
{
  "schema_version": 1,
  "pipeline_version": "docpage2md-pipeline-v1",
  "doc_name": "...",
  "pages": [
    {
      "slide_no": 1,
      "image_path": "...",
      "image_sha256": "...",
      "stage1": {"status": "ok", "cache": "hit|miss"},
      "stage2": {"status": "ok", "cache": "hit|miss"},
      "validation": {"errors": [], "warnings": []}
    }
  ],
  "models": {
    "vision": {},
    "brain": {}
  },
  "summary": {
    "ok": 0,
    "failed": 0,
    "cache_hits": 0,
    "estimated_cost": null,
    "actual_usage": null
  }
}
```

输出位置建议：

```text
{output_folder}\{doc_name}\run_report.json
```

失败模式：

- report 写入失败：不应使转换失败，但必须在日志中记录。
- 并发写 report：v1 可在单任务进程内收集后一次写入，避免多线程同时写。
- 多次运行覆盖 report：可保留 `run_report_latest.json`，同时按时间戳归档。

测试方案：

- mock 两页，一页 cache hit，一页失败，断言 report summary 正确。
- 验证 report 中模型身份与 `AppConfig` 一致。
- 验证 report 不包含 API Key 明文，只包含 env var 名。

### v1.6 第三方模型管理纳入或隔离

目标：

- 明确当前未提交的第三方模型管理改动在路线图中的位置。
- 防止后续缓存、报告和 refiner 直接依赖一个未稳定的数据层。

涉及模块：

- `docpage2md_app\config.py`
- `docpage2md_app\model_settings.py`
- `docpage2md_app\third_party_models.py`
- `docpage2md_app\cost.py`
- 后续 `manifest.py` / `report.py`

推荐接口/数据结构：

先抽象“已解析模型身份”，让 pipeline 不关心模型来自官方目录、历史设置还是第三方注册表：

```python
@dataclass(frozen=True)
class ResolvedModelConfig:
    role: str
    provider: str
    model_id: str
    base_url: str
    api_key_env: str
    supports_vision: bool | None = None
    supports_thinking: bool | None = None
    input_price: float | None = None
    output_price: float | None = None
    price_source: str | None = None
    registry_id: str | None = None
```

纳入策略：

- 若第三方模型管理要成为 v1 基础能力，应补齐 `third_party_models.py` 的测试、README 说明、registry schema version 和迁移策略。
- manifest/report 只记录 `ResolvedModelConfig` 的安全字段，不记录 API Key 明文。
- cache fingerprint 纳入 provider、model_id、base_url、api_key_env、thinking budget、registry_id。价格字段不影响模型输出，可不进 fingerprint。

隔离策略：

- 若短期不稳定，应让后续 v1-v3 的核心 pipeline 只依赖 `AppConfig` 或 `ResolvedModelConfig`，不直接 import `third_party_models.py`。
- `third_party_models.py` 只属于交互式模型选择层。
- 如果该文件未提交或不可用，基础转换和报告不应因 import 失败而崩溃。

失败模式：

- `model_settings.py` import 未跟踪文件失败：当前分支风险，必须在纳入前解决。
- 第三方 registry 中 model roles 标错：Vision 阶段可能选到不支持图像的模型，应在选择或运行前校验。
- `/models` discovery 推断 supports_vision 错误：只能作为候选标记，不应作为强保证。
- 用户修改 base_url 但 registry_id 不变：fingerprint 必须仍因 base_url 改变而失效。

测试方案：

- 单元测试 `parse_bulk_models_text()`、`upsert_third_party_model()`、`delete_third_party_model()`、`filter_registry_models()`。
- 单元测试 `_apply_registry_item()` 或等效解析函数不会保存 API Key 明文。
- 单元测试同一 registry item 改 base_url 后 fingerprint 改变。
- 集成测试第三方 Brain 模型配置进入 report 和成本估算。

## 10. v2 结构化中间层路线图

v2 目标：让 Stage 1 产物从“自然语言 Raw Data 字符串”升级为可验证 Page IR，同时保留 Raw Text 作为兼容和审计材料。

### v2.1 定义 Page IR / Block IR

目标：

- 建立 `docpage2md` 自己的结构化中间表示。
- 为 renderer、linter、refiner 和 provenance 提供共同数据合同。

涉及模块：

- 可新增 `docpage2md_app\ir.py`
- `docpage2md_app\models.py`
- `docpage2md_app\pipeline.py`
- `docpage2md_app\files.py`

推荐接口/数据结构：

```python
@dataclass
class PageIR:
    schema_version: int
    slide_no: int
    source_image: dict
    raw_text: str
    blocks: list[BlockIR]
    warnings: list[str]
    model: dict

@dataclass
class BlockIR:
    id: str
    type: str  # "heading" | "paragraph" | "formula" | "table" | "figure_note" | "list" | "image" | "unknown"
    text: str = ""
    level: int | None = None
    items: list[str] | None = None
    latex: str | None = None
    table: dict | None = None
    figure: dict | None = None
    origin: str = "vision_ocr"
    confidence: float | None = None
    source_span: dict | None = None
```

失败模式：

- Stage 1 模型无法直接输出 JSON：v2 可以先用 Raw Text parser 生成弱 IR，保留 `type: "unknown"`。
- JSON 解析失败：保存 Raw Text，Page IR status 为 `partial`，不阻断旧流程。
- Block 类型误判：允许 refiner 后续修正，但必须保留原始 `raw_text`。

测试方案：

- 单元测试 Page IR 序列化/反序列化。
- 单元测试 block ID 稳定生成。
- 用固定 Raw Text fixture 测试 parser 输出稳定。
- 测试未知字段透传或保留在 `extra` 字段中。

### v2.2 Stage 1 结构化输出兼容层

目标：

- 不一次性改掉 Vision prompt，而是在 Raw Data 外新增结构化提取路径。
- 支持新旧缓存共存。

涉及模块：

- `docpage2md_app\models.py`
- `docpage2md_app\prompts.py`
- `docpage2md_app\pipeline.py`
- `docpage2md_app\manifest.py`

推荐接口/数据结构：

Stage 1 输出可逐步变为：

```json
{
  "schema_version": 2,
  "status": "ok",
  "fingerprint": {},
  "raw_text": "...",
  "page_ir": {
    "schema_version": 1,
    "slide_no": 1,
    "blocks": []
  }
}
```

Prompt 可先要求模型在 Raw Text 之后附一个 JSON 区块，但不建议 v2 立即完全依赖模型 JSON。更稳妥路径：

- 先用程序从当前 Raw Text 中识别 `### Figure Analysis`、公式块、标题候选和段落。
- 再评估是否调整 Vision prompt 直接产出结构化 JSON。

失败模式：

- 模型输出 JSON 和 Raw Text 不一致：以 Raw Text 为审计源，IR 标记 `validation.warning`。
- 结构化解析漏掉公式：保留在 paragraph block 中，不丢内容。
- 旧 `Raw_XX.json` 无 `page_ir`：可在读取时惰性生成 weak IR。

测试方案：

- 旧 Raw cache 迁移测试。
- `### Figure Analysis` 转 `figure_note` block 测试。
- 公式 delimiter block 识别测试。
- JSON 解析失败 fallback 测试。

### v2.3 确定性 Markdown renderer

目标：

- 把最终 Markdown 从“模型直接产物”逐步变成 Page IR 的派生产物。
- 让 Markdown 输出可测试、可复现、可局部修复。

涉及模块：

- 可新增 `docpage2md_app\renderer.py`
- `docpage2md_app\pipeline.py`
- `docpage2md_app\models.py`

推荐接口/数据结构：

```python
def render_slide_markdown(page: PageIR) -> str:
    ...

def render_full_markdown(pages: list[PageIR], doc_name: str) -> str:
    ...
```

Block 渲染规则：

- `heading`：按 level 输出 `#`，但每页仍保留 `# Slide {slide_no}` 作为页标题。
- `paragraph`：输出文本段落。
- `formula`：行内或块级 LaTeX。
- `figure_note`：输出 `> [!NOTE] Figure 描述`。
- `table`：v2 可先输出 Markdown table 或保守保留 Raw Text。
- `unknown`：输出原始文本并记录 warning。

失败模式：

- Renderer 丢 block：测试中必须比较所有 block id 被消费。
- block 文本含 Markdown 特殊字符：不应盲目 escape 公式和表格。
- 页标题和内容标题冲突：页标题由 renderer 统一生成，内容标题降一级或保留为二级起。

测试方案：

- 每种 block 类型一个 renderer 单测。
- golden Page IR 到 Markdown 快照测试。
- 所有 block id 消费测试。
- 二次 render 幂等测试。

### v2.4 provenance 与来源分层

目标：

- 明确哪些文本来自 OCR，哪些来自视觉描述，哪些来自 LLM 修正，哪些是 renderer 模板。
- 为后续 refiner 和质量审计提供基础。

涉及模块：

- `docpage2md_app\ir.py`
- `docpage2md_app\renderer.py`
- `docpage2md_app\report.py`

推荐接口/数据结构：

```python
@dataclass
class ProvenanceEntry:
    block_id: str
    field: str
    char_start: int
    char_end: int
    origin: str  # "vision_ocr" | "vision_description" | "brain_refine" | "renderer" | "manual"
    op: str
    confidence: float | None
    note: str | None = None
```

失败模式：

- provenance 过细导致实现成本高：v2 可先 block 级，v3 再做字符级。
- Figure 描述被误当 OCR 文本：通过 `origin` 和 `type` 分开。
- renderer 模板内容影响覆盖率：模板内容应标记 `origin: "renderer"`，不参与 OCR 覆盖率。

测试方案：

- 渲染后 report 中每个 generated/template block 都有 provenance。
- OCR block 的 `origin` 保持 `vision_ocr`。
- Figure block 的 `origin` 为 `vision_description`。

### v2.5 分阶段缓存

目标：

- 支持“保留 Stage 1，重跑 Stage 2/refiner/renderer”。
- 支持“IR 变更时只重渲染，不重调模型”。

涉及模块：

- `docpage2md_app\manifest.py`
- `docpage2md_app\pipeline.py`
- `docpage2md_app\renderer.py`

推荐接口/数据结构：

缓存层级：

```text
Raw_01.json          # Stage 1 raw + page_ir
PageIR_01.json       # 可选独立 IR
Slide_01.md          # renderer/refiner 输出
Slide_01.meta.json   # 对应 PageIR hash + renderer version + refiner flags
```

fingerprint 拆分：

- Stage 1 fingerprint：image + vision model + stage1 prompt + stage1 logic。
- IR fingerprint：Raw hash + parser version + schema version。
- Render fingerprint：PageIR hash + renderer version + refiner version + Brain/refiner model if used。

失败模式：

- 多层缓存不一致：下游 fingerprint 必须引用上游 hash。
- 手工修改 Slide Markdown：meta hash 不再匹配，可标记为 manual override 或重建。
- PageIR schema 升级：旧 IR 要迁移或重建。

测试方案：

- 修改 renderer version 后只重建 Slide，不重跑 Vision。
- 修改图片 hash 后所有下游缓存失效。
- 修改 Brain/refiner model 后只重跑 refiner/renderer相关阶段。

## 11. v3 linter/refiner 路线图

v3 目标：在结构化 IR 之上引入 `mineru-refine` 式的 detector、suspect、受限 op、LLM 裁决和质量 linter。此阶段才真正迁移“LLM 不当写入者”的核心设计。

### v3.1 Detector 与 Suspect Worklist

目标：

- 用确定性规则定位可疑问题，让 LLM 只处理局部 suspect。

涉及模块：

- 可新增 `docpage2md_app\detect.py`
- `docpage2md_app\ir.py`
- `docpage2md_app\report.py`

推荐接口/数据结构：

```python
@dataclass(frozen=True)
class Suspect:
    kind: str
    page_id: str
    block_id: str | None
    evidence: str
    has_op: bool
    severity: str
    group_key: str | None = None
```

首批 detector：

- `api_error_output`：Markdown 或 Raw 中有错误前缀。
- `vision_failed`：Stage 1 失败。
- `empty_or_too_short`：输出过短。
- `ctx_leak`：出现 `<CTX>` 或前后页标记。
- `markdown_fence_wrapper`：全文代码围栏。
- `unbalanced_formula`：公式 delimiter 不平衡。
- `figure_analysis_unrendered`：`### Figure Analysis` 未转 note。
- `possible_cross_page_leak`：当前页输出包含前后页独有高相似片段。
- `unknown_block`：IR 中存在未分类大块。
- `table_shape_issue`：表格行列异常。

失败模式：

- detector 误报过多：suspect 要有 severity，v3 先只自动处理 high confidence 项。
- 跨页泄漏相似度误判：只作为 warning 或 LLM 裁决输入，不直接删除。
- 无 IR 的旧任务：detector 只运行 Markdown/Raw 层规则。

测试方案：

- 每个 detector 一组 fixture。
- 误报 fixture：合法公式、合法代码块、合法引用不应被 high severity 标记。
- worklist 稳定排序测试，保证输出可复现。

### v3.2 DocPage2MDOp 与 `apply_op_checked`

目标：

- 所有自动修复都经统一执行入口，支持 reject、回滚、removed spans 和 provenance。

涉及模块：

- 可新增 `docpage2md_app\ops.py`
- `docpage2md_app\ir.py`
- `docpage2md_app\validators.py`
- `docpage2md_app\report.py`

推荐接口/数据结构：

```python
@dataclass(frozen=True)
class DocPage2MDOp:
    op: str
    page_id: str
    target_id: str | None = None
    args: dict = field(default_factory=dict)
    reason: str = ""

@dataclass
class ApplyResult:
    ok: bool
    page: PageIR
    removed_spans: list[dict]
    provenance: list[ProvenanceEntry]
    rejection: str | None = None
```

首批 op：

- `markFailed(page_id, reason)`
- `dropBlock(block_id, reason)`
- `stripText(block_id, pattern)`
- `mergeBlocks(id_a, id_b)`
- `splitBlock(block_id, offset)`
- `setHeadingLevel(block_id, level)`
- `reorderBlocks(ids_in_order)`
- `replaceOcrChar(block_id, offset, before, after)`
- `convertFigureAnalysisToNote(block_id)`
- `normalizeFormula(block_id, delimiter_style)`

`apply_op_checked()` 基础闸门：

- op 引用 ID 必须存在。
- 删除或替换必须记录 removed/provenance。
- OCR 文本块不得无 provenance 新增内容。
- Figure 描述块允许生成式整理，但必须保留 origin。
- renderer 输出必须通过 v1/v2 validators。

失败模式：

- op 参数 stale：ID 不存在时 reject，不回退到数组下标。
- split offset 越界：reject。
- replace 字符不匹配 before：reject。
- reorder 丢 block：reject。
- op 通过但 validator 失败：rollback。

测试方案：

- 每个 op 的成功和 reject 测试。
- rollback 测试：validator 故意失败时原 PageIR 不变。
- removed spans 和 provenance 测试。
- idempotence 测试：同一 op 不应重复造成二次破坏。

### v3.3 LLM 裁决器降权

目标：

- 将 Brain 模型从“整页 Markdown 作者”逐步降为“局部 suspect 裁决器”。

涉及模块：

- 可新增 `docpage2md_app\refiner.py`
- `docpage2md_app\models.py`
- `docpage2md_app\detect.py`
- `docpage2md_app\ops.py`

推荐接口/数据结构：

```python
class RefinerClient(Protocol):
    def decide(self, suspect: Suspect, context: dict) -> dict:
        ...

def refine_page_ir(page: PageIR, neighbors: dict, config: AppConfig) -> RefineResult:
    ...
```

LLM 返回 JSON，不返回整页 Markdown：

```json
{
  "decision": "op",
  "op": "setHeadingLevel",
  "target_id": "blk_0001_0003",
  "args": {"level": 2},
  "reason": "..."
}
```

或：

```json
{
  "decision": "dismiss",
  "reason": "..."
}
```

失败模式：

- LLM 返回非 JSON：尝试一次 JSON repair，失败则 dismiss 并记录。
- LLM 同时给 op 和 dismiss：reject 并要求重裁，或 v3 初期直接 dismiss。
- LLM 请求不存在 op：reject。
- LLM 建议越权新增正文：reject。
- LLM 不可用：fail-open，保留 PageIR 和 renderer 输出。

测试方案：

- Mock LLM 返回合法 op，断言 op 被执行。
- Mock LLM 返回 dismiss，断言 report 记录 dismissed suspect。
- Mock LLM 返回坏 JSON，断言 fail-open 或 dismissed。
- Mock LLM 返回越权 op，断言 reject 且 PageIR 不变。

### v3.4 Markdown/LaTeX/跨页泄漏 linter

目标：

- 把质量问题从 prompt 规则转成程序可检查的 linter。

涉及模块：

- `docpage2md_app\validators.py`
- 可新增 `docpage2md_app\linter.py`
- `docpage2md_app\report.py`

推荐接口/数据结构：

```python
@dataclass(frozen=True)
class LintIssue:
    code: str
    severity: str  # "error" | "warning" | "info"
    page_id: str
    block_id: str | None
    message: str
    evidence: dict

def lint_page(page: PageIR, markdown: str, neighbors: dict) -> list[LintIssue]:
    ...
```

关键 lints：

- `markdown_heading_missing`
- `api_error_text`
- `ctx_marker_leak`
- `formula_unbalanced`
- `possible_neighbor_leak`
- `unrendered_figure_analysis`
- `unknown_block_rendered_raw`
- `table_row_mismatch`
- `empty_ocr_block`
- `generated_without_provenance`

失败模式：

- linter 太严格导致正常输出失败：severity 分层，v3 初期只把 `api_error_text`、`ctx_marker_leak`、`generated_without_provenance` 设为 error。
- 跨页泄漏检测需要 neighbors：无 neighbors 时跳过该 lint，记录 `not_applicable`。
- LaTeX 完整 parse 成本高：先做轻量 delimiter 检查，v4 再考虑更强工具。

测试方案：

- 每个 lint fixture。
- severity gate 测试：error 阻断成功缓存，warning 不阻断但进入 report。
- 跨页泄漏 fixture：当前页没有的前后页独有句子被捕捉。

### v3.5 Opt-in OCR confusion 与表格增强

目标：

- 在已有 provenance、op executor 和 linter 后，再引入高风险但高价值的模型修复。

涉及模块：

- 可新增 `docpage2md_app\confusion.py`
- 可新增 `docpage2md_app\tables.py`
- `docpage2md_app\ir.py`
- `docpage2md_app\ops.py`
- `docpage2md_app\report.py`

推荐接口/数据结构：

OCR confusion：

```python
@dataclass(frozen=True)
class OcrConfusionCandidate:
    block_id: str
    char_offset: int
    before: str
    after: str
    evidence: str
```

表格增强：

```python
@dataclass
class TableIR:
    rows: list[list[str]]
    source: str
    image_crop_path: str | None
    confidence: float | None
```

失败模式：

- OCR 替换误改专业符号：只允许白名单 pair、低密度、可回滚，并记录 provenance。
- 表格视觉重转写幻觉：必须有截图 crop、结构闸门和 coverage 闸门。
- 无表格 crop：不能启用视觉表格重转写，只能保留原表或降级。
- 降级为图片影响可读性：必须在 Markdown 中显式标记，并保留原 Raw。

测试方案：

- OCR pair 白名单和密度限制测试。
- OCR 替换 provenance 测试。
- 表格行列一致性测试。
- 视觉表格 mock 返回坏结构，断言 reject。
- 降级为图片测试，断言 report 记录。

## 12. v4 测试与质量闸门路线图

v4 目标：把 v1-v3 的质量机制变成持续可运行、可阻断回归的测试和 CI 闸门。

### v4.1 单元测试基础设施

目标：

- 覆盖不需要真实 API 的纯逻辑。
- 先把最容易回归的函数纳入测试。

涉及模块：

- `docpage2md_app\files.py`
- `docpage2md_app\session.py`
- `docpage2md_app\models.py`
- `docpage2md_app\cost.py`
- `docpage2md_app\third_party_models.py`
- v1-v3 新增模块

推荐接口/数据结构：

- 建议新增 `tests/`。
- 使用 `pytest`。
- 将交互式 `input()` 与纯逻辑分开，无法分开时用 monkeypatch。

失败模式：

- 交互逻辑难测：抽出 parser、selector、formatter 纯函数。
- 测试依赖本地 `log/`、`.cache/`：使用 `tmp_path`。
- Windows 路径差异：测试使用 `pathlib.Path`。

测试方案：

- `natural_sort_key()`。
- `scan_docpage_folders()`。
- `sanitize_stage_2_markdown()`。
- `validate_slide_markdown()`。
- `calculate_image_tokens()`。
- `parse_bulk_models_text()`。
- `upsert_third_party_model()`。
- manifest fingerprint。
- renderer。
- ops reject。

### v4.2 Mock 模型客户端与离线 pipeline 测试

目标：

- 让 Stage 1、Stage 2、refiner 和失败路径都可离线测试。

涉及模块：

- `docpage2md_app\models.py`
- `docpage2md_app\pipeline.py`
- `docpage2md_app\refiner.py`

推荐接口/数据结构：

```python
class VisionClient(Protocol):
    def extract(self, image_path: Path, prompt: str, config: AppConfig) -> StageResult:
        ...

class BrainClient(Protocol):
    def generate_or_decide(self, prompt_or_context: dict, config: AppConfig) -> StageResult:
        ...
```

失败模式：

- 现有函数直接调用 DashScope/urllib：需要先加薄适配层，不必一次重构所有 provider。
- mock 与真实接口漂移：适配层返回统一 `StageResult`。

测试方案：

- mock Vision 成功、失败、空响应。
- mock Brain 成功、错误字符串、异常、坏 JSON。
- pipeline 两页端到端离线测试。
- 缓存命中不调用 mock client 测试。

### v4.3 Golden fixtures 与幂等测试

目标：

- 防止 renderer、refiner 和 validators 的输出随意漂移。

涉及模块：

- `docpage2md_app\ir.py`
- `docpage2md_app\renderer.py`
- `docpage2md_app\detect.py`
- `docpage2md_app\ops.py`
- `docpage2md_app\refiner.py`

推荐接口/数据结构：

fixtures 建议：

```text
tests/fixtures/simple_text/
tests/fixtures/formula/
tests/fixtures/figure_analysis/
tests/fixtures/table/
tests/fixtures/cross_page_leak/
tests/fixtures/api_error/
```

每个 fixture 可包含：

```text
input_raw.json
page_ir.json
expected.md
expected_report.json
```

失败模式：

- Golden 过度僵化：只对 renderer 和 report schema 做精确断言；模型文本本身用 mock 固定。
- 输出时间戳影响快照：测试中固定时间或从 golden 比较中排除。

测试方案：

- Page IR render golden。
- refine 后再次 refine 无 op 的幂等测试。
- report schema golden。
- cache key golden。

### v4.4 CI 质量闸门

目标：

- 在提交前发现第三方模型管理、缓存、renderer、linter、refiner 的回归。

涉及模块：

- 项目根配置文件。
- `requirements.txt` 或测试依赖配置。
- `tests/`

推荐接口/数据结构：

建议质量门：

- `pytest`
- import smoke test：`python -m docpage2md_app --help` 或等效。
- 无真实 API 的 pipeline smoke test。
- report schema validation。
- 关键模块 lint 可后续引入。

失败模式：

- 当前项目没有测试依赖：可先把 `pytest` 作为开发依赖，不影响运行依赖。
- CLI 交互阻塞 CI：测试 `--list-models` 等非交互路径，或为 main 增加 dry-run。
- 未提交 `third_party_models.py` 导致 import smoke 失败：这正是应被 CI 捕捉的问题。

测试方案：

- CI 跑全量离线测试。
- 新增模型 registry 测试必须通过。
- 任一 error severity linter fixture 误放行则失败。

### v4.5 成本、usage 与质量指标回填

目标：

- 让成本估算、真实 usage、失败率、缓存命中率和质量问题数量进入 report。

涉及模块：

- `docpage2md_app\cost.py`
- `docpage2md_app\models.py`
- `docpage2md_app\report.py`
- `docpage2md_app\pipeline.py`

推荐接口/数据结构：

```json
{
  "usage": {
    "estimated": {"input_tokens": 0, "output_tokens": 0, "cost": 0.0},
    "actual": {"input_tokens": 0, "output_tokens": 0, "cost": 0.0}
  },
  "quality": {
    "lint_errors": 0,
    "lint_warnings": 0,
    "failed_pages": 0,
    "cache_hit_rate": 0.0
  }
}
```

失败模式：

- provider 不返回 usage：保留 `actual: null`，不要编造。
- 第三方模型价格未知：成本 report 标记 `price_source: "unknown"`。
- 估算与实际差异大：同时记录，不覆盖。

测试方案：

- usage 缺失时 report 正确为空。
- 价格未知时不抛异常。
- 成本估算和实际 usage 字段不包含 API Key。

## 13. 第三方模型管理改动的纳入与隔离策略

当前第三方模型管理是路线图里的关键交叉点，因为它影响模型身份、缓存指纹、成本估算和 report。

### 13.1 已验证现状

当前 `config.py` 已有：

- `third_party_models_path`，路径为 `log\third_party_models.json`。

当前 `model_settings.py` 已 import：

- `load_third_party_models`
- `filter_registry_models`
- `upsert_third_party_model`
- `delete_third_party_model`
- `discover_openai_compatible_models`
- `parse_bulk_models_text`
- `registry_item_to_model_record`

当前 `third_party_models.py` 提供：

- `load_third_party_models(config)`
- `save_third_party_models(config, models)`
- `upsert_third_party_model(config, item)`
- `delete_third_party_model(config, item_id)`
- `registry_item_to_model_record(item)`
- `filter_registry_models(models, role)`
- `parse_bulk_models_text(raw_text, defaults)`
- `discover_openai_compatible_models(base_url, api_key, timeout)`

registry payload 包含 `version`、`updated_at`、`models`。单个 item 包含 provider、base_url、api_key_env、model_id、roles、supports_vision、supports_thinking、input_price、output_price、price_source、verification、created_at、updated_at 等字段。该文件不保存 API Key 明文，而是保存 env var 名。

### 13.2 纳入路线图的方式

如果决定纳入：

- v1 必须补 registry 单元测试。
- v1 report 和 manifest 应记录 resolved model identity。
- v1 cache fingerprint 应纳入 provider、model_id、base_url、api_key_env 和 thinking budget。
- v1 成本估算应继续使用 third-party price 字段，但价格不影响输出，不进入输出 fingerprint。
- v2/v3 的 refiner 不直接读取 registry，只接收 resolved config。
- v4 CI 必须包含 import smoke，防止漏提交 `third_party_models.py`。

### 13.3 隔离路线图的方式

如果短期不稳定：

- 把第三方模型管理限定在交互式模型选择层。
- pipeline、manifest、report、renderer、refiner 只接收 `AppConfig` 或 `ResolvedModelConfig`。
- 不让 `detect.py`、`ops.py`、`renderer.py`、`validators.py` import `third_party_models.py`。
- 对 `model_settings.py` 的 import 风险做保护，或者确保 `third_party_models.py` 作为同一变更被提交。
- 新增 refiner 功能不要依赖 registry 存在；没有 registry 时仍可使用当前 `AppConfig`。

### 13.4 推荐决策

推荐把第三方模型管理作为 v1 的“模型身份基础设施”纳入，但前提是先完成提交边界和测试边界。原因：

- v1 cache fingerprint 和 report 必须准确记录 provider/model/base_url/api_key_env。
- 当前项目已经支持 DashScope、DeepSeek、OpenAI-compatible，第三方 registry 是自然延伸。
- 如果不稳定，后续所有缓存和报告都会绕过真实模型来源，难以审计。

但纳入不等于让核心 pipeline 依赖交互式 registry。正确边界是：交互层负责把用户选择解析成 `ResolvedModelConfig`，pipeline 只消费解析结果。

## 14. 推荐的最终架构形态

长期形态应是：

```text
图片目录
  -> 输入扫描与会话选择
  -> Stage 1 Vision extraction
       -> Raw Text
       -> Page IR
       -> Stage 1 manifest/report
  -> deterministic parser / weak IR fallback
  -> renderer 生成初稿 Markdown
  -> linter 检查
  -> detector 生成 suspect
  -> optional LLM refiner 只裁决有限 op
  -> apply_op_checked + validators
  -> final renderer
  -> Slide_XX.md + Slide_XX.meta.json + page report
  -> FULL.md + run_report.json
```

这个架构保留当前 `docpage2md` 最有价值的两阶段思路，但把最终输出从“模型直接写文件”转为“结构化 IR + renderer + 可选受限 refiner”。

## 15. 阶段依赖与优先级

建议优先级如下：

1. v1 必须先做。
   - 没有 manifest、错误隔离和 report，后续任何 refiner 都可能把坏结果缓存成成功结果。

2. v2 是 v3 的前置。
   - 没有 Page IR 和稳定 block ID，就无法安全定义 op，也无法做 `apply_op_checked`。

3. v3 不应跳过 detector 和 op executor。
   - 如果直接把 Brain prompt 改得更复杂，只会扩大不可测试面积。

4. v4 应从 v1 开始同步建设。
   - 不必等所有功能完成才加测试。最先应测试 sanitize、fingerprint、registry、cache skip 和 error quarantine。

## 16. 事实来源索引

既有报告：

- `D:\Repos\lab-python\docpage2md\docs\research\mineru-refine-research.md`
- `D:\Repos\lab-python\docpage2md\docs\research\docpage2md-research.md`

docpage2md 源码：

- `D:\Repos\lab-python\docpage2md\docpage2md_app\pipeline.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\models.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\prompts.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\config.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\files.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\model_settings.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\third_party_models.py`
- `D:\Repos\lab-python\docpage2md\docpage2md_app\cost.py`

mineru-refine 源码：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\types.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\id.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\detect.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\ops.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\invariant.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\agent_loop.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\refine.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\markdown.rs`
