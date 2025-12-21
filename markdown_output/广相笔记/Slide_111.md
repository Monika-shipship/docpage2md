# Slide 111

### 3.3.2 史瓦西解下的光线传播

将此前已解出的  
在 $\theta = \frac{\pi}{2}$， $ds^2 = -e^{\nu} c^2 dt^2 + e^{\nu} dr^2 + r^2 d\phi^2$.

$$
\begin{cases}
\frac{d^2 t}{ds^2} + \nu' \frac{dr}{ds} \frac{dt}{ds} = 0, \\
\frac{d^2 r}{ds^2} + \frac{1}{2} \nu' e^{2\nu} \left(\frac{d(ct)}{ds}\right)^2 - \frac{1}{2} \nu' \left(\frac{dr}{ds}\right)^2 - r e^{\nu} \left(\frac{d\phi}{ds}\right)^2 = 0, \\
\frac{d^2 \phi}{ds^2} + 2 \frac{1}{r} \frac{dr}{ds} \frac{d\phi}{ds} = 0, \\
e^{\nu} = 1 - \frac{2GM}{c^2 r}
\end{cases}
$$

代换 $s \to \lambda$，并令 $ds^2 = 0$ 可得.  
① 类角动量守恒  
$$
\frac{d^2 \phi}{d\lambda^2} + 2 \frac{1}{r} \frac{dr}{d\lambda} \frac{d\phi}{d\lambda} = 0 \implies \frac{d}{d\lambda} \left(r^2 \frac{d\phi}{d\lambda}\right) = 0 \implies r^2 \frac{d\phi}{d\lambda} = K
$$  
② $\frac{d^2 r}{d\lambda^2} + \frac{1}{2} \nu' e^{2\nu} \left(\frac{d(ct)}{d\lambda}\right)^2 - \frac{1}{2} \nu' \left(\frac{dr}{d\lambda}\right)^2 - r e^{\nu} \left(\frac{d\phi}{d\lambda}\right)^2 = 0$.  
利用 $\color{red}{0 = -e^{\nu} c^2 dt^2 + e^{\nu} dr^2 + r^2 d\phi^2}$ (比之前少一项)  
$$
\implies \left(\frac{dr}{d\lambda}\right)^2 = 0 + e^{2\nu} c^2 \left(\frac{dt}{d\lambda}\right)^2 - e^{\nu} r^2 \left(\frac{d\phi}{d\lambda}\right)^2.
$$

## Figure & Layout Description

图片为方格纸背景的手写物理推导笔记，整体布局为纵向排列的数学推导流程。顶部标题"3.3.2 史瓦西解下的光线传播"以黑色手写体书写，字迹略带倾斜。主体内容分为四个逻辑区块：  
1. 度规表达式区块：位于上部，包含$\theta = \pi/2$条件下的$ds^2$公式，使用标准手写数学符号，"e^ν"的指数符号清晰可见  
2. 测地线方程组区块：用大括号包裹的四行微分方程组，垂直排列，方程间用逗号分隔，最后一行是$e^ν$的显式表达式  
3. 参数替换推导区块：包含"代换 s→λ"说明及两个编号推导项（①和②），其中①项包含三步等价推导，用箭头连接  
4. 红色标注区块：关键等式"0 = ..."用红色笔迹书写，右侧有红色手写注释"比之前少一项"，与黑色正文形成鲜明对比  

所有公式均采用标准手写物理符号规范，微分符号"d"为直立体，变量符号为斜体。方格纸的浅灰色网格线作为背景，文字主要集中在页面中上部，底部留有空白。关键推导步骤通过箭头符号"→"和"⟹"连接，体现逻辑递进关系。

<CTX>
{
   "topic": "史瓦西度规中的零测地线与光线偏折推导",
   "keywords": ["史瓦西度规", "零测地线条件", "光线传播方程", "角动量守恒", "参数化替换"],
   "summary": "本页将通用测地线方程具体应用于史瓦西度规，通过参数替换和零测地线条件推导出光线传播的微分方程组，并显式给出角动量守恒关系",
   "pending_concepts": ["弱场近似下光线偏折角的显式计算", "史瓦西半径处的坐标奇异性处理", "角动量守恒常数K的物理意义"]
}
</CTX>