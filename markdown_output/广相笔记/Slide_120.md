# Slide 120

## 3.5 固有时与引力频移

线元的定义就是固有时，因为选取了+2号差，$|ds^2| = -ds^2$（对于质点运动），$ds = \sqrt{-ds^2}$，$ds \cdot ds = -ds^2$。

固有时定义为 $d\tau = \frac{1}{c} \sqrt{|ds^2|} = \frac{1}{c} \sqrt{-ds^2}$。

$ds^2 = g_{\mu\nu} dx^\mu dx^\nu$ 是线元。

$ds$ 是长度量纲，$d\tau$ 时间量纲。

弯曲时空中质点的运动方程为 
$$\frac{d^2 x^\lambda}{ds^2} + \Gamma^\lambda_{\alpha\beta} \frac{dx^\alpha}{ds} \frac{dx^\beta}{ds} = 0$$

利用 $d\tau = \frac{1}{c} ds$，有 
$$\frac{d^2 x^\lambda}{d\tau^2} + \Gamma^\lambda_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = 0$$
加速度量纲 速度量纲。

当有引力之外的力 $F^\lambda$ 时，方程变为
$$\frac{d^2 x^\lambda}{d\tau^2} + \Gamma^\lambda_{\alpha\beta} \frac{dx^\alpha}{d\tau} \frac{dx^\beta}{d\tau} = f^\lambda = \frac{F^\lambda}{m}$$

假设此方程的解为 $x^\mu = x^\mu(\tau)$。

这个轨道称为世界线。

由此知 $\tau$ 是客观存在的时间参数。

$\tau$ 正比于线元，是几何量！

由此可以改写其它理论，如 Schrödinger 时间改成固有时。

固有时的特征：
① $\tau$ 与坐标选择无关 $d\tau = \frac{1}{c} ds$，是不变量，几何量。

② $d\tau$ 在不同时空点不同 $d\tau = \frac{1}{c} \sqrt{-g_{\mu\nu} \frac{dx^\mu}{d\tau} \frac{dx^\nu}{d\tau}} d\tau$，$g_{\mu\nu} = g_{\mu\nu}(x)$。

③ $d\tau$ 与路径有关，$x^\mu = x^\mu(t)$，$\tau_{AB} = \int_A^B ds = \frac{1}{c} \int_A^B \sqrt{-g_{\mu\nu} \frac{dx^\mu}{dt} \frac{dx^\nu}{dt}} dt$

## Figure & Layout Description
图片背景为米黄色方格纸，带有均匀分布的浅灰色网格线，形成标准方格布局。所有内容均为黑色手写墨水书写，字迹清晰但略带手写特征。文字从左上角开始，按从上到下的顺序排列，整体左对齐。标题"3.5 固有时与引力频移"位于页面顶部，使用较大字号。公式与文字混合排布，关键公式使用标准数学符号书写，部分公式下方有手写注释（如"加速度量纲 速度量纲"）并带有波浪下划线强调。在"固有时的特征"部分，使用带圈数字①②③进行分点标注，每个特征点后紧跟公式说明。页面中公式与文字行间距适中，公式中的希腊字母和上下标清晰可辨。无彩色元素或图形插图，仅包含纯文本和数学表达式，整体呈现典型的课堂笔记风格，具有学术手稿的视觉特征。

<CTX>
{
   "topic": "固有时与引力频移的理论基础",
   "keywords": ["固有时", "线元", "世界线", "运动方程", "几何量", "度规张量", "加速度量纲", "时间参数"],
   "summary": "本页系统阐述固有时的定义、与线元的关系、质点运动方程在固有时下的表达形式及其三大特征，建立引力理论中时间参数的几何本质",
   "pending_concepts": ["+2号差的具体物理含义", "Schrödinger方程改写固有时的具体实现", "固有时与坐标时的定量关系", "世界线在实验中的可观测验证"]
}
</CTX>