# Slide 10

# 力学量的平均值、算符表示—平均值

(4) 粒子的动能 $T = \boldsymbol{p}^2 / 2m$

类似地，动能的平均值

$$
\langle T \rangle = \int_{-\infty}^{+\infty} \psi^*(\boldsymbol{r},t) \left( -\frac{\hbar^2}{2m} \nabla^2 \right) \psi(\boldsymbol{r},t) \, d\tau
$$

动能算符： $\hat{T} = -\frac{\hbar^2}{2m} \nabla^2$ 且有 $\hat{T} = \frac{\hat{\boldsymbol{p}}^2}{2m}$

(5) 粒子的总能 $E = T + V(\boldsymbol{r},t)$

平均值

$$
\langle E \rangle = \int_{-\infty}^{+\infty} \psi^*(\boldsymbol{r},t) \left( -\frac{\hbar^2}{2m} \nabla^2 + V(\boldsymbol{r},t) \right) \psi(\boldsymbol{r},t) \, d\tau
$$

总能算符： $\hat{H} = -\frac{\hbar^2}{2m} \nabla^2 + V(\boldsymbol{r},t) = \frac{\hat{\boldsymbol{p}}^2}{2m} + V(\boldsymbol{r},t)$

哈密顿算符

## Figure & Layout Description

页面顶部为黑色粗体主标题"力学量的平均值、算符表示—平均值"，下方有一条深灰色水平分隔线。内容分为两个主要部分：

1. **第(4)部分**：
   - 以蓝色字体标注"(4) 粒子的动能 $T = \boldsymbol{p}^2 / 2m$"
   - 黑色常规字体"类似地，动能的平均值"作为引导语
   - 一个大型行间公式展示动能平均值计算式，积分符号上下限为$-\infty$到$+\infty$，被积函数包含复共轭波函数$\psi^*$、动能算符表达式和波函数$\psi$
   - 公式下方有"动能算符："文字说明，后接两个并列的算符定义式，中间用"且有"连接

2. **第(5)部分**：
   - 以蓝色字体标注"(5) 粒子的总能 $E = T + V(\boldsymbol{r},t)$"
   - 黑色常规字体"平均值"作为引导语
   - 一个大型行间公式展示总能平均值计算式，结构与动能公式类似但包含势能项
   - 公式下方有"总能算符："文字说明，后接哈密顿算符的两种等价表达式
   - 最底部有红色加粗文字"哈密顿算符"作为重点标注

整体排版采用左对齐方式，公式与文字说明严格对应，数学符号使用标准物理 notation，关键算符定义使用较大字号突出显示。

<CTX>
{
   "topic": "动能与总能的平均值计算及对应算符表示",
   "keywords": ["动能算符", "哈密顿算符", "总能平均值", "波函数积分", "算符定义"],
   "summary": "本页建立了动能和总能的平均值计算公式，明确定义了动能算符和哈密顿算符的微分形式及其与动量算符的关系",
   "pending_concepts": ["力学量算符的普遍构造方法", "不同力学量算符的对易关系", "含时薛定谔方程的推导基础"]
}
</CTX>