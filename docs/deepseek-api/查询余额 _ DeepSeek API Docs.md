---
title: "查询余额 | DeepSeek API Docs"
source: "https://api-docs.deepseek.com/zh-cn/api/get-user-balance"
author:
published:
created: 2026-06-23
description: "查询账号余额"
tags:
  - "clippings"
---
## 查询余额

```markdown
GET https://api.deepseek.com/user/balance
```

## Responses

- 200

OK, 返回用户余额详情

- application/json

> [!-info] -info
> **
>
> Schema
>
> **
>
> **is\_available** boolean
>
> 当前账户是否有余额可供 API 调用
>
> > [!-info] -info
> > **
> >
> > balance\_infos
> >
> > **
> >
> > object\[\]
> >
> > - Array \[
> >
> > **currency** string
> >
> > **Possible values:** \[`CNY`, `USD`\]
> >
> > 货币，人民币或美元
> >
> > **total\_balance** string
> >
> > 总的可用余额，包括赠金和充值余额
> >
> > **granted\_balance** string
> >
> > 未过期的赠金余额
> >
> > **topped\_up\_balance** string
> >
> > 充值余额
> >
> > - \]

```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

```json
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "110.00",
      "granted_balance": "10.00",
      "topped_up_balance": "100.00"
    }
  ]
}
```

- curl
- python
- go
- nodejs
- ruby
- csharp
- php
- java
- powershell

Response

Click the `Send API Request` button above and see the response here!