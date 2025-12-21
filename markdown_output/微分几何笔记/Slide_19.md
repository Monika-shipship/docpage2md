# Slide 19

$\vec{b} = ? \quad \vec{b} = \vec{t} \wedge \vec{n}$

$\dot{\vec{b}} = \dot{\vec{t}} \wedge \vec{n} + \vec{t} \wedge \dot{\vec{n}}$

$= k(s) \vec{n} \wedge \vec{n} + \vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$

$= \underset{0}{k(s)\vec{n}\wedge\vec{n}} + \underset{0 + \tau(-\vec{n})}{\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})}$

$\dot{\vec{b}} = -\tau \vec{n}$

$$
\begin{cases}
\dot{\vec{t}} = \qquad k(s) \vec{n} \\
\dot{\vec{n}} = -k(s) \vec{t} \qquad + \tau \vec{b} \\
\dot{\vec{b}} = \qquad -\tau \vec{n}
\end{cases}
$$

$$
\frac{d}{dt}\begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix} = \begin{bmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix}
$$

<span style="color:red">$\tau$称挠率</span>

下讲其几何意义

设空间曲线 $\vec{r}$ 的曲率 $k > 0$，则 $\vec{r}$ 落在某个平面上的充要条件是 $\tau = 0$。

证 "$\Rightarrow$" 设 $\pi$ 是空间中的一张平面，设 $\vec{a}$ 是垂直于 $\pi$ 的单位向量

$<\vec{r}(s) - \vec{r}(s_0), \vec{a}> = 0$

求导得 $<\vec{t}(s), \vec{a}> = 0$

再求导得 $<k(s)\vec{n}(s), \vec{a}> = 0$

因 $k(s) > 0$ 空间曲线

$<\vec{n}(s), \vec{a}> = 0$

$<\dot{\vec{n}}(s), \vec{a}> = 0$  $<-k(s)\vec{t}(s) + \tau \vec{b}, \vec{a}> = 0$

$\vec{a} \perp \vec{t}, \vec{a} \perp \vec{n}, \vec{b} = \vec{t} \wedge \vec{n} \Rightarrow \vec{b} \parallel \vec{a}$

$\vec{b}, \vec{a}$ 单位向量 $\Rightarrow \vec{b} = \pm \vec{a}$

而 $<\tau \vec{b}, \vec{a}> = 0$

$\tau = 0$ 才相符

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记。整体布局从上至下分为三个主要区域：

1. **顶部区域**：包含Frenet标架中副法向量导数的推导过程。首先提出问题"$\vec{b} = ?$"，接着给出$\vec{b} = \vec{t} \wedge \vec{n}$的定义。然后推导$\dot{\vec{b}}$，使用向量叉积法则展开为$\dot{\vec{t}} \wedge \vec{n} + \vec{t} \wedge \dot{\vec{n}}$。进一步代入Frenet公式得到$k(s)\vec{n}\wedge\vec{n}$和$\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$，其中$k(s)\vec{n}\wedge\vec{n}$下方标注"0"，$\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$下方标注"0 + τ(-n̅)"。最终得到$\dot{\vec{b}} = -\tau \vec{n}$。

2. **中部区域**：包含Frenet-Serret公式的完整表达。左侧用大括号包裹三个方程：$\dot{\vec{t}} = k(s)\vec{n}$、$\dot{\vec{n}} = -k(s)\vec{t} + \tau \vec{b}$、$\dot{\vec{b}} = -\tau \vec{n}$。下方以矩阵形式表示为$\frac{d}{dt}\begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix} = \begin{bmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix}$。

3. **底部区域**：包含红色手写文字"τ称挠率"，下方是"下讲其几何意义"的提示。接着是关于空间曲线平面性的定理："设空间曲线$\vec{r}$的曲率$k > 0$，则$\vec{r}$落在某个平面上的充要条件是$\tau = 0$"。随后是证明部分，从"证"⇒""开始，通过向量内积性质逐步推导，包含多个内积等式和逻辑推导步骤。

视觉特征：文字为黑色手写体，关键术语"τ称挠率"用红色标注。公式推导过程中有下划线和注释说明中间步骤（如"0"标注）。整体书写在方格纸上，文字排列较为紧凑但层次分明，公式与文字说明交替出现。

<CTX>
{
   "topic": "挠率的定义与几何意义：Frenet-Serret公式的完整表达及平面曲线判定条件",
   "keywords": ["挠率", "Frenet-Serret公式", "平面曲线", "向量内积", "曲率"],
   "summary": "完成Frenet标架的完整微分方程组，定义挠率参数并证明空间曲线为平面曲线的充要条件是挠率为零",
   "pending_concepts": ["挠率的物理直观解释", "非平面曲线的挠率变化规律", "Frenet标架在三维运动中的应用"]
}
</CTX>