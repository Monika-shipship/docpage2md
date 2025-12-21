# Slide 37

$$\delta: D \to \overline{D},\ (x,y) \to (u,v) = \left( \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a},\ \arctan \frac{y}{x} \right)$$

$$\vec{r}_2(x,y) = \vec{r}_2 \circ \delta(x,y) = \vec{r}_2\left(u(x,y), v(x,y)\right) =$$
$$= \vec{r}_2\left( \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a},\ \arctan \frac{y}{x} \right)$$

$\vec{r}_2$ 和 $\vec{r}_1$ 是否为同一曲面？

$$
\begin{aligned}
&\arcsin x \quad x^2 + y^2 \leq a^2 \Rightarrow \frac{\sqrt{a^2 - x^2 - y^2}}{a} \leq 1 \Rightarrow \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a} \in \left[0, \frac{\pi}{2}\right] \\
&\Updownarrow \\
&u(x,y) \in \left[0, \frac{\pi}{2}\right]
\end{aligned}
$$

$$
\frac{y}{x} \in [-\infty, +\infty]
$$

$$
\arctan \frac{y}{x} \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right] \cup \left[\frac{\pi}{2}, \frac{3\pi}{2}\right] = [0, 2\pi]
$$

$$
u(x,y) \in [0, 2\pi]
$$

$\vec{r}_2(x,y)$ 表示完整的上半平面 $\left( \frac{y}{x} \text{ 扩充到 } -\infty \right)$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局呈纵向分层结构：
1. 顶部区域：用黑色墨水书写参数变换映射 $\delta$ 的定义，包含双变量函数表达式，其中 $\arcsin$ 和 $\arctan$ 项均以分数形式呈现，根号内为 $a^2 - x^2 - y^2$
2. 中上部：推导 $\vec{r}_2(x,y)$ 的复合函数表达式，分两行书写，第二行对参数进行展开
3. 中部：手写提问" $\vec{r}_2$ 和 $\vec{r}_1$ 是否为同一曲面？"，左侧配有 $\arcsin x$ 函数图像（坐标系中第一、三象限的S形曲线），右侧有简化的坐标轴示意图
4. 中下部：参数范围分析区域，包含三行推导：
   - 第一行展示 $x^2 + y^2 \leq a^2$ 的约束条件与 $\arcsin$ 取值范围的推导
   - 第二行标注 $y/x$ 的取值范围
   - 第三行分析 $\arctan$ 的取值范围合并过程
5. 底部：结论性陈述，包含 $\vec{r}_2(x,y)$ 的几何意义说明，其中"扩充到 $-\infty$"为手写补充说明
所有文字均为黑色手写体，公式符号与汉字混排，关键推导步骤用双向箭头（$\Updownarrow$）连接，部分区域有轻微涂改痕迹

<CTX>
{
   "topic": "球面参数化的覆盖范围与参数变换分析",
   "keywords": ["球面参数化", "参数变换", "上半球面", "参数范围", "覆盖范围"],
   "summary": "本页通过分析参数变换的取值范围，阐明了上半球面参数表示的完整覆盖特性及其与直角坐标的映射关系",
   "pending_concepts": ["参数连续性条件", "极点处的参数奇异性", "多参数片拼接机制"]
}
</CTX>