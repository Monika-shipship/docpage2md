# Slide 8

$$
\forall d(\gamma(x)+p, \gamma(y)+p) = |\gamma(x) - \gamma(y)| = d(x,y)
$$
设为 $\gamma'(0) = 0$ 得原

只要找到 $\gamma'(x) = xT$

加 $t\ \omega'$ $\gamma'(x) + \omega' = \gamma(x) = xT + \omega'$ $\downarrow_p$

所以绕要设不妨设

$\gamma$ 保持内积 $\Rightarrow T \in O(3)$

why

$\forall x,y \in E^3$

$$
\langle \gamma(x), \gamma(y) \rangle = \langle xT, yT \rangle = xT T^T y^T = \langle x, y \rangle = xy^T \quad \xrightarrow{} \quad x(TT^T - I)y^T = 0
$$
$$
TT^T = I
$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，黑色墨水书写。内容按垂直顺序排列：顶部是距离保持性的等式（含全称量词和绝对值符号）；中间部分包含中文注释"设为γ'(0)=0得原"和线性变换表达式"γ'(x)=xT"；下方有带箭头标注的平移项推导（含"加t ω'"和向下箭头标注"↓p"）；再往下是"所以绕要设不妨设"的结论性文字；底部区域展示内积保持性的详细推导，包含向量空间符号$E^3$、内积尖括号表示、矩阵转置符号$T^T$，以及最终正交条件$TT^T=I$。公式与文字交替出现，关键推导步骤用箭头符号连接，部分等式右侧有手写注释。整体布局为纵向线性结构，无颜色区分，仅通过手写字体大小和间距体现层次。

<CTX>
{
   "topic": "合同变换的正交矩阵表示与内积保持性",
   "keywords": ["合同变换", "正交矩阵", "平移向量", "距离保持", "O(3)", "内积保持", "矩阵转置"],
   "summary": "通过内积保持性严格证明合同变换的线性部分必须属于正交群O(3)，建立几何变换与矩阵群的代数对应关系",
   "pending_concepts": ["平移向量P在合同变换中的几何意义", "合同变换的定向保持/反转性质", "O(3)中行列式为±1的分类依据"]
}
</CTX>