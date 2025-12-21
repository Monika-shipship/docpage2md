# Slide 53

$$\tilde{n} = \frac{\tilde{Y}_u \wedge \tilde{Y}_v}{|\tilde{Y}_u \wedge \tilde{Y}_v|} = \det(T) \frac{(Y_u \wedge Y_v)T}{|Y_u \wedge Y_v|} = \det T \cdot n^T$$

$$d\tilde{n} = \det T \cdot dn^T$$

$$d\tilde{r} = dr^T$$

$$\tilde{II} = -\langle d\tilde{r}, d\tilde{n} \rangle$$
$$= -\langle dr^T, \det T \cdot dn^T \rangle$$
$$= -\det T \langle dr^T, dn^T \rangle$$
$$= -\det T \ dr^T T^T dn^T$$
$$= -\det T \ dr \ dn^T$$
$$= -\det T \ \langle dr, dn \rangle$$
$$= \det T \ II$$

故 $\det T = 1 \cdots$

$\det T = -1 \cdots$

## Figure & Layout Description
图片展示了一张浅黄色方格纸背景的手写数学推导，方格线为浅灰色，形成规则的网格布局。所有内容以黑色手写体呈现，字迹工整清晰。推导内容从上到下垂直排列，共包含12行数学表达式，分为四个逻辑区块：第一行是单位法向量的变换公式，第二、三行分别描述法向量微分和位置向量微分的变换关系，第四至第十行是第二基本形式的详细推导过程（包含7个等式步骤），最后两行是结论性陈述。公式中的向量符号（如$\tilde{n}$）带有波浪线标记，矩阵转置使用上标T表示，内积使用尖括号$\langle \cdot, \cdot \rangle$表示。整个推导过程左对齐，每行等号对齐形成清晰的逻辑链条，无额外图形或彩色标注。

<CTX>
{
   "topic": "第二基本形式在合同变换下的符号变化规律的数学推导",
   "keywords": ["合同变换", "刚体运动", "反向刚体运动", "雅可比行列式", "外积模长", "第二基本形式"],
   "summary": "通过向量外积和内积的严格推导，证明了第二基本形式在合同变换下满足$\\tilde{II} = \\det T \\cdot II$的变换规律，从而在刚体运动下保持不变，在反向刚体运动下符号取反",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>