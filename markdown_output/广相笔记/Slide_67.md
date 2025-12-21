# Slide 67

$$
R_{00} = \partial_\lambda \Gamma^\lambda_{00} - \partial_0 \Gamma^\lambda_{\lambda 0} + \Gamma^\lambda_{\lambda \nu} \Gamma^\nu_{00} - \Gamma^\lambda_{0 \nu} \Gamma^\nu_{\lambda 0}
$$
$$
= \partial_\lambda \frac{1}{c^2}\partial_\lambda \phi - \partial_0 \frac{1}{c^2}\partial_0 \phi + \frac{1}{c^2}\partial_\lambda \phi \frac{1}{c^2}\partial_\lambda \phi - \frac{1}{c^2}\partial_\lambda \phi \frac{1}{c^2}\partial_\lambda \phi
$$
$\phi$不含时，$\partial_0(\partial_i \phi) = \partial_i(\partial_0 \phi) = 0$.

$$
R_{00} = \frac{1}{c^2}\partial_i \partial_i \phi.
$$
$$
R^0_0 = g^{00}R_{00} = -\left(1 - \frac{2\phi}{c^2}\right)\frac{1}{c^2}\partial_i \partial_i \phi \quad \phi \ll c
$$
$$
\approx -\frac{1}{c^2}\partial_i \partial_i \phi
$$
$$
R^0_0 = -\frac{4\pi G}{c^2}\rho
$$
所以 $4\pi G \rho = \partial_i \partial_i \phi$

对于点源（静止）$\rho = M\delta^3(\vec{x})$.
$$
\nabla^2 \phi = 4\pi G M \delta^3(\vec{x})
$$

## Figure & Layout Description
手写内容书写在浅黄色方格纸背景上，方格线为浅灰色细线构成标准坐标网格。文字和公式全部用黑色墨水手写，字迹清晰但带有自然书写倾斜度。内容垂直排列共9行，从上至下依次为：1) Ricci张量$R_{00}$的完整定义式；2) 代入度规扰动项后的展开式；3) 关于$\phi$不含时的中文注释；4) 简化后的$R_{00}$表达式；5) $R^0_0$的计算式及$\phi \ll c$近似条件；6) 近似后的简化结果；7) 与能量密度$\rho$的关系式；8) 中文推导结论"所以..."及点源密度说明；9) 最终泊松方程形式。公式中所有偏导符号$\partial$均带有清晰下标，希腊字母$\phi$与拉丁字母区分明显，矢量符号$\vec{x}$在最后一行有明显箭头标注。中文注释与数学公式交替出现，关键物理量$\rho$、$M$等使用标准物理符号书写。

<CTX>
{
   "topic": "从Ricci张量分量推导牛顿引力势的泊松方程：点源情况下的曲率-密度关系",
   "keywords": ["Ricci张量", "度规扰动", "Christoffel符号", "牛顿势", "泊松方程", "点源密度"],
   "summary": "本页完成从Ricci张量分量到泊松方程的完整推导，建立质量密度与引力势的微分关系并验证点源情况下的δ函数解",
   "pending_concepts": ["Christoffel符号非零分量的物理意义", "度规扰动项$h_{00}$的符号约定依据", "为何仅保留一阶小量项"]
}
</CTX>