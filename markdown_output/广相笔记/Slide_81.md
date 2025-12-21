# Slide 81

$\partial_\mu (\sqrt{g} g^{\mu\nu}) = 0$ 等价于 $P^\lambda = P^\lambda_{\mu\nu} g^{\mu\nu} = 0$.

黎曼几何假设 $\nabla_\lambda g^{\mu\nu} = 0 \implies \nabla_\mu g^{\mu\nu} = 0$.

$P^\lambda_{\mu\nu} = \frac{\partial \ln \sqrt{g}}{\partial x^\mu} = \frac{1}{\sqrt{g}} \frac{\partial (\sqrt{g})}{\partial x^\mu}$.

$\partial_\lambda g^{\mu\nu} + P^\mu_{\lambda\alpha} g^{\alpha\nu} + P^\nu_{\lambda\alpha} g^{\mu\alpha} = 0$.

$\implies \partial_\mu g^{\mu\nu} + P^\mu_{\mu\alpha} g^{\alpha\nu} + P^\nu_{\mu\alpha} g^{\mu\alpha} = 0$.

$\partial_\mu g^{\mu\nu} + \frac{1}{\sqrt{g}} \frac{\partial \sqrt{g}}{\partial x^\alpha} g^{\alpha\nu} + P^\nu_{\mu\alpha} g^{\mu\alpha} = 0$.

$\underbrace{\partial_\mu g^{\mu\nu} + \frac{1}{\sqrt{g}} \frac{\partial \sqrt{g}}{\partial x^\alpha} g^{\alpha\nu}} + \underbrace{P^\nu_{\mu\alpha} g^{\mu\alpha}} = 0$

$\downarrow$

$\frac{1}{\sqrt{g}} \partial_\mu (\sqrt{g} g^{\mu\nu}) + P^\nu = 0$

故 $\partial_\mu (\sqrt{g} g^{\mu\nu}) = 0 \iff P^\nu = 0$.

满足上述条件时，坐标是调和函数 (Harmonious function, Harmonic coordinate condition)

$\Box x^\mu = \nabla^\lambda \nabla_\lambda x^\mu = 0$

$= g^{\nu\lambda} \nabla_\nu \nabla_\lambda x^\mu = 0$.

## Figure & Layout Description
图片为方格纸背景的手写推导稿，黑色墨水书写。内容从上至下排列，包含多行数学公式与中文说明。公式区域占据主要空间，其中：
1. 顶部以行内公式起始，包含协变导数符号 $\partial_\mu$ 和度规张量 $g^{\mu\nu}$
2. 中间部分有三处关键下划线标记：第一处横跨 $\partial_\mu g^{\mu\nu} + \frac{1}{\sqrt{g}} \frac{\partial \sqrt{g}}{\partial x^\alpha} g^{\alpha\nu}$ 项，第二处标记 $P^\nu_{\mu\alpha} g^{\mu\alpha}$ 项，第三处用向下箭头连接简化后的组合表达式
3. 公式中多次出现 Christoffel 符号 $P^\lambda_{\mu\nu}$ 的变体形式
4. 底部有英文术语 "Harmonious function" 和 "Harmonic coordinate condition" 的手写标注
5. 所有希腊字母（μ, ν, λ, α）均以标准手写体呈现，部分上标/下标存在轻微连笔但可辨识
6. 推导过程包含逻辑连接词 "等价于"、"故"、"满足...时" 等中文表述

<CTX>
{
   "topic": "谐和坐标条件的数学推导与调和函数性质",
   "keywords": ["谐和坐标条件", "Christoffel符号", "度规张量", "调和函数", "达朗贝尔算子", "协变导数", "弱场近似"],
   "summary": "本页通过度规张量的协变导数推导，严格证明了谐和坐标条件等价于坐标函数满足调和方程的数学本质",
   "pending_concepts": ["调和坐标在引力波实验中的具体应用", "非线性引力场中的坐标条件推广", "度规扰动h_μν与坐标条件的耦合效应"]
}
</CTX>