# Slide 52

性质 2：设曲面 $S: \mathbf{r} = \mathbf{r}(u,v), (u,v) \in D$，  
↑: 合同变换  
↑ 把 $S$ 变为 $\tilde{S}: \tilde{\mathbf{r}}(u,v) = \tilde{T} \circ \mathbf{r}(u,v) = \mathbf{r}(u,v)T + P_0$  
记 $II$ 和 $\tilde{II}$ 分别是 $S$ 和 $\tilde{S}$ 的第二基本形式  
若 $\tilde{T}$ 是刚体运动，$II = \tilde{II}$  
若 $\tilde{T}$ 是反向刚体运动，$II = -\tilde{II}$  
$\tilde{II} = -\langle d\tilde{\mathbf{r}}, d\tilde{\mathbf{n}} \rangle$  
证：$\tilde{\mathbf{r}}_u = \mathbf{r}_u T$, $\tilde{\mathbf{r}}_v = \mathbf{r}_v T$, $\tilde{T}_0(x) = xT$  
$\tilde{\mathbf{r}}_u \wedge \tilde{\mathbf{r}}_v = \mathbf{r}_u T \wedge \mathbf{r}_v T = \tilde{T}_0(\mathbf{r}_u) \wedge \tilde{T}_0(\mathbf{r}_v)$  
$= \det(T) \tilde{T}_0(\mathbf{r}_u \wedge \mathbf{r}_v)$  
$= \det(T) (\mathbf{r}_u \wedge \mathbf{r}_v) T$  
$|\tilde{\mathbf{r}}_u \wedge \tilde{\mathbf{r}}_v| = |\det(T) (\mathbf{r}_u \wedge \mathbf{r}_v) T|$  
$= |(\mathbf{r}_u \wedge \mathbf{r}_v) T| = \sqrt{\langle (\mathbf{r}_u \wedge \mathbf{r}_v)T, (\mathbf{r}_u \wedge \mathbf{r}_v)T \rangle}$  
$= (\mathbf{r}_u \wedge \mathbf{r}_v) T T^\top (\mathbf{r}_u \wedge \mathbf{r}_v)^\top$  
$= (\mathbf{r}_u \wedge \mathbf{r}_v) (\mathbf{r}_u \wedge \mathbf{r}_v)^\top = |\mathbf{r}_u \wedge \mathbf{r}_v|$

## Figure & Layout Description
手写笔记内容书写在浅米色方格纸背景上，网格线为浅灰色细线。文字以黑色墨水书写，整体呈竖直排列结构。顶部以较大字号书写"性质2："作为标题，其后接曲面定义公式。中间部分用"↑"符号引导的两行说明合同变换操作，字体略小于标题但大于正文。核心结论部分使用标准字号，分两行说明刚体运动与反向刚体运动对第二基本形式的影响。证明部分从"证："开始，采用多行对齐格式，每行公式通过等号对齐，其中向量符号$\mathbf{r}$和变换符号$T$保持统一书写风格。所有公式中的外积符号"$\wedge$"清晰可辨，行列式符号"$\det$"书写完整。证明过程末尾的范数计算步骤占据页面下半部分，通过多行推导展示模长不变性。整体布局呈现典型的课堂笔记特征：重点内容通过字号差异突出，推导过程按逻辑顺序垂直排列，无额外图形元素。

<CTX>
{
   "topic": "第二基本形式在合同变换下的符号变化规律",
   "keywords": ["合同变换", "刚体运动", "反向刚体运动", "雅可比行列式", "外积模长"],
   "summary": "阐明第二基本形式在刚体运动下保持不变、在反向刚体运动下符号取反的特性，并通过外积推导验证模长不变性",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>