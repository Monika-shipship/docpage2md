# Slide 102

$e^{\nu} = 1 - \frac{2GM}{c^2r} \Rightarrow (e^{\nu})' = e^{\nu}\nu' = \frac{2GM}{c^2r^2}$

$\nu' = \frac{2GM}{c^2r^2}e^{-\nu} \quad re^{\nu} = r(1 - \frac{2GM}{c^2r}) = r - \frac{2GM}{c^2}$

$$\frac{d^2r}{ds^2} + re^{\nu}\left(\frac{1}{2}\nu'r - 1\right)\left(\frac{d\phi}{ds}\right)^2 + \frac{1}{2}\nu'e^{\nu} = 0$$

代入得

$$-\frac{h^2}{c^2}u^2\frac{d^2u}{d\phi^2} + \left(\frac{1}{2}\frac{2GM}{c^2}\frac{1}{u} + \frac{2GM}{c^2}\right)\frac{h^2}{c^2}u^4 + \frac{GM}{c^2}u^2 = 0$$

$$-\frac{h^2}{c^2}u^2\frac{d^2u}{d\phi^2} + \frac{3GM}{c^2}\frac{h^2}{c^2}u^4 + \frac{h^2}{c^2}u^3 + \frac{GM}{c^2}u^2 = 0$$

$$\frac{d^2u}{d\phi^2} + u - \frac{3GM}{c^2}u^2 = \frac{GM}{h^2}$$

$$\frac{d^2u}{d\phi^2} + u = \frac{3GM}{c^2}u^2 + \frac{GM}{h^2}$$

设

$u_0$ 符合 $\frac{d^2u_0}{d\phi^2} + u_0 = \frac{GM}{h^2}$

$u_0 = \frac{1}{p}(1 + e\cos\phi) \quad p = \frac{b^2}{a}$

令 $\alpha = \frac{3GM}{c^2}$，得

## Figure & Layout Description

该图片为一张手写数学推导的PPT截图，背景为浅黄色方格纸样式，方格线为浅灰色。内容全部为黑色手写体数学公式和文字，布局为纵向排列。

1. 顶部区域：第一行公式 $e^{\nu} = 1 - \frac{2GM}{c^2r} \Rightarrow (e^{\nu})' = e^{\nu}\nu' = \frac{2GM}{c^2r^2}$，字体清晰，等号和箭头符号明显。
2. 第二行：$\nu' = \frac{2GM}{c^2r^2}e^{-\nu}$ 与 $re^{\nu} = r(1 - \frac{2GM}{c^2r}) = r - \frac{2GM}{c^2}$ 并列书写，中间用空格分隔。
3. 第三行：一个复杂的测地线方程，其中 $\frac{1}{2}\nu'r - 1$ 部分被红色笔迹标记了一个"1"，可能是修正或强调。
4. 第四行：简短的中文"代入得"，位于方程下方，字体稍小。
5. 第五行至第七行：推导过程的中间步骤，公式逐渐简化，第五行公式中 $\frac{1}{2}\frac{2GM}{c^2}\frac{1}{u}$ 部分有明显的分数结构。
6. 第八行：简化后的轨道微分方程 $\frac{d^2u}{d\phi^2} + u = \frac{3GM}{c^2}u^2 + \frac{GM}{h^2}$。
7. 第九行：中文"设"，字体较小。
8. 第十行至第十二行：关于$u_0$的定义和解的形式，其中$u_0 = \frac{1}{p}(1 + e\cos\phi)$与$p = \frac{b^2}{a}$并列书写。

整体布局紧凑，公式从上至下依次排列，无明显分隔线。红色标记仅在第三行出现一次，用于强调特定项。所有公式均使用标准数学符号，分数表示清晰，指数和下标书写规范。

<CTX>
{
   "topic": "史瓦西度规下行星轨道方程的倒代换求解",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "倒代换", "u=1/r", "轨道微分方程", "进动项"],
   "summary": "本页通过倒代换u=1/r将测地线方程转化为轨道微分方程，推导出含广义相对论修正项的轨道方程，并给出开普勒轨道的特解形式，为计算水星近日点进动奠定基础",
   "pending_concepts": ["ν(r)和λ(r)的物理意义", "轨道进动量的最终表达式", "面积速度定理的物理意义", "h的物理定义（轨道角动量）", "红色标记项的修正原因"]
}
</CTX>