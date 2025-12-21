# Slide 117

$$
\text{故 } -dr = \frac{1}{b}\left(\cos\phi - \beta\sin 2\phi\right)r^2 d\phi
$$

这里需要将 $\phi$ 表示为只有 $r$ 的函数

$$
\frac{1}{r} = \frac{1}{b}\sin\phi + \frac{\beta}{b}\left(2 - \sin^2\phi\right),\ \beta\text{小量}
$$

$$
\Rightarrow \sin\phi \approx \frac{b}{r}\quad \cos\phi = \sqrt{1 - \frac{b^2}{r^2}}
$$

$$
\left(\cos\phi - \beta\sin 2\phi\right) = \sqrt{1 - \frac{b^2}{r^2}} - \beta\cdot 2\frac{b}{r}\sqrt{1 - \frac{b^2}{r^2}} = \sqrt{1 - \frac{b^2}{r^2}}\left(1 - \frac{2\beta b}{r}\right)
$$

$$
\text{故 } -dr = \frac{1}{b}\sqrt{1 - \frac{b^2}{r^2}}\left(1 - \frac{2\beta b}{r}\right)r^2 d\phi
$$

$$
dr^2 = \frac{1}{b^2}\left(1 - \frac{b^2}{r^2}\right)\left(1 - \frac{2\beta b}{r}\right)^2 r^4 d\phi^2
$$

$$
r^2 d\phi^2 = \frac{b^2\,dr^2}{r^2\left(1 - \frac{b^2}{r^2}\right)\left(1 - \frac{2\beta b}{r}\right)^2}\quad \text{代入}
$$

$$
c^2 dt^2 = \frac{dr^2}{\left(1 - \frac{2\beta b}{r}\right)^2} + \frac{b^2\,dr^2}{r^2\left(1 - \frac{b^2}{r^2}\right)\left(1 - \frac{2\beta b}{r}\right)^3}
$$

$$
= \frac{dr^2}{\left(1 - \frac{2\beta b}{r}\right)^2}\left(1 + \frac{b^2}{r^2\left(1 - \frac{b^2}{r^2}\right)\left(1 - \frac{2\beta b}{r}\right)}\right)
$$

$$
c\,dt = \frac{dr}{\left(1 - \frac{2\beta b}{r}\right)}\sqrt{1 + \frac{b^2}{\left(r^2 - b^2\right)\left(1 - \frac{2\beta b}{r}\right)}}
$$

$\beta$ 一阶小量近似

## Figure & Layout Description
页面背景为米黄色方格纸，网格线呈浅灰色正交排列。所有内容以黑色手写体呈现，文字与公式混合排布。公式部分占据页面主要区域，按推导逻辑自上而下排列，每行公式间保留适当行距。中文注释穿插在公式之间，采用与公式相同的手写风格。页面右下角有极小字迹标注，因分辨率限制无法辨认具体内容，标记为[无法辨认]。公式中使用标准数学符号，包括希腊字母（β, φ, r）、微分符号（d）和根号等，部分公式通过箭头符号（⇒）和"代入"等中文标注体现推导逻辑。页面整体呈现典型的学术推导手稿特征，无彩色元素或图形插图。

<CTX>
{
   "topic": "雷达回波延迟的广义相对论计算",
   "keywords": ["雷达回波延迟", "广义相对论验证", "冲击参数", "度规方程", "时间延迟积分", "β一阶近似"],
   "summary": "本页完成雷达信号时间延迟积分表达式的推导，通过β一阶近似建立可计算的延迟公式框架",
   "pending_concepts": ["雷达延迟实验的具体观测数据", "b/(4β)的物理意义解释", "与光线偏折角计算的关联性", "β参数的具体物理含义"]
}
</CTX>