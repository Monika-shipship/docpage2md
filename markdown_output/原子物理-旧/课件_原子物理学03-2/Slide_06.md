# Slide 6

# 力学量的平均值、算符表示—平均值

一般地，设粒子的波函数为 $\psi(\mathbf{r}, t)$，则在 $t$ 时刻粒子出现在 $\mathbf{r}$ 附近 $d\tau$ 体积元内的概率为：

$$ \rho(\mathbf{r}, t) d\tau = \psi^*(\mathbf{r}, t) \psi(\mathbf{r}, t) d\tau $$

其中 $\rho(\mathbf{r}, t)$ 是概率密度。假设波函数已经归一化，即

$$ \int_{-\infty}^{+\infty} \rho(\mathbf{r}, t) d\tau = 1 $$

则位置 $\mathbf{r}$ 的平均值为：

$$ \langle \mathbf{r} \rangle = \int_{-\infty}^{+\infty} \mathbf{r} \rho(\mathbf{r}, t) d\tau = \int_{-\infty}^{+\infty} \psi^*(\mathbf{r}, t) \mathbf{r} \psi(\mathbf{r}, t) d\tau $$

## Figure & Layout Description
页面整体为白色背景，顶部有黑色粗体标题"力学量的平均值、算符表示—平均值"，字号约32pt，标题下方有一条深灰色（#555555）细实线作为分隔线，线宽约1.5pt，横跨整个页面宽度。正文内容采用黑色常规字体（约18pt），段落左对齐排列。公式部分以居中方式显示，使用标准数学符号排版，其中向量符号 $\mathbf{r}$ 以加粗形式呈现，积分符号上下限清晰标注。页面无图片、图表或装饰性元素，整体布局简洁，文字与公式间距适中，符合学术讲义的典型排版风格。

<CTX>
{
   "topic": "量子力学中力学量平均值的计算方法",
   "keywords": ["波函数", "概率密度", "归一化条件", "位置平均值", "量子力学算符", "概率幅"],
   "summary": "本页将概率论的平均值概念引入量子力学体系，通过波函数定义概率密度函数，并推导出位置算符平均值的积分表达式",
   "pending_concepts": ["动量平均值的计算方法", "动能与角动量平均值的推导", "力学量算符的普遍定义"]
}
</CTX>