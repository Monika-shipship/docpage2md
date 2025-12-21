# Slide 103

设 $u = u_0 + \lambda u_1$，则  
$$\frac{d^2}{d\phi^2}(u_0 + \lambda u_1) + u_0 + \lambda u_1 = \lambda (u_0 + \lambda u_1)^2 + \frac{GM}{h^2}$$  
因 $\lambda$ 为小量  
$$\lambda \frac{d^2 u_1}{d\phi^2} + \lambda u_1 = \lambda u_0^2$$  
$$\Rightarrow \frac{d^2 u_1}{d\phi^2} + u_1 = u_0^2 = \frac{1}{p^2}(1 + 2e \cos\phi + e^2 \cos^2\phi)$$  
利用 $\cos 2\phi = 2\cos^2\phi - 1 \Rightarrow \cos^2\phi = \frac{1}{2}(1 + \cos 2\phi)$ 有  
$$\frac{d^2 u_1}{d\phi^2} + u_1 = \frac{1}{p^2}\left(1 + 2e \cos\phi + \frac{e^2}{2}(1 + \cos 2\phi)\right)$$  
$$= \frac{1}{p^2}\left(1 + \frac{e^2}{2} + 2e \cos\phi + \frac{e^2}{2} \cos 2\phi\right).$$  
通解已由 $u_0$ 解出，猜特解  
$$u_1 = A + B \cos\phi + C \cos 2\phi$$  
$$x'' + x = E \cos t \quad \lambda^2 + 1 = 0$$  
$$(D^2 + 1)x = E \cos t \quad \lambda = \pm i$$  
$$x = \frac{1}{D^2 + 1} E \cos t \quad \Rightarrow t e^{i\omega t} \quad \text{Re} \Rightarrow t$$  
$$(t \cos t)'' = (\cos t - t \sin t)' = -\sin t - \sin t - t \cos t$$  
$$(t \sin t)'' = (\sin t + t \cos t)' = \cos t + \cos t - t \sin t$$

## Figure & Layout Description
手写数学推导内容书写于浅米色方格纸背景上，网格线为浅灰色细线。文字与公式均以黑色墨水书写，字迹工整但带有手写体特征。内容纵向排列，从上至下依次为：变量设定语句、主微分方程推导、小量近似处理、三角恒等式代换、特解猜测形式，以及底部的辅助微分方程解法示例。公式部分包含多层嵌套的分式、二阶导数符号（$\frac{d^2}{d\phi^2}$）和三角函数表达式。推导过程中的关键步骤通过箭头（$\Rightarrow$）和"利用"等中文提示词衔接。页面无彩色标记或图形元素，纯文字与公式构成，整体布局符合学术推导笔记的典型特征。

<CTX>
{
   "topic": "史瓦西度规下轨道方程的一阶摄动解法",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "倒代换", "u=1/r", "轨道微分方程", "进动项", "摄动法", "特解猜测"],
   "summary": "本页通过摄动法推导一阶修正方程，利用三角恒等式简化非齐次项并构造特解形式，为计算水星近日点进动提供数学基础",
   "pending_concepts": ["特解系数A/B/C的确定方法", "摄动项对轨道进动的具体贡献", "齐次解与特解的物理意义区分", "GM/h²项的物理来源"]
}
</CTX>