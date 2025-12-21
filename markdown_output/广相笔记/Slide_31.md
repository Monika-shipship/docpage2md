# Slide 31

$$A^{\mu\nu} a_{\mu\lambda} = \frac{1}{n} a \delta_{\lambda}^{\nu}$$

则 $A^{\mu\nu} a_{\mu\nu} = \frac{1}{n} a \delta_{\nu}^{\nu} = \frac{1}{n} a \cdot n$

$A^{\mu\nu} a_{\mu\nu} = a$  
$A^{\mu\nu} a_{\mu\lambda} a^{\lambda\delta} = \frac{1}{n} a \delta_{\lambda}^{\nu} a^{\lambda\delta}$

$A^{\mu\nu} \delta_{\mu}^{\delta} = \frac{1}{n} a a^{\nu\delta}$

$A^{\delta\nu} = \frac{1}{n} a a^{\delta\nu}$

$a^{\nu\delta} = \frac{n A^{\delta\nu}}{a}$

$(a^{-1})_{\nu\delta} = \frac{(a_{\nu\delta})_{\text{adj}}}{a}$

$(a_{\nu\delta})_{\text{adj}} = n \cdot A^{\delta\nu}$

若 $a_{\mu\nu} = a_{\nu\mu}$

由 $A^{\mu\nu} a_{\mu\lambda} = \frac{1}{n} \delta_{\lambda}^{\nu} a$

$A^{\mu\nu} a_{\lambda\mu} = \frac{1}{n} \delta_{\lambda}^{\nu} a$

$A^{\mu\nu} a_{\lambda\mu} a^{\delta\lambda} = \frac{1}{n} \delta_{\lambda}^{\nu} a a^{\delta\lambda}$

$A^{\mu\nu} \delta_{\mu}^{\delta} = \frac{1}{n} a a^{\delta\nu}$

$A^{\delta\nu} = \frac{1}{n} a a^{\delta\nu}$

$$A^{\mu\nu} = \frac{1}{n} a a^{\mu\nu}$$

于是 $A^{\mu\nu} a_{\nu\mu} = \frac{1}{n} a a^{\mu\nu} a_{\nu\mu} = a \cdot \frac{1}{n} \cdot n$

$$A^{\mu\nu} a_{\nu\mu} = a$$

$$\text{adj } a = n A^T$$

## Figure & Layout Description

图片为方格纸背景的手写数学推导页，整体布局呈纵向多列结构。顶部区域包含三行核心公式：第一行是 $A^{\mu\nu} a_{\mu\lambda} = \frac{1}{n} a \delta_{\lambda}^{\nu}$；第二行以"则"字开头推导 $A^{\mu\nu} a_{\mu\nu}$ 的表达式；第三行左右分栏，左侧为 $A^{\mu\nu} a_{\mu\nu} = a$，右侧为 $A^{\mu\nu} a_{\mu\lambda} a^{\lambda\delta}$ 的展开式。中部偏左有蓝色矩形框标注"若 $a_{\mu\nu} = a_{\nu\mu}$"，框线为蓝色实线，覆盖两行手写内容。右侧区域有垂直排列的推导链，包含 $A^{\mu\nu} \delta_{\mu}^{\delta}$ 和 $a^{\nu\delta}$ 等公式。底部区域有三个红色矩形框：左侧框住 $A^{\mu\nu} = \frac{1}{n} a a^{\mu\nu}$，中间框住 $A^{\mu\nu} a_{\nu\mu} = a$，右侧框住 $\text{adj } a = n A^T$，所有框线为红色实线且略有手写抖动。公式中的下标/上标清晰可辨，如 $\delta_{\lambda}^{\nu}$ 的上下标位置准确，"adj" 以手写体标注。部分推导步骤用波浪线标记关键变量（如 $a_{\mu\lambda}$ 下方的红色波浪线）。整体视觉层次分明，推导逻辑从上至下流动，重点结论通过彩色框突出显示。

<CTX>
{
   "topic": "伴随矩阵的显式表达式与对称矩阵性质",
   "keywords": ["伴随矩阵", "余因子", "矩阵对称性", "行列式", "逆矩阵关系"],
   "summary": "本页推导出伴随矩阵的显式公式 $A^{\mu\nu} = \frac{1}{n} a a^{\mu\nu}$ 并证明当原矩阵对称时 $\text{adj } a = n A^T$ 的关键性质",
   "pending_concepts": ["余因子矩阵在非对称情形下的修正形式", "伴随矩阵与逆矩阵的完整表达式 $a^{-1} = \frac{1}{\det a} \text{adj } a$ 的验证步骤", "高维行列式导数与协变微分的关联"]
}
</CTX>