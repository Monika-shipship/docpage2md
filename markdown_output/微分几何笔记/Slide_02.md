# Slide 2

## 2. 坐标和坐标变换

### What's 坐标

在 $E^3$ 中，取一原点，取三个向量 $\vec{v_1}, \vec{v_2}, \vec{v_3}$  
若 $\vec{v_1}, \vec{v_2}, \vec{v_3}$ 线性无关，称 $\{O; \vec{v_1}, \vec{v_2}, \vec{v_3}\}$ 为标架  

若 $\vec{v_1}, \vec{v_2}, \vec{v_3}$ 为相互正交的单位向量，称 $\{O; \vec{v_1}, \vec{v_2}, \vec{v_3}\}$ 为  
单位正交标架（么正标架）  

设 $\{O; \vec{e_1}, \vec{e_2}, \vec{e_3}\}$ 为正交标架，$\langle \vec{e_i}, \vec{e_j} \rangle = \delta_{ij} = \begin{cases} 0 & i \neq j \\ 1 & i = j \end{cases}$  
$\forall \vec{a} \in E^3$，$\vec{a} = a_i \vec{e_i}$ 称 $a_i$ 为 $\vec{a}$ 向量之坐标  

点 $\forall P \in E^3$，$\overrightarrow{OP} = x_i \vec{e_i}$ 称 $x_i$ 为 $P$ 的坐标  

注：坐标和标架有关，不同标架坐标不同  
$E^3$ 一一对应 $\mathbb{R}^3$ 因同构所以同一空间  
$E^3 \cong \mathbb{R}^3$  

$\forall P \in E^3$，$\sigma: \overrightarrow{OP} = \sum x_i \vec{e_i} \to (x_1, x_2, x_3) \in \mathbb{R}^3$

## Figure & Layout Description
图片为方格纸背景的手写笔记，整体布局为纵向排列。标题"2. 坐标和坐标变换"用橙色手写体书写，位于页面顶部，字体较大且字迹舒展；副标题"What's 坐标"同样用橙色书写，位置略低于主标题。正文内容以黑色手写体呈现，分为多个自然段落。第一段"在 $E^3$ 中..."起始处有明显缩进，后续段落保持对齐。数学符号如向量符号$\vec{v}$、内积$\langle \cdot, \cdot \rangle$、克罗内克δ$\delta_{ij}$等均用标准手写格式呈现，下标清晰可辨。公式部分采用自然书写顺序，无特殊排版。页面底部有"注："引导的说明性文字，末尾包含同构符号$E^3 \cong \mathbb{R}^3$和映射定义。整体字迹工整，关键术语如"标架"、"单位正交标架"等有明显强调，部分文字下方有手写横线标注。

<CTX>
{
   "topic": "坐标与坐标变换",
   "keywords": ["标架", "单位正交标架", "坐标定义", "向量坐标", "空间同构"],
   "summary": "定义了E³空间中的标架概念，阐明坐标与标架的依赖关系，并建立E³与R³的同构映射",
   "pending_concepts": ["坐标变换的具体实现方法", "不同标架间的转换关系"]
}
</CTX>