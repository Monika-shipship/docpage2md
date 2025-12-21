# Slide 12

任意分割 $[c,d]$，如 $c = t_0 < t_1 < t_2 < \cdots < t_n = d$  
$\Delta t_i = t_i - t_{i-1} > 0$  
$\lambda = \max\{\Delta t_i, i=1,2,\cdots,n\}$  

$$
\lim_{\Delta t_i \to 0} \sum_{i=1}^{n} \left| \vec{r}(t_i) - \vec{r}(t_{i-1}) \right| = \lim_{\Delta t_i \to 0} \sum_{i=1}^{n} \frac{\left| \vec{r}(t_i) - \vec{r}(t_{i-1}) \right|}{\Delta t_i} \Delta t_i = \int_{c}^{d} |\vec{r}'(t)| \, dt
$$

$d \to t$，$s(t) = \int_{c}^{t} |\vec{r}'(u)| \, du$，$s'(t) = |\vec{r}'(t)| > 0$，$s(t)$ 是严格增，反函数存在 $t = t(s)$  
$t \to s$ 换元，$\vec{r}(s) = \vec{r}(t(s)) = (x(t(s)), y(t(s)))$ 弧长参数曲线  
$s$ 称弧长参数  

注① 正则曲线总可以取弧长参数  
因为正则曲线 $\Rightarrow s'(t) = |\vec{r}'(t)| > 0$，有反函数  

注② 弧长参数曲线的切向量是单位向量  
$$
\left| \frac{d\vec{r}}{ds} \right| = \left| \frac{d\vec{r}}{dt} \right| \left| \frac{dt}{ds} \right| = \frac{ds}{dt} \cdot \frac{dt}{ds} = 1
$$

注③ "$\cdot$" 表示对参数 $s$ 求导，如  
$$
\vec{r}'(s) = \frac{d\vec{r}}{ds} = (\dot{x}(s), \dot{y}(s))
$$

注④ 记 $\vec{e}(s) = \vec{r}'(s)$，曲线 $\vec{r}(s)$ 在 $s = s_0$ 处的切线方程  
$$
\vec{r}(s) - \vec{r}(s_0) = \vec{e}(s_0) (s - s_0)
$$

取单位法向量 $\vec{n}(s)$，使得  
$\{\vec{r}'(s), \vec{e}(s), \vec{n}(s)\}$ 为右手正交标架

## Figure & Layout Description
图像为方格纸背景的手写数学笔记，整体布局分为三个垂直区域：左侧主文本区、右侧辅助图示区、底部补充图示区。左侧占据约70%宽度，从上至下依次排列：分割定义与极限公式推导（含多行积分表达式）、弧长函数定义、四条带编号的注释。右侧上部有手绘曲线示意图，曲线从左下向右上延伸，标注离散点 $\vec{r}(t_0)$, $\vec{r}(t_1)$, ..., $\vec{r}(t_n)$ 及相邻点连线，曲线为黑色实线，标注文字为黑色手写体。底部中央有第二个曲线示意图，显示曲线局部切线，标注"切向量"（沿切线方向）和"法向量"（垂直切线），箭头用黑色细线绘制。所有文字均为黑色墨水手写，字体工整但略带连笔，公式符号清晰可辨。方格纸网格线为浅灰色，形成1cm×1cm的正方形背景。层级上，主公式推导位于中上部，注释部分在中下部，两个图示分别嵌入在公式推导右侧和底部空白处，形成图文穿插结构。

<CTX>
{
   "topic": "弧长参数化与自然标架的构建",
   "keywords": ["正则曲线", "弧长参数", "单位切向量", "自然标架", "右手正交标架"],
   "summary": "完成弧长参数化的严格推导，证明切向量为单位向量，并建立基于弧长参数的右手正交自然标架体系",
   "pending_concepts": ["不同参数化对曲线性质的影响机制", "法向量的唯一确定方法"]
}
</CTX>