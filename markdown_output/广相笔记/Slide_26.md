# Slide 26

因此 $\frac{1}{4} \frac{\varepsilon^{\lambda\sigma}}{\sqrt{g}} \frac{\varepsilon^{\mu\nu}}{\sqrt{g}} R_{\lambda\sigma\mu\nu}$ 是标量  
在坐标变换下不变  
$$
= \frac{1}{4} \left( \frac{\varepsilon^{12}}{\sqrt{g}} \frac{\varepsilon^{12}}{\sqrt{g}} R_{1212} + \frac{\varepsilon^{12}}{\sqrt{g}} \frac{\varepsilon^{21}}{\sqrt{g}} R_{1221} \right. \\
\left. + \frac{\varepsilon^{21}}{\sqrt{g}} \frac{\varepsilon^{12}}{\sqrt{g}} R_{2112} + \frac{\varepsilon^{21}}{\sqrt{g}} \frac{\varepsilon^{21}}{\sqrt{g}} R_{2121} \right)
$$
$\varepsilon^{12} = 1 \quad \varepsilon^{21} = -1 \quad R_{1212} = -R_{1221}$  
$= -R_{2112} = R_{2121}$  
故 $= \frac{1}{4} \cdot 4 \frac{R_{1212}}{g} = \frac{R_{1212}}{g}$ 是标量，不变量.  

Gauss曲率：$K = -\frac{R_{1212}}{g}$ 是不变量  
$$
K = -\frac{1}{4} \frac{\varepsilon^{\lambda\sigma}}{\sqrt{g}} \frac{\varepsilon^{\mu\nu}}{\sqrt{g}} R_{\lambda\sigma\mu\nu}
$$
$$
\chi(K) = \frac{1}{2\pi} \int_{\Sigma} K ds
$$
$n=2k$ 维流形上 GBC 仍适用.

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局呈纵向分层结构。顶部以"因此"起始的结论性语句占据第一行，采用较大字号手写体；第二行"在坐标变换下不变"作为过渡说明。中间部分为多行公式推导，包含四组Riemann曲率张量项的展开，公式通过等号对齐形成清晰的逻辑流，其中$\varepsilon$张量的上标组合（12,21）与曲率张量下标组合（1212,1221等）通过手写斜体区分。关键关系式$\varepsilon^{12}=1$等单独成行并列排布。推导结果部分使用"故"字引导，最终简化为$\frac{R_{1212}}{g}$的表达式。底部区域包含Gauss曲率定义、曲率张量的Levi-Civita表示式、欧拉示性数积分公式，以及关于Gauss-Bonnet定理适用维度的结论性说明。所有文字均为黑色墨水书写，公式中张量指标采用手写斜体，分式结构通过水平线清晰呈现，关键符号（如$\sqrt{g}$）保留根号手写形态。

<CTX>
{
   "topic": "Gauss曲率不变性与Gauss-Bonnet定理的二维形式",
   "keywords": ["Levi-Civita张量", "度规行列式", "Gauss曲率", "欧拉示性数", "Gauss-Bonnet定理"],
   "summary": "本页通过Levi-Civita张量推导出Gauss曲率作为坐标不变量的表达式，并建立其与欧拉示性数的积分关系，完成二维曲面Gauss-Bonnet定理的数学表述",
   "pending_concepts": ["高维Gauss-Bonnet定理的推广形式", "Hodge对偶算子在曲率积分中的作用", "流形边界条件对欧拉示性数的影响"]
}
</CTX>