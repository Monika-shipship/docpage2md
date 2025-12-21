# Slide 86

由
$$\Gamma^{\lambda}_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma} (\partial_{\mu} g_{\sigma\nu} + \partial_{\nu} g_{\sigma\mu} - \partial_{\sigma} g_{\mu\nu}) \tag{20}$$

将中心球对称度规代入上式可得
$$\begin{aligned}
\Gamma^{0}_{00} &= \frac{1}{2c} \dot{\nu}, \quad \Gamma^{0}_{01} = \Gamma^{0}_{10} = \frac{1}{2} \nu', \quad \Gamma^{0}_{11} = \frac{1}{2c} e^{\lambda-\nu} \dot{\lambda}, \quad \Gamma^{1}_{00} = \frac{1}{2} \nu' e^{\nu-\lambda} \\
\Gamma^{1}_{10} &= \Gamma^{1}_{01} = \frac{1}{2c} \dot{\lambda}, \quad \Gamma^{1}_{11} = \frac{1}{2} \lambda', \quad \Gamma^{1}_{22} = -r e^{-\lambda}, \quad \Gamma^{1}_{33} = -r e^{-\lambda} \sin^2 \theta \\
\Gamma^{2}_{12} &= \Gamma^{2}_{21} = \Gamma^{3}_{13} = \Gamma^{3}_{31} = \frac{1}{r}, \quad \Gamma^{2}_{33} = -\sin \theta \cos \theta, \quad \Gamma^{3}_{32} = \Gamma^{3}_{23} = \cot \theta
\end{aligned} \tag{21}$$

且（有指标求和的）
$$\Gamma^{\lambda}_{\lambda 1} = \frac{2}{r} + \frac{1}{2} (\nu' + \lambda'), \Gamma^{\lambda}_{\lambda 2} = \cot \theta, \Gamma^{\lambda}_{\lambda 3} = 0, \quad \Gamma^{\lambda}_{\lambda 0} = \frac{1}{2c} (\dot{\nu} + \dot{\lambda})$$
$$\lambda' = \frac{\partial \lambda}{\partial r}, \quad \nu' = \frac{\partial \nu}{\partial r}, \quad \dot{\lambda} = \frac{\partial \lambda}{\partial t}, \quad \dot{\nu} = \frac{\partial \nu}{\partial t} \tag{22}$$

推导：$ds^2 = -c^2 e^{\nu} dt^2 + e^{\lambda} dr^2 + r^2 (d\theta^2 + \sin^2 \theta d\phi^2)$

$g_{00} = -e^{\nu}$, $g_{11} = e^{\lambda}$, $g_{22} = r^2$, $g_{33} = r^2 \sin^2 \theta$

$\Gamma^{\lambda}_{\mu\nu} = \frac{1}{2} g^{\lambda\sigma} (\partial_{\mu} g_{\sigma\nu} + \partial_{\nu} g_{\sigma\mu} - \partial_{\sigma} g_{\mu\nu})$

当$\sigma=0$，$\partial_{\mu}, \partial_{\nu}$至少有一个为0 两全为1

$\Gamma^{0}_{00} = \frac{1}{2} g^{00} (\partial_{0} g_{00}) = \frac{1}{2} (-e^{-\nu}) \frac{\partial}{\partial t}(-e^{\nu}) = \frac{1}{2c} e^{-\nu} e^{\nu} \dot{\nu} = \frac{\dot{\nu}}{2c}$

$\Gamma^{0}_{01} = \Gamma^{0}_{10} = \frac{1}{2} g^{00} (\partial_{1} g_{00}) = \frac{1}{2} (-e^{-\nu}) \frac{\partial}{\partial r}(-e^{\nu}) = \frac{1}{2c} e^{-\nu} e^{\nu} \nu' = \frac{\nu'}{2c}$

$\Gamma^{0}_{11} = \frac{1}{2} g^{00} (0+0-\partial_{0} g_{11})$，而$g_{22}, g_{33}$对$t$偏导都为$0$，故只有$\Gamma^{0}_{11} \neq 0$。

## Figure & Layout Description
该PPT页面采用网格背景设计，整体分为三个主要区域。上半部分（约占页面2/3）为印刷体内容，背景为白色，文字和公式均为黑色。此区域包含三组数学公式：公式(20)作为黎曼联络的定义式位于顶部；公式(21)展示球对称度规下联络系数的显式计算结果，采用多行对齐格式；公式(22)列出指标求和条件及偏导数定义。中部有一条水平分隔带，由左侧黑色区域（约占1/3宽度）和右侧红色区域（约占2/3宽度）组成，红色区域印有白色文字"中心球对称解与新引力效应"。下半部分（约占页面1/3）为手写推导内容，书写在与上半部分相同的网格背景上，字迹为黑色墨水，包含度规假设形式、度规分量定义及部分联络系数的手工计算过程。整体布局层次分明，印刷内容与手写推导通过颜色分隔带明确区分，公式编号采用右对齐方式，关键推导步骤用逗号分隔并保持逻辑连贯性。

<CTX>
{
   "topic": "黎曼联络的显式计算与球对称度规应用",
   "keywords": ["黎曼联络", "球对称度规", "指标求和", "联络系数计算", "度规分量"],
   "summary": "本页通过球对称度规的具体形式，系统计算了黎曼联络的各个分量，完成了从度规假设到联络系数的显式推导，为后续曲率张量计算和引力场方程求解提供了关键中间步骤",
   "pending_concepts": ["曲率张量的具体计算过程", "Einstein场方程与联络系数的关联", "边界条件对度规参数的约束", "Schwarzschild解的最终形式验证"]
}
</CTX>