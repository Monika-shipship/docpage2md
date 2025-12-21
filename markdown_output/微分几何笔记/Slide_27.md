# Slide 27

4.1 曲线的弧长参数，曲率，挠率在刚体运动下不变

证 设 $s$ 是 $\gamma$ 的弧长参数，$T$ 是刚体运动，则  
$$
\tilde{\gamma}(s) = T \gamma(s) + p_0, \quad \det(T) = 1, \ T \in O(3)
$$
$$
\tilde{\gamma}(s) = T \circ \gamma(s)
$$
$$
|\tilde{\gamma}'(s)| = \left| \frac{d}{ds} (\gamma(s) T + p_0) \right| = |\gamma'(s) T| 
$$
$$
= \sqrt{\langle \gamma'(s) T, \gamma'(s) T \rangle} = \sqrt{\gamma'(s) T T^T \gamma'(s)} = \sqrt{\gamma'(s) \gamma'(s)} = |\gamma'(s)|
$$
故 $|\tilde{\gamma}'(s)|$ 不变  
$$
\kappa(s) = |\dot{t}|
$$
$$
\tilde{\gamma} = T(\gamma) = T\gamma + p_0
$$
$$
\tilde{t} = \tilde{\gamma}'(s) = \gamma' T = t T
$$
$$
\dot{\tilde{t}} = \ddot{\gamma}'(s) = \ddot{\gamma} T
$$
$$
\tilde{\kappa} = |\dot{\tilde{t}}| = |\ddot{\gamma} T| = \sqrt{\langle \ddot{\gamma} T, \ddot{\gamma} T \rangle} = \sqrt{\ddot{\gamma} T T^T \ddot{\gamma}} = \sqrt{\ddot{\gamma} \ddot{\gamma}} = |\ddot{\gamma}| = |\dot{t}|
$$
$$
\tilde{\kappa} = \kappa
$$
曲率不变  
$$
\dot{t} = -\kappa n
$$
$$
t' = \tau n \times t
$$
$$
\tilde{n} = \frac{\dot{\tilde{t}}}{|\dot{\tilde{t}}|} = \frac{\ddot{\gamma} T}{|\ddot{\gamma} T|} = \frac{\ddot{\gamma} T}{\kappa} = \frac{\dot{t}}{\kappa} T = \frac{\dot{t}}{|\dot{t}|} T = n T
$$
$$
\Rightarrow \tilde{n} = n T
$$
$$
\tilde{b} = \tilde{t} \wedge \tilde{n} = t T \wedge n T = T(t) \wedge T(n) \stackrel{\text{问题5}}{=} \det(T) T(t \wedge n) = T(b) = b T
$$
$$
\text{令 } \gamma'(s) = x T, \text{ 保原点}
$$
$$
\Rightarrow \tilde{b} = b T
$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记，采用黑色墨水书写。整体布局为纵向排列的数学证明过程，包含标题、证明步骤、公式推导三部分。标题"4.1 曲线的弧长参数，曲率，挠率在刚体运动下不变"位于左上角，使用加粗手写体。证明部分从"证"字开始，分层展示刚体运动变换公式、弧长参数不变性推导、曲率与挠率的不变性证明。公式部分包含多级推导，使用竖线表示向量模长、尖括号表示内积、波浪线表示变换后变量。关键结论如"故$|\tilde{\gamma}'(s)|$不变"和"曲率不变"以加粗手写体突出显示。推导中穿插"问题5"等注释说明，最后以向量叉积关系收尾。方格纸的浅灰色网格线作为背景，文字与公式严格对齐网格，形成清晰的行列结构。

<CTX>
{
   "topic": "曲线几何量在刚体运动下的不变性证明",
   "keywords": ["刚体运动", "弧长参数", "曲率不变性", "挠率不变性", "正交变换"],
   "summary": "证明曲线的弧长参数、曲率和挠率在刚体运动下保持不变，建立几何不变量与运动变换的内在联系",
   "pending_concepts": ["挠率的几何意义", "非弧长参数下的Frenet公式修正"]
}
</CTX>