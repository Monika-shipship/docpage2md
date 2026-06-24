---
title: "模型 & 价格 | DeepSeek API Docs"
source: "https://api-docs.deepseek.com/zh-cn/quick_start/pricing"
author:
published:
created: 2026-06-23
description: "下表所列模型价格以“百万 tokens”为单位。Token 是模型用来表示自然语言文本的的最小单位，可以是一个词、一个数字或一个标点符号等。我们将根据模型输入和输出的总 token 数进行计量计费。"
tags:
  - "clippings"
---
## 模型 & 价格

下表所列模型价格以“百万 tokens”为单位。Token 是模型用来表示自然语言文本的的最小单位，可以是一个词、一个数字或一个标点符号等。我们将根据模型输入和输出的总 token 数进行计量计费。

---

## 模型细节

**

<table><tbody><tr><td colspan="2">模型</td><td>deepseek-v4-flash <sup>(1)</sup></td><td>deepseek-v4-pro</td></tr><tr><td colspan="2">BASE URL (OpenAI 格式)</td><td colspan="2"><a href="https://api.deepseek.com/">https://api.deepseek.com</a></td></tr><tr><td colspan="2">BASE URL (Anthropic 格式)</td><td colspan="2"><a href="https://api.deepseek.com/anthropic">https://api.deepseek.com/anthropic</a></td></tr><tr><td colspan="2">模型版本</td><td>DeepSeek-V4-Flash</td><td>DeepSeek-V4-Pro</td></tr><tr><td colspan="2">思考模式</td><td colspan="2">支持非思考与思考模式（默认）<br>切换方式详见 <a href="https://api-docs.deepseek.com/zh-cn/guides/thinking_mode">思考模式</a></td></tr><tr><td colspan="2">上下文长度</td><td colspan="2">1M</td></tr><tr><td colspan="2">输出长度</td><td colspan="2">最大 384K</td></tr><tr><td rowspan="4">功能</td><td><a href="https://api-docs.deepseek.com/zh-cn/guides/json_mode">Json Output</a></td><td>支持</td><td>支持</td></tr><tr><td><a href="https://api-docs.deepseek.com/zh-cn/guides/tool_calls">Tool Calls</a></td><td>支持</td><td>支持</td></tr><tr><td><a href="https://api-docs.deepseek.com/zh-cn/guides/chat_prefix_completion">对话前缀续写（Beta）</a></td><td>支持</td><td>支持</td></tr><tr><td><a href="https://api-docs.deepseek.com/zh-cn/guides/fim_completion">FIM 补全（Beta）</a></td><td>仅非思考模式支持</td><td>仅非思考模式支持</td></tr><tr><td rowspan="3">价格</td><td>百万tokens输入（缓存命中）</td><td>0.02元</td><td>0.025元</td></tr><tr><td>百万tokens输入（缓存未命中）</td><td>1元</td><td>3元</td></tr><tr><td>百万tokens输出</td><td>2元</td><td>6元</td></tr><tr><td colspan="2">并发限制 <sup>(2)</sup></td><td>2500</td><td>500</td></tr></tbody></table>

**

(1) deepseek-chat 与 deepseek-reasoner 两个模型名将于北京时间 2026/07/24 23:59 弃用。出于兼容考虑，二者分别对应 deepseek-v4-flash 的非思考与思考模式。
(2) 更多并发限制细节，请参考 [限速与隔离](https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit)

---

## 扣费规则

扣减费用 = token 消耗量 × 模型单价，对应的费用将直接从充值余额或赠送余额中进行扣减。 当充值余额与赠送余额同时存在时，优先扣减赠送余额。

产品价格可能发生变动，DeepSeek 保留修改价格的权利。请您依据实际用量按需充值，定期查看此页面以获知最新价格信息。