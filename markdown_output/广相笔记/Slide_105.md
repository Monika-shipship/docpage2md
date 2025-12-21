# Slide 105

$$ \phi \approx 2\pi + \delta\phi $$

$$ \sin(\phi) = \frac{\alpha}{P} \left( \sin\phi + (2\pi + \delta\phi) \cos\phi \right) $$

$$ \delta = \frac{\alpha}{P} (\delta + 2\pi + \delta) $$

$$ \delta \approx \frac{\alpha}{P} (2\delta + 2\pi) \approx \frac{2\alpha}{P} (\delta + \pi) $$

$$ \left(1 - \frac{2\alpha}{P}\right) \delta \approx \frac{2\alpha\pi}{P} $$

$$ \delta \approx \frac{2\alpha\pi}{P \left(1 - \frac{2\alpha}{P}\right)} \approx \frac{2\alpha\pi}{P} \left(1 + \frac{2\alpha}{P}\right) $$

$$ \approx 2\frac{\alpha\pi}{P} = 2\pi \frac{\alpha}{P} $$

$\delta$ 就是进动角， $2\pi \frac{\alpha}{P}$ ，

其中 $\alpha = \frac{3GM}{c^2}$ ， $P = \frac{b^2}{a}$ ， $P = a(1 - e^2)$

故 $\delta = 2\pi \frac{3GM}{c^2} \cdot \frac{1}{a(1 - e^2)} = \frac{6\pi GM}{c^2 a (1 - e^2)}$

这是转一周之进动。

再利用 $T = 2\pi \sqrt{\frac{a^3}{GM}}$ ， $\frac{T^2}{a^3} = \frac{4\pi^2}{GM}$ $\Rightarrow GM = \frac{4\pi^2}{T^2} a^3$

$\Rightarrow \delta = \frac{6\pi}{c^2 a (1 - e^2)} \cdot \frac{4\pi^2}{T^2} a^3 = \frac{24\pi^3 a^2}{c^2 T^2 (1 - e^2)}$

右侧补充公式：
$r = \frac{p}{1 + e \cos\phi}$
$a + c = \frac{p}{1 - e}$
$a - c = \frac{p}{1 + e}$
$2a = p \frac{2}{1 - e^2} \Rightarrow a = \frac{p}{1 - e^2}$
$p = a(1 - e^2)$

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记，使用黑色墨水书写。整体布局分为左右两个垂直区域：左侧为主推导区（占页面2/3宽度），包含9行核心公式推导；右侧为补充公式区（占页面1/3宽度），包含5行轨道参数关系式。所有公式自上而下垂直排列，行间距均匀。左侧区域第一行起始为"φ ≈ 2π + δφ"，后续公式包含分数运算（如$\frac{\alpha}{P}$）和括号展开，第5-7行出现分式复合结构；右侧区域与左侧平行对齐，包含$r = \frac{p}{1 + e \cos\phi}$等椭圆轨道参数关系。手写文字具有明显书写连笔特征，部分符号（如"δ"）存在轻微倾斜，但所有数学符号和下标均清晰可辨。页面无彩色标记或图形元素，纯文字公式构成完整推导链条。

<CTX>
{
   "topic": "近日点进动角度的定量推导与轨道参数关联",
   "keywords": ["测地线方程", "固有时参数化", "史瓦西度规", "行星轨道方程", "倒代换", "u=1/r", "轨道微分方程", "进动项", "摄动法", "特解系数", "长期积累项", "开普勒第三定律", "水星近日点进动"],
   "summary": "本页通过轨道参数代换和开普勒定律推导出进动角δ的完整表达式，建立了相对论修正项与观测周期的定量关系",
   "pending_concepts": ["进动角度的数值计算示例", "相对论修正项与牛顿力学结果的对比", "水星观测数据与理论值的匹配验证"]
}
</CTX>