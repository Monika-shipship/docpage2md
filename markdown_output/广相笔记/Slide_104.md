# Slide 104

故 $\cos\phi$ 项引出解 $\sim \phi \sin\phi$（因为 $i$ 是 $x^2+1$ 之根）  
$\cos 2\phi$ 项只有 $az\phi$ 项  
常数项 $\to$ 常数项  

所以设 $u_1 = A + B\phi \sin\phi + C \cos 2\phi$  

$$
u_1'' + u_1 = A + 2B \cos\phi - 3C \cos 2\phi
$$
$$
= \frac{1}{p^2} \left(1 + \frac{e^2}{z} + 2e \cos\phi + \frac{e^2}{z} \cos 2\phi \right)
$$

故 $A = \frac{1}{p^2} \left(1 + \frac{e^2}{z} \right)$, $B = \frac{e}{p^2}$, $C = -\frac{e^2}{6p^2}$  

$u = u_0 + \delta u_1$  
$$
= \frac{1}{p} (1 + e \cos\phi) + \delta \left(A + B\phi \sin\phi + C \cos 2\phi \right)
$$

只有这项积累，有长期影响  

$$
u \approx \frac{1}{p} \left(1 + e \cos\phi + \frac{\delta e}{p} \phi \sin\phi \right)
$$

现考察其近日点所处位置的变化；$r$ 最短时，$u$ 最大  
$$
u' \approx \frac{1}{p} \left(-e \sin\phi + \frac{\delta e}{p} (\sin\phi + \phi \cos\phi) \right)
$$
$u' = 0$ 时  

## Figure & Layout Description  
图片为手写数学推导内容，书写于浅米色方格稿纸上（方格线为浅灰色）。文字与公式以黑色墨水书写，字迹工整但带有自然书写痕迹。整体布局为垂直排列的推导步骤：  
1. 顶部两行文字说明三角函数项的解形式，括号内注释用较小字体书写  
2. 中间部分为多行公式推导，包含等号对齐的微分方程展开  
3. 关键系数 $A,B,C$ 以等式形式单独列出，系数表达式中分式结构清晰  
4. 底部包含物理意义说明（"只有这项积累..."）和导数条件讨论  
5. 部分公式下方有波浪线标记（如 $\delta u_1$ 表达式下方），右侧有"近日点"手写标注  
6. 所有数学符号保持手写特征：$\phi$ 带小尾巴，$p$ 有横杠，分式分数线为水平直线  
7. 推导过程中存在少量修正痕迹（如"az项"可能原为其他符号）  

<CTX>
{
   "topic": "史瓦西度规轨道方程一阶摄动解的系数确定与长期效应分析",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "倒代换", "u=1/r", "轨道微分方程", "进动项", "摄动法", "特解系数", "长期积累项"],
   "summary": "本页通过匹配非齐次项系数完成特解参数确定，并指出$\phi \sin\phi$项的长期积累效应是近日点进动的数学根源",
   "pending_concepts": ["az项中z的物理含义", "长期积累项与水星进动角度的定量关系", "齐次解在轨道方程中的具体作用"]
}
</CTX>