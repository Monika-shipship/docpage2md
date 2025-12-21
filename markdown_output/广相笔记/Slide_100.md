# Slide 100

测地线方程

$$\frac{d^2x^0}{ds^2} + \Gamma^0_{\alpha\beta}\frac{dx^\alpha}{ds}\frac{dx^\beta}{ds} = 0$$

可写作 $ds = c d\tau$

$$\frac{d^2x^0}{d\tau^2} + \Gamma^0_{\alpha\beta}\frac{dx^\alpha}{d\tau}\frac{dx^\beta}{d\tau} = 0$$

$x^0 = x^0(\tau)$

$\tau$为描述粒子运动的固有时

## 3.2.4 GR中行星轨道

在 $\theta = \frac{\pi}{2}$, $ds^2 = -e^\nu c^2dt^2 + e^\lambda dr^2 + r^2d\phi^2$

$$
\begin{cases}
\frac{d^2t}{ds^2} + \nu'\frac{dr}{ds}\frac{dt}{ds} = 0 \\
\frac{d^2r}{ds^2} + \frac{1}{2}\nu'e^{2\nu}\left(\frac{dct}{ds}\right)^2 - \frac{1}{2}\lambda'\left(\frac{dr}{ds}\right)^2 - re^\lambda\left(\frac{d\phi}{ds}\right)^2 = 0 \\
\frac{d^2\phi}{ds^2} + 2\frac{1}{r}\frac{dr}{ds}\frac{d\phi}{ds} = 0 \\
e^\nu = 1 - \frac{2GM}{c^2r}
\end{cases}
$$

## Figure & Layout Description
图片为方格纸背景的手写笔记，纸张底色为米黄色，方格线为浅灰色。内容以黑色墨水书写，从上至下排列。顶部是"测地线方程"标题，字体较大且略带倾斜。下方是两组测地线方程，第一组使用参数s，第二组使用参数τ，两组方程结构相似但参数不同。中间有"可写作 $ds = c d\tau$"的说明文字，以及$x^0 = x^0(\tau)$和"τ为描述粒子运动的固有时"的解释。下半部分以"3.2.4 GR中行星轨道"为小节标题，标题右侧有"θ=π/2"的标注。随后是度规表达式，再下方是一个大括号括起的四元方程组，最后一行是$e^\nu$的具体表达式。整体布局清晰，公式与文字交错排列，方格纸背景提供了清晰的坐标参考，使公式结构一目了然。所有公式均手写完成，部分符号（如Γ）书写较为紧凑，但关键数学符号清晰可辨。

<CTX>
{
   "topic": "测地线方程的固有时参数化与史瓦西度规下行星轨道方程",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "轨道角动量"],
   "summary": "本页展示了测地线方程在固有时参数化下的形式，并推导了史瓦西度规下θ=π/2平面内的行星轨道方程组，建立了广义相对论中行星运动的基本方程框架",
   "pending_concepts": ["Γ符号具体推导步骤", "ν(r)和λ(r)的物理意义", "轨道进动量的最终表达式", "面积速度定理的物理意义", "测地线方程各分量的物理解释"]
}
</CTX>