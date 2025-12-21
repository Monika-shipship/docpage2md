# Slide 112

代入 $\left( \frac{d\phi}{d\lambda} \right)^2$ 得：
$$
\frac{d^2 r}{d\lambda^2} + r e^{\nu} \left( \frac{1}{2} \nu' r - 1 \right) \left( \frac{d\phi}{d\lambda} \right)^2 + \frac{1}{2} \nu' e^{\nu} = 0
$$

所有过程与之前类似  
与比比相似，用倒代换 $u = \frac{1}{r}$  
$$
r^2 \frac{d\phi}{d\lambda} = \frac{h}{c}, \quad \frac{d\phi}{d\lambda} = u^2 \frac{h}{c}, \quad \left( \frac{d\phi}{d\lambda} \right)^2 = \frac{h^2}{c^2} u^4
$$
$$
\frac{dr}{d\lambda} = -\frac{1}{u^2} \frac{du}{d\lambda} = -\frac{1}{u^2} \frac{du}{d\phi} \frac{d\phi}{d\lambda} = -\frac{h}{c} \frac{du}{d\phi}
$$
$$
\frac{d^2 r}{d\lambda^2} = -\frac{h}{c} \frac{d^2 u}{d\phi^2} \frac{d\phi}{d\lambda} = -\frac{h^2}{c^2} u^2 \frac{d^2 u}{d\phi^2}
$$
$$
e^{\nu} = 1 - \frac{2GM}{c^2 r} \Rightarrow (e^{\nu})' = e^{\nu} \nu' = \frac{2GM}{c^2 r^2}
$$
$$
\nu' = \frac{2GM}{c^2 r^2} e^{-\nu}, \quad r e^{\nu} = r \left( 1 - \frac{2GM}{c^2 r} \right) = \frac{1}{u} - \frac{2GM}{c^2}
$$
$$
\frac{d^2 r}{d\lambda^2} + r e^{\nu} \left( \frac{1}{2} \nu' r - 1 \right) \left( \frac{d\phi}{d\lambda} \right)^2 + 0 = 0
$$
代入得
$$
-\frac{h^2}{c^2} u^2 \frac{d^2 u}{d\phi^2} + \left( \frac{1}{2} \cdot \frac{2GM}{c^2} \cdot \frac{1}{u} + \frac{2GM}{c^2} \right) \frac{h^2}{c^2} u^4 + \frac{GM}{c^2 r^2} = 0
$$

## Figure & Layout Description
手写数学推导内容占据整个方格纸背景页面。文字为黑色墨水书写，部分关键项用红色标记：
1. 第一个微分方程中，$+\frac{1}{2}\nu'e^\nu$ 项被红色方框圈出并划掉，下方标注红色"0"
2. 页面中部有红色圆圈标记在"0"处
3. 最后一个方程中，$+\frac{GM}{c^2 r^2}$ 项被红色斜线划掉
4. 公式与文字混合排布，推导过程呈纵向递进结构
5. 所有数学符号使用手写体，包含上下标和分式结构
6. 纸张为浅黄色方格坐标纸，网格线为浅灰色

<CTX>
{
   "topic": "史瓦西度规中光线传播方程的变量替换推导",
   "keywords": ["倒代换", "角动量守恒", "微分方程化简", "史瓦西度规参数", "光线轨迹方程"],
   "summary": "本页通过倒代换u=1/r将径向坐标微分方程转换为角度参数方程，完成光线传播方程的关键化简步骤",
   "pending_concepts": ["弱场近似下光线偏折角的显式计算", "史瓦西半径处的坐标奇异性处理", "角动量守恒常数K的物理意义"]
}
</CTX>