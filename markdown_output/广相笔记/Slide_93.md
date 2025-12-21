# Slide 93

$V' = \frac{e^{-\lambda} - 1}{r}, \quad \lambda' = \frac{1 - e^{\lambda}}{r}$

所以 $\lambda' + V' = 0 \implies \lambda + V = f(t)$.

而 $\lambda = \lambda(r)$ 与 $(t)$ 无关

$\frac{\partial V}{\partial t} = \frac{\partial f(t)}{\partial t}$

$\frac{\partial}{\partial t}(V - f(t)) = 0$

故 $V - f(t) = \overline{V}(r)$

作时间尺度变换：

$\tilde{t} = \psi(t)$

$(d\tilde{t})^2 = \left(\frac{d\psi}{dt}\right)^2 (dt)^2$

若 $\left(\frac{d\psi}{dt}\right)^2 = e^{f(t)}$

有 $(d\tilde{t})^2 = e^{f(t)} (dt)^2 \implies (dt)^2 = e^{-f(t)} (d\tilde{t})^2$

$\implies e^{V}(dt)^2 = e^{V - f(t)} (d\tilde{t})^2 = e^{\overline{V}} (d\tilde{t})^2$.

## Figure & Layout Description
图片呈现于浅黄色方格纸背景上，手写内容以黑色墨水为主，关键推导步骤用红色墨水标注。顶部并列书写两个度规函数微分表达式，采用分式结构。其下方有一行红色手写体文字，包含"所以"等推导连接词，使用箭头符号表示逻辑推导关系。中间区域为多行黑色推导步骤，包含偏导数运算、函数关系式和时间坐标变换设定。公式与文字垂直排列，行间距均匀，占据页面主要区域。红色文字在视觉上形成强调效果，与黑色内容形成层次区分。所有数学符号书写规范，分式结构清晰，指数符号使用上标形式。页面无边框或装饰元素，完全聚焦于数学推导过程的呈现。

<CTX>
{
   "topic": "中心球对称Einstein场方程的时间坐标变换与度规不变性分析",
   "keywords": ["Einstein场方程", "度规函数ν", "度规函数λ", "时间坐标变换", "度规不变性"],
   "summary": "本页通过时间坐标变换推导出度规函数的不变性关系，建立了原始坐标与新坐标系下度规分量的转换关系",
   "pending_concepts": ["时间坐标变换的具体物理意义", "e^ν的物理诠释", "Schwarzschild解的完整推导路径", "坐标奇点与物理奇点的数学判据"]
}
</CTX>