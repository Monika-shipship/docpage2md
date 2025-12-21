# Slide 41

④ $f(u) = \cos u$, $g(u) = \sin u$

$\vec{r}(u,v) = (\cos u \cos v, \cos u \sin v, \sin u)$

球面

## 2. 切平面和法向

考虑曲面 $S: \vec{r}(u,v) = (X(u,v), Y(u,v), Z(u,v)), (u,v) \in D$.

设 $P = P(u,v) \in S$

$P$ 点位置向量为 $\vec{r}(u,v)$

固定 $u = a$, 则 $\vec{r}(a,v)$ 是一条空间曲线

$\vec{r}(u,v)$ 在 $v = b$ 处的切向量为
$$\vec{r}_v(a,b) = \frac{\partial \vec{r}(u,v)}{\partial v}\bigg|_{v=b} = \frac{\partial \vec{r}}{\partial v}(a,b)$$
且与 $S$ 在点 $P_0$ 处相切 $P_0 = P(a,b)$

固定 $v = b$, 则 $\vec{r}(u,b)$ 是一条空间曲线, $u$ 变叫 $u$ 曲线

$\vec{r}(u,b)$ 在 $u = a$ 处的切向量为
$$\vec{r}_u(a,b) = \frac{\partial \vec{r}(u,b)}{\partial u}\bigg|_{u=a} = \frac{\partial \vec{r}}{\partial u}(a,b)$$
且与 $S$ 在点 $P_0$ 处相切 $P_0 = P(a,b)$

$\vec{r}_u$ 与 $\vec{r}_v$ 坐标切向量, $\vec{n} = \vec{r}_u \times \vec{r}_v$ 法向量, 所在直线 法线

正则即 $\vec{r}_u$ 与 $\vec{r}_v$ 线性无关, 张成切平面 $T_{P_0}S$

$\{P_0: \vec{r}_u, \vec{r}_v, \vec{r}_u \times \vec{r}_v\}$ 右手正交标架

## Figure & Layout Description

该PPT页面为手写数学笔记风格，背景为浅色方格纸。页面顶部左侧有带圈数字"④"，其右侧是关于球面参数方程的定义，包含函数$f(u)$和$g(u)$的表达式及向量函数$\vec{r}(u,v)$的完整表示，下方标注"球面"二字。

页面主体部分以"2. 切平面和法向"为二级标题，详细阐述曲面切平面与法向量的理论。文字内容为黑色手写体，公式清晰规范。右侧附有手绘曲面示意图，图中用黑色线条勾勒出曲面轮廓，蓝色标注"u=a, 称v曲线 $\vec{r}(a,v)$"，红色标注"v=b, 称为u曲线 $\vec{r}(u,b)$"。图中还用箭头标示了切向量$\vec{r}_u$、$\vec{r}_v$和法向量$\vec{n}=\vec{r}_u\times\vec{r}_v$，并标注"切平面"位置。示意图旁边有橙色手写注释"法向量"。

整体布局为左文右图结构，文字部分占据约2/3页面，图形部分占据右侧1/3。公式与文字混排，重要概念用不同颜色标注（右侧图示中的蓝色和红色标注），形成清晰的视觉层次。页面底部有"右手正交标架"的结论性描述。

<CTX>
{
   "topic": "曲面的切平面与法向量理论",
   "keywords": ["切平面", "法向量", "坐标切向量", "正则曲面", "右手正交标架"],
   "summary": "本页深入讲解曲面切平面与法向量的定义、计算方法及几何意义，阐述了坐标切向量与切平面的关系",
   "pending_concepts": ["曲面的第一基本形式", "高斯曲率与平均曲率", "曲面的第二基本形式", "参数化曲面的度量性质"]
}
</CTX>