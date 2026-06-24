---
title: "对话补全 | DeepSeek API Docs"
source: "https://api-docs.deepseek.com/zh-cn/api/create-chat-completion"
author:
published:
created: 2026-06-23
description: "根据输入的上下文，来让模型补全对话内容。"
tags:
  - "clippings"
---
## 对话补全

```markdown
POST https://api.deepseek.com/chat/completions
```

根据输入的上下文，来让模型补全对话内容。

## Request

- application/json

> [!-info] -info
> ### Body
>
> **
>
> required
>
> **
>
> > [!-info] -info
> > **
> >
> > messages
> >
> > **
> >
> > object\[\]
> >
> > required
>
> **model** stringrequired
>
> **Possible values:** \[`deepseek-v4-flash`, `deepseek-v4-pro`\]
>
> 使用的模型的 ID。
>
> > [!-info] -info
> > **
> >
> > thinking
> >
> > **
> >
> > object
> >
> > nullable
>
> **reasoning\_effort** string
>
> **Possible values:** \[`high`, `max`\]
>
> 控制模型的推理强度。对普通请求，默认为 `high` 。对一些复杂 Agent 类请求（如 Claude Code、OpenCode），自动设置为 `max` 。出于兼容考虑 `low` 、 `medium` 会映射为 `high`, `xhigh` 会映射为 `max` 。
>
> **max\_tokens** integernullable
>
> 限制一次请求中模型生成 completion 的最大 token 数。输入 token 和输出 token 的总长度受模型的上下文长度的限制。取值范围与默认值详见 [文档](https://api-docs.deepseek.com/zh-cn/quick_start/pricing) 。
>
> > [!-info] -info
> > **
> >
> > response\_format
> >
> > **
> >
> > object
> >
> > nullable
>
> > [!-info] -info
> > **
> >
> > stop
> >
> > **
> >
> > object
> >
> > **
> >
> > nullable
> >
> > **
>
> **stream** booleannullable
>
> 如果设置为 True，将会以 SSE（server-sent events）的形式以流式发送消息增量。消息流以 `data: [DONE]` 结尾。
>
> > [!-info] -info
> > **
> >
> > stream\_options
> >
> > **
> >
> > object
> >
> > nullable
>
> **temperature** numbernullable
>
> **Possible values:** `<= 2`
>
> **Default value:** `1`
>
> 采样温度，介于 0 和 2 之间。更高的值，如 0.8，会使输出更随机，而更低的值，如 0.2，会使其更加集中和确定。 我们通常建议可以更改这个值或者更改 `top_p` ，但不建议同时对两者进行修改。
>
> **top\_p** numbernullable
>
> **Possible values:** `<= 1`
>
> **Default value:** `1`
>
> 作为调节采样温度的替代方案，模型会考虑前 `top_p` 概率的 token 的结果。所以 0.1 就意味着只有包括在最高 10% 概率中的 token 会被考虑。 我们通常建议修改这个值或者更改 `temperature` ，但不建议同时对两者进行修改。
>
> > [!-info] -info
> > **
> >
> > tools
> >
> > **
> >
> > object\[\]
> >
> > nullable
>
> > [!-info] -info
> > **
> >
> > tool\_choice
> >
> > **
> >
> > object
> >
> > **
> >
> > nullable
> >
> > **
>
> **logprobs** booleannullable
>
> 是否返回所输出 token 的对数概率。如果为 true，则在 `message` 的 `content` 中返回每个输出 token 的对数概率。
>
> **top\_logprobs** integernullable
>
> **Possible values:** `<= 20`
>
> 一个介于 0 到 20 之间的整数 N，指定每个输出位置返回输出概率 top N 的 token，且返回这些 token 的对数概率。指定此参数时，logprobs 必须为 true。
>
> **user\_id** nullable
>
> 您自定义的 user\_id，可选字符集为 \[a-zA-Z0-9\\-\_\]，最大长度为 512。请不要在 user\_id 中包含用户隐私信息。
>
> - user\_id 可用于区分您业务侧的用户身份，以帮助我们进行内容安全处理。
> - user\_id 可用于 KVCache 缓存隔离，以进行隐私管理。
> - user\_id 可用于我们对您业务侧用户进行调度隔离。
> - 关于 user\_id 参数更详细的描述，请参考 [限速与隔离](https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit)
>
> **frequency\_penalty** deprecated
>
> 该参数已不再支持。传入该参数将不会产生任何效果。
>
> **presence\_penalty** deprecated
>
> 该参数已不再支持。传入该参数将不会产生任何效果。

- curl
- python
- go
- nodejs
- ruby
- csharp
- php
- java
- powershell

- OpenAI SDK

- REQUESTS
- HTTP.CLIENT

ResponseClear

Click the `Send API Request` button above and see the response here!