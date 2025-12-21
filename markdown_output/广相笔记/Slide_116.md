# Slide 116

## 3.4 雷达回波之延迟

$$\beta = \frac{GM}{c^2 b}$$

$$u = \frac{1}{b} \sin\phi + \frac{\beta}{b} (2 - \sin^2\phi) \quad , \quad \beta = \frac{GM}{c^2 b} \quad \frac{GM}{c^2} = \beta b$$

设地球、反射星、太阳不动，求反射来回之时间。

$$T_{\text{all}} = 2T \quad , \quad T = t(b \to r_1) + t(b \to r_2)$$

$$t(b \to r) = \int_b^r dt \quad \text{而只知 } r \text{ 与 } \phi \text{ 关系}$$

$$\theta = \frac{\pi}{2} \text{ 处}$$

$$ds^2 = 0 = - \left(1 - \frac{2GM}{c^2 r}\right) c^2 dt^2 + \frac{dr^2}{1 - \frac{2GM}{c^2 r}} + r^2 d\phi^2$$

代入 $\frac{GM}{c^2} = \beta b$, 其中 $\beta = \frac{GM}{c^2 b}$

故 $$c^2 dt^2 = \frac{dr^2}{\left(1 - \frac{2\beta b}{r}\right)^2} + \frac{r^2 d\phi^2}{1 - \frac{2\beta b}{r}}$$

$$\frac{1}{r} = \frac{1}{b} \sin\phi + \frac{\beta}{b} (2 - \sin^2\phi)$$

$$-\frac{1}{r^2} dr = \frac{1}{b} (\cos\phi - \beta \cdot 2 \sin\phi \cos\phi) d\phi$$

## Figure & Layout Description

该幻灯片呈现于浅米色方格纸背景上，手写笔记风格。顶部左侧用黑色墨水书写二级标题"3.4 雷达回波之延迟"，右侧标注"反射星"。中央偏上位置绘制天体示意图：中心为标注"Sun"的黑色实线圆，左侧标注"Earth"的黑点，右上方标注"反射星"的黑点。从Earth到反射星的弯曲实线表示光线路径，路径与Sun最近点处标注垂直线段"b"（冲击参数），并标注"b/(4β)"。从Sun中心到Earth和反射星分别引出线段标注"r₁"和"r₂"，在Sun与反射星连线处标注角度"φ"。示意图右侧有两组公式：上方为"β = GM/(c²b)"，下方有向下的箭头符号和"b↑"、"b/(4β)"标注。示意图下方为数学推导区域，包含多行手写公式和中文说明：第一行为"u = (1/b)sinφ + (β/b)(2 - sin²φ)"及"β = GM/(c²b)"；第二行为中文"设地球、反射星、太阳不动，求反射来回之时间"；后续为时间计算公式"T_all = 2T, T = t(b→r₁) + t(b→r₂)"、积分表达式"t(b→r) = ∫_b^r dt"及说明"而只知r与φ关系"；再下方标注"θ=π/2处"并列出度规方程"ds²=0=..."；最后是代入过程和微分关系式。所有文字和公式均用黑色墨水书写，字迹工整但带有手写特征，网格线为浅灰色细线，整体布局上图下文、左文右图，公式与文字紧密排列形成逻辑推导流。

<CTX>
{
   "topic": "雷达回波延迟的广义相对论计算",
   "keywords": ["雷达回波延迟", "广义相对论验证", "冲击参数", "度规方程", "时间延迟积分"],
   "summary": "本页推导雷达信号在太阳引力场中的往返时间延迟公式，建立从光线路径到时间积分的完整数学框架",
   "pending_concepts": ["雷达延迟实验的具体观测数据", "b/(4β)的物理意义解释", "与光线偏折角计算的关联性"]
}
</CTX>