# Slide 50

再计算 $(|V/c| \ll 1, \frac{|h_{\mu\nu}|}{|\eta_{\mu\nu}|} \ll 1)$ 时的联络 $\Gamma^\lambda_{\mu\nu}$

在 Riemann 几何中有
$$\Gamma^\lambda_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma} (\partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu})$$

当 $\lambda = i$, $i,j = 1,2,3$
$$[g_{\mu\nu}] = \begin{bmatrix} -(1+h_{00}) & & \\ & 1 & \\ & & 1 \end{bmatrix}, \quad [g^{\mu\nu}] = \begin{bmatrix} -\frac{1}{1+h_{00}} & & \\ & 1 & \\ & & 1 \end{bmatrix}$$
$g^{i0} = 0$, $g^{00} = -(1+h_{00})$, $g^{0i} = 0$  
$g^{ij} = \delta^{ij}$, $g_{ij} = \delta_{ij}$

$$\Gamma^i_{\mu\nu} = \frac{1}{2} g^{i\sigma} (\partial_\mu g_{\nu\sigma} + \partial_\nu g_{\mu\sigma} - \partial_\sigma g_{\mu\nu})$$
$g^{i0} = 0$, $\sigma=0$ 不用看，令 $\sigma = j$
$$\Gamma^i_{\mu\nu} = \frac{1}{2} g^{ij} (\partial_\mu g_{\nu j} + \partial_\nu g_{\mu j} - \partial_j g_{\mu\nu})$$

## Figure & Layout Description
图片为手写体数学推导内容，书写在浅色方格纸上，背景有浅灰色正方形网格线（约5mm×5mm）。文字使用黑色墨水笔迹，整体呈左上至右下倾斜排列。内容分为6个逻辑区块：  
1. 顶部标题行（占2行高度）：包含弱场条件的数学表达式和"联络"关键词  
2. 第二区块（居中）：Riemann几何中联络的标准公式，使用较大字号书写  
3. 第三区块（左对齐）：指标范围说明"当λ=i, i,j=1,2,3"  
4. 第四区块（矩阵形式）：度规张量[g_{μν}]及其逆[g^{μν}]的对角矩阵表示，用方括号包裹，非对角元素留空表示0  
5. 第五区块（分行排列）：度规分量的具体表达式，包含4行公式（g^{i0}=0等）  
6. 底部区块（2行公式）：空间指标i的联络简化推导过程  
所有公式中的上标/下标均通过手写位置区分（如Γ^λ_μν中λ在上、μν在下），偏导符号∂采用手写体风格。无彩色标记或图形元素，整体为垂直流式布局，公式间留有适当行距。

<CTX>
{
   "topic": "弱场条件下联络张量的分量计算",
   "keywords": ["Christoffel符号", "弱场近似", "度规扰动", "Riemann几何", "空间指标联络"],
   "summary": "推导弱场低速条件下空间指标联络的具体表达式，建立度规扰动与引力势的微分关系",
   "pending_concepts": ["测地线方程中时间分量的具体推导", "h_{00}与牛顿引力势的定量对应验证", "联络项在运动方程中的物理诠释"]
}
</CTX>