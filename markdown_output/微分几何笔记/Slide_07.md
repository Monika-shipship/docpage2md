# Slide 7

## 定理 2.1  
$\Gamma$ 是合同变换 $\Leftrightarrow \exists \, T \in O(3)$ 及 $P \in \mathbb{R}^3$  
s.t. $\Gamma(x) = xT + P$, $x = (x_1, x_2, x_3) \in E^3$

### 充分性："$\Leftarrow$"（给定 $T, P$）  
$\forall \, x, y \in E^3$,  
$$
\Gamma(x) = xT + P, \quad \Gamma(y) = yT + P
$$
$$
d(\Gamma(x), \Gamma(y)) \stackrel{?}{=} d(x, y)
$$
$$
d(\Gamma(x), \Gamma(y)) = |\Gamma(x) - \Gamma(y)| = |xT - yT|
$$
$$
= |(x - y)T| = \sqrt{\langle (x - y)T, (x - y)T \rangle} = \sqrt{(x - y)T T^\top (x - y)^\top}
$$
$$
= \sqrt{(x - y)(x - y)^\top} = d(x, y)
$$

### 必要性："$\Rightarrow$"  
$\Gamma(0) = 0'$ （不保原点）  
$\Gamma(0) + \overrightarrow{00'} = 0$ ✓  
（若 $\Gamma$ 合同，则 $\Gamma + P$ 是合同，平移）

---

## Figure & Layout Description  
- **背景**：浅米色方格纸（网格线为浅灰色，间距均匀）  
- **文字与公式**：黑色手写体，字迹工整但略有倾斜，整体呈纵向排列  
- **层级结构**：  
  1. 顶部为定理标题"定理 2.1"，使用较大字号  
  2. 核心条件以逻辑符号"$\Leftrightarrow$"分隔，右侧标注存在性条件  
  3. "充分性"与"必要性"作为二级标题，分别用引号标注方向"$\Leftarrow$"和"$\Rightarrow$"  
  4. 公式推导部分逐行展开，关键等式（如距离定义、向量运算）使用多行对齐  
  5. 底部有手写注释"平移"及括号说明"若 $\Gamma$ 合同，则 $\Gamma + P$ 是合同"  
- **特殊符号**：  
  - 正交群符号"$O(3)$"与向量空间"$\mathbb{R}^3$"清晰可辨  
  - 距离符号"$d(\cdot, \cdot)$"、向量转置"$T^\top$"、内积"$\langle \cdot, \cdot \rangle$"均规范书写  
  - 推导中出现向量差$(x - y)$及其转置$(x - y)^\top$的矩阵运算  

---

<CTX>
{
   "topic": "合同变换的代数表示与等价性证明",
   "keywords": ["合同变换", "正交矩阵", "平移向量", "距离保持", "O(3)", "代数表示", "充分必要条件"],
   "summary": "通过正交矩阵和平移向量的组合严格证明合同变换的代数表示，建立几何变换与矩阵群的对应关系",
   "pending_concepts": ["平移向量P在合同变换中的几何意义", "合同变换的定向保持/反转性质", "O(3)中行列式为±1的分类依据"]
}
</CTX>