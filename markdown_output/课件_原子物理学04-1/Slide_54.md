# Slide 54

## 势能的相对论修正(了解)

由于这种颤振运动，电子感受到的核库仑势需要做修正：

$$\Delta E_V = \frac{\hbar^2}{8m_e^2c^2} \nabla^2 V(r)$$

对于氢原子或类氢离子

$$V(r) = -\frac{Ze^2}{4\pi\varepsilon_0 r}$$

$$\Delta E_V = \frac{\hbar^2}{8m_e^2c^2} \nabla^2 V(r) = \frac{\hbar^2}{8m_e^2c^2} \frac{-Ze^2}{4\pi\varepsilon_0} \nabla^2 (1/r) = \frac{\hbar^2}{8m_e^2c^2} \frac{Ze^2}{4\pi\varepsilon_0} 4\pi\delta(r)$$
$$= \frac{\pi\hbar^2}{2m_e^2c^2} \frac{Ze^2}{4\pi\varepsilon_0} \delta(r)$$

在类氢离子的本征态下，求其平均值

$$\Delta E_V = \frac{\pi\hbar^2}{2m_e^2c^2} \frac{Ze^2}{4\pi\varepsilon_0} \langle\delta(r)\rangle = \frac{\pi\hbar^2}{2m_e^2c^2} \frac{Ze^2}{4\pi\varepsilon_0} \int u_{nlm_l}^* \delta(r) u_{nlm_l} d\tau$$
$$= \frac{\pi\hbar^2}{2m_e^2c^2} \frac{Ze^2}{4\pi\varepsilon_0} \left| u_{nlm_l}(0) \right|^2$$

## Figure & Layout Description

页面顶部为黑色粗体标题"势能的相对论修正(了解)"，下方有一条深蓝色水平分割线。正文内容分为三部分：第一部分是理论说明文字，包含一段描述性文字和一个行间公式；第二部分以"对于氢原子或类氢离子"为小标题，包含势能函数表达式和推导过程；第三部分以"在类氢离子的本征态下，求其平均值"为小标题，包含平均值计算公式。页面左侧有一个蓝色右向箭头图形，指向推导过程的起始公式。所有公式均采用居中排版，文字内容为黑色常规字体。公式中的物理量符号（如$V(r)$、$\delta(r)$）和常数（如$\varepsilon_0$、$m_e$）均使用标准数学符号格式，下标和上标清晰可见。页面背景为纯白色，整体布局遵循学术PPT的典型结构，重点公式通过箭头和分段排版突出显示。

<CTX>
{
   "topic": "势能相对论修正的数学推导与δ函数应用",
   "keywords": ["颤振运动", "zitterbewegung", "狄拉克方程", "正负能态干涉", "势能修正", "δ函数", "波函数原点值"],
   "summary": "本页通过拉普拉斯算符作用于库仑势推导出势能修正的δ函数形式，并给出类氢体系中修正能量与波函数原点模平方的定量关系",
   "pending_concepts": ["δ函数在量子力学中的物理意义", "波函数原点值的具体计算方法", "相对论修正对光谱线的影响"]
}
</CTX>