# Slide 13

e.g. $\gamma(t) = (a \cos t, a \sin t)$  
$\vec{v} = \gamma'(t) = (-a \sin t, a \cos t)$  
$\vec{t} = \frac{\vec{v}}{|\vec{v}|} = (-\sin t, \cos t)$  
$\vec{n} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \vec{t} = (-\cos t, -\sin t)$  
$S = \int_0^t |\vec{v}| dt = a t$  
$\vec{t} = \left(-\sin \frac{S}{a}, \cos \frac{S}{a}\right)$  
$\vec{n} = \left(-\cos \frac{S}{a}, -\sin \frac{S}{a}\right)$  
$\vec{t}'(s) = \frac{1}{a} \vec{n}(s)$  
$\vec{n}'(s) = -\frac{1}{a} \vec{t}(s)$  

$\{ \vec{t}(s), \vec{b}(s), \vec{n}(s) \}$ 称 Frenet 标架  

$$
\begin{cases} 
\langle \vec{t}, \vec{t} \rangle = 1 \implies \langle \vec{t}', \vec{t} \rangle = 0 \implies \vec{t}' \parallel \vec{n},\ \vec{t}' = K \vec{n} \\
\langle \vec{n}, \vec{n} \rangle = 1 \implies \langle \vec{n}', \vec{n} \rangle = 0 \implies \vec{n}' \parallel \vec{t},\ \vec{n}' = g \vec{t} \\
\langle \vec{t}, \vec{n} \rangle = 0 \implies \langle \vec{t}', \vec{n} \rangle + \langle \vec{t}, \vec{n}' \rangle = 0 \implies K + g = 0 \implies \vec{n}' = -K \vec{t}
\end{cases}
$$

则 $\vec{t}' = K(s) \vec{n} \quad K(s) = \langle \vec{t}', \vec{n} \rangle$  
$\vec{n}' = -K(s) \vec{t}$  

$$
\frac{d}{ds} \begin{bmatrix} \vec{t} \\ \vec{n} \end{bmatrix} = \begin{bmatrix} 0 & K(s) \\ -K(s) & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \end{bmatrix}
$$
反映了曲线上每一点的弯曲程度  

由具体例，$a$为半径，  
$\vec{t}'(s) = \frac{1}{a} \vec{n}(s)$  
$\vec{n}'(s) = -\frac{1}{a} \vec{t}(s)$  
则 $K(s)$ 称为曲线的曲率  

## Figure & Layout Description
页面为方格纸背景的手写数学推导笔记。内容分为四个纵向区域：
1. 左上区域：从"e.g."开始的参数化曲线推导，包含6行公式，使用黑色墨水书写，矩阵用方括号表示
2. 中间区域：包含积分计算、参数替换公式，以及Frenet标架的定义文字
3. 左下区域：手绘的平面曲线示意图，标注了$\gamma(s)$（曲线上一点）、$\vec{t}(s)$（切向量，沿曲线切线方向）、$\vec{n}(s)$（法向量，指向曲线凹侧）三个向量
4. 右下区域：蓝色高亮的Frenet-Serret公式矩阵和"曲线的曲率"定义文字，蓝色区域覆盖2行内容，右侧有手写注释"反映了曲线上每一点的弯曲程度"

整体布局为从上至下的逻辑推导流，公式与图形穿插排列。关键公式（Frenet-Serret方程和曲率定义）用蓝色荧光笔标记，形成视觉焦点。所有向量符号均用箭头符号$\vec{}$表示，矩阵使用标准方括号格式。

<CTX>
{
   "topic": "Frenet-Serret公式与曲线曲率的定义",
   "keywords": ["Frenet标架", "曲率", "自然参数化", "切向量", "法向量", "Frenet-Serret公式"],
   "summary": "建立基于弧长参数的Frenet标架体系，推导出描述曲线弯曲特性的曲率公式，并通过矩阵形式的Frenet-Serret方程量化曲线几何性质",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的物理意义与数学表达"]
}
</CTX>