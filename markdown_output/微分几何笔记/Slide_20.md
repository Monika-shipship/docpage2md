# Slide 20

"⇐" $\tau=0 \Rightarrow \dot{\vec{b}}=0$, $\vec{b}$为常向量$\vec{C}$ ($\dot{\vec{b}}=-\tau\vec{n}$)  
$$
\frac{d}{ds} \langle \vec{r}'(s), \vec{b} \rangle = \langle \vec{r}''(s), \vec{b} \rangle = 0
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle = C
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle - C = 0
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle - C \langle \vec{b}, \vec{b} \rangle = 0
$$
$$
\langle \vec{r}'(s) - C\vec{b}, \vec{b} \rangle = 0
$$
$$
\text{令 } \vec{r}'(s_0) = C\vec{b} \quad \Rightarrow \quad \langle \vec{r}'(s) - \vec{r}'(s_0), \vec{b} \rangle = 0
$$

几何意义：离开平面的程度  

e.g. 求 $\vec{r}(t) = (a\cos t,\, a\sin t,\, bt)$ 的曲率和挠率  
$$
s(t) = \int_0^t \sqrt{(a\sin t)^2 + (a\cos t)^2 + b^2}\, dt = \sqrt{a^2 + b^2}\, t \equiv ct
$$
$$
\text{令 } \frac{1}{c}s \quad \Rightarrow \quad \vec{r}(s) = \left(a\cos\frac{s}{c},\, a\sin\frac{s}{c},\, \frac{bs}{c}\right)
$$
$$
\vec{r}'(s) = \dot{\vec{r}}(s) = \left(-\frac{a}{c}\sin\frac{s}{c},\, \frac{a}{c}\cos\frac{s}{c},\, \frac{b}{c}\right)
$$
$$
\ddot{\vec{r}}(s) = \left(-\frac{a}{c^2}\cos\frac{s}{c},\, -\frac{a}{c^2}\sin\frac{s}{c},\, 0\right)
$$
$$
\vec{t} = \kappa\vec{n},\quad \kappa(s) = |\ddot{\vec{r}}(s)| = \frac{a}{c^2} = \frac{a}{a^2 + b^2}
$$
$$
\vec{n} = \frac{\ddot{\vec{r}}}{|\ddot{\vec{r}}|} = \left(-\cos\frac{s}{c},\, -\sin\frac{s}{c},\, 0\right)
$$
$$
\vec{b} = \vec{t} \times \vec{n} = \begin{vmatrix}
\vec{i} & \vec{j} & \vec{k} \\
-\frac{a}{c}\sin\frac{s}{c} & \frac{a}{c}\cos\frac{s}{c} & \frac{b}{c} \\
-\cos\frac{s}{c} & -\sin\frac{s}{c} & 0
\end{vmatrix} = \left(\frac{b}{c}\sin\frac{s}{c},\, \frac{b}{c}\cos\frac{s}{c},\, \frac{a}{c}\right)
$$
$$
\dot{\vec{b}} = -\tau\vec{n}
$$
$$
\tau = |\dot{\vec{b}}| = \frac{b}{c^2} = \frac{b}{a^2 + b^2}
$$
$$
\kappa(s) = \frac{a}{a^2 + b^2},\quad \tau(s) = \frac{b}{a^2 + b^2}
$$

## Figure & Layout Description
The slide displays handwritten mathematical content on a grid paper background with light gray grid lines forming square cells (approximately 5mm x 5mm). The text is written in black ink with varying stroke weights indicating hand-written emphasis. The layout is vertically divided into two main sections:

1. **Upper Section (60% of height)**: Contains theoretical derivation of torsion properties with logical implications ("⇐" symbol), vector equations using angle brackets for inner products, and step-by-step algebraic manipulations. The equations are aligned left with decreasing indentation for subordinate steps. The phrase "几何意义：离开平面的程度" is centered below the derivation.

2. **Lower Section (40% of height)**: Contains a concrete example starting with "e.g." followed by parametric equations of a helix. The example includes integral calculations, vector differentiations, and determinant expansions. The final results for curvature and torsion are prominently displayed in larger handwriting. At the very bottom, there is a simple 3D coordinate system sketch with labeled x, y, z axes and a helical curve drawn around the z-axis.

The handwriting shows consistent mathematical notation with vector arrows ($\vec{r}, \vec{b}$), derivatives ($\dot{\vec{b}}$), and proper use of Greek letters (τ for torsion, κ for curvature). The grid paper background provides structural alignment for the equations.

<CTX>
{
   "topic": "挠率的几何意义与螺旋线实例计算：通过具体曲线验证挠率与曲率的计算方法",
   "keywords": ["挠率", "Frenet-Serret公式", "平面曲线", "螺旋线", "曲率"],
   "summary": "通过螺旋线参数方程的具体计算，验证挠率与曲率的公式推导，明确挠率表征空间曲线离开平面程度的几何意义",
   "pending_concepts": ["挠率的物理直观解释", "非平面曲线的挠率变化规律", "Frenet标架在三维运动中的应用"]
}
</CTX>