# Slide 75

所以 $\delta I_g = \frac{c^3}{16\pi G} \int_M G_{\mu\nu} \sqrt{-g} g^{\mu\nu} d^4 x$  
$= \frac{c^3}{16\pi G} \int_M \left( R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} \right) \sqrt{-g} g^{\mu\nu} d^4 x$

2.5.3. 总的作用量  
$I = I_g + I_m$  
$\uparrow \quad \uparrow$  
引力场 $\quad$ 引力源物质  

FLRW Metric $\frac{\ddot{a}}{a} = H$ 哈勃，可观测.  
$\frac{\ddot{a}}{a} < 0$ 减速因子<0, 加速  
$ds^2 = -c^2 dt^2 + a(t)^2 \left[ \frac{dr^2}{1-kr^2} + r^2 (d\theta^2 + \sin^2\theta d\phi^2) \right]$

$I_g = \int_M \mathcal{L}_g \sqrt{-g} d^4 x, \; \mathcal{L}_g = \frac{c^3}{16\pi G} R$

$I_m = \frac{1}{c} \int_M \mathcal{L}_m \sqrt{-g} d^4 x, \; \mathcal{L}_m$ 引力源物质的拉格朗日量  
$\uparrow \quad ??? \quad \text{if so}, \; \mathcal{L}_m \sim \frac{J}{x^3}, \; \text{拉氏密度}$

假设 $\mathcal{L}_m$ 不含 $g^{\mu\nu}$, 引力场只是背景,  
再作变分 $\delta I_m = \frac{1}{c} \int_M \frac{\partial (\mathcal{L}_m \sqrt{-g})}{\partial g^{\mu\nu}} \delta g^{\mu\nu} d^4 x$

## Figure & Layout Description
图片展示一张浅黄色方格纸背景的手写笔记，网格线为浅蓝色，文字为黑色墨水手写体。页面内容从上至下垂直排布，分为四个主要区域：  
1. 顶部区域：包含两行行间公式，使用连分数和积分符号，公式中包含$c^3$、$16\pi G$、$G_{\mu\nu}$等张量符号，积分域标记为$M$，微分项为$d^4 x$。  
2. 中上区域：以"2.5.3. 总的作用量"作为二级标题（手写体加粗），下方有$I = I_g + I_m$公式，其下用两个向上箭头标注"引力场"和"引力源物质"，文字略小于公式。右侧并列"FLRW Metric"标题，其下有$\frac{\ddot{a}}{a} = H$等宇宙学参数说明及$ds^2$度规公式，该公式包含分式结构和三角函数项。  
3. 中下区域：包含$I_g$和$I_m$的定义公式，其中$I_m$公式下方有向上箭头指向"???"符号，右侧标注"if so"条件语句及$\mathcal{L}_m \sim \frac{J}{x^3}$关系式。  
4. 底部区域：两行文字说明，第一行"假设 $\mathcal{L}_m$ 不含 $g^{\mu\nu}$..."为常规手写体，第二行变分公式$\delta I_m = ...$为完整行间公式。  
整体布局层次分明，公式与文字穿插，关键术语（如"FLRW Metric"）使用大写英文字母突出，手写笔迹流畅但部分连笔（如"拉格朗日量"的"日"字略模糊）。公式中的张量指标（如$\mu\nu$）采用标准下标位置，积分符号和根号清晰可辨。

<CTX>
{
   "topic": "总引力作用量的分解结构与物质部分变分原理",
   "keywords": ["总作用量分解", "FLRW度规", "物质拉格朗日量", "变分原理", "引力场背景假设"],
   "summary": "本页阐述了总引力作用量的分解结构，包括引力场部分和物质部分，并引入FLRW宇宙学度规及变分原理在物质作用量中的应用，明确物质拉格朗日量与度规的依赖关系假设",
   "pending_concepts": ["Einstein场方程的具体导出过程", "弱场近似下GR与Newton理论的定量对应", "16π系数的数学起源", "物质拉格朗日量Lm的显式表达式", "FLRW度规中k参数的物理意义"]
}
</CTX>