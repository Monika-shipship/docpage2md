# Slide 52

当 $\lambda=0$ 时，$g^{00} = -(1+h_{00}) \neq 0$，$g^{0k} = 0$。

$$ \Gamma^0_{\mu\nu} = \frac{1}{2} g^{0\sigma} \left( \partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu} \right) $$
$$ = \frac{1}{2} g^{00} \left( \partial_\mu g_{\nu 0} + \partial_\nu g_{\mu 0} - \partial_0 g_{\mu\nu} \right) $$

**A 若 $\mu = \nu = 0$**：
$$ \Gamma^0_{00} = \frac{1}{2} g^{00} \partial_0 g_{00} $$
$g_{00}$ 不含 $t$  
$$ \Gamma^0_{00} = 0 $$

**B $\mu = i$, $\nu = 0$**：
$$ \Gamma^0_{i0} = \frac{1}{2} g^{00} \left( \partial_i g_{00} + \partial_0 g_{i0} - \partial_0 g_{i0} \right) $$
$$ = \frac{1}{2} g^{00} \partial_i g_{00} $$
$$ \Gamma^0_{i0} = -\frac{1}{2} (1+h_{00}) \partial_i h_{00} $$

## Figure & Layout Description
图片为方格纸背景的手写推导内容，整体布局为纵向排列的数学推导过程。顶部以"II $\lambda=0$ 时"作为标题，其右侧并列书写两个度规分量条件。正文分为两大部分，用"A 若"和"B"标注。公式采用手写体，关键符号如$\Gamma^0_{\mu\nu}$、$g^{00}$等均以标准张量记号书写，其中下标和上标位置准确。推导过程包含多级等式展开，第二行公式通过等号对齐方式延续第一行表达式。"A 若"部分单独列出$\mu=\nu=0$的特例，包含三行公式推导和一行中文注释"$g_{00}$ 不含 $t$"。"B"部分处理$\mu=i,\nu=0$情况，包含四行公式推导，末行结果中$h_{00}$与$\partial_i$符号清晰可辨。所有文字均为黑色墨水书写，方格纸网格线为浅灰色，构成5mm×5mm的均匀方格背景。公式中的分数均以水平分数线表示，偏导符号$\partial$书写规范。

<CTX>
{
   "topic": "弱场条件下Christoffel符号时间-空间分量的显式推导",
   "keywords": ["Christoffel符号", "弱场近似", "度规扰动", "时间-空间联络", "h_{00}梯度"],
   "summary": "完成弱场近似下时间-空间分量联络Γ^0_{i0}的显式计算，揭示其与度规扰动h_{00}空间梯度的直接关联",
   "pending_concepts": ["测地线方程中时间分量的具体推导", "h_{00}与牛顿引力势的定量对应验证", "联络项在运动方程中的物理诠释"]
}
</CTX>