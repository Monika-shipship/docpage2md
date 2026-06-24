# 模型管理器架构

## 目标

模型管理器的目标是把不同阶段用到的模型从硬编码中解耦出来，让用户可以按角色、档位和第三方 API 灵活切换。

当前固定角色：

- `layout_engine`：MinerU 精准解析 API，默认 `vlm`。
- `page_vision`：整页视觉识别。
- `crop_vision`：图、表、公式 crop 精读。
- `ocr_helper`：可选 OCR 专用模型。
- `brain`：前后页上下文纠错。
- `refiner`：局部 suspect 裁决。
- `reviewer`：可选内容正确性审查。

## 默认档位

`cheap`：

- `layout_engine`: MinerU `vlm`
- `page_vision`: `qwen3-vl-flash`
- `crop_vision`: `qwen3-vl-flash`
- `ocr_helper`: `qwen-vl-ocr-latest`
- `brain`: `deepseek-v4-flash`
- `refiner`: `deepseek-v4-flash`

`balanced`：

- `layout_engine`: MinerU `vlm`
- `page_vision`: `qwen3-vl-plus`
- `crop_vision`: `qwen3-vl-plus`
- `ocr_helper`: `qwen-vl-ocr-latest`
- `brain`: `deepseek-v4-flash`
- `refiner`: `deepseek-v4-flash`

`accurate`：

- `layout_engine`: MinerU `vlm`
- `page_vision`: `qwen3.7-plus`
- `crop_vision`: `qwen3.7-plus`
- `ocr_helper`: `qwen-vl-ocr-latest`
- `brain`: `deepseek-v4-pro`
- `refiner`: `deepseek-v4-pro`

`manual`：

- 用户逐个 role 选择 provider、model、base_url、api_key_env。
- 支持 OpenAI-compatible 第三方 API。
- 支持把视觉、Brain、refiner 全部切到第三方服务。

## 数据结构

当前实现入口是 `docpage2md_app/model_profiles.py`，核心数据结构是 `RoleBinding`：

```text
role
provider
model
base_url
api_key_env
thinking_enabled
json_mode
supports_vision
note
```

后续如需扩展完整 registry，可增加：

```text
Provider
  name
  api_style
  base_url
  api_key_env
  supports_vision
  supports_json
  supports_thinking
  supports_tools

Model
  id
  provider
  roles
  context_window
  max_output
  price_ref
  quality_tier
  supports_images
  supports_reasoning_content
```

## 安全约束

- 配置文件、缓存、report 只允许保存环境变量名，不保存 key 值。
- `run_report.json` 只记录 provider、model、base_url、api_key_env。
- 如果用户误把疑似 token 写入模型配置，启动时应提示迁移到环境变量。
- 模型 `reasoning_content` 不写入 Markdown；默认也不持久化原始思考过程。

## 价格来源

默认不联网刷新价格。价格优先来自本地文档：

- `docs/deepseek-api/模型 & 价格 _ DeepSeek API Docs.md`
- `docs/reference-pricing/模型调用计费2026.6.23.md`

联网刷新或导入复制版价格页应作为显式命令，不在主流程自动执行。
