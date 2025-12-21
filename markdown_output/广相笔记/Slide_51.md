# Slide 51

当 $\mu=\nu=0$ 时  
$$\Gamma^i_{00} = \frac{1}{2} g^{ij} \left( \partial_0 g_{j0} + \partial_0 g_{0j} - \partial_j g_{00} \right)$$  
$$= \frac{1}{2} g^{ij} \left( -\partial_j g_{00} \right)$$  
$$= -\frac{1}{2} \partial_i g_{00} = -\frac{1}{2} \partial_i \left( \eta_{00} + h_{00} \right)$$  
$$\boxed{\Gamma^i_{00} = -\frac{1}{2} \partial_i h_{00}}$$  

当 $\mu=\nu \neq 0$ 时，令 $\mu=l, \nu=m,\ l,m=1,2,3$  
$$\Gamma^i_{lm} = \frac{1}{2} g^{ij} \left( \partial_l g_{mj} + \partial_m g_{lj} - \partial_j g_{ml} \right)$$  
$$= \frac{1}{2} \delta^{ij} \left( \partial_l \delta_{mj} + \partial_m \delta_{lj} - \partial_j \delta_{ml} \right)$$  
都为对 1 导 $=0$  
$$\boxed{\Gamma^i_{lm} = 0}$$  

## Figure & Layout Description
图片为方格纸背景的手写推导过程，整体分为上下两个主要区域。上半部分推导 $\mu=\nu=0$ 情况，下半部分推导 $\mu=\nu \neq 0$ 情况。所有公式以黑色墨水书写，关键结果被红色手绘矩形框标注：上半部分的最终结果 $\Gamma^i_{00} = -\frac{1}{2} \partial_i h_{00}$ 被红色框包围，左侧有红色叉号标记；下半部分的 $\Gamma^i_{lm} = 0$ 也被红色框包围。公式推导中包含多层等式变换，部分步骤用括号标注简化条件（如 $g^{ij} \to \delta^{ij}$）。文字与公式混合排版，推导过程从左至右、自上而下逐行展开，关键物理量 $h_{00}$ 和 $\delta_{ij}$ 用下标明确标识。红色框线略显不规则，体现手写特征，但清晰突出核心结论。

<CTX>
{
   "topic": "弱场条件下Christoffel符号分量的具体推导",
   "keywords": ["Christoffel符号", "弱场近似", "度规扰动", "时间分量联络", "空间指标联络"],
   "summary": "完成弱场近似下时间-时间分量和空间-空间分量联络的显式计算，验证空间指标联络在弱场中为零的特性",
   "pending_concepts": ["测地线方程中时间分量的具体推导", "h_{00}与牛顿引力势的定量对应验证", "联络项在运动方程中的物理诠释"]
}
</CTX>