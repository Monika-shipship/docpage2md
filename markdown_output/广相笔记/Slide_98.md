# Slide 98

## 测地线方程

$$
\frac{d^2 x^\alpha}{ds^2} + \Gamma^\alpha_{\beta\gamma} \frac{dx^\beta}{ds} \frac{dx^\gamma}{ds} = 0
$$

化为

$\alpha=0$: 
$$
\frac{d^2 (ct)}{ds^2} + \Gamma^0_{\beta\gamma} \frac{dx^\beta}{ds} \frac{dx^\gamma}{ds} = 0
$$
$$
\frac{d^2 (ct)}{ds^2} + \frac{1}{2}\nu' \frac{dr}{ds} \frac{d(ct)}{ds} = 0
$$
$$
\frac{d^2 t}{ds^2} + \nu' \frac{dr}{ds} \frac{dt}{ds} = 0
$$

$\alpha=1$:
$$
\frac{d^2 r}{ds^2} + \frac{1}{2}\nu' e^{2\lambda} \left(\frac{d(ct)}{ds}\right)^2 + \frac{1}{2}\lambda' \left(\frac{dr}{ds}\right)^2 - r e^{-\lambda} \left(\frac{d\theta}{ds}\right)^2 - r e^{-\lambda} \sin^2\theta \left(\frac{d\phi}{ds}\right)^2 = 0
$$

$\alpha=2$:
$$
\frac{d^2 \theta}{ds^2} + 2\frac{1}{r} \frac{dr}{ds} \frac{d\theta}{ds} - \sin\theta\cos\theta \left(\frac{d\phi}{ds}\right)^2 = 0
$$

$\alpha=3$:
$$
\frac{d^2 \phi}{ds^2} + 2\frac{1}{r} \frac{dr}{ds} \frac{d\phi}{ds} + 2\cot\theta \frac{d\theta}{ds} \frac{d\phi}{ds} = 0
$$

使 $\theta = \frac{\pi}{2}$，且 $\lambda = -\nu$，有：
$$
\frac{1}{\tan\theta}
$$

---

由 **史瓦西中** $\lambda = \lambda(r)$, $\nu = \nu(r)$, $\lambda + \nu = 0$

$$
\Gamma^\lambda_{\mu\nu} = \frac{1}{2}g^{\lambda\sigma}(\partial_\mu g_{\sigma\nu} + \partial_\nu g_{\sigma\mu} - \partial_\sigma g_{\mu\nu})
$$

将中心球对称度规代入上式可得

$\Gamma^0_{00} = \frac{1}{2c}\dot{\nu}$, $\Gamma^0_{01} = \Gamma^0_{10} = \frac{1}{2}\nu'$, $\Gamma^0_{11} = \frac{1}{2c}e^{\nu-\lambda}\dot{\lambda}$, $\Gamma^1_{00} = \frac{1}{2}e^{\nu-\lambda}\nu'$

$\Gamma^1_{10} = \Gamma^1_{01} = \frac{1}{2c}\dot{\lambda}$, $\Gamma^1_{11} = \frac{1}{2}\lambda'$, $\Gamma^1_{22} = -re^{-\lambda}$, $\Gamma^1_{33} = -re^{-\lambda}\sin^2\theta$

$\Gamma^2_{12} = \Gamma^2_{21} = \Gamma^3_{13} = \Gamma^3_{31} = \frac{1}{r}$, $\Gamma^2_{33} = -\sin\theta\cos\theta$, $\Gamma^3_{32} = \cot\theta$

且（有指标求和的）

$$
\Gamma^\lambda_{\lambda 1} = \frac{2}{r} + \frac{1}{2}(\nu' + \lambda'), \Gamma^\lambda_{\lambda 2} = \cot\theta, \Gamma^\lambda_{\lambda 3} = 0, \Gamma^\lambda_{\lambda 0} = \frac{1}{2}(\dot{\nu} + \dot{\lambda})
$$

$$
\lambda' = \frac{\partial\lambda}{\partial r},\quad \nu' = \frac{\partial\nu}{\partial r},\quad \dot{\lambda} = \frac{\partial\lambda}{\partial t},\quad \dot{\nu} = \frac{\partial\nu}{\partial t}
$$

## Figure & Layout Description

页面采用左右分栏布局：左侧为手写体推导区域（米黄色方格纸背景），右侧为印刷体公式区域（白色背景）。左侧顶部手写"测地线方程"标题，其下方为测地线方程通式，接着以"化为"引导分情况讨论（α=0,1,2,3），每种情况均列出对应微分方程。手写公式中包含多处修改痕迹，如α=0行下方有二次推导的简化式。右侧印刷内容顶部有红色手写批注"史瓦西中"，包含Christoffel符号定义式及代入球对称度规后的具体表达式，部分公式旁有红色"=0"标记。底部有黑色横条标注"中心球对称解与新引力效应"，其中"新引力效应"为红色字体。整体文字以黑色为主，关键修正和标注使用红色墨水，手写公式存在连笔和简写现象（如"ct"简写为"ct"），印刷公式中存在下标模糊处（如Γ^λ_{λ0}的λ下标）。

<CTX>
{
   "topic": "史瓦西度规下的测地线方程分量推导与参数化处理",
   "keywords": ["测地线方程", "Christoffel符号计算", "球对称度规", "轨道参数化", "λ-ν关系"],
   "summary": "本页完成史瓦西度规下测地线方程各分量的具体展开，并通过θ=π/2和λ=-ν条件简化方程，建立轨道参数化的数学基础",
   "pending_concepts": ["Γ符号具体推导步骤", "ν(r)和λ(r)的物理意义", "参数s与坐标时间t的转换关系", "轨道进动量的最终表达式"]
}
</CTX>