# Slide 18

$g^{\lambda\mu}(R_{\lambda\sigma\mu\nu} - R_{\lambda\nu\mu\sigma}) = 0$ 改成13

故 $R_{\sigma\mu}^{\mu} = R_{\nu\mu\sigma}^{\mu}$

故 $R_{\sigma\nu} = R_{\nu\sigma}$

标量曲率: curvature scalar :

$R = g^{\mu\nu}R_{\mu\nu}$

用里奇张量和度规缩并

有 Bianchi 恒等式

$$\partial_{\lambda}R_{\sigma\mu\nu}^{\rho} + \partial_{\mu}R_{\sigma\nu\lambda}^{\rho} + \partial_{\nu}R_{\sigma\lambda\mu}^{\rho} = 0$$

令 $\rho = \mu$，则

$$\partial_{\lambda}R_{\sigma\mu\nu}^{\mu} + \partial_{\mu}R_{\sigma\nu\lambda}^{\mu} + \partial_{\nu}R_{\sigma\lambda\mu}^{\mu} = 0$$

交换34反称

$$\partial_{\lambda}R_{\sigma\nu} + \partial_{\mu}R_{\sigma\nu\lambda}^{\mu} = \partial_{\nu}R_{\sigma\lambda}^{\mu}$$

由 $R_{\sigma\nu} = R_{\sigma\mu\nu}^{\mu}$ 是对称张量

$$\partial_{\lambda}R_{\sigma\nu} + \partial_{\mu}R_{\sigma\nu\lambda}^{\mu} = \partial_{\nu}R_{\sigma\lambda}$$

## Figure & Layout Description
手写内容书写在浅黄色方格纸背景上，方格线为浅灰色细线。文字以黑色墨水书写，字迹清晰但带有手写特征。公式与文字混合排布：顶部为第一行张量方程，右上角有蓝色手写注记"改成13"；中部包含三行推导结论，其中"故"字开头的两行公式垂直排列；下方有"标量曲率"标题及定义式，其下有中文注释"用里奇张量和度规缩并"；再往下是Bianchi恒等式部分，包含完整恒等式和指标替换后的变体，其中"令ρ=μ"行与公式分两行书写；右下角有蓝色手写注释"交换34反称"；最底部为对称性说明及最终推导式。公式中的张量指标存在上下标混合排布，部分希腊字母（如σ,ν,μ）在手写体中略显相似但可通过上下文区分。整体布局遵循从上至下的推导逻辑顺序，关键结论通过"故"字引导，重要注释使用蓝色墨水突出显示。

<CTX>
{
   "topic": "Ricci曲率张量对称性与Bianchi恒等式缩并推导",
   "keywords": ["Ricci对称性", "Bianchi恒等式缩并", "指标轮换", "度规缩并", "曲率标量定义"],
   "summary": "通过度规缩并操作验证Ricci张量的对称性，并推导Bianchi恒等式在指标替换后的简化形式，建立曲率标量与Ricci张量的关联",
   "pending_concepts": ["曲率标量的物理意义", "爱因斯坦场方程的构建基础", "共形曲率张量的分解方法"]
}
</CTX>