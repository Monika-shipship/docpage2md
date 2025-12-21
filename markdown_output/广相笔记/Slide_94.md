# Slide 94

所以 $ e^{\nu} (dt)^2 = e^{\bar{\nu}} (d\bar{t})^2 $

$ ds^2 $ 中 $ \nu $ 换为 $ \bar{\nu} $，可使 $ \lambda + \bar{\nu} = 0 $ 且 $ ds^2 $ 形式不变

保证了 $ \lambda $ 和 $ \bar{\nu} $ 仅为 $ r $ 的函数，与 $ t $ 无关

$$
\begin{cases}
\lambda + \nu = f(t) \\
\nu - f(t) = \bar{\nu}(r)
\end{cases}
\Rightarrow -\lambda(r) = \bar{\nu}(r)
$$

$ e^{-\lambda} = e^{\bar{\nu}} $

此后，就用 $ \nu $ 标示 $ \bar{\nu} $，即变换后的，有 $ \lambda(r) + \nu(r) = 0 $，$ e^{-\lambda} = e^{\nu} $。

$ \nu' = \frac{e^{-\lambda} - 1}{r} $，$ \lambda' = \frac{1 - e^{\lambda}}{r} $ 解 $ e^{-\lambda} $

$ \frac{d\lambda}{dr} = \frac{1 - e^{\lambda}}{r} $

$ \frac{d\lambda}{1 - e^{\lambda}} = \frac{dr}{r} $

$ \frac{e^{-\lambda} d\lambda}{e^{-\lambda} - 1} = \frac{-de^{-\lambda}}{e^{-\lambda} - 1} = \frac{dr}{r} $

$ \frac{de^{-\lambda}}{e^{-\lambda} - 1} + \frac{dr}{r} = 0 $

$ \ln|e^{-\lambda} - 1| + \ln r = \ln \alpha $

## Figure & Layout Description

图片为方格纸背景的手写数学推导，黑色墨水书写。页面布局为纵向排列的数学公式与文字说明，文字与公式按逻辑顺序分段排列。顶部为等式推导，中间部分包含联立方程组，底部为微分方程求解步骤。文字与公式均对齐于方格线，公式中的分式结构通过水平线清晰分隔分子分母。关键变量（如ν、λ、r）使用斜体手写，上标与下标位置准确。联立方程组使用大括号括起，右侧标注推导结论。微分符号（dλ/dr）采用斜体d，与变量r保持适当间距。最后一行积分结果包含绝对值符号与对数项，等号左右对齐工整。页面整体呈现典型的物理学家手稿风格，公式推导过程完整且逻辑连贯。

<CTX>
{
   "topic": "度规函数ν与λ的微分方程求解及坐标变换关系",
   "keywords": ["Einstein场方程", "度规函数ν", "度规函数λ", "时间坐标变换", "度规不变性", "微分方程求解"],
   "summary": "本页通过微分方程推导得出度规函数ν与λ的显式关系式，并建立其与径向坐标r的积分解形式",
   "pending_concepts": ["Schwarzschild解的完整推导路径", "坐标奇点与物理奇点的数学判据", "度规函数积分常数的物理意义"]
}
</CTX>