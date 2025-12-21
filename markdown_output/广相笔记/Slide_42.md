# Slide 42

$$
= -\frac{1}{2} \frac{d}{d\sigma} \left( \frac{1}{\sqrt{-g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta}} g_{\alpha\beta} \left( \delta_\mu^\alpha \dot{x}^\beta + \delta_\mu^\beta \dot{x}^\alpha \right) \right)
$$

$$
= -\frac{1}{2} \frac{d}{d\sigma} \left( \frac{1}{\sqrt{-g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta}} \left( g_{\mu\beta} \dot{x}^\beta + g_{\alpha\mu} \dot{x}^\alpha \right) \right)
$$

$$
= -\frac{1}{2} \frac{d}{d\sigma} \left( \frac{g_{\mu\beta} \dot{x}^\beta + g_{\alpha\mu} \dot{x}^\alpha}{\frac{ds}{d\sigma}} \right)
$$

$$
g_{\alpha\beta} = g_{\alpha\beta}(x) \quad \frac{ds}{d\sigma} = \sqrt{-g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta}
$$

$$
\frac{dg_{\alpha\beta}}{d\sigma} = \frac{\partial g_{\alpha\beta}}{\partial x^\nu} \frac{dx^\nu}{d\sigma} = \partial_\nu (g_{\alpha\beta}) \dot{x}^\nu
$$

$$
= -\frac{1}{2} \left[ \left( \partial_\nu (g_{\mu\beta}) \dot{x}^\nu \dot{x}^\beta + \partial_\nu (g_{\alpha\mu}) \dot{x}^\nu \dot{x}^\alpha + 2g_{\alpha\mu} \ddot{x}^\alpha \right) \frac{ds}{d\sigma} - \frac{d^2s}{d\sigma^2} \left( g_{\mu\beta} \dot{x}^\beta + g_{\alpha\mu} \dot{x}^\alpha \right) \right] \frac{1}{\left( \frac{ds}{d\sigma} \right)^2}
$$

$$
= -\frac{1}{2} \frac{1}{\frac{ds}{d\sigma}} \left[ \partial_\nu (g_{\mu\beta}) \dot{x}^\nu \dot{x}^\beta + \partial_\nu (g_{\alpha\mu}) \dot{x}^\nu \dot{x}^\alpha + 2g_{\alpha\mu} \ddot{x}^\alpha \right] + \frac{1}{2} \frac{\frac{d^2s}{d\sigma^2}}{\left( \frac{ds}{d\sigma} \right)^2} \left( g_{\mu\beta} \dot{x}^\beta + g_{\alpha\mu} \dot{x}^\alpha \right)
$$

## Figure & Layout Description
图片展示一张米黄色方格纸背景的手写数学推导，网格线为浅灰色细线构成1cm×1cm方格。所有内容以黑色墨水书写，公式从上至下垂直排列共8行。第一至第三行公式左侧对齐等号，使用标准分数结构和括号分组；第四、五行以短句形式横向排列两个定义式；第六行开始出现大型方括号结构，包含多层导数项；最后两行公式通过水平分数线分解为两项。关键符号特征：带点的$x$（$\dot{x}$）表示对$\sigma$的导数，$\delta$符号带有上下标，度规张量$g_{\alpha\beta}$的下标清晰可辨，分母中的$\frac{ds}{d\sigma}$以完整分数形式呈现。整体布局遵循从左到右、从上到下的推导逻辑，无颜色标记或图形元素，纯数学符号构成。

<CTX>
{
   "topic": "测地线方程变分推导的导数展开",
   "keywords": ["测地线", "变分原理", "欧拉-拉格朗日方程", "度规张量导数", "变分导数"],
   "summary": "本页详细展开测地线变分推导中的导数计算过程，揭示度规张量对坐标的依赖性如何影响测地线方程的形成",
   "pending_concepts": ["测地线方程的具体解法", "仿射参量的物理意义", "类时/类空测地线的区分条件", "度规张量的协变导数"]
}
</CTX>