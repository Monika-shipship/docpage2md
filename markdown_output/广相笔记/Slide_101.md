# Slide 101

由 $ds^2$ 表达式得 $ds^2 = -|ds^2|$ 负的 $ds^2 = -c^2 d\tau^2$。  
$ds^2 = -e^{\nu} c^2 dt^2 + e^{\lambda} dr^2 + r^2 d\phi^2$。  

$$1 = +e^{\nu} c^2 \left(\frac{dt}{ds}\right)^2 - e^{\lambda} \left(\frac{dr}{ds}\right)^2 - r^2 \left(\frac{d\phi}{ds}\right)^2,$$

$$\left(\frac{dr}{ds}\right)^2 = e^{\lambda} \left(-1 + e^{\nu} c^2 \left(\frac{dt}{ds}\right)^2 - r^2 \left(\frac{d\phi}{ds}\right)^2\right)$$
$$= -e^{\lambda} + e^{\nu + \lambda} c^2 \left(\frac{dt}{ds}\right)^2 - e^{\lambda} r^2 \left(\frac{d\phi}{ds}\right)^2.$$

代入：  
$$\frac{d^2 r}{ds^2} + \frac{1}{2}\nu' e^{2\lambda} \left(\frac{dct}{ds}\right)^2 - \frac{1}{2}\nu' \left(\frac{dr}{ds}\right)^2 - r e^{\nu} \left(\frac{d\phi}{ds}\right)^2 = 0.$$

$$\frac{d^2 r}{ds^2} + \frac{1}{2}\nu' e^{2\lambda} \left(\frac{dct}{ds}\right)^2 - r e^{\nu} \left(\frac{d\phi}{ds}\right)^2 + \frac{1}{2}\nu' e^{\lambda} - \frac{1}{2}\nu' e^{\nu + \lambda} c^2 \left(\frac{dt}{ds}\right)^2 + \frac{1}{2}\nu' e^{\lambda} r^2 \left(\frac{d\phi}{ds}\right)^2 = 0.$$

$$\frac{d^2 r}{ds^2} + r e^{\nu} \left(\frac{1}{2}\nu' r - 1\right) \left(\frac{d\phi}{ds}\right)^2 + \frac{1}{2}\nu' e^{\nu} = 0.$$

与此相似，用倒代换 $u = \frac{1}{r}$  
$$r^2 \frac{d\phi}{ds} = \frac{h}{c}, \quad \Rightarrow \quad \frac{d\phi}{ds} = u^2 \frac{h}{c}, \quad \left(\frac{d\phi}{ds}\right)^2 = \frac{h^2}{c^2} u^4.$$

$$\frac{dr}{ds} = -\frac{1}{u^2} \frac{du}{ds} = -\frac{1}{u^2} \frac{du}{d\phi} \frac{d\phi}{ds} = -\frac{h}{c} \frac{du}{d\phi}.$$

$$\frac{d^2 r}{ds^2} = -\frac{h}{c} \frac{d^2 u}{d\phi^2} \frac{d\phi}{ds} = -\frac{h^2}{c^2} u^2 \frac{d^2 u}{d\phi^2}.$$

## Figure & Layout Description
图片展示在方格纸背景上的手写数学推导，整体布局为垂直排列的推导步骤，共12行核心内容。文字以黑色墨水书写，关键修正和强调部分使用彩色标记：  
- **红色标记**：位于右上角区域，包含"ds² = -c²dτ²"和"$\frac{d\tau^2}{ds^2} = -\left(\frac{dt}{ds}\right)^2$"的完整公式；第三行开头的"+"号、第四行括号内的"-1"、第八行的"+"号均用红色标注，表明关键符号修正。  
- **蓝色标记**：第七行中三个关键项被蓝色下划线标记——包括"- r e^ν (dφ/ds)²"、"- (1/2)ν' e^{ν+λ} c² (dt/ds)²"和"+ (1/2)ν' e^λ r² (dφ/ds)²"，突出这些项在方程重组中的作用。  
- **文字层级**：从上至下依次为度规定义→参数化方程→代数变形→测地线方程代入→轨道方程简化→倒代换应用，形成逻辑递进结构。  
- **书写特征**：手写字体工整但带有推导过程中的修改痕迹（如第三行开头的红色"+"号覆盖了原黑色符号），方格纸的浅灰色网格线作为背景，每行推导占据约2-3个网格高度。

<CTX>
{
   "topic": "史瓦西度规下行星轨道方程的推导与倒代换应用",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "轨道角动量", "倒代换", "u=1/r"],
   "summary": "本页完成史瓦西度规下行星轨道方程的具体推导，通过代数变形和倒代换u=1/r将测地线方程转化为轨道微分方程，为计算轨道进动奠定数学基础",
   "pending_concepts": ["ν(r)和λ(r)的物理意义", "轨道进动量的最终表达式", "面积速度定理的物理意义", "测地线方程各分量的物理解释", "h的物理定义（轨道角动量）"]
}
</CTX>