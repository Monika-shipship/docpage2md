# Slide 107

### 3.2.7 行星运动中的能量守恒  
前文已由测地线方程得到，  

$$
\begin{cases}
\frac{d^2 t}{ds^2} + V' \frac{dr}{ds} \frac{dt}{ds} = 0, \\
\frac{d^2 r}{ds^2} + \frac{1}{2} V' e^{2V} \left( \frac{dct}{ds} \right)^2 - \frac{1}{2} V' \left( \frac{dr}{ds} \right)^2 - r e^V \left( \frac{d\phi}{ds} \right)^2 = 0, \\
\frac{d^2 \phi}{ds^2} + 2 \frac{1}{r} \frac{dr}{ds} \frac{d\phi}{ds} = 0.
\end{cases}
$$

$$
\frac{d^2 t}{ds^2} + V' \frac{dr}{ds} \frac{dt}{ds} = 0 \implies \frac{d^2 t}{ds^2} + \frac{dV}{dr} \frac{dr}{ds} \frac{dt}{ds} = 0
$$

即  
$$
\frac{d^2 t}{ds^2} + \frac{dV}{ds} \frac{dt}{ds} = 0.
$$

$$
\frac{d}{ds} \left( \frac{dt}{ds} \right) + \frac{dV}{ds} \frac{dt}{ds} = 0.
$$

$$
\frac{dV}{ds} = -\frac{\frac{d}{ds} \left( \frac{dt}{ds} \right)}{\frac{dt}{ds}} = -\frac{d}{ds} \left( \ln \left( \frac{dt}{ds} \right) \right)
$$

$$
dV = -d \left( \ln \left( \frac{dt}{ds} \right) \right)
$$

$$
V = -\ln \left( \frac{dt}{ds} \right) + \ln C
$$

$$
e^V = \frac{ds}{dt} \cdot C
$$

即  
$$
\frac{1}{K} = e^{-V} \frac{ds}{dt}.
$$

## Figure & Layout Description  
图片为方格纸背景的手写推导页，整体布局呈纵向线性结构。顶部以黑色手写体标注章节标题“3.2.7 行星运动中的能量守恒”，字体略大于正文。下方接续说明性文字“前文已由测地线方程得到，”，后接一个三行联立方程组，方程组左侧以大括号统一括起，每行公式独立排列。方程组下方为连续推导步骤，每步公式单独成行并附有逻辑连接词（如“即”“$\implies$”）。所有公式均使用黑色墨水书写，字迹工整但存在手写特征（如“$V'$”的撇号倾斜、分数线略带弧度）。背景为浅米色方格纸，网格线为浅灰色细线，每格约1cm×1cm。公式中部分符号存在上下标（如“$e^{2V}$”“$\frac{d^2 t}{ds^2}$”），积分与微分符号清晰可辨。推导末尾出现“即”字引导结论，整体逻辑流从方程组到积分求解逐步展开。

<CTX>
{
   "topic": "行星运动中的能量守恒与测地线方程推导",
   "keywords": ["测地线方程", "能量守恒", "相对论动力学", "积分常数", "坐标变换"],
   "summary": "本页通过测地线方程推导出行星运动的能量守恒微分方程，并完成积分求解得到关键关系式 $e^V = C \\cdot \\frac{ds}{dt}$",
   "pending_concepts": ["积分常数C的物理意义", "与近日点进动的直接关联", "坐标参数s与时间t的物理对应关系"]
}
</CTX>