# Slide 72

由于 $g_{\mu\nu} = g_{\nu\mu}$，$\delta g = g^{\mu\nu} \delta g_{\mu\nu}$，$g = -g_{\mu\nu} \delta g^{\mu\nu} g$.  
$$\delta \sqrt{-g} = \frac{-1}{2\sqrt{-g}} \cdot \delta g = -\frac{1}{2\sqrt{-g}} \left( -g_{\mu\nu} \delta g^{\mu\nu} g \right)$$  
$$= \frac{1}{2} \sqrt{-g} \, g_{\mu\nu} \delta(g^{\mu\nu}) \quad . \quad \frac{g}{\sqrt{-g}} = \frac{(-g)}{\sqrt{-g}} = -\sqrt{-g}$$  
$$R_{\mu\nu} g^{\mu\nu} \delta(\sqrt{-g}) = -\frac{1}{2} R \sqrt{-g} \, g_{\mu\nu} \delta(g^{\mu\nu}) \quad .$$  
$$\delta(R\sqrt{-g}) = \partial_\mu(\sqrt{-g} \phi^\mu) + R_{\mu\nu} \delta g^{\mu\nu} \sqrt{-g} + \frac{1}{2} R \sqrt{-g} \, g_{\mu\nu} \delta(g^{\mu\nu})$$  
$$= \partial_\mu(\sqrt{-g} \phi^\mu) + \left( R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} \right) \delta(g^{\mu\nu}) \sqrt{-g}$$  
$$\underbrace{\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad}_{\downarrow}$$  
$$G_{\mu\nu}$$  
不变体元：$\sqrt{-g} \, d^4x$，标曲率积分后再变分  
$$\delta \int_M R \sqrt{-g} \, d^4x = \int_M \delta(R\sqrt{-g}) \, d^4x \, ,$$

## Figure & Layout Description
图片为方格纸背景的手写推导笔记，文字以黑色墨水为主，关键步骤用红色墨水标注。内容纵向排列成多行公式，从上至下依次展开度规变分推导过程。第一行起始为中文说明"由于"，后续为连续数学推导。公式中多次出现红色下划线（如$R_{\mu\nu} g^{\mu\nu} \delta(\sqrt{-g})$项）和红色箭头标记（如$\frac{1}{2} R \sqrt{-g} \, g_{\mu\nu} \delta(g^{\mu\nu})$前的等号）。右侧有辅助推导式$\frac{g}{\sqrt{-g}} = -\sqrt{-g}$独立成列。底部用中文标注"不变体元"等物理意义说明，最后以作用量变分等式收尾。整体布局呈现典型的课堂推导笔记特征：逻辑步骤清晰但留有手写修正痕迹，红色标记用于强调关键变换步骤。

<CTX>
{
   "topic": "Einstein张量的显式构造与作用量变分完成",
   "keywords": ["度规变分符号关系", "Einstein张量构造", "里奇标量变分", "作用量变分原理"],
   "summary": "通过度规变分推导出Einstein张量显式表达式$G_{\\mu\\nu}=R_{\\mu\\nu}-\\frac{1}{2}Rg_{\\mu\\nu}$，完成引力作用量变分的核心数学步骤",
   "pending_concepts": ["变分结果如何导出Einstein场方程", "Palatini公式与度规变分的等价性证明", "$\\delta g^{\\mu\\nu}$与$\\delta g_{\\mu\\nu}$符号关系的严格推导"]
}
</CTX>