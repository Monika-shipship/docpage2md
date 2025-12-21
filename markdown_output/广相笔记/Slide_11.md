# Slide 11

$$g^{\sigma\delta}g_{\sigma\lambda}\Gamma^{\delta}_{\mu\nu} = g^{\sigma\delta}\Gamma_{\lambda,\mu\nu}$$

$$\Gamma^{\delta}_{\mu\nu} = \frac{1}{2}g^{\sigma\delta}\left(\partial_{\mu}g_{\sigma\nu} + \partial_{\nu}g_{\sigma\mu} - \partial_{\sigma}g_{\mu\nu}\right)$$

下证 $\Gamma^{\lambda}_{\mu\lambda} = \frac{\partial(\ln\sqrt{g})}{\partial x^{\mu}}$

因 $\Gamma^{\lambda}_{\mu\nu} = \frac{1}{2}g^{\sigma\lambda}\left(\partial_{\mu}g_{\sigma\nu} + \partial_{\nu}g_{\sigma\mu} - \partial_{\sigma}g_{\mu\nu}\right)$

则令 $\nu = \lambda$

$$\Gamma^{\lambda}_{\mu\lambda} = \frac{1}{2}g^{\sigma\lambda}\left(\partial_{\mu}g_{\sigma\lambda} + \partial_{\lambda}g_{\sigma\mu} - \partial_{\sigma}g_{\mu\lambda}\right)$$

再证 $g^{\lambda\sigma}\partial_{\lambda}g_{\sigma\mu} = g^{\sigma\lambda}\partial_{\sigma}g_{\lambda\mu} = g^{\sigma\lambda}\partial_{\sigma}g_{\mu\lambda}$

故红框处被抵消

$$\Gamma^{\lambda}_{\mu\lambda} = \frac{1}{2}g^{\sigma\lambda}\partial_{\mu}g_{\sigma\lambda}$$

$A^{-1} = \frac{adj(A)}{det A}$  $adj A$: $A$的伴随矩阵

$(g_{\lambda\sigma})^{-1} = g^{\lambda\sigma} = \frac{G^{\lambda\sigma}}{g}$  $g = det\,g^{\lambda\sigma}$

$G^{\lambda\sigma} = \frac{1}{n}g \cdot g^{\lambda\sigma}$

$G^{\lambda\sigma}g_{\sigma\delta} = \frac{1}{n}g \cdot g^{\lambda\sigma}g_{\sigma\delta} = \frac{1}{n}g\,\delta^{\lambda}_{\delta}$  $\delta \to \lambda$

## Figure & Layout Description

The image shows a handwritten mathematical derivation on grid paper with a light beige background. The main content consists of black ink equations and annotations, with key elements highlighted in red and blue. 

1. **Layout Structure**:
   - Top section contains two fundamental equations for Christoffel symbols with a prominent red wavy underline beneath the second equation.
   - Middle section begins with "下证" (proving below) followed by a derivation of $\Gamma^{\lambda}_{\mu\lambda}$, containing a red rectangular box around the final simplified form.
   - Right side has blue annotations: "λσ交换" (λσ exchange) and "g可对称" (g is symmetric).
   - Bottom section includes matrix inverse formulas with detailed determinant relationships.

2. **Color Coding**:
   - Red is used for: 
     * Wavy underline under the Christoffel symbol definition
     * Rectangular box around the final simplified expression
     * Underline beneath the phrase "故红框处被抵消"
   - Blue is used for technical annotations about index symmetry
   - Black is the primary color for all equations and text

3. **Visual Hierarchy**:
   - Key equations are centered and spaced for readability
   - Derivation steps flow vertically with logical progression
   - Critical simplification steps are emphasized with red boxing
   - Auxiliary explanations (matrix inverse properties) appear at the bottom

4. **Handwriting Characteristics**:
   - Mathematical symbols are clearly written with proper tensor notation
   - Subscripts/superscripts are consistently positioned
   - Some Chinese annotations appear between equations for explanation

<CTX>
{
   "topic": "克氏联络的显式表达式推导与度规相容性验证",
   "keywords": ["克氏联络", "度规相容条件", "指标轮换", "克氏降指标", "黎曼联络唯一性", "协变导数展开", "指标升降"],
   "summary": "本页通过度规相容条件和指标轮换技巧，严格推导出克氏联络的显式表达式，并验证了其与度规的相容性，确立了黎曼几何中联络系数的唯一确定形式",
   "pending_concepts": ["曲率张量的显式计算", "测地线方程的推导", "联络系数的物理意义", "克氏联络在弯曲时空中的应用"]
}
</CTX>