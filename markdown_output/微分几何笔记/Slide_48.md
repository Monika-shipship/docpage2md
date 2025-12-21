# Slide 48

故

$$ \langle \vec{n}_{(u_0,v_0)}, \Delta \vec{r} \rangle = \frac{1}{2} \left( \langle \vec{n}, \vec{r}_{uu} \rangle \Delta u^2 + 2 \langle \vec{n}, \vec{r}_{uv} \rangle \Delta u \Delta v + \langle \vec{n}, \vec{r}_{vv} \rangle \Delta v^2 \right) + O(\Delta u^2 + \Delta v^2) $$

设为 $\delta := \langle \vec{n}, \Delta \vec{r} \rangle$

$\delta$ 是到切平面的有向距离

$\delta > 0$, $\Delta \vec{r}$ 指向 $\vec{n}$ 同侧

$\delta < 0$, $\Delta \vec{r}$ 指离 $\vec{n}$ 同侧

$\Delta u^2 + \Delta v^2$ 充分小时

$$ \delta = \frac{1}{2} \left( L \, du \, du + 2M \, du \, dv + N \, dv \, dv \right) = \frac{1}{2} \text{II}(d\mathbf{r}) $$

几何意义：沿着某个方向，离开切平面的程度

e.g. 3.1

柱面 $\vec{r} = (x(u), y(u), v)$, $u$ 是弧长参数 $x_u^2 + y_u^2 = 1$

$\vec{r}_u = (x_u, y_u, 0)$  
$\vec{r}_v = (0, 0, 1)$  
$\vec{n} = \frac{\vec{r}_u \times \vec{r}_v}{|\vec{r}_u \times \vec{r}_v|} = \begin{vmatrix} i & j & k \\ x_u & y_u & 0 \\ 0 & 0 & 1 \end{vmatrix} = (y_u, -x_u, 0)$

$\vec{r}_{uu} = (x_{uu}, y_{uu}, 0)$  
$\vec{r}_{uv} = \vec{r}_{vu} = (0, 0, 0)$  
$\vec{r}_{vv} = (0, 0, 0)$

## Figure & Layout Description
图片为手写数学推导内容，背景是浅黄色方格纸（1cm×1cm网格）。文字以黑色墨水书写，关键符号"δ"用蓝色墨水突出标注。整体布局为垂直流式结构：顶部是"故"字引导的行间公式；其下是"设为"定义行，其中"δ"符号为蓝色；接着是四行文本说明，包含δ的几何意义和符号条件；随后是"Δu²+Δv²充分小时"的条件说明；再下方是第二行间公式；接着是"几何意义"的说明行；最后是"e.g. 3.1"示例部分，包含柱面参数化定义和多行向量计算。公式中的向量符号（如$\vec{n}$）均带有箭头标记，行列式使用标准三阶矩阵表示，所有下标（如$uu$, $uv$）清晰可辨。页面无标题栏或页脚，所有内容集中在方格纸中央区域，文字密度适中，行间距约1.5个网格高度。蓝色标注仅出现在"δ"符号处，用于强调核心变量，形成视觉焦点。

<CTX>
{
   "topic": "第二基本形式的几何意义与柱面实例验证",
   "keywords": ["第二基本形式", "有向距离", "法向分量", "柱面参数化", "曲面弯曲度量"],
   "summary": "本页通过有向距离δ的定义阐明第二基本形式的几何本质，并以柱面为例完成具体计算，验证了曲面局部弯曲的二阶微分特性",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的测地线理论", "曲面的黎曼度量", "曲面局部展开的几何应用"]
}
</CTX>