# Slide 44

## 3.2 曲面的第一基本形式

参数方程：
$$\vec{r} = \vec{r}(u, v)$$

切向量：
$$\vec{v} = \lambda \vec{r}_u + \mu \vec{r}_v$$

内积计算：
$$\langle \vec{v}, \vec{v} \rangle = \lambda^2 \vec{r}_u^2 + 2\lambda\mu \vec{r}_u \cdot \vec{r}_v + \mu^2 \vec{r}_v^2 = \lambda^2 E + 2\lambda\mu F + \mu^2 G$$

曲面上的曲线 $\vec{\gamma}(u(t), v(t))$，其中：
$$E = \vec{r}_u^2, \quad F = \langle \vec{r}_u, \vec{r}_v \rangle, \quad G = \vec{r}_v^2$$

切向量：
$$\frac{d\vec{\gamma}(t)}{dt} = \vec{r}_u u'(t) + \vec{r}_v v'(t)$$

弧长元素：
$$ds^2 = E \, du \, du + 2F \, du \, dv + G \, dv \, dv$$

第一基本形式：
$$\mathrm{I} = \begin{bmatrix} du & dv \end{bmatrix} \begin{bmatrix} E & F \\ F & G \end{bmatrix} \begin{bmatrix} du \\ dv \end{bmatrix}$$

## Figure & Layout Description

图片为方格纸背景的笔记页面，整体布局为纵向排列的手写数学推导。背景为浅黄色方格纸，网格线为浅灰色，每格约1cm×1cm。文字与公式以黑色墨水书写，笔迹清晰，字迹工整。内容分为五个逻辑区块：

1. **标题区**：左上角书写"3.2 曲面的第一基本形式"，字体稍大，加粗感明显。
2. **参数方程与切向量**：标题下方依次列出参数方程 $\vec{r} = \vec{r}(u, v)$ 和切向量表达式 $\vec{v} = \lambda \vec{r}_u + \mu \vec{r}_v$，公式独立成行，符号 $\lambda, \mu$ 使用斜体。
3. **内积展开式**：切向量内积推导分两行书写，第一行展开为 $\lambda^2 \vec{r}_u^2 + 2\lambda\mu \vec{r}_u \cdot \vec{r}_v + \mu^2 \vec{r}_v^2$，第二行简化为 $\lambda^2 E + 2\lambda\mu F + \mu^2 G$，等号对齐。
4. **曲面度量系数定义**：标注"S上的曲线 $\vec{\gamma}(u(t), v(t))$"，右侧并列定义 $E = \vec{r}_u^2$、$F = \langle \vec{r}_u, \vec{r}_v \rangle$、$G = \vec{r}_v^2$，三者以逗号分隔。
5. **弧长与第一基本形式**：底部依次列出切向量导数、弧长元素公式 $ds^2$ 及第一基本形式的矩阵表达式，矩阵部分使用方括号明确分块结构。

所有公式中向量符号 $\vec{r}, \vec{v}, \vec{\gamma}$ 均带有箭头，内积使用 $\langle \cdot, \cdot \rangle$ 符号，微分符号 $du, dv$ 与系数间保留空格以增强可读性。

<CTX>
{
   "topic": "曲面的第一基本形式理论",
   "keywords": ["切平面", "法向量", "坐标切向量", "正则曲面", "右手正交标架", "第一基本形式", "EFG系数", "弧长元素"],
   "summary": "本页定义了曲面第一基本形式的数学表达，建立了参数化曲面的度量基础，引入EFG系数描述曲面局部几何性质",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的第二基本形式", "曲面的测地线理论", "曲面的黎曼度量"]
}
</CTX>