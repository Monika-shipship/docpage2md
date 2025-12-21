# Slide 63

假设 $j^{\mu}$ 是守恒流， $\nabla_{\mu} j^{\mu} = 0$

则 $j^{\mu} \nabla_{\mu} u^{\nu} = 0$  
$\downarrow$  
$\rho u^{\mu} \nabla_{\mu} u^{\nu} = 0$  
$P \neq 0$，在 $x = x(s)$ 处

右侧注释：  
$d\nu^{\lambda} = 0$， $\nu^{\lambda} = \nu^{\lambda}(x^{\mu})$  
$\frac{d\nu^{\lambda}}{ds} = \frac{\partial \nu^{\lambda}}{\partial x^{\mu}} \frac{dx^{\mu}}{ds} = 0$  
$\downarrow$  
$\partial_{\mu} \nu^{\lambda} u^{\mu} = 0$  
$\downarrow$  
$\nabla_{\mu} \nu^{\lambda} u^{\mu} = 0$ (Riemann)

$u^{\mu} \nabla_{\mu} u^{\nu} = 0$. (自平移条件!)  

$u^{\mu} (\partial_{\mu} u^{\nu} + \Gamma^{\nu}_{\mu\lambda} u^{\lambda}) = 0$  

$u^{\mu} \partial_{\mu} u^{\nu} + \Gamma^{\nu}_{\mu\lambda} u^{\lambda} u^{\mu} = 0$  

$u^{\mu} \partial_{\mu} u^{\nu} = \frac{dx^{\mu}}{ds} \frac{\partial u^{\nu}}{\partial x^{\mu}} = \frac{\partial u^{\nu}}{\partial x^{\mu}} \frac{dx^{\mu}}{ds} = \frac{du^{\nu}}{ds}$  

$\nabla_{\mu} j^{\mu} = 0 \implies \frac{du^{\nu}}{ds} + \Gamma^{\nu}_{\mu\lambda} u^{\lambda} u^{\mu} = 0$

## Figure & Layout Description
图片呈现为手写笔记形式，背景为浅米色方格纸（网格线为浅灰色，间距均匀）。所有文字和公式均为黑色墨水手写，字迹略显潦草但整体可辨。布局分为左右两部分：左侧占据约70%宽度，是主推导流程，按垂直顺序排列；右侧30%宽度为辅助注释区。主推导区从顶部开始依次书写，包含多级推导步骤，每步间用向下的箭头符号"↓"表示逻辑递进。公式中使用了上标（如$\mu, \nu, \lambda$）、下标（如$\nabla_{\mu}$）和希腊字母（如$\Gamma$），部分公式旁有中文注释（如"自平移条件!"）。右侧注释区以较小字号书写，包含微分关系推导（如$d\nu^{\lambda} = 0$），并标注"Riemann"字样。页面底部有最终推导结果，公式中使用了分数形式（如$\frac{du^{\nu}}{ds}$）。整体层级清晰：顶部为假设条件，中部为核心推导链，右侧为补充说明，底部为结论。无彩色元素或图形，仅通过手写笔画粗细区分重点（如"自平移条件!"后有感叹号强调）。

<CTX>
{
   "topic": "测地线方程的推导：从守恒流到自平移条件",
   "keywords": ["测地线方程", "守恒流", "自平移条件", "协变导数", "Christoffel符号"],
   "summary": "本页通过物质密度流的协变守恒条件推导出测地线方程的具体形式，建立了质点运动方程与时空几何的直接联系",
   "pending_concepts": ["测地线方程在弯曲时空中的直观物理解释", "Christoffel符号的几何意义", "自平移条件与平行移动的等价性"]
}
</CTX>