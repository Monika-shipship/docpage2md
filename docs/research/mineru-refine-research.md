# mineru-refine 项目研究报告

研究对象：`D:\Repos\lab-python\工具\文档处理\mineru-refine`

报告输出位置：`D:\Repos\lab-python\docpage2md\docs\research\mineru-refine-research.md`

研究方式：静态阅读仓库源码、README、绑定、脚本、plugin 与测试文件。本文只记录已从源码或项目文件中验证的事实；对 `docpage2md` 的部分为迁移分析与建议，不把建议写成已实现事实。

## 1. 总体结论

`mineru-refine` 是一个面向 MinerU `content_list.json` 的后处理、审计与修复项目。它的核心定位不是“重新解析 PDF”，也不是“让大模型自由重写 Markdown”，而是在 MinerU 已经输出结构化 item 数组之后，对常见结构错误做受控清洗，并尽量保证输出仍然是 MinerU 原 schema 的 `content_list`。

它的核心思想可以概括为：

1. 输入输出同 schema：输入是 MinerU item 对象数组，输出仍是 item 对象数组，未知字段原样透传。
2. 内部加稳定 ID：在处理阶段给 item 加 `it_0001` 这类内部 ID，所有操作引用稳定 ID，而不是数组下标。
3. 先检测疑点，再让 LLM 裁决：确定性 detector 先生成 suspect，LLM 只能在有限工具集内选择操作、观察或放弃。
4. 操作集有限且可验证：所有改动通过 `apply_op_checked` 落地，落地后过保真闸门，不合格就回滚。
5. 失败时保守返回：LLM 不可用、panic 或关键前置条件缺失时 fail-open，返回原输入或当前安全结果，并在 report 中标记。
6. 可审计：返回 `items` 之外还有 `report` 和 `provenance`，记录执行了什么、丢弃了什么、拒绝了什么、使用了多少 token、哪些 opt-in 层改了哪些字符。
7. 可多形态集成：同一个 Rust core 同时被 CLI、HTTP server、Python PyO3、JS napi-rs、Rust library、Claude Code plugin 复用。

对 `docpage2md` 最有价值的迁移点不是照搬 Rust 实现，而是把“结构化中间结果 + 受限修复操作 + 保真/审计闸门 + fail-open”的设计移植到现有 Python 应用里。这样能在不破坏主流程的前提下增加一个后处理层，降低 OCR/解析后处理引入不可控重写的风险。

## 2. 项目目标、输入输出与边界

### 2.1 目标

根 README `D:\Repos\lab-python\工具\文档处理\mineru-refine\README.md` 明确说明：MinerU 会把 PDF 解析成 `content_list.json`，其中每个 item 是正文、标题、表格、图片、公式等结构块。`mineru-refine` 接收这个 `content_list`，修掉解析产生的高频结构问题，然后返回同 schema 的 `content_list`。

core crate README `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\README.md` 进一步强调：本 crate 是核心实现，Python 与 JS 绑定都是薄包装；它只做削减与重组，不做任意增写。这个约束在 `invariant.rs` 与 `ops.rs` 的保真检查里有实现支撑。

已验证的目标问题包括：

- 伪标题：正文被 MinerU 误判为标题。
- 跨页拆表、跨页拆列表：表格或列表被分成多个 item。
- 页眉页脚、页码、残留 Markdown/LaTeX 标记。
- 巨块文本、疑似漏标标题、标题尾部残留标记、分离 caption。
- OCR 形近字混淆，属于 opt-in 层。
- 重度乱码表格视觉重转写，属于 opt-in 层。
- 重写失败后把仍然乱码的表格降级成图片，属于 opt-in 层。

### 2.2 输入

核心输入是 MinerU 的 `content_list` item 数组。源码里对应：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\types.rs`
- `MineruItem(pub Map<String, Value>)`

`MineruItem` 使用 `serde_json::Map<String, Value>` 包裹原始对象，而不是定义一个强类型、字段固定的 Rust struct。这是 schema 透明的关键：项目只认识需要读写的字段，但不会丢弃未知字段。

CLI 与 HTTP 还能接收一个包装对象，包装对象包含 `items` 和选项。例如 CLI `src/bin/cli.rs` 支持：

- 直接从 stdin 读取 JSON array。
- 或读取 object，字段包括 `items`、`sha256`、`maxIterations`、`imageDir`、`fixOcrConfusion`、`extraConfusionPairs`、`rewriteGarbledTables`、`degradeGarbledTables`。

Python 与 JS 绑定的选项命名与各自生态一致：

- Python 使用 snake_case，例如 `max_iterations`、`image_dir`、`fix_ocr_confusion`。
- JS 使用 camelCase，例如 `maxIterations`、`imageDir`、`fixOcrConfusion`。

### 2.3 输出

公共 API 返回的高层结构是：

- `items`：清洗后的 `content_list`，字段集合和类型尽量保持 MinerU schema 兼容。
- `provenance`：可审计来源记录，尤其是 opt-in 的 OCR 混淆修正和乱码表视觉重转写。
- `report`：操作计数、dismissed 记录、removed spans、违规信息、token usage、fail-open 标记、opt-in 层统计等。

源码证据：

- `types.rs` 中定义 `RefineResult`、`ProvenanceEntry`、`Report`、`RemovedSpan`、`TokenUsage`。
- `refine.rs` 中 `refine()` 组装 `RefineResult`。
- `id.rs` 中 `strip_ids()` 在返回前移除内部 ID，保证输出不给下游暴露内部实现字段。

CLI 输出 stdout 是纯 JSON，进度不混入 stdout，而是写 stderr，前缀为 `[mineru-refine:progress]`。对应源码：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\cli.rs`

HTTP streaming 输出 SSE，包含 `progress` 事件与末尾 `result` 事件。对应源码：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\server.rs`

### 2.4 明确边界

`mineru-refine` core 不负责解析原始 PDF、DOC、PPT 或图片。README 中说明 Python/JS/Rust/HTTP 版都从已解析的 `content_list` 起步。

端到端“原始文件进，干净 Markdown 出”的能力在 Claude Code plugin 里实现。plugin 脚本会调用 MinerU 官方 API 获取 `content_list.json` 和 images，然后再调用 `mineru-refine` 清洗，并渲染 `full.md`。

相关路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\skills\mineru-prime\SKILL.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\scripts\mineru_fetch.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\scripts\refine.ts`

## 3. 安装、调用方式与项目形态

### 3.1 Rust library

Rust core crate 位于：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine`

安装方式在 README 中给出：

```bash
cargo add mineru-refine
```

主要入口在：

- `src/lib.rs`
- `src/refine.rs`

`lib.rs` 对外 re-export 了核心类型与函数，包括：

- `MineruItem`
- `RefineOptions`
- `RefineResult`
- `refine`
- `render_markdown`
- `detect_suspects`
- `cache_key_for`
- `cache_key_for_opts`
- `clear_refine_cache`
- prompt/version 常量

Rust library 是其他形态的共同底座。

### 3.2 CLI

CLI 源码：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\cli.rs`

安装方式：

```bash
cargo install mineru-refine --features bin
```

典型调用：

```bash
cat content_list.json | mineru-refine > refined.json
```

CLI 读取 stdin，解析 JSON array 或 object。object 模式支持传入：

- `items`
- `sha256`
- `maxIterations`
- `imageDir`
- `fixOcrConfusion`
- `extraConfusionPairs`
- `rewriteGarbledTables`
- `degradeGarbledTables`

CLI 特别重要的设计是把 progress 写到 stderr，结果 JSON 写到 stdout。这样调用方可以安全地把 stdout 重定向成文件，不会被进度帧污染。

### 3.3 HTTP server

HTTP server 源码：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\server.rs`

启动方式：

```bash
mineru-refine-server
```

默认端口是 8771，可通过 `MINERU_REFINE_PORT` 修改。路由包括：

- `GET /health`
- `POST /refine`
- `POST /refine/stream`

`POST /refine` 返回普通 JSON 结果。

`POST /refine/stream` 返回 SSE。源码注释和实现显示：

- 每轮发 `event: progress`，data 是 progress JSON。
- 末尾发 `event: result`，data 是最终 `RefineResult` JSON。
- 坏请求直接返回 400，不伪装成 SSE。
- 客户端断开时静默丢 progress 帧，不影响后台 refine。

这个形态适合非 Rust/Python/JS 调用方，或希望把 postprocess 部署成独立服务的场景。

### 3.4 Python 绑定

Python 绑定路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\python`
- `bindings\python\src\lib.rs`
- `bindings\python\README.md`
- `bindings\python\pyproject.toml`
- `bindings\python\Cargo.toml`

安装方式：

```bash
pip install mineru-refine
```

要求 Python 版本不低于 3.9。绑定通过 PyO3 暴露：

- `refine(...)`
- `render_markdown(...)`
- `detect_suspects(...)`
- `clear_refine_cache()`

从源码和 README 可验证的行为：

- Python `refine` 接收 `list[dict]` 形式的 `content_list`。
- 返回 dict，包含 `items`、`provenance`、`report`。
- 支持 progress callback，回调收到 dict。
- 绑定释放 GIL，让 Rust 异步/CPU 工作不阻塞 Python 解释器主锁。

这对 `docpage2md` 很有参考价值，因为 `docpage2md` 当前是 Python 项目。如果引入类似设计，优先级应是“用 Python 实现同类后处理接口”，而不是立刻引入 PyO3/Rust 复杂度。

### 3.5 JS/TS 绑定

JS 绑定路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js`
- `bindings\js\src\lib.rs`
- `bindings\js\index.js`
- `bindings\js\index.d.ts`
- `bindings\js\package.json`
- `bindings\js\build.rs`
- `bindings\js\README.md`
- `bindings\js\test\smoke.test.ts`

安装方式：

```bash
bun add mineru-refine
# 或
npm i mineru-refine
```

运行环境是 Bun 或 Node 18+。导出能力包括：

- `refine(items, opts?, onProgress?)`
- `renderMarkdown(items)`
- `detectSuspects(items)`
- `clearRefineCache()`

`index.js` 负责加载平台相关的 native `.node` 插件。`index.d.ts` 给 TS 消费方提供类型。napi 绑定里的 progress 使用 ThreadsafeFunction 非阻塞回调，这是为了让 Rust 线程安全地向 JS runtime 发送进度。

### 3.6 Claude Code plugin

plugin 路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin`
- `plugin\.claude-plugin\plugin.json`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\.claude-plugin\marketplace.json`
- `plugin\README.md`
- `plugin\skills\mineru-prime\SKILL.md`
- `plugin\scripts\mineru_fetch.ts`
- `plugin\scripts\refine.ts`
- `plugin\bin\mineru-prime-fetch`
- `plugin\bin\mineru-prime-refine`

plugin 是真正的端到端工作流：

1. 把 PDF/DOC/PPT/图片交给 MinerU 官方 API。
2. 下载并展开 MinerU 结果，得到 `content_list.json`、images、layout 等。
3. 调用 JS 绑定 `mineru-refine` 清洗。
4. 输出 drop-in 替身目录。

plugin README 说明输出目录包含：

- `images/`：镜像原图目录。
- `layout.json`：原样镜像。
- `content_list.json`：替换为清洗版。
- `full.md`：从清洗后的 `content_list` 重新渲染。
- `refine_report.json`：审计报告。

plugin 默认打开三层 opt-in 清洗：

- OCR 形近字修正。
- 乱码表视觉重转写。
- 乱码表降级兜底。

bin wrapper 还有一个很实际的细节：它会把当前工作目录里的 `.env` source 到真实环境变量后再启动 Bun。原因是 Rust native binding 读的是 `std::env`，只在 Bun 的 JS `process.env` 里设置并不够。

## 4. Rust core 模块职责

### 4.1 `types.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\types.rs`

核心职责：

1. 定义 schema 透明的 MinerU item 包装。
2. 定义内部处理 item。
3. 定义 suspect、work item、operation call。
4. 定义 refine 结果、报告、provenance、token usage。
5. 定义 opt-in 层的数据结构。

关键类型：

- `MineruItem(Map<String, Value>)`
- `RefItem`
- `SuspectKind`
- `Suspect`
- `WorkItem`
- `OpCall`
- `RemovedSpan`
- `ProvenanceEntry`
- `Report`
- `RefineResult`
- `ConfusionFix`
- `TableRewriteFix`

`MineruItem` 的设计避免了强行绑定 MinerU 的所有字段。它只通过 helper 读取或写入项目关心的字段，例如 `type`、`text`、`text_level`、`table_body`、`table_caption`、`img_path`、`page_idx`、`bbox`、`list_items` 等。未知字段留在原 map 中，序列化时继续透传。

`OpCall` 是有限操作集的入口。LLM 不能生成任意 patch，只能提交这些操作调用。根据源码和测试覆盖，操作族包括：

- `merge`
- `split`
- `demote`
- `promote`
- `reorder`
- `drop`
- `strip`
- `deleteChar`
- `mergeTable`
- `mergeList`
- `extractCaption`
- `dropCaption`

这个文件是“数据契约中心”，也是后续迁移到 `docpage2md` 时应先设计的部分：先定义中间 item、suspect、op、report，再写具体检测器和执行器。

### 4.2 `id.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\id.rs`

虽然用户清单没有单独要求 `id.rs`，但稳定 ID 是关键设计，必须纳入。

核心职责：

- 给输入 item 分配内部 ID。
- 生成新 item 的 ID。
- 返回前剥离内部 ID。
- 根据 ID 找当前数组中的 item。

关键函数/类型：

- `IdGen`
- `assign_ids`
- `strip_ids`
- `must_index_of_id`

稳定 ID 解决的问题是数组下标漂移。清洗过程中可能发生 merge、split、drop、reorder。如果让 LLM 或 op 使用数组下标，前一个操作之后所有后续索引都可能失效。使用 `it_0001` 这类稳定 ID 可以让 op 指向具体对象，同时又能在返回结果前完全移除内部字段。

### 4.3 `detect.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\detect.rs`

核心职责：

- 对当前 item 数组做确定性扫描。
- 生成 suspect/worklist。
- 给 suspect 标注 kind、证据、可选 op hint、分组信息。

根据源码与测试，检测的 suspect 类型包括：

- `pseudo_heading`：疑似伪标题。
- `cross_page_break`：跨页文本断裂。
- `giant_block`：异常大文本块。
- `page_artifact`：页码、页眉页脚等页面工件。
- `residual_markup`：残留 Markdown/LaTeX/链接等标记。
- `split_table`：疑似分页拆表。
- `split_list`：疑似拆列表。
- `empty_table`：空表或壳表。
- `missed_heading`：疑似漏标标题。
- `trailing_marker`：标题尾部标记。
- `separated_caption`：caption 与主体分离。
- `caption_heading`：caption 被误标成 heading。
- `caption_artifact`：caption 里的工件。
- `extra_char`：疑似多余字符。
- `caption_issue`：caption 类问题的标记集合。

这个模块的设计很重要：LLM 不负责“满文档寻找问题”，它只面对 detector 已经定位的局部疑点。这样减少 token、降低幻觉，也便于写单测。

### 4.4 `ops.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\ops.rs`

核心职责：

- 实现有限操作集。
- 校验每个操作的前置条件。
- 记录 removed spans。
- 调用保真检查。
- 违反保真时回滚。

关键入口：

- `apply_op_checked(items, call, ctx)`
- `ApplyContext`
- `ApplyResult`
- `RejectKind`

`ops.rs` 的注释明确说明 `apply_op_checked` 是唯一对外执行入口：执行、保真闸、几何派生，违反即回滚。

典型安全约束：

- `merge` 只允许相邻文本或经过明确规则允许的跨 furniture 合并。
- `split` 要求 offset 合法，不能产生空半段，子 item 继承几何信息，尾段丢掉 heading level。
- `reorder` 限定连续范围，不允许任意全局洗牌。
- `drop` 有白名单，例如页码短文本、壳表等，不能随意删含内容的 table。
- `strip` 只能匹配白名单 pattern，并写 removed span。
- `deleteChar` 有字符与上下文白名单。
- `mergeTable` 对 table body 只做结构受控合并，保留字节/行级保真。
- `mergeList` 拼接 list items，并处理英文边界空格。
- `extractCaption` / `dropCaption` 处理 caption 与表体分离或 caption 污染。

测试 `ops_test.rs` 覆盖了大量边界，包括 bbox union、非相邻 reject、strip 审计 trail、table body byte-faithful、ragged column merge、rowspan carryover、drop whitelist、几何保真回滚等。

### 4.5 `invariant.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\invariant.rs`

核心职责：

- 定义输出是否“保真”。
- 阻止操作引入新内容或破坏几何/表格主体。

关键函数：

- `check_fidelity`
- `check_char_subset`
- `check_table_bodies`
- `check_geometry`
- `content_chars`
- `table_rows`
- `non_ws_len`

保真原则分几层：

1. 内容字符子集：输出的内容字符必须来自输入，不能新增非空白字符。`content_chars` 统计 `text`、`list_items`、`table_caption` 等内容字段。
2. 表体单独处理：`table_body` 不混入普通字符 multiset，而是按 byte equality 或 table row/shell pool 检查。这样避免 HTML 表格被普通字符统计误判，同时允许受控的 `mergeTable`。
3. 几何约束：如果输入有 `bbox` / `page_idx`，输出必须保持可解释几何。非法 bbox 或外来 page 会失败。
4. 空白相对宽容：测试中明确有 whitespace changes 不违规的用例。

这个模块是项目可信度的核心。LLM 决策只是建议，最终能不能落地由 invariant 判定。

### 4.6 `agent_loop.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\agent_loop.rs`

核心职责：

- 把 suspects 组织成 worklist。
- 构造工具调用 schema 和 prompt。
- 运行 tool-use loop。
- 支持观察工具、操作工具和 dismiss。
- 根据稳定 ID 执行操作。
- 处理并发、分组联合裁决、振荡保护、进度回调和 dismissed 记录。

关键类型/函数：

- `Progress`
- `LoopOptions`
- `run_agent_loop`
- `handle_op_call`
- `judge_split_table_vision`

`Progress` 包含：

- `iterations`
- `maxIterations`
- `worklistRemaining`
- `inputSuspects`

进度每轮发送，并在终止时发送剩余为 0 的 terminal progress。`loop_test.rs` 中有 `progress_sink_emits_per_iteration_with_terminal_zero` 覆盖该行为。

tool-use loop 的特点：

- system prompt 稳定放在 messages 前缀，源码注释提到这是为了吃 DeepSeek prefix cache。
- LLM 可以请求观察，例如查看邻近 item、查看上下文，而不是一次性把全量文档塞进 prompt。
- LLM 的操作调用会被映射为 `OpCall`，再交给 `apply_op_checked`。
- JSON arguments 有 repair 逻辑，`loop_test.rs` 有 broken JSON arguments repaired 的测试。
- 对互相矛盾的 dismiss 与 op，有重裁决路径。
- 对 sibling group、相同页工件等会联合裁决，避免同类问题逐个重复调用。
- 有 oscillation guard，防止刚 merge 的产物又被 split。

`split_table` 是特殊分支：源码注释显示“是否同一张表被分页拆开”只走视觉裁决，输出决策后 merge 仍走 `apply_op_checked` 保真闸。缺少图片或 vision API 失败时不会退回文本路径瞎猜，而是 shelve/dismiss 相关疑点。

### 4.7 `refine.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\refine.rs`

核心职责：

- 暴露 public `refine()`。
- 组织完整 pipeline。
- 实现 cache key。
- 实现 fail-open。
- 调机械清洗、agent loop、garbled 层、degrade 层、confusion 层。
- 汇总 report、provenance、token usage。

关键常量：

- `REFINE_LOGIC_VERSION = "0.13.0"`
- `PROMPT_VERSION = "p9"`
- `MODEL_ID = crate::llm::DEEPSEEK_DEFAULT_MODEL`

关键函数：

- `refine`
- `cache_key_for`
- `cache_key_for_opts`
- `clear_refine_cache`
- `adaptive_max_iterations`
- `apply_garbled_layer`
- `apply_confusion_layer`

pipeline 顺序按源码可验证为：

1. 根据 `sha256` 和 opts 计算 cache key。
2. 分配内部 ID。
3. 根据 opts 构建 confusion table、vision/image loader 等前置资源。
4. 运行 mechanical clean。
5. 运行 agent loop。
6. 对 loop 后结果做 `check_fidelity`。
7. 如果打开 `rewrite_garbled_tables`，运行 garbled rewrite 层。
8. 如果打开 `degrade_garbled_tables`，运行 garbled degrade 层。
9. 如果打开 `fix_ocr_confusion`，运行 confusion 层。
10. 汇总 token usage、provenance、report。
11. `strip_ids`，返回同 schema items。

fail-open 通过 closure 和 `catch_unwind` 风格的防护实现。典型场景：

- LLM API key 缺失或调用失败，且没有成功安全改动。
- panic 被捕获。
- opt-in 层前置条件不满足且无法安全继续。

cache key 设计：

- 基础 key 包含 `sha256`、`REFINE_LOGIC_VERSION`、有效 DeepSeek model、`PROMPT_VERSION`。
- 如果打开 confusion，追加 confusion prompt version 和 extra pairs。
- 如果打开 garbled rewrite，追加 garbled prompt version。
- 如果打开 degrade，追加 degrade version。

这避免了不同模型、prompt 或开关共享错误缓存。

### 4.8 `mechanical.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\mechanical.rs`

核心职责：

- 在 LLM loop 前做确定性、低风险清洗。
- 清掉表格中的机械噪声。
- 为后续保真基线建立更干净的输入。

关键函数：

- `mechanical_clean`

从源码和测试可验证的能力包括：

- 删除空表格行。
- 处理 continuation row。
- 清理单元格 whitespace。
- 清理 URL 中异常空格。
- 清理 Markdown escape。
- 清理单元格 LaTeX 残留。
- 使用 token vote 识别某些重复性 token 噪声。

mechanical 的改动计入 `mech*` 类操作统计。它有自己的 validation，并不是绕过保真体系。`mechanical_test.rs` 覆盖了清理行为与边界。

这个模块体现了一个重要经验：不要把显然可规则化的清理交给 LLM。先做确定性机械清理，可以减少 LLM 调用量和误判面。

### 4.9 `confusion.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\confusion.rs`

核心职责：

- 实现 opt-in 的 OCR 形近字混淆修正层。
- 只在 `fix_ocr_confusion=true` 时运行。
- 把 LLM 限制为提出候选/裁决，最终替换必须通过准入规则。

关键常量/函数：

- `CONFUSION_PROMPT_VERSION = "c3"`
- `fix_confusions`
- `ConfusionTable::build`
- `BUILTIN_CONFUSION_CLASSES`

设计约束：

- 替换粒度是精确 1 字符替换。
- 替换必须来自内置 confusion class 或 `extra_confusion_pairs`。
- 有密度 caps，避免一段文本被大规模改写。
- frequency vote 可直接接受部分高置信候选。
- 否则需要 LLM second opinion。
- 对 table body 的 tokenization 会排除 HTML tags/entities，避免改坏表格结构。
- observation feedback 只进行有限轮次，测试中有 second round then stops。

输出审计：

- `report.confusionFixes`
- `report.confusionRejected`
- `report.confusionObservations`
- `provenance` 中 origin 为 `ocr_confusion` 的条目。

这个层不是默认核心清洗，而是可选增强。对 `docpage2md` 来说，OCR 纠错通常有价值，但必须有白名单和 provenance，否则很容易把正确文本改错。

### 4.10 `garbled.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\garbled.rs`

核心职责：

- 检测重度乱码表。
- 可选用视觉模型重转写乱码表格。
- 如果仍然乱码，可选降级为图片 item。

关键常量/函数：

- `GARBLED_PROMPT_VERSION = "g1"`
- `DEGRADE_VERSION`
- `garbled_score`
- `detect_garbled_table`
- `rewrite_garbled_tables`
- `degrade_garbled_tables`

检测方法：

- 使用中文词覆盖率字典 `data/cn_words.txt`。
- 样本不足时不判乱码。
- 测试显示阈值逻辑会区分 clean 与 garbled，`garbled_score_requires_sample` 明确覆盖样本不足。

视觉重转写：

- 依赖表格 `img_path` 和 image loader。
- 调用 vision client 的 `transcribe_table`。
- 有结构闸门、对齐闸门、覆盖率回归闸门。
- 如果提案错位或覆盖率变差，整表回退，`table_body` 逐字节不动。
- provenance 记录每个 rewrite cell 在新 `table_body` 中的字符区间。

降级层：

- `degrade_garbled_tables` 把仍然乱码且有 `img_path` 的 table 转成 image。
- `removedSpans` 中记录 reason，例如 `garbled:degrade_to_image(...)`。
- 没有 `img_path` 的乱码表不能降级，保留原表。

这个模块对 MinerU 表格场景高度定制。对 `docpage2md` 的迁移价值取决于 `docpage2md` 是否有表格图片裁剪和结构化表格中间表示。

### 4.11 `markdown.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\markdown.rs`

核心职责：

- 将 `content_list` 确定性渲染为 Markdown。

关键函数：

- `render_markdown`

渲染行为：

- `text` item 按 `text_level` 渲染 heading 或段落。
- 跳过 furniture。
- table 渲染 caption、body、footnote。
- image/chart 渲染图像引用。
- equation 渲染公式。
- list 渲染列表项。
- 未知类型做 best effort。

`markdown_test.rs` 包含：

- headings、paragraphs、furniture、tables、images、equations、lists 的渲染测试。
- 空文本和空 caption 跳过。
- 当真实 MinerU `full.md` 可用时，与原版 `full.md` 做近似对拍。

这个设计说明：Markdown 输出应该是结构化 item 的派生产物，而不是独立主状态。修复应发生在结构化层，Markdown 只是 render。

### 4.12 `llm.rs`

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\llm.rs`

核心职责：

- 封装 OpenAI-compatible 文本与视觉模型调用。
- 定义 `ChatClient`、`VisionClient`、`LoadImage` 等 trait。
- 提供 DeepSeek 和 Qwen-VL 客户端。

已验证行为：

- DeepSeek key 读取 `DEEPSEEK_APIKEY`，也接受 `RAGENT_DEEPSEEK_APIKEY`。
- DeepSeek 默认 base URL 是 `https://api.deepseek.com`，可用 `DEEPSEEK_BASE_URL` 覆盖。
- DeepSeek 默认模型由 `DEEPSEEK_DEFAULT_MODEL` 给出，README 中默认是 `deepseek-v4-pro`，可用 `DEEPSEEK_MODEL` 覆盖。
- Qwen key 读取 `QWEN_APIKEY`。
- Qwen base/model 可通过 `QWEN_BASE_URL`、`QWEN_VISION_MODEL` 覆盖。
- 请求使用 OpenAI-compatible 风格。
- 文本裁决使用 tool choice，temperature 为 0，并关闭 thinking。
- Qwen-VL image 以 base64 data URL 形式传入。
- DashScope 场景使用 `top_k: 1` 增强确定性。
- JSON 输出有提取和 safe-json-repair。

这个文件与 tests 中的 mock trait 共同构成“生产调用可替换、测试不打网络”的架构基础。

## 5. 关键设计详解

### 5.1 同 schema 输出

实现位置：

- `types.rs` 的 `MineruItem(Map<String, Value>)`
- `id.rs` 的 `strip_ids`
- `refine.rs` 返回前组装 `RefineResult`

解决的问题：

- 下游已经按 MinerU schema 消费 `content_list.json`，如果后处理改 schema，会造成集成成本。
- MinerU schema 可能有版本差异或附加字段，强类型 struct 容易丢字段。

代价：

- 编译期类型检查变弱，字段读写需要大量 helper 和 runtime 校验。
- 复杂逻辑要防止拼错字段名。

对 `docpage2md` 的适用性：

- 高。`docpage2md` 如果已有自己的 page/block/span/table 中间结构，后处理层最好保持输入输出结构兼容，不应该让清洗器改变主流程的数据契约。
- 建议先定义“原始字段透传 + 内部字段临时注入 + 返回前清理”的约束。

### 5.2 稳定 ID

实现位置：

- `id.rs`
- `agent_loop.rs`
- `ops.rs`

解决的问题：

- merge、split、drop、reorder 会改变数组下标。
- LLM 或工具如果引用 index，很容易在多步 loop 中指错对象。

代价：

- 所有 op 都要维护 ID 生命周期。
- split/merge 生成新 ID 时必须清晰记录来源。
- 返回前必须 strip，避免污染下游 schema。

对 `docpage2md` 的适用性：

- 高。OCR/图片转 Markdown 后处理通常也会有 block 合并、拆分、排序、删除。稳定 ID 能显著降低多步处理的错配风险。
- 可以直接在 Python 中用 `blk_000001` 之类 ID，不必引入 Rust。

### 5.3 有限操作集

实现位置：

- `types.rs` 的 `OpCall`
- `ops.rs` 的 `apply_op_checked`
- `agent_loop.rs` 的 tool schema

解决的问题：

- 防止 LLM 输出任意重写文本。
- 把“是否应该改”与“如何安全地改”分离：LLM 负责判断，程序负责执行。

代价：

- 初期需要为每种改动设计 op、前置条件、回滚和测试。
- 新错误类型如果没有对应 op，只能 dismiss 或新增 op。

对 `docpage2md` 的适用性：

- 高。尤其适合后处理 Markdown 结构：合并段落、拆分段落、调整 heading level、删除页码、合并表格、修正列表等都可以做成 op。
- 不适合让 LLM “整页重写 Markdown”，除非业务目标本身接受生成式改写。

### 5.4 tool-use loop

实现位置：

- `agent_loop.rs`
- `llm.rs`
- `loop_test.rs`

解决的问题：

- LLM 一次性处理全文成本高且容易误改。
- 局部 suspect 可以逐个或分组裁决。
- 观察工具允许 LLM 在需要时看上下文，而不是默认吞全部上下文。

代价：

- 实现复杂度高，需要处理 JSON repair、工具调用失败、重复裁决、并发一致性。
- 多轮 loop 会增加延迟。

对 `docpage2md` 的适用性：

- 中高。若 `docpage2md` 引入 LLM 后处理，建议先做单轮 suspect 裁决，再逐步演进到完整 tool-use loop。
- 对纯本地 OCR 清洗或简单规则修复，完整 loop 可能过重。

### 5.5 fail-open

实现位置：

- `refine.rs`
- `refine_test.rs` 中 `llm_unavailable_fails_open_returning_input`

解决的问题：

- 后处理失败不应破坏主解析结果。
- API key 缺失、模型异常、panic 都不应让用户丢失原始内容。

代价：

- 需要在 report 中明确标记，否则调用方可能误以为清洗成功。
- 对局部失败与全局失败要区分，否则会过度保守。

对 `docpage2md` 的适用性：

- 极高。png/image 到 markdown 的主路径应该优先稳定。任何可选 refine 层失败时都应返回原始 Markdown/结构，并给出可见 warning/report。

### 5.6 保真闸门

实现位置：

- `invariant.rs`
- `ops.rs`
- `refine.rs`
- `invariant_test.rs`
- `ops_test.rs`

解决的问题：

- 防止模型或 bug 引入输入中不存在的内容。
- 防止表格 HTML 被无意改坏。
- 防止几何信息变成无效坐标或外来页面。

代价：

- “不新增字符”的严格约束会限制 OCR 纠错、语义补全、图片描述生成。
- 表格 row/shell 检查实现复杂。
- 需要针对业务定义哪些字段算 content，哪些字段算结构。

对 `docpage2md` 的适用性：

- 高，但需要分层。`docpage2md` 如果要从图片生成描述，严格 no-new-char 不适用，因为 OCR/视觉描述本来会生成新文本。
- 建议采用三类合同：
  1. 结构清洗层：不新增内容字符。
  2. OCR 纠错层：只允许白名单字符替换，并记录 provenance。
  3. 生成增强层：允许新增内容，但必须标注为 generated，不与 OCR 原文混淆。

### 5.7 cache key

实现位置：

- `refine.rs` 的 `cache_key_for`、`cache_key_for_opts`
- `garbled_test.rs` 中 cache key 隔离测试
- `refine_test.rs` 中 cache hit 测试

解决的问题：

- 同一个输入在同一逻辑、同一模型、同一 prompt 下不必重复调用 LLM。
- 模型、prompt、选项变化时必须隔离缓存。

代价：

- key 设计必须完整，否则会出现脏缓存。
- 如果输入 hash 不稳定，缓存命中率会差。

对 `docpage2md` 的适用性：

- 高。建议 `docpage2md` 的缓存 key 至少包含：
  - 输入图片或中间结构 hash。
  - OCR/model 名称与版本。
  - prompt 版本。
  - 后处理逻辑版本。
  - option flags。
  - 重要字典/规则版本。

### 5.8 审计报告

实现位置：

- `types.rs` 的 `Report`、`RemovedSpan`、`ProvenanceEntry`
- `refine.rs` 的 report/provenance assembly
- `ops.rs` removed spans
- `confusion.rs`、`garbled.rs` opt-in provenance

解决的问题：

- 用户需要知道哪些内容被删、哪些被改、哪些被拒。
- 后处理出错时需要可追溯证据。
- 测试和线上诊断都依赖结构化 report。

代价：

- 每个 op 都要记录审计信息。
- report schema 需要版本兼容。

对 `docpage2md` 的适用性：

- 极高。图片转 Markdown 的最大风险之一是不可见误删/误改。建议至少记录：
  - 删除 span。
  - 合并/拆分 block。
  - heading level 调整。
  - 表格结构调整。
  - OCR 纠错前后字符。
  - LLM token/cost。
  - fail-open 和 dismissed suspect。

### 5.9 progress

实现位置：

- `agent_loop.rs` 的 `Progress`
- `cli.rs`
- `server.rs`
- `bindings/python/src/lib.rs`
- `bindings/js/src/lib.rs`
- `loop_test.rs`

解决的问题：

- 文档清洗可能有多轮 LLM 调用，不能让用户面对无反馈等待。
- CLI/HTTP/JS/Python 都需要统一进度模型。

代价：

- 每个绑定都要处理跨线程或跨 runtime 回调。
- progress 事件不能污染正式输出。

对 `docpage2md` 的适用性：

- 高。`docpage2md` 若处理多页图片、PPT 或 PDF，progress 应成为统一接口，而不是散落 print。
- CLI 可用 stderr NDJSON；Web 可用 SSE/WebSocket；Python GUI 可用 callback。

### 5.10 测试体系

实现位置：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests`

测试特点：

- 全程 mock LLM，不打网络。
- golden fixture 验证端到端输出。
- fidelity 测试验证字符子集、table body、geometry。
- ops 测试覆盖大量 reject/rollback 边界。
- loop 测试覆盖 progress、JSON repair、oscillation guard、分组裁决。
- refine 测试覆盖 fail-open、cache、schema 透明、idempotence。
- confusion 测试覆盖白名单、frequency vote、feedback、密度限制。
- garbled 测试覆盖视觉重写、结构闸门、错位拒绝、coverage regression 回退、degrade。
- markdown 测试覆盖结构化 render。

对 `docpage2md` 的适用性：

- 极高。尤其是“mock 模型，不打网络”应作为硬要求。否则测试会慢、不稳定、成本不可控。

## 6. 真实工作流、脚本、绑定与 plugin

### 6.1 justfile

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\justfile`

`justfile` 是开发工作流入口。根据已读内容，它包含构建、测试、Python dev wheel、真实 refine、真实 API smoke 等任务。README 中也提到：

- `just py-dev`：构建 Python 绑定并装进本地 venv。
- `just refine-real`：对真实 `content_list` 跑 refine。

迁移启示：

- `docpage2md` 也应把“本地测试、真实样本 smoke、端到端导出、报告生成”固化为脚本，而不是依赖人工命令记忆。

### 6.2 examples

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\refine_real.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\offline_audit.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\qwen_smoke.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\garbled_smoke.rs`

这些 examples 不是 README 装饰，而是实际工作流：

- `refine_real.rs`：对真实输入调用 refine。
- `offline_audit.rs`：离线审计。
- `qwen_smoke.rs`：视觉模型 smoke。
- `garbled_smoke.rs`：乱码表层 smoke。

迁移启示：

- 如果 `docpage2md` 引入可选模型后处理，应提供 offline audit 和 smoke 脚本，分别验证“无需网络的审计”和“真实模型连接是否可用”。

### 6.3 scripts

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\mineru_fetch.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\bump_version.py`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\gen_cn_words.py`

脚本职责：

- `mineru_fetch.ts`：调用 MinerU API 拉取解析结果。
- `bump_version.py`：版本升级辅助。
- `gen_cn_words.py`：生成中文词覆盖率字典，供 garbled detector 使用。

迁移启示：

- 字典、规则、prompt、逻辑版本都应该有明确生成/升级脚本。
- 对 `docpage2md` 而言，如果要做中文 OCR 纠错或乱码检测，词典生成脚本比手工维护大列表更可靠。

### 6.4 Python binding

路径：

- `bindings\python\src\lib.rs`
- `bindings\python\README.md`
- `bindings\python\pyproject.toml`

绑定价值：

- 给 Python 用户提供与 Rust core 同构的接口。
- 支持 progress callback。
- 返回 Python dict/list，无需用户理解 Rust 类型。

对 `docpage2md` 的意义：

- `docpage2md` 当前作为 Python 项目，短期更应学习它的 API 形状，而不是学习 PyO3 本身。
- 如果未来将性能敏感核心抽到 Rust，再参考这个绑定模式。

### 6.5 JS binding

路径：

- `bindings\js\src\lib.rs`
- `bindings\js\index.js`
- `bindings\js\index.d.ts`
- `bindings\js\test\smoke.test.ts`

绑定价值：

- 让 plugin 和 Node/Bun 用户复用同一 core。
- `index.d.ts` 让选项和返回值可被 TS 检查。
- smoke test 验证 native binding 可加载和基本调用。

对 `docpage2md` 的意义：

- 如果 `docpage2md` 将来提供 Web/Node 插件生态，可参考。
- 当前优先级不高，除非已有 JS 消费方。

### 6.6 Claude Code plugin

路径：

- `plugin\.claude-plugin\plugin.json`
- `.claude-plugin\marketplace.json`
- `plugin\skills\mineru-prime\SKILL.md`
- `plugin\scripts\mineru_fetch.ts`
- `plugin\scripts\refine.ts`
- `plugin\bin\mineru-prime-fetch`
- `plugin\bin\mineru-prime-refine`

plugin 把“库”变成“用户工作流”。它不要求用户先理解 MinerU API、目录结构和 refine 参数，而是把步骤编排起来：

1. 检查依赖和环境变量。
2. fetch MinerU 结果。
3. refine 清洗。
4. 输出 drop-in 目录。
5. 汇报疑点前后对比与审计摘要。

对 `docpage2md` 的意义：

- 如果项目目标是给最终用户处理文件，而不是仅提供库，必须有类似“端到端工作流包装”。
- 报告、原始产物、清洗产物最好并排输出，避免覆盖原始结果。

## 7. 测试体系细读

### 7.1 shared mock

路径：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\common\mod.rs`

关键内容：

- `golden_input`
- `golden_expected`
- `MockChat`
- `ExplodingChat`
- `FnVision`
- `FnLoader`
- `Scripted`

它构造了一个带多类问题的 golden 文档，并提供脚本化 mock LLM/vision/image loader。这样所有核心测试都能离线、确定性运行。

### 7.2 detector tests

路径：

- `detect_test.rs`

作用：

- 验证 suspect 检测是否稳定。
- 确保特定结构问题被正确定位。

对迁移启示：

- `docpage2md` 应该先为 detector 写测试，再让 LLM 介入。检测器是可控性的来源。

### 7.3 ops tests

路径：

- `ops_test.rs`

覆盖范围很广，包括：

- demote/promote。
- merge/split/reorder。
- drop/strip/deleteChar。
- mergeTable/mergeList。
- extractCaption/dropCaption。
- geometry gate rollback。
- table body byte-faithful。
- ragged table、rowspan、跨页 fragment 等复杂表格。

对迁移启示：

- 每新增一个 op，都要先写 reject 条件和回滚测试。
- 表格类 op 的测试成本最高，不能靠人工 eyeball。

### 7.4 invariant tests

路径：

- `invariant_test.rs`

覆盖：

- 内容字符统计范围。
- reduction/reorder 合法性。
- 新字符违规。
- multiset overflow 违规。
- whitespace 宽容。
- table body byte tamper。
- geometry 有无 bbox 的不同策略。
- merge table row subset。

对迁移启示：

- `docpage2md` 的 invariant 应该独立成模块，不要埋在 op 里。

### 7.5 loop tests

路径：

- `loop_test.rs`

覆盖：

- observation round trip。
- progress terminal zero。
- oscillation guard。
- max rounds exhausted。
- broken JSON arguments repair。
- contradictory dismiss plus op。
- sibling group joint adjudication。
- stale outline dismissal rechallenge。
- same text page artifacts joint adjudicated。

对迁移启示：

- 一旦引入 agent loop，必须测试“模型不按预期返回”时的行为。

### 7.6 refine tests

路径：

- `refine_test.rs`

覆盖：

- golden fixture。
- no new non-whitespace chars。
- table bodies byte identical。
- actionable suspects monotonically decrease。
- geometry resolvable。
- idempotent second run zero LLM calls。
- LLM unavailable fail-open。
- all ops rejected suspends suspects。
- cache hits。
- schema transparent unknown fields pass through。
- empty/clean input no LLM。
- maxIterations hard stop。
- single suspect failure only suspends that suspect。
- vision split table。
- adaptive max iterations。
- end-to-end missed heading/trailing marker/mechanical cleanup/extra char。

对迁移启示：

- `docpage2md` 后处理也应有“第二次运行 no-op”的幂等性测试。

### 7.7 confusion tests

路径：

- `confusion_test.rs`

覆盖：

- 白名单和内置混淆类。
- frequency vote。
- LLM second opinion。
- density cap。
- observation feedback。
- table body tokenization。
- provenance 和 rejected 统计。

对迁移启示：

- OCR 纠错最容易看似提升、实则误改。必须通过小粒度候选、白名单、密度限制、审计来约束。

### 7.8 garbled tests

路径：

- `garbled_test.rs`

覆盖：

- 乱码表检测。
- 视觉重转写 golden。
- structural gate。
- misalignment gate。
- coverage regression whole-table revert。
- flag off no vision call。
- missing image source fail-open 或 shelve。
- cache key isolation。
- degrade to image。

对迁移启示：

- 视觉模型输出结构化表格时，必须有结构闸门。不能直接信任模型给出的 table。

### 7.9 markdown tests

路径：

- `markdown_test.rs`

覆盖：

- heading、paragraph、furniture、table、image、equation、list 渲染。
- empty text/caption。
- 与真实 MinerU full.md 对拍。

对迁移启示：

- Markdown renderer 应该可测试且确定性，不应混入 LLM。

## 8. 对 docpage2md 的可迁移思想清单

下表中的“适合度”是对当前 `docpage2md` 这类 Python 图片/文档转 Markdown 项目的判断，不表示 mineru-refine 已经在 `docpage2md` 中实现。

| 可迁移思想 | 解决什么问题 | 代价 | 是否适合 docpage2md |
|---|---|---|---|
| 同 schema 后处理层 | 后处理不破坏主流程输出契约，下游零改动或少改动 | 需要定义清楚内部字段和返回前清理 | 高。建议先作为可选 refine 阶段接在现有输出后 |
| schema 透明 item wrapper | 避免丢失上游未知字段，兼容格式演进 | 字段访问是 runtime 校验，类型安全弱 | 高。Python dict 本来适合，但要有 helper 管理字段 |
| 稳定内部 ID | 避免数组下标在 merge/split/drop 后漂移 | 所有 op 都要维护 ID 生命周期 | 高。适合 block/span/table 后处理 |
| detector 先生成 suspect | 降低 LLM 上下文和误判，让问题定位可测试 | 要写规则和测试 | 高。docpage2md 应先规则定位 OCR/结构疑点 |
| LLM 只裁决，不直接改全文 | 降低幻觉和任意改写 | 需要工具 schema 和 op executor | 高。尤其适合生产型转换工具 |
| 有限操作集 | 把改动限定为可验证动作 | 新错误类型要新增 op | 高。可从 merge/split/drop/promote/demote/strip 开始 |
| `apply_op_checked` 单入口 | 所有改动统一校验、审计、回滚 | 初期架构约束更重 | 高。建议 docpage2md 也不要让代码到处直接改 block |
| 保真闸门 | 防止新增内容、表格破坏、几何错误 | 对生成式任务过于严格，需要分层 | 高，但要按 OCR/生成/清洗分不同合同 |
| table body 专门 invariant | 普通字符 multiset 不适合 HTML/表格结构 | 实现复杂，测试成本高 | 中高。若 docpage2md 输出表格，值得做 |
| fail-open | 后处理失败不影响原始转换结果 | 需要 UI/API 明确提示 | 极高。应作为可选 refine 的默认策略 |
| cache key 包含逻辑/模型/prompt/flags | 避免重复成本和脏缓存 | key 漏字段会污染结果 | 高。LLM/OCR 都需要 |
| 结构化 report | 用户知道改了什么、删了什么、失败在哪 | 每个 op 都要写审计 | 极高。尤其适合调试图片转 Markdown 误差 |
| provenance | 字符级/单元格级追踪替换来源 | 记录粒度设计较复杂 | 高。先从 OCR 纠错和删除 span 做起 |
| progress 统一模型 | 长任务有反馈，多端一致 | CLI/Web/Python 要分别适配 | 高。docpage2md 多页处理需要 |
| mechanical prepass | 低风险规则清理不浪费 LLM | 规则需要维护 | 高。先做空白、页码、重复标记、URL 空格等 |
| opt-in OCR confusion | 修正常见 OCR 形近字 | 容易误改，需要白名单和密度限制 | 中高。中文 OCR 场景适合，默认应保守 |
| opt-in garbled table rewrite | 用视觉模型救结构化 OCR 已坏的表格 | 需要表格图片裁剪、视觉模型、结构闸门 | 视情况。如果 docpage2md 有表格 crop，则适合；否则成本高 |
| garbled degrade to image | 表格无法可靠转写时保留视觉信息 | Markdown 体验下降，需图片路径管理 | 中高。比输出坏表格更安全 |
| deterministic Markdown renderer | Markdown 是结构派生产物，便于测试 | 需要维护 renderer | 高。docpage2md 应避免多个地方各自拼 Markdown |
| mock LLM tests | 测试稳定、无网络、低成本 | 需要抽象模型接口 | 极高。任何模型功能都应可 mock |
| idempotence 测试 | 防止二次 refine 继续破坏结果 | 需要稳定输出和缓存策略 | 高。后处理器应二次运行 no-op |
| plugin 式端到端包装 | 把库能力变成用户工作流 | 需要维护依赖检测、目录约定、报告输出 | 中。取决于 docpage2md 是否要做 Codex/Claude 插件 |
| Rust core + 多语言绑定 | 高性能、一套逻辑多端复用 | Rust/PyO3/napi 发布复杂 | 低到中。当前 docpage2md 是 Python 项目，短期不建议优先迁移到 Rust |

## 9. 建议的 docpage2md 落地路线

### 9.1 第一阶段：无 LLM 的结构化 refine

目标：不引入新外部模型，不改变主业务代码大结构，只加一个可选后处理模块。

建议内容：

1. 定义 `RefineItem` 或继续使用 dict，但加内部 `_rid`。
2. 定义 report schema：
   - `opCounts`
   - `removedSpans`
   - `dismissedSuspects`
   - `violations`
   - `failOpen`
3. 实现 detector：
   - 页码/页眉页脚。
   - 空段落。
   - 重复换行。
   - 明显 Markdown 残留。
   - 疑似误标 heading。
4. 实现最小 op：
   - `drop`
   - `strip`
   - `mergeText`
   - `splitText`
   - `promoteHeading`
   - `demoteHeading`
5. 实现 `apply_op_checked`：
   - 每个 op 返回新 item list 和 audit。
   - 失败时不修改原数据。
6. 实现 invariant：
   - 非生成模式下不新增内容字符。
   - 删除必须进入 removed spans。
   - 图片路径、page index 不得凭空出现。
7. 加测试：
   - golden fixture。
   - no new chars。
   - schema passthrough。
   - fail-open。
   - idempotence。

这一阶段能吸收 mineru-refine 的最大收益，同时风险最低。

### 9.2 第二阶段：LLM 裁决但不自由改写

目标：只在规则 detector 发现疑点后，让 LLM 判断是否执行已有 op。

建议内容：

1. 抽象 `ChatClient`，测试用 mock。
2. 每个 suspect 构造小上下文，不发全文。
3. LLM 返回 JSON/tool call，字段只允许：
   - `op`
   - `targetId`
   - 必要参数
   - `reason`
4. 程序端执行 op，而不是让 LLM 返回改后的 Markdown。
5. 所有失败进入 dismissed/report。
6. cache key 包含 input hash、model、prompt version、logic version。

这一阶段不建议一开始做复杂 agent loop，可先做 single-pass suspect decision。等有真实样本证明需要观察工具和多轮，再引入完整 loop。

### 9.3 第三阶段：OCR confusion 与表格增强

目标：处理 OCR 常见错误和表格坏结构，但保留强审计。

建议内容：

1. OCR confusion：
   - 内置混淆类。
   - 用户额外 pair。
   - 单字符替换。
   - 密度限制。
   - provenance。
2. 表格：
   - 如果有单元格结构，先做 mechanical clean。
   - 如果有表格截图 crop，再考虑视觉重转写。
   - 视觉结果必须过结构闸门。
   - 不确定时降级为图片，而不是输出错误表格。

这部分要视 `docpage2md` 的真实输入和结构化程度决定，不宜在基础 refine 未稳定时提前做。

## 10. 不建议直接照搬的部分

### 10.1 不建议短期改成 Rust core

mineru-refine 的 Rust core 很完整，但它是为多语言分发和高可靠后处理设计的。`docpage2md` 当前工作区显示是 Python 项目，短期直接引入 Rust/PyO3 会带来：

- 构建链复杂。
- Windows 发布复杂。
- Python 业务调试门槛上升。
- 现有配置和模型管理需要跨语言同步。

更合理的路径是先在 Python 中迁移架构思想，等性能或多语言分发成为硬需求再考虑 Rust core。

### 10.2 不建议直接套用 MinerU 字段和 detector

mineru-refine 的很多规则依赖 MinerU schema：

- `text_level`
- `table_body`
- `table_caption`
- `img_path`
- `bbox`
- `page_idx`
- `list_items`

如果 `docpage2md` 的结构不同，必须先做 schema mapping。不能把 `detect.rs` 里的规则机械翻译成 Python，否则会产生大量误报。

### 10.3 不建议默认打开生成式纠错

mineru-refine 对 core 层坚持“不新增一个字”，对 OCR confusion 和 garbled rewrite 也做成 opt-in，并记录 provenance。`docpage2md` 如果默认让 LLM 润色/补全文字，会显著提高幻觉风险。

建议默认只启用保守结构清理；生成式增强必须显式开启，并在输出中标识 generated 来源。

## 11. 可作为 docpage2md 设计参考的接口草案

下面是基于 mineru-refine 思想给 `docpage2md` 的 Python 侧接口草案，不表示当前仓库已经实现：

```python
def refine_blocks(
    items: list[dict],
    *,
    input_sha256: str | None = None,
    max_iterations: int | None = None,
    fix_ocr_confusion: bool = False,
    rewrite_tables_with_vision: bool = False,
    progress: Callable[[dict], None] | None = None,
) -> dict:
    return {
        "items": refined_items,
        "provenance": provenance,
        "report": report,
    }
```

最小 report：

```json
{
  "logicVersion": "docpage2md-refine-0.1",
  "promptVersion": "p1",
  "modelId": "configured-model",
  "opCounts": {},
  "removedSpans": [],
  "dismissedSuspects": [],
  "violations": [],
  "tokenUsage": {"prompt": 0, "completion": 0},
  "failOpen": false
}
```

最小 op：

```json
{"op": "mergeText", "a": "blk_0001", "b": "blk_0002"}
{"op": "drop", "id": "blk_0003", "reason": "page_number"}
{"op": "strip", "id": "blk_0004", "pattern": "markdown_link_residue"}
{"op": "demoteHeading", "id": "blk_0005"}
{"op": "promoteHeading", "id": "blk_0006", "level": 2}
```

关键点不是字段名，而是保持这些约束：

- op 只引用稳定 ID。
- op executor 是唯一改动入口。
- 每个 op 都可 reject。
- reject 不修改原 items。
- 所有删除和替换进入 report/provenance。
- 返回前移除内部 ID。

## 12. 风险与注意事项

1. mineru-refine 的 README 与源码总体一致，但本文的实现细节以源码为准。
2. 本次研究未运行真实 LLM 调用，也未执行项目测试；测试体系分析来自测试源码。
3. `garbled.rs` 的中文词覆盖率逻辑是领域特定能力，不应在没有样本标定的情况下直接迁移。
4. `split_table` 视觉路径依赖 MinerU `img_path` 指向裁剪图。若 `docpage2md` 没有等价图片 crop，不能直接复用这类判断。
5. fail-open 必须在 UI/API 上显式暴露，否则用户可能误以为 refine 成功。
6. 严格 no-new-char 和 OCR 纠错存在天然冲突，必须分层处理。

## 13. 源码证据索引

核心文档：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\TODO.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\Cargo.toml`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\justfile`

Rust core：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\lib.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\types.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\id.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\detect.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\ops.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\invariant.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\agent_loop.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\refine.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\mechanical.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\confusion.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\garbled.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\markdown.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\llm.rs`

CLI/HTTP：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\cli.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\src\bin\server.rs`

绑定：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\python\src\lib.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\python\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\python\pyproject.toml`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\src\lib.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\index.js`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\index.d.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\package.json`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\bindings\js\test\smoke.test.ts`

脚本与 examples：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\mineru_fetch.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\bump_version.py`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\scripts\gen_cn_words.py`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\refine_real.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\offline_audit.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\qwen_smoke.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\examples\garbled_smoke.rs`

plugin：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\.claude-plugin\marketplace.json`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\.claude-plugin\plugin.json`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\README.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\skills\mineru-prime\SKILL.md`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\scripts\mineru_fetch.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\scripts\refine.ts`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\scripts\package.json`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\bin\mineru-prime-fetch`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\plugin\bin\mineru-prime-refine`

测试：

- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\common\mod.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\detect_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\ops_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\invariant_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\mechanical_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\markdown_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\loop_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\refine_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\confusion_test.rs`
- `D:\Repos\lab-python\工具\文档处理\mineru-refine\crates\mineru-refine\tests\garbled_test.rs`

