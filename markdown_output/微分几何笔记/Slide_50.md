# Slide 50

$$Y_\theta \wedge Y_\varphi = \left( r^2 \cos^2\theta \cos\varphi,\ r^2 \cos^2\theta \sin\varphi,\ -r^2 \sin\theta \cos\theta \cos^2\varphi - r^2 \sin\theta \cos\theta \sin^2\varphi - r^2 \sin\theta \cos\theta \right)$$

$$|Y_\theta \wedge Y_\varphi| = r^2 \cos\theta \sqrt{1} = r^2 \cos\theta$$

$$\vec{n} = \left( \cos\theta \cos\varphi,\ \cos\theta \sin\varphi,\ \sin\theta \right)$$

$$Y_\theta = \left( -r \sin\theta \cos\varphi,\ -r \sin\theta \sin\varphi,\ r \cos\theta \right)$$

$$Y_\varphi = \left( -r \cos\theta \sin\varphi,\ r \cos\theta \cos\varphi,\ 0 \right)$$

$$Y_{\theta\theta} = \left( -r \cos\theta \cos\varphi,\ -r \cos\theta \sin\varphi,\ -r \sin\theta \right)$$

$$Y_{\theta\varphi} = \left( r \sin\theta \sin\varphi,\ -r \sin\theta \cos\varphi,\ 0 \right)$$

$$Y_{\varphi\varphi} = \left( -r \cos\theta \cos\varphi,\ -r \cos\theta \sin\varphi,\ 0 \right)$$

$$L = \langle \vec{n}, Y_{\theta\theta} \rangle = -r \cos^2\theta \cos^2\varphi - r \cos^2\theta \sin^2\varphi - r \sin^2\theta = -r$$

$$M = \langle \vec{n}, Y_{\theta\varphi} \rangle = r \sin\theta \cos\theta \sin\varphi \cos\varphi - r \sin\theta \cos\theta \sin\varphi \cos\varphi = 0$$

$$N = \langle \vec{n}, Y_{\varphi\varphi} \rangle = -r \cos^2\theta \cos^2\varphi - r \cos^2\theta \sin^2\varphi = -r \cos^2\theta$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，所有内容以黑色墨水书写。公式从上至下垂直排列，共包含9组核心公式。其中$\vec{n}$向量表达式和$Y_{\theta\theta}$向量表达式下方有红色下划线标注重点。第一组公式展示叉乘结果，第二组计算其模长，第三组定义单位法向量，后续依次列出切向量、二阶偏导向量及第二基本形式系数计算。公式间存在分步推导关系，如模长计算先显示中间步骤再简化结果。手写体清晰但存在连笔现象，例如$\theta$与$\varphi$的区分需结合上下文判断。背景方格线为浅灰色，每行公式占据约2-3个方格高度，整体布局紧凑但层次分明。

<CTX>
{
   "topic": "球面第二基本形式系数的显式计算",
   "keywords": ["第二基本形式系数", "单位法向量", "二阶偏导向量", "曲面曲率计算"],
   "summary": "通过球面参数化显式计算出第二基本形式系数L=-r, M=0, N=-r cos²θ，为后续高斯曲率推导奠定基础",
   "pending_concepts": ["高斯曲率与第二基本形式的关系", "球面测地线的几何特性", "曲面嵌入欧氏空间的曲率性质"]
}
</CTX>