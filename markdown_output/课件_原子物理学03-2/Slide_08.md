# Slide 8

# 力学量的平均值、算符表示—平均值

将位置空间的波函数用平面单色波展开：

$$ \psi(\mathbf{r},t) = \frac{1}{(2\pi\hbar)^{3/2}} \int_{-\infty}^{+\infty} \phi(\mathbf{p}) e^{\frac{i}{\hbar}(\mathbf{p}\cdot\mathbf{r} - Et)} d\mathbf{p} $$
$$ = \frac{1}{(2\pi\hbar)^{3/2}} \int_{-\infty}^{+\infty} \phi(\mathbf{p},t) e^{\frac{i}{\hbar}\mathbf{p}\cdot\mathbf{r}} d\mathbf{p} $$

动量空间体积元 $d\mathbf{p} = dp_x dp_y dp_z$

展开系数是 $\psi(\mathbf{r},t)$ 的傅立叶变换

$$ \phi(\mathbf{p},t) = \frac{1}{(2\pi\hbar)^{3/2}} \int_{-\infty}^{+\infty} \psi(\mathbf{r},t) e^{-\frac{i}{\hbar}\mathbf{p}\cdot\mathbf{r}} d\tau $$

$\left|\phi(\mathbf{p},t)\right|^2$ 表示平面波 $e^{\frac{i}{\hbar}\mathbf{p}\cdot\mathbf{r}}$ 的所占的比重，即粒子动量取为 $\mathbf{p}$ 的概率。

$\phi(\mathbf{p},t)$ 称为**动量空间波函数**。

## Figure & Layout Description
PPT页面采用白色背景，黑色文字为主。标题"力学量的平均值、算符表示—平均值"为黑色粗体字，位于页面顶部，下方有一条蓝色细横线作为分隔线。正文内容分为多个段落，数学公式居中排版，使用标准的数学符号字体。第一个公式块包含两行等式，第二行公式右侧标注"动量空间体积元 $d\mathbf{p} = dp_x dp_y dp_z$"作为补充说明。公式中的向量符号（如$\mathbf{r}$, $\mathbf{p}$）以粗体显示，积分符号、指数函数等数学符号清晰规范。关键术语"动量空间波函数"以红色字体突出显示，其余文本为黑色常规字体。页面布局层次分明：标题→展开说明→公式→补充解释→概率解释→术语定义，逻辑流程清晰。公式中的$\hbar$符号采用标准的h-bar表示，积分上下限使用$-\infty$到$+\infty$的规范写法。

<CTX>
{
   "topic": "量子力学中动量表象的波函数展开与平均值计算基础",
   "keywords": ["波函数", "概率密度", "傅里叶变换", "动量空间波函数", "概率幅", "位置表象"],
   "summary": "本页阐述了位置空间波函数向动量空间的傅里叶展开方法，定义了动量空间波函数及其概率解释，为后续动量平均值计算奠定基础",
   "pending_concepts": ["动量算符在动量表象中的具体形式", "动量平均值的积分表达式推导", "动量与位置表象之间的算符转换关系"]
}
</CTX>