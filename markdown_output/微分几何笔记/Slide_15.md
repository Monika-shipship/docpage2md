# Slide 15

e.g. $\vec{r} = (\cos(s), \sin(s))$

e.g. $\vec{r} = (\cos(-s), \sin(-s))$

$\vec{t}(s) = \vec{r}'(s) = (\sin(-s), -\cos(-s))$

$\vec{n}(s) = \vec{t}'(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \vec{t}(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$

$\vec{t}'(s) = (-1) \vec{n} \quad k(s) = -1$

e.g. $\vec{r}(t) = (t, \sin t)$

$S(t) = \int_0^t |\vec{r}'(u)|  du = \int_0^t \sqrt{1 + \cos^2 u}  du$

$\frac{ds}{dt} = \sqrt{1 + \cos^2 u}$

$\vec{t}(s) = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds} = (1, \cos t) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{n}(s) = \vec{t}(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = (-\cos t, 1) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{t}'(s) = \frac{d\vec{t}}{ds} = \frac{d\vec{t}}{dt} \frac{dt}{ds} = \left(-\frac{1}{2} \frac{2\cos t(-\sin t)}{(1 + \cos^2 t)^{3/2}}, \star \right) \frac{1}{\sqrt{1 + \cos^2 t}}$

$= \left( \frac{\cos t \sin t}{(1 + \cos^2 t)^{3/2}}, \star \right) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{t}' = k(s) \vec{n}$

$k(s) = \frac{-\sin t}{(1 + \cos^2 t)^{3/2}} \quad k = \frac{y''}{(1 + y'^2)^{3/2}}$

e.g. 一般参数方程的曲线 $\vec{r} = (x(t), y(t))$

$S(t) = \int_0^t \sqrt{(x'(t))^2 + (y'(t))^2}  dt$

$\frac{ds}{dt} = \sqrt{x'^2 + y'^2}$

$\vec{t} = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds} = (x'(t), y'(t)) \frac{1}{\sqrt{x'^2 + y'^2}}$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局分为三个主要区域。顶部区域左右并列两个几何示意图：左侧图显示一个以原点为中心的单位圆，坐标系中y轴正向标注蓝色向量$\vec{t}(s)$和$\vec{n}(s)$，右侧蓝色标注"$k(s) > 0$"；右侧图同样为单位圆，但向量方向相反，标注蓝色向量$\vec{t}(s)$和$\vec{n}(s)$，右侧蓝色标注"$k(s) < 0$"，其右侧附有一个小型坐标系示意图。中部区域包含圆曲线的向量计算公式，包括切向量、法向量和曲率关系式，其中矩阵$\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$被多次使用。底部区域分为两部分：上半部分是参数曲线$\vec{r}(t) = (t, \sin t)$的详细推导，包含弧长积分、切向量和法向量计算；下半部分是一般参数曲线的通用公式推导。文字主要为黑色手写体，关键标注（如曲率符号）使用蓝色墨水，所有公式和文字均写在方格坐标纸上，形成清晰的行列对齐结构。

<CTX>
{
   "topic": "曲率的计算实例与一般参数曲线的曲率公式",
   "keywords": ["弧长参数化", "曲率计算", "弯曲方向判定", "法向量旋转", "参数曲线曲率"],
   "summary": "通过圆和正弦曲线的具体示例演示曲率计算过程，建立曲率符号与曲线弯曲方向的对应关系，并推导出一般参数曲线的显式曲率公式",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的几何意义与数学表达"]
}
</CTX>