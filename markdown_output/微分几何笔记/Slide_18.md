# Slide 18

注：
1. 切向量、主法向量、副法向量所在直线称为切线、主法线、副法线
2. $\text{span}\{\vec{t}, \vec{n}\}$ 称密切平面
3. $\text{span}\{\vec{t}, \vec{b}\}$ 称从切平面
4. $\text{span}\{\vec{b}, \vec{n}\}$ 称法平面
5. $\{\vec{t}'(s), \vec{t}(s), \vec{n}(s), \vec{b}(s)\}$ 与自然标架定向相同

### $\mathbb{E}^3$ 中的 Frenet 标架

$$\vec{t}' = k(s) \vec{n}$$

$$\langle \vec{t}, \vec{t} \rangle = 1,\quad \langle \vec{t}', \vec{t} \rangle = 0$$
$$\langle \vec{n}, \vec{n} \rangle = 1,\quad \langle \vec{n}', \vec{n} \rangle = 0$$
$$\langle \vec{b}, \vec{b} \rangle = 1,\quad \langle \vec{b}', \vec{b} \rangle = 0$$
$$\langle \vec{n}, \vec{t} \rangle = 0,\quad \langle \vec{n}', \vec{t} \rangle + \langle \vec{n}, \vec{t}' \rangle = 0$$
$$\Rightarrow \langle \vec{n}', \vec{t} \rangle = -\langle \vec{n}, k(s)\vec{n} \rangle = -k(s)$$

设 $\tau = \langle \vec{n}', \vec{b} \rangle$

$\{\vec{t}(s);\ \vec{t}, \vec{n}, \vec{b}\}$

$$\vec{n}' = x\vec{t} + y\vec{n} + z\vec{b}$$
$$\langle \vec{n}', \vec{t} \rangle = -k(s) = x$$
$$\langle \vec{n}', \vec{n} \rangle = 0 = y$$
$$\langle \vec{n}', \vec{b} \rangle = \tau = z$$

于是 $\vec{n}' = -k(s)\vec{t} + \tau \vec{b}$

## Figure & Layout Description
图片为方格纸背景的手写笔记，整体分为上下两个逻辑区域。上半部分是带编号的5条注释说明，采用黑色墨水书写，其中第2条"密切平面"用蓝色墨水标注；第3、4条右侧有红色叉号标记，第2条右侧有红色勾号和箭头标记。下半部分是Frenet标架的数学推导，包含多行向量内积公式和坐标分解步骤。关键公式如$\vec{t}' = k(s) \vec{n}$和最终推导结果$\vec{n}' = -k(s)\vec{t} + \tau \vec{b}$占据主要视觉空间。推导过程中有手绘的向量关系图示（标注b、n、t的夹角关系），位于坐标分解公式的右侧。页面右上角可见红色笔迹的修改痕迹，包括对"密切平面"的强调标记和公式推导中的修正符号。整体文字布局紧密，公式与文字说明交替排列，重要结论通过等号对齐方式突出显示。

<CTX>
{
   "topic": "Frenet标架的数学表达与坐标分解",
   "keywords": ["Frenet标架", "曲率", "挠率", "向量内积", "坐标分解"],
   "summary": "推导主法向量导数的坐标表达式，引入挠率参数τ并建立其与Frenet标架的关联",
   "pending_concepts": ["挠率的几何意义与物理诠释", "Frenet-Serret公式的完整矩阵形式"]
}
</CTX>