# 微分几何笔记 汇总

> 生成时间: 2025-12-21 11:37:07

# Slide 1

无文本内容

## Figure & Layout Description
页面背景为米白色（#F9F7F3），覆盖由浅灰色细线（#E0E0E0）构成的均匀网格。网格由20列×30行的正方形单元格组成，每个单元格边长约1.5cm。水平与垂直线条粗细一致（0.5pt），形成规则的坐标系式布局。整个页面无任何文字、图形、图标或装饰性元素，无明显视觉焦点，无层级区分，呈现完全空白的网格化工作底图状态。

<CTX>
{
   "topic": "空白演示页",
   "keywords": [],
   "summary": "本页未包含任何教学内容，可能用于布局规划或占位",
   "pending_concepts": []
}
</CTX>

---

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

---

# Slide 3

## 坐标变化

取两组基 关系：$\vec{e_i'} = t_{ij} \vec{e_j}$

$\{O; \vec{e_1}, \vec{e_2}, \vec{e_3}\}$  
$O' = (a_1, a_2, a_3)$  
$P = (x_1, x_2, x_3)$

$\{O'; \vec{e_1'}, \vec{e_2'}, \vec{e_3'}\}$  
$P = (y_1, y_2, y_3)$

$$\overrightarrow{OP} = \overrightarrow{OO'} + \overrightarrow{O'P} \quad ①$$
$$\overrightarrow{OP} = x_j \vec{e_j} \quad \overrightarrow{OO'} = a_j \vec{e_j} \quad ②$$
$$\overrightarrow{O'P} = y_i \vec{e_i'} \quad ③$$
②③代入①  
$$x_j \vec{e_j} = a_j \vec{e_j} + y_i \vec{e_i'}$$
代入 $\vec{e_i'} = t_{ij} \vec{e_j}$  
$$x_j \vec{e_j} = a_j \vec{e_j} + y_i t_{ij} \vec{e_j}$$

## Figure & Layout Description

图像背景为浅黄色方格纸，所有内容以黑色手写体呈现。页面顶部中央是标题"坐标变化"，字体较大且清晰。标题下方分为三个主要区域：

1. 左上区域：列出两组基的定义，第一组基表示为$\{O; \vec{e_1}, \vec{e_2}, \vec{e_3}\}$，第二组基表示为$\{O'; \vec{e_1'}, \vec{e_2'}, \vec{e_3'}\}$，旁边分别标注了坐标原点$O'$和点$P$的坐标表示。

2. 中部区域：绘制了一个三维坐标变换示意图。左侧坐标系以点$O$为原点，坐标轴$\vec{e_1}$、$\vec{e_2}$、$\vec{e_3}$分别指向左下方、右方和上方；右侧坐标系以点$O'$为原点，坐标轴$\vec{e_1'}$、$\vec{e_2'}$、$\vec{e_3'}$分别指向右下方、右上方和上方。两个坐标系之间用蓝色线条连接，形成从$O$到$O'$再到$P$的向量路径。点$P$被标记在两个坐标系之间的空间中，有蓝色向量从$O$指向$P$。

3. 下部区域：列出了坐标变换的推导过程，包含三个编号公式①、②、③及后续推导步骤。公式之间有明确的逻辑关系标注，如"②③代入①"和"代入 $\vec{e_i'} = t_{ij} \vec{e_j}$"等。

整个页面布局清晰，数学符号使用标准手写体，向量符号用箭头表示，下标清晰可辨。坐标变换图示使用蓝色线条突出显示，与黑色文字形成对比，便于理解向量关系。

<CTX>
{
   "topic": "坐标与坐标变换",
   "keywords": ["坐标变换", "基变换", "坐标系转换", "变换矩阵", "向量表示"],
   "summary": "推导了不同坐标系（标架）之间的坐标变换公式，展示了如何通过基向量关系实现坐标转换",
   "pending_concepts": ["变换矩阵的性质", "正交变换的条件", "坐标变换的逆过程"]
}
</CTX>

---

# Slide 4

$x_j^i = a_j^i + t_i^j y_i$ ↓理：$e_i^j$线性无关

记 $T = (t_i^j)$ 矩阵

$\vec{e_i'} = t_i^j \vec{e_j}$ 过渡矩阵

$\langle \vec{e_i'}, \vec{e_j'} \rangle = \delta_{ij} = e_i' e_j'^T = t_i^k e_k \cdot t_j^l e_l^T = t_i^k t_j^l \delta_{kl}$

$= t_i^k t_j^k = t_i^k (T^T)_k^j = (TT^T)_{ij} = \delta_{ij}$

$T$ 为正交矩阵

注：①定向：在 $E^3$ 中给定了一个正交标架

②在正交标架下的过渡矩阵 $T$ 是正交矩阵，且 $\det(T)=1$，两个正交标架定向相同；$\det(T)=-1$，两个正交标架定向相同

例 $\{O; e_1, e_2, e_3\}$ 和 $\{O; e_2, e_3, e_1\}$

$e_1' = 0 e_2 + 0 e_3 + 1 e_1$

$e_2' = 1 e_2 + 0 e_3 + 0 e_1$

$e_3' = 0 e_2 + 1 e_3 + 0 e_1$

$$
\begin{vmatrix}
0 & 0 & 1 \\
1 & 0 & 0 \\
0 & 1 & 0
\end{vmatrix} = 1 \quad \text{定向相同}
$$

## Figure & Layout Description
图片背景为米黄色方格纸，网格线呈浅灰色，形成均匀的正方形网格。文字内容以黑色手写体呈现，字迹工整且笔画清晰。右上角"↓理：$e_i^j$线性无关"部分疑似用红色笔迹书写，与主体黑色文字形成对比。公式内容自上而下垂直排列，第一行公式$x_j^i = a_j^i + t_i^j y_i$右侧有红色箭头标注。中间区域包含多行矩阵推导公式，内积表达式$\langle \vec{e_i'}, \vec{e_j'} \rangle$及其展开推导占据核心位置，公式间通过等号自然衔接。"注："部分以带圈数字①②分点列出，位于推导公式下方。底部"例"部分展示两个三维标架的对应关系，过渡矩阵以行列式形式呈现，行列式数值计算结果标注在右侧。整体布局层次分明，推导逻辑由上至下递进，关键结论"T为正交矩阵"单独成行突出显示。

<CTX>
{
   "topic": "正交标架与定向",
   "keywords": ["坐标变换", "基变换", "正交矩阵", "定向", "行列式", "过渡矩阵"],
   "summary": "推导了正交标架间过渡矩阵的正交性条件，并阐明行列式符号与标架定向的关系",
   "pending_concepts": ["行列式符号与定向的几何解释", "正交变换的几何意义", "非正交标架下的坐标变换"]
}
</CTX>

---

# Slide 5

e.g.2 $\{0; e_1, e_2, e_3\}$ 和 $\{0'; -e_1, e_2, e_3\}$

$$
\begin{pmatrix} e_1' \\ e_2' \\ e_3' \end{pmatrix} = \begin{pmatrix} -1 & & \\ & 1 & \\ & & 1 \end{pmatrix} \begin{pmatrix} -e_1 \\ e_2 \\ e_3 \end{pmatrix}, \quad |A| = -1
$$

③ 定向相同是等价关系  
对称性 $A = \{0, e_1, e_2, e_3\}$, $B = \{0', e_1', e_2', e_3'\}$  
$A \sim B$ 时 $\begin{pmatrix} e_1 \\ e_2 \\ e_3 \end{pmatrix} = T \begin{pmatrix} e_1' \\ e_2' \\ e_3' \end{pmatrix}$  
$T^{-1}( \quad ) = ( \quad )$ [无法辨认]  
传递性  

④ $E^3$ 中正交标架按定向作等价划分  
有两种标架  
① 右手正交  
② 左手正交  

⑤ $\{0, \vec{i}, \vec{j}, \vec{k}\}$ 给定的标架称自然标架（右手标架）

## Figure & Layout Description
手写笔记形式的PPT页面，背景为浅米色方格纸（1cm×1cm网格）。所有内容用黑色墨水书写，字迹为中文手写体。页面顶部是"e.g.2"示例，包含两个标架集合表示和矩阵变换公式，其中矩阵用括号竖排表示，行列式值"|A|=-1"标注在等式右侧。中部以带圈数字"③"开头讨论定向等价关系，下分"对称性"和"传递性"两个子项，包含基向量坐标变换公式，部分矩阵元素因书写模糊无法辨认。下部以"④"和"⑤"编号列出定向分类和自然标架定义，其中"④"项使用分支箭头符号（"＜"形）连接两种标架类型。文字存在手写特征：向量符号用上箭头（如$\vec{i}$），标架集合用花括号，矩阵元素间留有明显空白间距，部分括号因书写连笔需结合上下文推断。

<CTX>
{
   "topic": "定向的等价关系与标架分类",
   "keywords": ["坐标变换", "基变换", "正交矩阵", "定向", "行列式", "过渡矩阵", "等价关系", "右手标架", "左手标架"],
   "summary": "阐明定向相同的等价关系性质，并建立E³空间中正交标架按定向的二分法分类体系",
   "pending_concepts": ["等价关系的传递性证明", "自然标架的唯一性条件", "定向几何意义的直观解释"]
}
</CTX>

---

# Slide 6

### 3. 合同变换

设 $\{ O; e_1, e_2, e_3 \}$ 为正交标架，$P, Q \in E^3$

$P = (x_1, x_2, x_3)$，$Q = (y_1, y_2, y_3)$

$d(P,Q) = \sqrt{\sum (x_i - y_i)^2} = |P - Q|$

$d(P,Q) = |\overrightarrow{PQ}| = \sqrt{\langle \overrightarrow{PQ}, \overrightarrow{PQ} \rangle}$

甚么是变换：$E^3$ 中点之间的一一对应  
即 $f: E^3 \to E^3$，$1$-$1$ 映射

合同变换：保持距离的变换，即 $\forall P, Q \in E^3$  
$d(fP, fQ) = d(P, Q)$

合同变换的代数表示（刻化）  
$O(3) = \{ T_{3 \times 3} \mid TT^T = I \}$

## Figure & Layout Description

图片背景为浅黄色方格纸，网格线为浅灰色细线。所有内容以黑色手写体书写，字迹工整且具有明显的手写特征。页面顶部居中位置书写标题"3. 合同变换"，字体略大于正文。正文内容垂直排列：

1. 第一行定义部分：左侧书写"设 $\{ O; e_1, e_2, e_3 \}$ 为正交标架"，右侧对齐书写"$P, Q \in E^3$"
2. 第二行坐标定义：左侧"$P = (x_1, x_2, x_3)$"，右侧"$Q = (y_1, y_2, y_3)$"
3. 距离公式部分：包含两个等价表达式，右侧有手绘的点P到点Q的箭头示意图（P在下，Q在上，带箭头的斜线）
4. 变换定义部分：使用中文解释"甚么是变换"，并给出映射表示
5. 合同变换定义部分：明确写出保持距离的数学条件
6. 代数表示部分：位于页面底部，包含正交群$O(3)$的集合表示

所有公式中的求和符号$\sum$、向量符号$\overrightarrow{PQ}$、内积符号$\langle \cdot, \cdot \rangle$均以标准手写体呈现。页面右侧有简略的几何示意图，用箭头表示从P到Q的向量关系。

<CTX>
{
   "topic": "合同变换的定义与代数表示",
   "keywords": ["合同变换", "正交标架", "距离保持", "正交群", "O(3)", "代数表示", "一一对应"],
   "summary": "定义合同变换为保持欧氏距离的点集双射，并建立其与正交矩阵群O(3)的代数对应关系",
   "pending_concepts": ["正交群O(3)的行列式性质", "合同变换与定向的关系", "合同变换的几何直观解释"]
}
</CTX>

---

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

---

# Slide 8

$$
\forall d(\gamma(x)+p, \gamma(y)+p) = |\gamma(x) - \gamma(y)| = d(x,y)
$$
设为 $\gamma'(0) = 0$ 得原

只要找到 $\gamma'(x) = xT$

加 $t\ \omega'$ $\gamma'(x) + \omega' = \gamma(x) = xT + \omega'$ $\downarrow_p$

所以绕要设不妨设

$\gamma$ 保持内积 $\Rightarrow T \in O(3)$

why

$\forall x,y \in E^3$

$$
\langle \gamma(x), \gamma(y) \rangle = \langle xT, yT \rangle = xT T^T y^T = \langle x, y \rangle = xy^T \quad \xrightarrow{} \quad x(TT^T - I)y^T = 0
$$
$$
TT^T = I
$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，黑色墨水书写。内容按垂直顺序排列：顶部是距离保持性的等式（含全称量词和绝对值符号）；中间部分包含中文注释"设为γ'(0)=0得原"和线性变换表达式"γ'(x)=xT"；下方有带箭头标注的平移项推导（含"加t ω'"和向下箭头标注"↓p"）；再往下是"所以绕要设不妨设"的结论性文字；底部区域展示内积保持性的详细推导，包含向量空间符号$E^3$、内积尖括号表示、矩阵转置符号$T^T$，以及最终正交条件$TT^T=I$。公式与文字交替出现，关键推导步骤用箭头符号连接，部分等式右侧有手写注释。整体布局为纵向线性结构，无颜色区分，仅通过手写字体大小和间距体现层次。

<CTX>
{
   "topic": "合同变换的正交矩阵表示与内积保持性",
   "keywords": ["合同变换", "正交矩阵", "平移向量", "距离保持", "O(3)", "内积保持", "矩阵转置"],
   "summary": "通过内积保持性严格证明合同变换的线性部分必须属于正交群O(3)，建立几何变换与矩阵群的代数对应关系",
   "pending_concepts": ["平移向量P在合同变换中的几何意义", "合同变换的定向保持/反转性质", "O(3)中行列式为±1的分类依据"]
}
</CTX>

---

# Slide 9

合同变换的几何意义：平移，旋转，镜面反射的复合

$T(x) = xT + P$

$\det(T) = 1$ 平移+旋转 刚体运动  
$\det(T) = -1$ 一定包含镜面的 反向刚体运动

定义一个集合  
$\{ T: T \text{是合同变换} \}$ + 定义运算满足四定律

得群 Group，称作合同变换群

$T_1(x) = xT_1 + P_1$  
$T_2(x) = xT_2 + P_2$

$T_1 \circ T_2 = xT_2 T_1 + P_1$  
$\quad = (xT_2 + P_2)T_1 + P_1$  
$\quad = xT_2 T_1 + P_2 T_1 + P_1$

单位元 $I(x) = x = xI + 0$

## Figure & Layout Description
页面为浅米色方格纸背景，黑色手写体文字。标题"合同变换的几何意义：平移，旋转，镜面反射的复合"位于页面顶部居中位置，采用较大字号书写。下方内容按逻辑顺序垂直排列：第一行是变换公式$T(x) = xT + P$；第二、三行分别列出行列式条件$\det(T) = 1$和$\det(T) = -1$及其几何解释；第四行开始定义集合$\{ T: T \text{是合同变换} \}$并说明运算满足四定律；第五行说明构成群结构；随后列出$T_1$和$T_2$的定义式；最后是复合运算的三步推导过程和单位元定义。文字书写紧凑，公式与中文说明穿插排列，推导过程采用缩进对齐方式呈现，关键符号（如$T_1$、$P_1$）使用下标清晰标注。页面整体无彩色元素，仅包含黑色墨迹和浅灰色网格线，网格线为正方形，边长约5mm。

<CTX>
{
   "topic": "合同变换的几何意义与群结构",
   "keywords": ["合同变换", "刚体运动", "反向刚体运动", "行列式符号", "合同变换群", "复合运算"],
   "summary": "阐述合同变换的几何意义（平移/旋转/镜面反射复合），通过行列式符号区分定向保持与反转的刚体运动，并证明合同变换在复合运算下构成群结构",
   "pending_concepts": ["平移向量P在合同变换中的几何意义", "合同变换群的子群结构（如SO(3)）", "反向刚体运动的具体几何构造"]
}
</CTX>

---

# Slide 10

### 4. 正交标架与合同变换群

设 $\{X; e_1, e_2, e_3\}$ 是正交标架  
$X$ 原点，$e_1, e_2, e_3$ 以 $X$ 为起点的正交单位向量  

$F$：坐标标架的全体  

$F$ 和合同变换群一一对应  

## 第二章 曲线的局部理论

### § 2.1 曲线的概念

#### 1. 曲线的定义

- **平面曲线 ($E^2$)**  
  $\vec{r}: (a,b) \to E^2$  
  $t \to (x(t), y(t))$  
  即 $\vec{r}(t) = (x(t), y(t)) = x(t)\vec{i} + y(t)\vec{j}$  
  $\{\vec{i}, \vec{j}\}$ 自然标架  

- **空间曲线 ($E^3$)**  
  $\vec{r}: (a,b,c) \to E^3$  
  $t \to (x(t), y(t), z(t))$  
  即 $\vec{r}(t) = (x(t), y(t), z(t))$  

## Figure & Layout Description

图片为手写数学笔记，背景为浅色方格纸，文字以黑色墨水书写。整体布局分为上下两部分：

1. **上半部分**：  
   - 标题“4. 正交标架与合同变换群”位于顶部，手写字体较大且笔画较重。  
   - 下方分三行书写定义内容：  
     - 第一行：“设 $\{X; e_1, e_2, e_3\}$ 是正交标架”中“设”字上方有手写批注“原点”  
     - 第二行：“$X$ 原点，$e_1, e_2, e_3$ 以 $X$ 为起点的正交单位向量”中“原点”二字书写略倾斜  
     - 第三行：“$F$：坐标标架的全体”及“$F$ 和合同变换群一一对应”中“F”字母较大且带下划线  

2. **下半部分**：  
   - 标题“第二章 曲线的局部理论”位于中间偏左，手写字体加粗且“局部”二字有连笔  
   - 右侧附有手绘曲线示意图：  
     - 一条光滑曲线从左下向右上延伸，标注参数范围 $t \in (a,b)$  
     - 曲线上一点 $P$ 用实心点标记，坐标标注为 $(x(t), y(t))$  
     - 从原点 $O$ 指向 $P$ 的向量 $\vec{r}(t)$ 用带箭头线段表示，切向量 $\vec{r}'(t)$ 以短箭头标注在曲线切线方向  
   - 左侧分点书写“§ 2.1 曲线的概念”及“1. 曲线的定义”，包含平面/空间曲线的参数方程定义  
   - 公式中“自然标架”旁手写标注 $\{\vec{i}, \vec{j}\}$，其中“自然”二字存在连笔  

3. **视觉细节**：  
   - 所有向量符号（$\vec{r}$, $\vec{i}$, $\vec{j}$）均以手写箭头表示，箭头长度约2mm  
   - 曲线图中 $O$ 为坐标原点，$P$ 为曲线上动点，切向量 $\vec{r}'(t)$ 与曲线相切角度约30度  
   - 纸张网格线为浅灰色正方形（约5mm×5mm），部分手写内容压在网格线上但不影响识别  
   - 空间曲线定义中“$(a,b,c)$”的逗号存在连笔，疑似应为参数区间 $(a,b)$ 但按原样记录

<CTX>
{
   "topic": "正交标架与合同变换群的对应关系及曲线参数化基础",
   "keywords": ["正交标架", "坐标标架全体", "合同变换群对应", "参数曲线", "自然标架"],
   "summary": "建立正交标架集合与合同变换群的一一对应关系，并引入平面/空间曲线的参数化定义体系",
   "pending_concepts": ["正交标架在合同变换下的具体作用机制", "自然标架与正交标架的关联性", "参数曲线中t的几何意义"]
}
</CTX>

---

# Slide 11

正则曲线 $\gamma: (a,b) \to E^2(E^3)$ 满足  
① 曲线光滑 $x(t), y(t), z(t) \in C^\infty$  $\forall$ 不光滑，曲线无角点  
② $\left| \frac{d\gamma}{dt} \right| > 0$  排除常值向量，不能停 $|\vec{v}| > 0$

例题：  
e.g.1 $y = f(x) \in C^\infty$  
$\vec{r}(t) = (t, f(t)) \mid_{x=t} \in C^\infty$  
$\left| \frac{d\vec{r}}{dt} \right| = \sqrt{1 + [f'(t)]^2} > 0$  
正则  

e.g.2 $F(x,y) \in C^\infty$，曲线 $C = \{ (x,y) \in E^2 \mid F(x,y) = 0 \}$  
$F$ 光滑 $C$ 光滑  
$\left| \frac{d\vec{r}}{dt} \right| = \sqrt{[F_x]^2 + [F_y]^2} > 0$  

e.g.3 $\vec{r}(t) = (a\cos t, a\sin t) \quad t \in [0,4\pi)$  
$\vec{r}(t) = (a\cos 2t, a\sin t) \quad t \in [0,4\pi]$  

一样曲线？  
| 映射 | 定义域 | 对应法则 | 值域 |
|------|--------|----------|------|
|      | √      | ×        | 2圈 4圈 × |

§2.2 平面曲线  
考虑平面正则曲线 $\vec{r}(t) = (x(t), y(t)) \quad t \in (a,b)$  
$\vec{r}'(t) = (x'(t), y'(t)) \neq \vec{0}$ 称为曲线的切向量（速度向量）  
指向 $t$ 增大方向，$|\vec{r}'(t)| > 0$  
曲线的弧长，曲线 $\vec{r}(t)$ 从 $t=c$ 到 $t=d$ 的弧长记为 $S$  
则 $S = \int_c^d |\vec{r}'(t)| dt$

## Figure & Layout Description
手写笔记形式的PPT页面，背景为浅绿色方格纸（1cm×1cm网格），黑色墨水书写。页面顶部为"正则曲线"定义，包含两个带圈序号的条件：①描述曲线光滑性（$C^\infty$类），右侧有"∀不光滑，曲线无角点"的补充说明；②描述导数模长条件，右侧有"排除常值向量，不能停"的注释。中部"例题："标题下分三个例子：e.g.1展示函数图像参数化，e.g.2展示隐式曲线定义，e.g.3展示圆周的不同参数化形式。"一样曲线？"部分用表格形式对比映射特性，表格中"定义域"列标有√，"对应法则"列标有×，"值域"列标注"2圈 4圈 ×"。底部"§2.2 平面曲线"章节包含切向量定义和弧长积分公式。所有数学符号均用斜体书写，关键条件用下划线或竖线标注，公式与文字混排紧密，无明显留白。

<CTX>
{
   "topic": "正则曲线的严格定义与参数化方法",
   "keywords": ["正则曲线", "参数曲线", "切向量", "弧长计算", "隐式曲线"],
   "summary": "建立正则曲线的数学定义体系，通过三类典型例题说明判定条件，并推导平面曲线的切向量与弧长积分公式",
   "pending_concepts": ["弧长参数化的具体实现方法", "切向量与自然标架的几何关联", "不同参数化对曲线性质的影响机制"]
}
</CTX>

---

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

---

# Slide 13

e.g. $\gamma(t) = (a \cos t, a \sin t)$  
$\vec{v} = \gamma'(t) = (-a \sin t, a \cos t)$  
$\vec{t} = \frac{\vec{v}}{|\vec{v}|} = (-\sin t, \cos t)$  
$\vec{n} = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \vec{t} = (-\cos t, -\sin t)$  
$S = \int_0^t |\vec{v}| dt = a t$  
$\vec{t} = \left(-\sin \frac{S}{a}, \cos \frac{S}{a}\right)$  
$\vec{n} = \left(-\cos \frac{S}{a}, -\sin \frac{S}{a}\right)$  
$\vec{t}'(s) = \frac{1}{a} \vec{n}(s)$  
$\vec{n}'(s) = -\frac{1}{a} \vec{t}(s)$  

$\{ \vec{t}(s), \vec{b}(s), \vec{n}(s) \}$ 称 Frenet 标架  

$$
\begin{cases} 
\langle \vec{t}, \vec{t} \rangle = 1 \implies \langle \vec{t}', \vec{t} \rangle = 0 \implies \vec{t}' \parallel \vec{n},\ \vec{t}' = K \vec{n} \\
\langle \vec{n}, \vec{n} \rangle = 1 \implies \langle \vec{n}', \vec{n} \rangle = 0 \implies \vec{n}' \parallel \vec{t},\ \vec{n}' = g \vec{t} \\
\langle \vec{t}, \vec{n} \rangle = 0 \implies \langle \vec{t}', \vec{n} \rangle + \langle \vec{t}, \vec{n}' \rangle = 0 \implies K + g = 0 \implies \vec{n}' = -K \vec{t}
\end{cases}
$$

则 $\vec{t}' = K(s) \vec{n} \quad K(s) = \langle \vec{t}', \vec{n} \rangle$  
$\vec{n}' = -K(s) \vec{t}$  

$$
\frac{d}{ds} \begin{bmatrix} \vec{t} \\ \vec{n} \end{bmatrix} = \begin{bmatrix} 0 & K(s) \\ -K(s) & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \end{bmatrix}
$$
反映了曲线上每一点的弯曲程度  

由具体例，$a$为半径，  
$\vec{t}'(s) = \frac{1}{a} \vec{n}(s)$  
$\vec{n}'(s) = -\frac{1}{a} \vec{t}(s)$  
则 $K(s)$ 称为曲线的曲率  

## Figure & Layout Description
页面为方格纸背景的手写数学推导笔记。内容分为四个纵向区域：
1. 左上区域：从"e.g."开始的参数化曲线推导，包含6行公式，使用黑色墨水书写，矩阵用方括号表示
2. 中间区域：包含积分计算、参数替换公式，以及Frenet标架的定义文字
3. 左下区域：手绘的平面曲线示意图，标注了$\gamma(s)$（曲线上一点）、$\vec{t}(s)$（切向量，沿曲线切线方向）、$\vec{n}(s)$（法向量，指向曲线凹侧）三个向量
4. 右下区域：蓝色高亮的Frenet-Serret公式矩阵和"曲线的曲率"定义文字，蓝色区域覆盖2行内容，右侧有手写注释"反映了曲线上每一点的弯曲程度"

整体布局为从上至下的逻辑推导流，公式与图形穿插排列。关键公式（Frenet-Serret方程和曲率定义）用蓝色荧光笔标记，形成视觉焦点。所有向量符号均用箭头符号$\vec{}$表示，矩阵使用标准方括号格式。

<CTX>
{
   "topic": "Frenet-Serret公式与曲线曲率的定义",
   "keywords": ["Frenet标架", "曲率", "自然参数化", "切向量", "法向量", "Frenet-Serret公式"],
   "summary": "建立基于弧长参数的Frenet标架体系，推导出描述曲线弯曲特性的曲率公式，并通过矩阵形式的Frenet-Serret方程量化曲线几何性质",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的物理意义与数学表达"]
}
</CTX>

---

# Slide 14

## 曲率的几何意义

把 $\vec{\gamma}(s)$ 在 $s = s_0$ 处 Taylor 展开
$$
\vec{\gamma}(s) = \vec{\gamma}(s_0) + \dot{\vec{\gamma}}(s_0)(s - s_0) + \frac{1}{2}\ddot{\vec{\gamma}}(s_0)(s - s_0)^2 + \cdots
$$
$$
= \vec{\gamma}(s_0) + \vec{t}(s_0)(s - s_0) + \frac{1}{2}k(s_0)\vec{n}(s_0)(s - s_0)^2 + \cdots
$$

$k(s_0)$ 越大，越弯曲

Gauss 映射 $g: r \to S^1$  
$s \to \vec{n}(s)$  
$g(s) = \vec{n}(s)$，且有 $|g'(s)| = |\dot{\vec{n}}(s)|$，速度 $= |-k(s)\vec{t}(s)| = |k(s)|$

$\vec{n}(s)$ 的转动速率  
$$
|\dot{\vec{n}}(s)| = |-k(s)\vec{t}(s)| = |k(s)|
$$
$$
\dot{\vec{n}}(s) = -k(s)\vec{t}(s)
$$
$$
\Delta \vec{n} = -k(s)\vec{t}(s)\Delta s
$$
- $k(s) < 0$：$\vec{n}$ 指向弯曲相反方向（凹）  
- $k(s) > 0$：$\vec{n}$ 指向弯曲相同方向（凸）

## Figure & Layout Description

页面背景为浅黄色网格纸，整体为手写笔记风格。内容分为三个主要区域：

1. **上半区域**：包含标题"曲率的几何意义"及Taylor展开推导。第一行公式展示$\vec{\gamma}(s)$在$s=s_0$处的泰勒展开，第二行公式将其转换为Frenet标架形式。公式中$\vec{t}(s_0)$项用黑色书写，$\frac{1}{2}k(s_0)\vec{n}(s_0)(s-s_0)^2$项用红色标注。

2. **中部图形区**：
   - 左侧曲线图：黑色曲线表示$\vec{\gamma}(s)$，起点标注为$\vec{\gamma}(s_0)$，红色箭头表示从$\vec{\gamma}(s_0)$到$\vec{\gamma}(s)$的位移向量
   - 红色虚线箭头标注$\frac{1}{2}k(s_0)\vec{n}(s_0)(s-s_0)^2$，黑色实线箭头标注$\vec{t}(s_0)(s-s_0)$
   - 下方有独立曲线图：展示$\vec{n}(s)$和$\vec{t}(s)$在曲线上的方向变化，法向量$\vec{n}(s)$用短箭头表示，切向量$\vec{t}(s)$用长箭头表示
   - 右侧有单位圆示意图：圆内标注$\vec{n}(s)$，圆外标注$s'$，表示Gauss映射的几何关系

3. **下半文字区**：
   - "Gauss映射"部分用黑色手写体，包含映射定义$g: r \to S^1$及导数关系
   - 法向量转动率公式区：包含三个关键公式，其中$\dot{\vec{n}}(s) = -k(s)\vec{t}(s)$公式旁有手绘向量旋转示意图
   - 符号说明区：用箭头图示表示$k<0$（凹）和$k>0$（凸）时法向量指向，$k>0$处有顺时针旋转箭头标注

所有文字均为黑色手写体，关键公式和几何要素用红色强调。页面布局呈纵向递进结构，从理论推导到几何直观再到映射解释，形成完整逻辑链。

<CTX>
{
   "topic": "曲率的几何意义与Gauss映射",
   "keywords": ["Taylor展开", "曲率几何解释", "Gauss映射", "法向量转动率", "弯曲方向判定"],
   "summary": "通过Taylor展开揭示曲率与曲线偏离切线程度的定量关系，引入Gauss映射建立曲率与法向量转动速率的等价性，阐明曲率符号与弯曲方向的对应关系",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的几何意义与数学表达"]
}
</CTX>

---

# Slide 15

e.g. $\vec{r} = (\cos(s), \sin(s))$

e.g. $\vec{r} = (\cos(-s), \sin(-s))$

$\vec{t}(s) = \vec{r}'(s) = (\sin(-s), -\cos(-s))$

$\vec{n}(s) = \vec{t}'(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \vec{t}(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$

$\vec{t}'(s) = (-1) \vec{n} \quad k(s) = -1$

e.g. $\vec{r}(t) = (t, \sin t)$

$S(t) = \int_0^t |\vec{r}'(u)|  du = \int_0^t \sqrt{1 + \cos^2 u}  du$

$\frac{ds}{dt} = \sqrt{1 + \cos^2 u}$

$\vec{t}(s) = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds} = (1, \cos t) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{n}(s) = \vec{t}(s) \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = (-\cos t, 1) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{t}'(s) = \frac{d\vec{t}}{ds} = \frac{d\vec{t}}{dt} \frac{dt}{ds} = \left(-\frac{1}{2} \frac{2\cos t(-\sin t)}{(1 + \cos^2 t)^{3/2}}, \star \right) \frac{1}{\sqrt{1 + \cos^2 t}}$

$= \left( \frac{\cos t \sin t}{(1 + \cos^2 t)^{3/2}}, \star \right) \frac{1}{\sqrt{1 + \cos^2 t}}$

$\vec{t}' = k(s) \vec{n}$

$k(s) = \frac{-\sin t}{(1 + \cos^2 t)^{3/2}} \quad k = \frac{y''}{(1 + y'^2)^{3/2}}$

e.g. 一般参数方程的曲线 $\vec{r} = (x(t), y(t))$

$S(t) = \int_0^t \sqrt{(x'(t))^2 + (y'(t))^2}  dt$

$\frac{ds}{dt} = \sqrt{x'^2 + y'^2}$

$\vec{t} = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds} = (x'(t), y'(t)) \frac{1}{\sqrt{x'^2 + y'^2}}$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局分为三个主要区域。顶部区域左右并列两个几何示意图：左侧图显示一个以原点为中心的单位圆，坐标系中y轴正向标注蓝色向量$\vec{t}(s)$和$\vec{n}(s)$，右侧蓝色标注"$k(s) > 0$"；右侧图同样为单位圆，但向量方向相反，标注蓝色向量$\vec{t}(s)$和$\vec{n}(s)$，右侧蓝色标注"$k(s) < 0$"，其右侧附有一个小型坐标系示意图。中部区域包含圆曲线的向量计算公式，包括切向量、法向量和曲率关系式，其中矩阵$\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$被多次使用。底部区域分为两部分：上半部分是参数曲线$\vec{r}(t) = (t, \sin t)$的详细推导，包含弧长积分、切向量和法向量计算；下半部分是一般参数曲线的通用公式推导。文字主要为黑色手写体，关键标注（如曲率符号）使用蓝色墨水，所有公式和文字均写在方格坐标纸上，形成清晰的行列对齐结构。

<CTX>
{
   "topic": "曲率的计算实例与一般参数曲线的曲率公式",
   "keywords": ["弧长参数化", "曲率计算", "弯曲方向判定", "法向量旋转", "参数曲线曲率"],
   "summary": "通过圆和正弦曲线的具体示例演示曲率计算过程，建立曲率符号与曲线弯曲方向的对应关系，并推导出一般参数曲线的显式曲率公式",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的几何意义与数学表达"]
}
</CTX>

---

# Slide 16

$$
\vec{t} = \frac{d\vec{E}}{ds} = \frac{d\vec{E}}{dt} \frac{dt}{ds} = \left( \left( \frac{x'}{\sqrt{x'^2 + y'^2}} \right)', \left( \frac{y'}{\sqrt{x'^2 + y'^2}} \right)' \right) \frac{1}{\sqrt{x'^2 + y'^2}} = \left( \frac{x'' \sqrt{x'^2 + y'^2} - \frac{2x'x'' + 2y'y''}{2\sqrt{x'^2 + y'^2}} \cdot x'}{x'^2 + y'^2}, \star \right) \cdot \frac{dt}{ds}
$$

$$
\frac{dt}{ds} \left( \frac{x'' \sqrt{x'^2 + y'^2} - \frac{x'x'' + y'y''}{\sqrt{x'^2 + y'^2}} \cdot x'}{x'^2 + y'^2}, \star \right) = \left( \frac{x''}{\sqrt{x'^2 + y'^2}} - \frac{(x'x'' + y'y'')x'}{(x'^2 + y'^2)^{3/2}}, \star \right) \frac{dt}{ds}
$$

$$
= \frac{x''(x'^2 + y'^2) - x'^2 x'' - x'y'y''}{(x'^2 + y'^2)^{3/2}} \cdot \frac{dt}{ds}
$$

$$
= \frac{x'' y'^2 - x' y' y''}{(x'^2 + y'^2)^{3/2}} \cdot \frac{1}{\sqrt{x'^2 + y'^2}} \downarrow \frac{dt}{ds}
$$

$$
\vec{n} = \vec{t} \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = (-y'(t), x'(t)) \frac{1}{\sqrt{x'^2 + y'^2}}
$$

$$
\vec{t}' = k(s) \vec{n}
$$

$$
k(s) = \frac{x'' y'^2 - x' y' y''}{(x'^2 + y'^2)^{3/2}} \cdot \frac{1}{\sqrt{x'^2 + y'^2}} = \frac{x'y'' - x''y'}{(x'^2 + y'^2)^{3/2}}
$$

$$
= \frac{x'y'' - y'x''}{(x'^2 + y'^2)^{3/2}}
$$

$$
y = f(x) \quad k = \frac{f''}{(1 + f'^2)^{3/2}}
$$

极坐标函数 $\vec{r} = f(\theta) \vec{e}_r$

$$
\vec{r}(\theta) = (f \cos\theta, f \sin\theta)
$$

代入 $\frac{x'y'' - y'x''}{\sqrt{x'^2 + y'^2}}$ 即可

$$
a_n = \frac{v^2}{\rho} \quad \rho = \frac{v^3}{|\vec{a}_n \times \vec{v}|}
$$

## Figure & Layout Description

手写数学推导内容绘制在方格纸背景上，整体布局为纵向多行公式排列。顶部起始为单位切向量$\vec{t}$的推导过程，包含多步微分运算和分式化简。中间区域展示法向量$\vec{n}$的定义及曲率向量关系式$\vec{t}' = k(s)\vec{n}$。右下角有一个极坐标示意图，包含极点、极轴、角度标记$\theta$和径向向量$\vec{r}$，用黑色曲线表示极坐标曲线。公式中使用大量导数符号（$'$和$''$）、平方根和分式结构，部分推导步骤旁有对勾符号（✓）标记关键化简步骤。所有文字和符号均为黑色手写体，网格线为浅灰色，公式按逻辑流程自上而下排列，关键等式通过等号对齐形成视觉连贯性。

<CTX>
{
   "topic": "一般参数曲线曲率公式的严格推导与极坐标应用",
   "keywords": ["参数曲线曲率", "显式曲率公式", "法向量旋转矩阵", "极坐标曲率计算", "弯曲方向符号判定"],
   "summary": "完成从弧长参数化到一般参数曲线的曲率公式推导，建立曲率符号与坐标系旋转方向的对应关系，并给出极坐标形式的曲率计算方法",
   "pending_concepts": ["三维空间中副法向量的引入机制", "挠率的几何意义与数学表达"]
}
</CTX>

---

# Slide 17

## 2.3 $E^3$ 的曲线

在 $E^3$ 中，设 $\vec{r}(t) = (x(t), y(t), z(t))$，$t \in (a,b)$，正则曲线  
$$S(t) = \int_0^t |\vec{r}'(u)| \, du$$  
$$\frac{dS}{dt} = |\vec{r}'(t)| > 0,\ S \text{ 严格增}$$  
存在反函数 $t = t(s)$，则  
$$\vec{r}(s) = (x(s), y(s), z(s))$$  
$$\vec{t} = \dot{\vec{r}}(s)$$  

法向量：垂直于 $\vec{t}$ 的向量称为法向量  
所有法线构成了法平面  
$$\langle \vec{t}, \vec{t} \rangle = 1 \quad \text{求导} \quad \langle \dot{\vec{t}}, \vec{t} \rangle = 0 \quad \dot{\vec{t}} \perp \vec{t}$$  
$\Rightarrow \dot{\vec{t}}$ 是 $\vec{r}(s)$ 的一个法向量，但 $\dot{\vec{t}}$ 和 $\vec{n}$ 不一定平行！  

定义 **空间曲率**  
$$\kappa(s) = |\dot{\vec{t}}| = |\ddot{\vec{r}}| = \sqrt{\ddot{x}^2 + \ddot{y}^2 + \ddot{z}^2} \quad (\dot{\vec{t}} \neq 0)$$  
一定大于 0！  
$$\vec{n} = \frac{\dot{\vec{t}}}{|\dot{\vec{t}}|} = \frac{\dot{\vec{t}}}{\kappa} \quad \text{称主法向量}$$  

定义副法向量 $\vec{b} = \vec{t} \times \vec{n}$  

有标架 $\{\vec{r}(s);\ \vec{t}(s),\ \vec{n}(s),\ \vec{b}(s)\}$  
称空间曲线的 Frenet 标架，正交标架，活动标架  

## Figure & Layout Description

页面为浅黄色方格纸背景的手写笔记，整体布局为纵向排版。标题"2.3 $E^3$的曲线"位于页面顶部左侧，使用黑色手写字体。正文内容以黑色墨水书写，公式与文字混合排布，关键术语通过颜色区分：

1. **颜色标记**：
   - "空间曲率"四字用蓝色墨水书写
   - 主法向量公式 $\vec{n} = \frac{\dot{\vec{t}}}{|\dot{\vec{t}}|}$ 旁有红色箭头指向右侧
   - "主法向量"三字下方有波浪线标记

2. **图形元素**：
   - 页面右下角有手绘曲线示意图，包含：
     * 一段向上弯曲的黑色曲线
     * 曲线上标注点 $O$ 和 $\vec{r}(s)$ 矢量
     * 从 $O$ 点引出三个向量：切向量 $\vec{t}$、主法向量 $\vec{n}$、副法向量 $\vec{b}$
     * 向量用带箭头的线段表示，$\vec{n}$ 与 $\vec{t}$ 垂直，$\vec{b}$ 与前两者构成右手系

3. **文字层级**：
   - 标题为一级结构
   - 定义性语句（"定义空间曲率"等）使用加粗处理
   - 推导过程按逻辑顺序分行排列，关键步骤（如"求导"）用中文标注
   - 公式与文字混合排版，部分公式使用行间格式突出显示

4. **特殊标记**：
   - "但 $\dot{\vec{t}}$ 和 $\vec{n}$ 不一定平行！"后有手写感叹号
   - "不一定平行"四字旁有手绘叉号标记
   - 积分公式中的积分限和微分符号清晰可见

<CTX>
{
   "topic": "三维空间曲线的Frenet标架体系与曲率定义",
   "keywords": ["Frenet标架", "主法向量", "副法向量", "空间曲率", "活动标架"],
   "summary": "建立三维曲线的Frenet标架体系，明确定义切向量、主法向量和副法向量的几何关系，给出空间曲率的严格数学表达",
   "pending_concepts": ["挠率的几何意义与数学表达", "Frenet-Serret公式的完整推导"]
}
</CTX>

---

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

---

# Slide 19

$\vec{b} = ? \quad \vec{b} = \vec{t} \wedge \vec{n}$

$\dot{\vec{b}} = \dot{\vec{t}} \wedge \vec{n} + \vec{t} \wedge \dot{\vec{n}}$

$= k(s) \vec{n} \wedge \vec{n} + \vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$

$= \underset{0}{k(s)\vec{n}\wedge\vec{n}} + \underset{0 + \tau(-\vec{n})}{\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})}$

$\dot{\vec{b}} = -\tau \vec{n}$

$$
\begin{cases}
\dot{\vec{t}} = \qquad k(s) \vec{n} \\
\dot{\vec{n}} = -k(s) \vec{t} \qquad + \tau \vec{b} \\
\dot{\vec{b}} = \qquad -\tau \vec{n}
\end{cases}
$$

$$
\frac{d}{dt}\begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix} = \begin{bmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix}
$$

<span style="color:red">$\tau$称挠率</span>

下讲其几何意义

设空间曲线 $\vec{r}$ 的曲率 $k > 0$，则 $\vec{r}$ 落在某个平面上的充要条件是 $\tau = 0$。

证 "$\Rightarrow$" 设 $\pi$ 是空间中的一张平面，设 $\vec{a}$ 是垂直于 $\pi$ 的单位向量

$<\vec{r}(s) - \vec{r}(s_0), \vec{a}> = 0$

求导得 $<\vec{t}(s), \vec{a}> = 0$

再求导得 $<k(s)\vec{n}(s), \vec{a}> = 0$

因 $k(s) > 0$ 空间曲线

$<\vec{n}(s), \vec{a}> = 0$

$<\dot{\vec{n}}(s), \vec{a}> = 0$  $<-k(s)\vec{t}(s) + \tau \vec{b}, \vec{a}> = 0$

$\vec{a} \perp \vec{t}, \vec{a} \perp \vec{n}, \vec{b} = \vec{t} \wedge \vec{n} \Rightarrow \vec{b} \parallel \vec{a}$

$\vec{b}, \vec{a}$ 单位向量 $\Rightarrow \vec{b} = \pm \vec{a}$

而 $<\tau \vec{b}, \vec{a}> = 0$

$\tau = 0$ 才相符

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记。整体布局从上至下分为三个主要区域：

1. **顶部区域**：包含Frenet标架中副法向量导数的推导过程。首先提出问题"$\vec{b} = ?$"，接着给出$\vec{b} = \vec{t} \wedge \vec{n}$的定义。然后推导$\dot{\vec{b}}$，使用向量叉积法则展开为$\dot{\vec{t}} \wedge \vec{n} + \vec{t} \wedge \dot{\vec{n}}$。进一步代入Frenet公式得到$k(s)\vec{n}\wedge\vec{n}$和$\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$，其中$k(s)\vec{n}\wedge\vec{n}$下方标注"0"，$\vec{t} \wedge (-k(s)\vec{t} + \tau \vec{b})$下方标注"0 + τ(-n̅)"。最终得到$\dot{\vec{b}} = -\tau \vec{n}$。

2. **中部区域**：包含Frenet-Serret公式的完整表达。左侧用大括号包裹三个方程：$\dot{\vec{t}} = k(s)\vec{n}$、$\dot{\vec{n}} = -k(s)\vec{t} + \tau \vec{b}$、$\dot{\vec{b}} = -\tau \vec{n}$。下方以矩阵形式表示为$\frac{d}{dt}\begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix} = \begin{bmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{bmatrix} \begin{bmatrix} \vec{t} \\ \vec{n} \\ \vec{b} \end{bmatrix}$。

3. **底部区域**：包含红色手写文字"τ称挠率"，下方是"下讲其几何意义"的提示。接着是关于空间曲线平面性的定理："设空间曲线$\vec{r}$的曲率$k > 0$，则$\vec{r}$落在某个平面上的充要条件是$\tau = 0$"。随后是证明部分，从"证"⇒""开始，通过向量内积性质逐步推导，包含多个内积等式和逻辑推导步骤。

视觉特征：文字为黑色手写体，关键术语"τ称挠率"用红色标注。公式推导过程中有下划线和注释说明中间步骤（如"0"标注）。整体书写在方格纸上，文字排列较为紧凑但层次分明，公式与文字说明交替出现。

<CTX>
{
   "topic": "挠率的定义与几何意义：Frenet-Serret公式的完整表达及平面曲线判定条件",
   "keywords": ["挠率", "Frenet-Serret公式", "平面曲线", "向量内积", "曲率"],
   "summary": "完成Frenet标架的完整微分方程组，定义挠率参数并证明空间曲线为平面曲线的充要条件是挠率为零",
   "pending_concepts": ["挠率的物理直观解释", "非平面曲线的挠率变化规律", "Frenet标架在三维运动中的应用"]
}
</CTX>

---

# Slide 20

"⇐" $\tau=0 \Rightarrow \dot{\vec{b}}=0$, $\vec{b}$为常向量$\vec{C}$ ($\dot{\vec{b}}=-\tau\vec{n}$)  
$$
\frac{d}{ds} \langle \vec{r}'(s), \vec{b} \rangle = \langle \vec{r}''(s), \vec{b} \rangle = 0
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle = C
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle - C = 0
$$
$$
\langle \vec{r}'(s), \vec{b} \rangle - C \langle \vec{b}, \vec{b} \rangle = 0
$$
$$
\langle \vec{r}'(s) - C\vec{b}, \vec{b} \rangle = 0
$$
$$
\text{令 } \vec{r}'(s_0) = C\vec{b} \quad \Rightarrow \quad \langle \vec{r}'(s) - \vec{r}'(s_0), \vec{b} \rangle = 0
$$

几何意义：离开平面的程度  

e.g. 求 $\vec{r}(t) = (a\cos t,\, a\sin t,\, bt)$ 的曲率和挠率  
$$
s(t) = \int_0^t \sqrt{(a\sin t)^2 + (a\cos t)^2 + b^2}\, dt = \sqrt{a^2 + b^2}\, t \equiv ct
$$
$$
\text{令 } \frac{1}{c}s \quad \Rightarrow \quad \vec{r}(s) = \left(a\cos\frac{s}{c},\, a\sin\frac{s}{c},\, \frac{bs}{c}\right)
$$
$$
\vec{r}'(s) = \dot{\vec{r}}(s) = \left(-\frac{a}{c}\sin\frac{s}{c},\, \frac{a}{c}\cos\frac{s}{c},\, \frac{b}{c}\right)
$$
$$
\ddot{\vec{r}}(s) = \left(-\frac{a}{c^2}\cos\frac{s}{c},\, -\frac{a}{c^2}\sin\frac{s}{c},\, 0\right)
$$
$$
\vec{t} = \kappa\vec{n},\quad \kappa(s) = |\ddot{\vec{r}}(s)| = \frac{a}{c^2} = \frac{a}{a^2 + b^2}
$$
$$
\vec{n} = \frac{\ddot{\vec{r}}}{|\ddot{\vec{r}}|} = \left(-\cos\frac{s}{c},\, -\sin\frac{s}{c},\, 0\right)
$$
$$
\vec{b} = \vec{t} \times \vec{n} = \begin{vmatrix}
\vec{i} & \vec{j} & \vec{k} \\
-\frac{a}{c}\sin\frac{s}{c} & \frac{a}{c}\cos\frac{s}{c} & \frac{b}{c} \\
-\cos\frac{s}{c} & -\sin\frac{s}{c} & 0
\end{vmatrix} = \left(\frac{b}{c}\sin\frac{s}{c},\, \frac{b}{c}\cos\frac{s}{c},\, \frac{a}{c}\right)
$$
$$
\dot{\vec{b}} = -\tau\vec{n}
$$
$$
\tau = |\dot{\vec{b}}| = \frac{b}{c^2} = \frac{b}{a^2 + b^2}
$$
$$
\kappa(s) = \frac{a}{a^2 + b^2},\quad \tau(s) = \frac{b}{a^2 + b^2}
$$

## Figure & Layout Description
The slide displays handwritten mathematical content on a grid paper background with light gray grid lines forming square cells (approximately 5mm x 5mm). The text is written in black ink with varying stroke weights indicating hand-written emphasis. The layout is vertically divided into two main sections:

1. **Upper Section (60% of height)**: Contains theoretical derivation of torsion properties with logical implications ("⇐" symbol), vector equations using angle brackets for inner products, and step-by-step algebraic manipulations. The equations are aligned left with decreasing indentation for subordinate steps. The phrase "几何意义：离开平面的程度" is centered below the derivation.

2. **Lower Section (40% of height)**: Contains a concrete example starting with "e.g." followed by parametric equations of a helix. The example includes integral calculations, vector differentiations, and determinant expansions. The final results for curvature and torsion are prominently displayed in larger handwriting. At the very bottom, there is a simple 3D coordinate system sketch with labeled x, y, z axes and a helical curve drawn around the z-axis.

The handwriting shows consistent mathematical notation with vector arrows ($\vec{r}, \vec{b}$), derivatives ($\dot{\vec{b}}$), and proper use of Greek letters (τ for torsion, κ for curvature). The grid paper background provides structural alignment for the equations.

<CTX>
{
   "topic": "挠率的几何意义与螺旋线实例计算：通过具体曲线验证挠率与曲率的计算方法",
   "keywords": ["挠率", "Frenet-Serret公式", "平面曲线", "螺旋线", "曲率"],
   "summary": "通过螺旋线参数方程的具体计算，验证挠率与曲率的公式推导，明确挠率表征空间曲线离开平面程度的几何意义",
   "pending_concepts": ["挠率的物理直观解释", "非平面曲线的挠率变化规律", "Frenet标架在三维运动中的应用"]
}
</CTX>

---

# Slide 21

现研究 挠率正负号的意义

若曲线 $\vec{r}(s)$ 在 $s=0$ 处的 三阶 $\vec{r}$ 展开
$$\vec{r}(s) = \vec{r}(0) + \dot{\vec{r}}(0)s + \frac{1}{2}\ddot{\vec{r}}(0)s^2 + \frac{1}{6}\dddot{\vec{r}}(0)s^3 + O(s^3)$$

$\dot{\vec{r}}(0) = \vec{t}(0)$, $\ddot{\vec{r}}(0) = k(0)\vec{n}(0)$

$$\dddot{\vec{r}}(0) = k(0)\dot{\vec{n}}(0) + \dot{k}(0)\vec{n}(0)$$
$$= k(0)[-k(0)\vec{t}(0) + \tau(0)\vec{b}(0)] + \dot{k}(0)\vec{n}(0)$$
$$= -k^2(0)\vec{t}(0) + \dot{k}(0)\vec{n}(0) + k(0)\tau(0)\vec{b}(0)$$

$$\vec{r}(s) = \vec{r}(0) + \vec{t}(0)s + \frac{1}{2}k(0)\vec{n}(0)s^2$$
$$+ \frac{1}{6}k(0)\vec{n}(0)s^3 - \frac{1}{6}k^2(0)\vec{t}(0)s^3 + \frac{1}{6}k(0)\tau(0)\vec{b}(0)s^3$$
$$= \vec{r}(0) + \left(s - \frac{1}{6}k^2(0)s^3\right)\vec{t}(0) + \left(\frac{1}{2}k(0)s^2 + \frac{1}{6}\dot{k}(0)s^3\right)\vec{n}(0)$$
$$+ \frac{1}{6}k(0)\tau(0)s^3\vec{b}(0) + O(s^3)$$

取 Frenet 标架 $\{\vec{r}_0; \vec{t}(0), \vec{n}(0), \vec{b}(0)\}$ 为自然标架 $\{O; \vec{i}, \vec{j}, \vec{k}\}$

$$\vec{r}(s) = \left(s - \frac{1}{6}k^2(0)s^3, \frac{1}{2}k(0)s^2 + \frac{1}{6}\dot{k}(0)s^3, \frac{1}{6}k(0)\tau(0)s^3\right)$$

$$x(s) = s - \frac{1}{6}k^2(0)s^3 + O_x(s^3)$$
$$y(s) = \frac{1}{2}k(0)s^2 + \frac{1}{6}\dot{k}(0)s^3 + O_y(s^3)$$
$$z(s) = \frac{1}{6}k(0)\tau(0)s^3 + O_z(s^3)$$

现使 $s$ 足够小

## Figure & Layout Description

该页面为手写在方格纸上的数学推导内容，整体布局为上部文字推导，下部图形说明。

1. **背景与格式**：内容书写在浅黄色方格纸上，方格线为浅灰色，构成标准的坐标纸背景。文字和公式均为黑色手写体。

2. **文字与公式区域**：
   - 顶部是标题"现研究 挠率正负号的意义"，字体较大，位于页面上方。
   - 中部是详细的数学推导，包括曲线$\vec{r}(s)$在$s=0$处的三阶Taylor展开推导过程。
   - 推导包含多个步骤，每个步骤占一行或两行，公式排列整齐，有明显的逻辑层次。
   - 推导中使用了向量符号（如$\vec{r}$、$\vec{t}$、$\vec{n}$、$\vec{b}$）和微分符号（如$\dot{\vec{r}}$、$\ddot{\vec{r}}$、$\dddot{\vec{r}}$）。
   - 推导最后部分定义了$x(s)$、$y(s)$、$z(s)$的表达式。

3. **图形区域**：
   - 页面底部有三个坐标系示意图，从左到右排列。
   - 左侧图：显示三维坐标系，标注了$\vec{t}$（x轴）、$\vec{n}$（y轴）、$\vec{b}$（z轴），并标注"密切平面"。图中有一条曲线穿过原点，标注了$s>0$和$s<0$的部分，以及"曲线下从下到上穿过密切平面"的文字说明。
   - 中间图：显示二维坐标系，x轴为$\vec{t}$，z轴为$\vec{b}$，曲线从原点出发，标注了$\tau>0$和$\tau<0$的曲线部分。
   - 右侧图：显示二维坐标系，y轴为$\vec{n}$，z轴为$\vec{b}$，曲线从原点出发，标注了$s>0$和$s<0$的部分，以及$(\frac{1}{2}ks^2, \frac{1}{6}k\tau s^3)$的表达式。

4. **视觉层次**：
   - 文字推导部分占据页面上半部分约60%的区域
   - 图形部分占据页面下半部分约40%的区域
   - 整体排版清晰，推导步骤按逻辑顺序排列，图形与文字内容紧密相关
   - 手写笔迹工整，公式符号清晰可辨

<CTX>
{
   "topic": "挠率正负号的几何意义：通过三阶Taylor展开分析曲线局部形状",
   "keywords": ["挠率正负号", "Taylor展开", "Frenet标架", "密切平面", "曲线局部性质"],
   "summary": "通过曲线在s=0处的三阶Taylor展开，推导出挠率正负号如何影响曲线在密切平面两侧的分布，明确挠率正负表征曲线穿过密切平面的方向",
   "pending_concepts": ["挠率正负号在实际工程中的应用示例", "不同挠率值对应的典型曲线形状", "挠率与曲率共同作用下的三维曲线演化规律"]
}
</CTX>

---

# Slide 22

在 $E^3$ 中，求正则曲线的曲率和挠率

$$
S(t) = \int_0^t |\vec{r}'(u)| \, du
$$

$$
\frac{dS}{dt} = |\vec{r}'(u)| > 0
$$

$$
\vec{T}(s) = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds}
$$

$$
\vec{T}' = k \vec{n}, \quad k(s) = |\vec{T}'(s)|
$$

$$
\frac{d\vec{T}(s)}{ds} = \frac{d}{ds} \left( \frac{d\vec{r}}{dt} \frac{dt}{ds} \right) = \frac{d}{dt} \left( \frac{d\vec{r}}{dt} \frac{dt}{ds} \right) \frac{dt}{ds}
$$

$$
= \left( \frac{d^2\vec{r}}{dt^2} \frac{dt}{ds} + \frac{d\vec{r}}{dt} \frac{d}{dt} \left( \frac{dt}{ds} \right) \right) \frac{dt}{ds}
$$

$$
= \left( [无法辨认] + \frac{d\vec{r}}{dt} \frac{d}{ds} \left( \frac{dt}{ds} \right) \frac{ds}{dt} \right) \frac{dt}{ds}
$$

$$
= \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2t}{ds^2}
$$

$$
\vec{b} = \vec{t} \wedge \vec{n}, \quad \vec{n} = \frac{\vec{T}'}{|\vec{T}'|} = \frac{\vec{T}'}{k(s)}
$$

$$
\vec{b} = \vec{t} \wedge \frac{\vec{T}'}{k} = (\vec{t} \wedge \vec{T}') \frac{1}{k}
$$

$$
|\vec{b}| = |\vec{t} \wedge \vec{T}'| \frac{1}{k} \implies k = |\vec{t} \wedge \vec{T}'|
$$

$$
\vec{t} \wedge \vec{T}' = \frac{d\vec{r}}{dt} \frac{dt}{ds} \wedge \left( \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2t}{ds^2} \right)
$$

$$
= \left( \frac{dt}{ds} \right)^3 \vec{r}' \wedge \vec{r}'' + 0
$$

$$
|\vec{t} \wedge \vec{T}'| = \left| \left( \frac{dt}{ds} \right)^3 \right| |\vec{r}' \wedge \vec{r}''|
$$

$$
= \left( \frac{dt}{ds} \right)^3 |\vec{r}' \wedge \vec{r}''|
$$

$$
k(s) = \frac{|\vec{r}' \wedge \vec{r}''|}{|\vec{r}'|^3} \sim \rho = \frac{v^3}{|\vec{r}' \wedge \vec{r}''|}
$$

## Figure & Layout Description

图片呈现为方格纸背景的手写数学推导，整体为单页PPT布局。文字为黑色墨水书写，排版呈纵向分步推导结构。顶部第一行是中文标题"在E³中，求正则曲线的曲率和挠率"，字体略大于正文。下方依次排列15行数学公式，公式间有逻辑递进关系，通过等号对齐形成视觉流。关键公式如$S(t)$定义、$\frac{dS}{dt}$、$\vec{T}(s)$等使用较大字号，推导步骤中的中间过程字体稍小。部分公式存在手写修正痕迹：第8行"= ( [无法辨认] + ..."处有明显空白，第12行"$\vec{b} = \vec{t} \wedge \frac{\vec{T}'}{k}$"中分数线较粗，第15行末尾"$\rho = \frac{v^3}{|\vec{r}' \wedge \vec{r}''|}$"的分母部分有下划线强调。所有向量符号均用箭头标注（如$\vec{r}$），叉乘符号统一使用$\wedge$。背景方格线为浅灰色，间距约0.5cm，公式文字与网格线形成清晰的坐标参考系。

<CTX>
{
   "topic": "曲率和挠率的向量计算公式推导",
   "keywords": ["曲率计算", "挠率公式", "Frenet标架", "向量叉乘", "弧长参数化"],
   "summary": "通过向量微分运算推导出曲率k=|r'∧r''|/|r'|³和挠率ρ=v³/|r'∧r''|的显式表达式，建立速度加速度与几何特征量的直接联系",
   "pending_concepts": ["挠率的具体计算步骤", "三维曲线可视化示例", "曲率与挠率在运动学中的物理意义"]
}
</CTX>

---

# Slide 23

$$\dot{\vec{T}}(s) = k(s) \vec{n}(s)$$
$$\ddot{\vec{T}}(s) = \dot{k}(s) \vec{n}(s) + k(s) \dot{\vec{n}}(s)$$
$$= \dot{k}(s) \vec{n}(s) + k(s) \left( -k(s) \vec{t} + \tau(s) \vec{b} \right)$$
$$= \dot{k}(s) \vec{n}(s) - k^2(s) \vec{t} + k(s)\tau(s) \vec{b}$$
$$\langle \ddot{\vec{T}}(s), \vec{b} \rangle = k(s)\tau(s)$$
$$\Rightarrow \tau(s) = \frac{\langle \ddot{\vec{T}}(s), \vec{b} \rangle}{k(s)}$$

$$\vec{b}(s) = \vec{t} \wedge \vec{n} = \vec{t} \wedge \left( \frac{\dot{\vec{T}}}{k} \right) = \left( \vec{r}' \wedge \vec{r}'' \right) \frac{1}{k}$$
$$= \left( \frac{dt}{ds} \right)^3 \left( \vec{r}' \wedge \vec{r}'' \right) \frac{1}{k}$$

$$\ddot{\vec{T}} = ?$$
$$\frac{d\vec{t}}{ds} = \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2 t}{ds^2}$$
$$\ddot{\vec{T}}(s) = \frac{d}{dt} \left( \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2 t}{ds^2} \right) \frac{dt}{ds}$$
$$= \left[ \frac{d^3\vec{r}}{dt^3} \left( \frac{dt}{ds} \right)^2 + \frac{d^2\vec{r}}{dt^2} \cdot 2 \left( \frac{dt}{ds} \right) \frac{d}{dt}\left( \frac{dt}{ds} \right) + \frac{d^2\vec{r}}{dt^2} \frac{d^2 t}{ds^2} + \frac{d\vec{r}}{dt} \frac{d}{dt}\left( \frac{d^2 t}{ds^2} \right) \right] \frac{dt}{ds}$$
$$= \frac{d^3\vec{r}}{dt^3} \left( \frac{dt}{ds} \right)^3 + 3 \frac{d^2\vec{r}}{dt^2} \frac{d^2 t}{ds^2} \frac{dt}{ds} + \frac{d\vec{r}}{dt} \frac{d^3 t}{ds^3} \left( \frac{dt}{ds} \right)^2$$

$$\langle \ddot{\vec{T}}(s), \vec{b} \rangle = \left\langle \frac{d^3\vec{r}}{dt^3} \left( \frac{dt}{ds} \right)^3 + 3 \frac{d^2\vec{r}}{dt^2} \frac{d^2 t}{ds^2} \frac{dt}{ds} + \frac{d\vec{r}}{dt} \frac{d^3 t}{ds^3} \left( \frac{dt}{ds} \right)^2, \left( \frac{dt}{ds} \right)^3 (\vec{r}' \wedge \vec{r}'') \frac{1}{k} \right\rangle$$

## Figure & Layout Description
The image shows a single slide of handwritten mathematical derivations on grid paper with light gray lines forming 1cm x 1cm squares. All content is written in black ink with consistent stroke weight. The layout follows a top-to-bottom derivation flow with multiple equation blocks. The upper portion contains Frenet-Serret formulas with vector notation (arrows over T, n, b), while the middle section shows inner product calculations. The lower half features detailed chain rule expansions with fractional derivatives. Key structural elements include: 1) Aligned equal signs forming vertical derivation columns, 2) Parenthetical groupings for vector operations, 3) Superscript dots denoting time derivatives (single dot for first derivative, double dot for second), 4) Angle brackets for inner products, and 5) Wedge symbols (∧) for cross products. The handwriting is neat with consistent symbol sizing, though some derivative fractions are tightly spaced. No colors other than black ink on white background are present.

<CTX>
{
   "topic": "挠率公式的显式推导与参数转换",
   "keywords": ["曲率计算", "挠率公式", "Frenet标架", "链式法则", "参数替换"],
   "summary": "完成挠率τ的显式表达式推导，建立弧长参数s与时间参数t的转换关系，得到基于坐标导数的挠率计算公式",
   "pending_concepts": ["三维曲线可视化示例", "曲率与挠率在运动学中的物理意义"]
}
</CTX>

---

# Slide 24

$$ = \frac{1}{\kappa} \left( \frac{dt}{ds} \right)^6 \langle \vec{r}''', \vec{r}' \wedge \vec{r}'' \rangle + \frac{3}{\kappa} \left( \frac{dt}{ds} \right)^4 \frac{d^2 t}{ds^2} \langle \vec{r}'', \vec{r}' \wedge \vec{r}'' \rangle_0 + \frac{1}{\kappa} \frac{d^3 t}{ds^3} \left( \frac{dt}{ds} \right)^5 \langle \vec{r}', \vec{r}' \wedge \vec{r}'' \rangle_{40} $$

$$ \langle \ddot{t}(s), \vec{b} \rangle = \frac{1}{\kappa} \left( \frac{dt}{ds} \right)^6 \langle \vec{r}''', \vec{r}' \wedge \vec{r}'' \rangle $$
$$ = \frac{1}{\kappa} \left( \frac{dt}{ds} \right)^6 (\vec{r}''', \vec{r}', \vec{r}'') $$
$$ \langle \ddot{t}(s), \vec{b} \rangle = \frac{1}{\kappa} \left( \frac{dt}{ds} \right)^6 (\vec{r}', \vec{r}'', \vec{r}''') $$

$$ \tau(s) = \frac{\langle \ddot{t}(s), \vec{b} \rangle}{\kappa(s)} = \frac{1}{\kappa^2} \left| \frac{dt}{ds} \right|^6 (\vec{r}', \vec{r}'', \vec{r}''') $$
$$ = \frac{|r'|^6}{|\vec{r}' \wedge \vec{r}''|^2} \cdot \frac{(\vec{r}', \vec{r}'', \vec{r}''')}{|r'|^6} $$
$$ t(s) = \frac{(\vec{r}', \vec{r}'', \vec{r}''')}{|\vec{r}' \wedge \vec{r}''|^2} \quad e = \frac{|\vec{v}|}{\vec{a}_n \times \vec{v}} \sim \frac{\vec{v} \cdot (\vec{a} \times \dot{\vec{a}})}{|\vec{v} \times \vec{a}|} \sim \dddot{s} $$

综上 $\kappa(s) = \frac{|\vec{r}' \wedge \vec{r}''|}{|\vec{r}'|^3} \quad \tau(s) = \frac{(\vec{r}', \vec{r}'', \vec{r}''')}{|\vec{r}' \wedge \vec{r}''|^2}$

4. (2) $\vec{r}' = (3-2t, 6t, 3+2t) \quad |\vec{r}'| = \sqrt{11}$  
$\vec{r}'' = (-2, 6, 2)$  
$\vec{r}''' = 0$  
$\kappa(s) = \frac{|\vec{r}' \wedge \vec{r}''|}{|\vec{r}'|^3} = \begin{vmatrix} i & j & k \\ 3-2t & 6t & 3+2t \end{vmatrix}$

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记，浅灰色网格线构成标准坐标纸布局。所有内容以黑色墨水书写，公式自上而下分块排列，每块公式通过等号对齐形成逻辑流。顶部是包含曲率κ和挠率τ的复合表达式，使用尖括号⟨⟩表示内积、∧表示向量叉乘；中间部分展示Frenet标架中切向量二阶导与副法向量的内积推导，含多个向量三重积表达式；底部为编号"4.(2)"的具体参数化曲线示例，包含向量坐标分量和行列式结构。公式中向量符号统一用箭头标注（如$\vec{r}$），导数阶数通过单撇/双撇/三撇表示，关键变量如κ(s)、τ(s)在推导末尾被明确框定。部分公式右侧有手写注释（如"0"、"40"下标），推导过程存在分式结构和绝对值符号，整体呈现典型的微分几何手稿特征。

<CTX>
{
   "topic": "挠率公式的显式推导与参数化曲线实例验证",
   "keywords": ["曲率计算", "挠率公式", "Frenet标架", "参数化曲线示例", "向量三重积"],
   "summary": "通过具体参数化曲线示例完成曲率与挠率公式的数值验证，建立坐标导数与几何量的直接计算关系",
   "pending_concepts": ["三维曲线可视化示例", "曲率与挠率在运动学中的物理意义"]
}
</CTX>

---

# Slide 25

## §2.4 曲线论基本定理

设 $\vec{r}(t) \in E^3$ 是正则曲线，$t \in (a,b)$，$t = t(u)$ 是参数变换，$\frac{dt}{du} \neq 0$，$u \in (\alpha,\beta)$

若 $\frac{dt}{du} > 0$，则称参数变换 $t = t(u)$ 保持定向  
若 $\frac{dt}{du} < 0$，保持反向

e.g.  
左侧坐标系示意图：  
- 横轴向右箭头标注 $A$  
- 纵轴向上箭头标注 $w=2$  
- 横轴上 $w=0$ 位置有标记点  

**例子1**：  
尺子线段 $t$，$t \in (0,2)$，$\vec{r}(t) = (t,0)$，$\overrightarrow{OA}$  
尺子线段 $u$，$u \in (0,1)$，$t=2u$，$\vec{r}(t) = (2u,0)$  
$\frac{dt}{du} = 2 > 0$，保持定向，$\overrightarrow{OA}$

**例子2**：  
尺子线段 $w$，$w \in (0,1)$，$t=2-w$，$\vec{r}(t) = (2-w,0)$  
$\frac{dt}{du} = -1 < 0$，保持反向，曲线 $\overrightarrow{AO}$  
说明对应曲线不同了对应就不同

注：  
① $t = t(u)$ 保持定向，$\vec{r}(t)$ 和 $\vec{r}(u)$ 是相同的曲线  
$t = t(u)$ 保持反向，$\vec{r}(t)$ 和 $\vec{r}(u)$ 是相反的曲线  

② 弧长参数变换保持定向，且弧长参数之间相差一个常数是唯一的  
设 $s_1$ 和 $s_2$ 是 $\vec{r}$ 的弧长参数，且 $s_1 = s_1(s_2)$  
$$
S_1(s_2) = \int_{0}^{s_2} |\vec{r}'(u)| du
$$
$$
\frac{ds_1}{ds_2} = |\vec{r}'(u)| = 1 > 0
$$
（单位向量）  
故保持定向  
相差常数唯一？  
$$
1 = \left| \frac{d\vec{r}}{ds_1} \right| = \left| \frac{d\vec{r}}{ds_2} \right| \frac{ds_2}{ds_1} = \frac{ds_2}{ds_1}
$$
$ds_2 = ds_1$  
$s_2 = s_1 + \text{Const}$

## Figure & Layout Description

页面背景为浅黄色方格纸，手写黑色墨迹内容占据整个画面。顶部中央以较大字体书写章节标题"§2.4 曲线论基本定理"，右上角有手写"证明"二字。正文分为定义区、示例区和注释区：

1. **定义区**（上半部分）：  
   - 两行参数变换定义，包含向量符号 $\vec{r}(t)$ 和导数 $\frac{dt}{du}$  
   - "保持定向"和"保持反向"分两行书写，后者右对齐

2. **示例区**（中部）：  
   - 左侧有坐标系示意图：横轴向右箭头标注"A"，纵轴向上箭头标注"w=2"，横轴上"w=0"位置有标记点  
   - 三个水平线段图示：  
     * 顶部线段标有0-1-2刻度（对应t参数）  
     * 中间线段标有0-0.5-1刻度（对应u参数）  
     * 底部线段标有2-1-0刻度（对应w参数）  
   - 每个图示右侧配有参数变换公式和导数计算

3. **注释区**（下半部分）：  
   - 两个带圈序号的注释点，含弧长参数的积分公式  
   - 多个手写公式垂直排列，包含积分符号和导数链式表达式  
   - "单位向量"标注在公式下方，用小括号括起

所有文字均为手写体，公式与文字混排，部分符号（如向量箭头）用斜线标注，数字"2"的写法带有横杠。

<CTX>
{
   "topic": "曲线论基本定理与参数变换的定向性质",
   "keywords": ["参数变换", "定向保持", "弧长参数", "正则曲线", "曲线方向"],
   "summary": "阐明参数变换对曲线定向的影响机制，证明弧长参数的唯一性及其与定向保持的内在联系",
   "pending_concepts": ["参数变换对Frenet标架的影响", "定向保持与曲线几何不变量的关系"]
}
</CTX>

---

# Slide 26

③ 曲率，挠率和容许参数无关

容许参数：正则曲线对应参数 要求 $\frac{ds}{du} > 0$

Frenet 公式  
$$\dot{\vec{t}} = k(s) \vec{n}$$  
$$\dot{\vec{n}} = -k(s)\vec{t} + \tau(s) \vec{b}$$  
$$\dot{\vec{b}} = -\tau(s)\vec{n}$$  

定义：  
$\vec{t}(s) = \dot{\vec{r}}(s)$  
$\vec{n} = \frac{\ddot{\vec{r}}}{|\ddot{\vec{r}}|} = \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|}$  
$\dot{\vec{n}} = \frac{d}{ds} \left( \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|} \right)$  
$\vec{b} = \vec{t} \wedge \vec{n} = \dot{\vec{r}}(s) \wedge \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|}$  
$\dot{\vec{b}} = \frac{d}{ds} \left( \dot{\vec{r}}(s) \wedge \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|} \right)$  

所以 Frenet 标架只和 $\dot{\vec{r}}(s)$ 和 $\ddot{\vec{r}}(s)$ 有关

现只用证 $\dot{\vec{r}}(s)$ 与容许参数无关

设 $s_1$ 和 $s_2$：  
$s_1 = s_2 + C$  
$\frac{d\vec{r}}{ds_1} = \frac{d\vec{r}}{d(s_2 + C)} = \frac{d\vec{r}}{ds_2}$  
$\frac{d}{ds_1} \left( \frac{d\vec{r}}{ds_1} \right) = \frac{d}{ds_2} \left( \frac{d\vec{r}}{ds_2} \right)$  

所以 $\dot{\vec{r}}(s)$ 与 $s$ 的选取无关

设 $t$ 是 $\vec{r}(u)$ 的容许参数  
$S(t) = \int_0^t |\vec{r}'(u)| du$  
$S'(t) = |\vec{r}'(u)| > 0$（$S$ 严格增）  
存在反函数 $t = t(s)$  

所以与容许参数无关

## Figure & Layout Description
手写笔记呈现于米黄色方格纸背景上，网格线为浅灰色细线。内容以黑色墨水书写，整体分为三个逻辑区域：顶部为标题区（"③ 曲率，挠率和容许参数无关"及容许参数定义），中部为Frenet公式列表与推导过程（包含6组向量公式），底部为参数无关性证明（含积分表达式和反函数推导）。文字布局呈纵向排列，公式间通过等号对齐形成视觉层次。关键结论"所以Frenet标架只和..."使用下划线强调，"S严格增"旁有手写箭头标注。部分符号如$\vec{r}$、$\dot{\vec{t}}$等向量符号书写清晰，积分上下限和导数符号完整。左侧有手写"n阶"标记，疑似章节编号。

<CTX>
{
   "topic": "Frenet标架与容许参数的无关性证明",
   "keywords": ["曲率", "挠率", "Frenet标架", "弧长参数", "参数变换不变性"],
   "summary": "证明Frenet标架仅依赖弧长参数，与容许参数选择无关，建立几何不变量与参数化的本质联系",
   "pending_concepts": ["挠率的几何意义", "非弧长参数下的Frenet公式修正"]
}
</CTX>

---

# Slide 27

4.1 曲线的弧长参数，曲率，挠率在刚体运动下不变

证 设 $s$ 是 $\gamma$ 的弧长参数，$T$ 是刚体运动，则  
$$
\tilde{\gamma}(s) = T \gamma(s) + p_0, \quad \det(T) = 1, \ T \in O(3)
$$
$$
\tilde{\gamma}(s) = T \circ \gamma(s)
$$
$$
|\tilde{\gamma}'(s)| = \left| \frac{d}{ds} (\gamma(s) T + p_0) \right| = |\gamma'(s) T| 
$$
$$
= \sqrt{\langle \gamma'(s) T, \gamma'(s) T \rangle} = \sqrt{\gamma'(s) T T^T \gamma'(s)} = \sqrt{\gamma'(s) \gamma'(s)} = |\gamma'(s)|
$$
故 $|\tilde{\gamma}'(s)|$ 不变  
$$
\kappa(s) = |\dot{t}|
$$
$$
\tilde{\gamma} = T(\gamma) = T\gamma + p_0
$$
$$
\tilde{t} = \tilde{\gamma}'(s) = \gamma' T = t T
$$
$$
\dot{\tilde{t}} = \ddot{\gamma}'(s) = \ddot{\gamma} T
$$
$$
\tilde{\kappa} = |\dot{\tilde{t}}| = |\ddot{\gamma} T| = \sqrt{\langle \ddot{\gamma} T, \ddot{\gamma} T \rangle} = \sqrt{\ddot{\gamma} T T^T \ddot{\gamma}} = \sqrt{\ddot{\gamma} \ddot{\gamma}} = |\ddot{\gamma}| = |\dot{t}|
$$
$$
\tilde{\kappa} = \kappa
$$
曲率不变  
$$
\dot{t} = -\kappa n
$$
$$
t' = \tau n \times t
$$
$$
\tilde{n} = \frac{\dot{\tilde{t}}}{|\dot{\tilde{t}}|} = \frac{\ddot{\gamma} T}{|\ddot{\gamma} T|} = \frac{\ddot{\gamma} T}{\kappa} = \frac{\dot{t}}{\kappa} T = \frac{\dot{t}}{|\dot{t}|} T = n T
$$
$$
\Rightarrow \tilde{n} = n T
$$
$$
\tilde{b} = \tilde{t} \wedge \tilde{n} = t T \wedge n T = T(t) \wedge T(n) \stackrel{\text{问题5}}{=} \det(T) T(t \wedge n) = T(b) = b T
$$
$$
\text{令 } \gamma'(s) = x T, \text{ 保原点}
$$
$$
\Rightarrow \tilde{b} = b T
$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导笔记，采用黑色墨水书写。整体布局为纵向排列的数学证明过程，包含标题、证明步骤、公式推导三部分。标题"4.1 曲线的弧长参数，曲率，挠率在刚体运动下不变"位于左上角，使用加粗手写体。证明部分从"证"字开始，分层展示刚体运动变换公式、弧长参数不变性推导、曲率与挠率的不变性证明。公式部分包含多级推导，使用竖线表示向量模长、尖括号表示内积、波浪线表示变换后变量。关键结论如"故$|\tilde{\gamma}'(s)|$不变"和"曲率不变"以加粗手写体突出显示。推导中穿插"问题5"等注释说明，最后以向量叉积关系收尾。方格纸的浅灰色网格线作为背景，文字与公式严格对齐网格，形成清晰的行列结构。

<CTX>
{
   "topic": "曲线几何量在刚体运动下的不变性证明",
   "keywords": ["刚体运动", "弧长参数", "曲率不变性", "挠率不变性", "正交变换"],
   "summary": "证明曲线的弧长参数、曲率和挠率在刚体运动下保持不变，建立几何不变量与运动变换的内在联系",
   "pending_concepts": ["挠率的几何意义", "非弧长参数下的Frenet公式修正"]
}
</CTX>

---

# Slide 28

$$
\dot{\vec{b}} = \vec{b}' T
$$
$$
-\tau \vec{n} = (-\tau \vec{n}') T
$$
$$
-\tau \vec{n}' T = -\tau \vec{n}' T
$$
$$
(\tau - \tau) \vec{n}' T = 0
$$
$$
\langle \vec{n}' T, \vec{n}' T \rangle = \vec{n}' T T^T \vec{n}'^T = 1
$$
故 $\tau = \tau$  
挠率不变

给定 $\vec{r}(t) \in E^3$，可求 $k, \tau$  
反之，给定两个函数，其中一个大于0，是否存在曲线 $\vec{r}$，使 $\vec{r}$ 的曲率和挠率分别为这两个函数？

4.3 定理：设 $k: (a,b) \to \mathbb{R}_+$，$\tau: (a,b) \to \mathbb{R}$，$k, \tau \in C^\infty(a,b)$  
则在相差一个刚体运动下，存在唯一的曲线 $\vec{r}: (a,b) \to E^3$  
以弧长为参数，$k, \tau$ 为曲率、挠率  

**证**：  
存在性：$s$ 不一定是弧长参数，$\vec{e}_1$ 给定（初值可选）  
考虑下面的一阶齐次常微分方程组，初值给定为 $\vec{r}^0, \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0$，且 $\{\vec{r}^0; \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0\}$ 是 Frenet 标架  
设  
$$
\begin{cases}
\frac{d\vec{r}}{ds} = \vec{e}_1 & \#1 \\
\frac{d\vec{e}_1}{ds} = k \vec{e}_2 & \#2 \\
\frac{d\vec{e}_2}{ds} = -k \vec{e}_1 + \tau \vec{e}_3 & \#3 \\
\frac{d\vec{e}_3}{ds} = -\tau \vec{e}_2 & \#4
\end{cases}
$$  
只需证明 $\{\vec{r}; \vec{e}_1, \vec{e}_2, \vec{e}_3\}$ 是 Frenet 标架

## Figure & Layout Description
- **背景与布局**：页面为浅黄色方格纸背景，灰色细线构成标准方格网格（每格约0.5cm×0.5cm）。所有内容为黑色手写体，按垂直顺序分为三个主要区域：
  1. **顶部公式推导区**（占页面1/3）：包含6行连续等式推导，前4行为曲线几何量变换关系，第5行为内积计算，第6行为结论"故 $\tau = \tau$"，末行标注"挠率不变"
  2. **中部问题陈述区**（占页面1/3）：两行手写文字，提出曲线重构问题，包含数学符号 $\vec{r}(t) \in E^3$ 和函数条件描述
  3. **底部定理证明区**（占页面1/3）：以"4.3 定理"为标题，包含定理陈述、证明框架说明和4个方程的微分方程组。方程组采用大括号包裹，每行右侧标注#1-#4编号
- **文字特征**：手写体字迹清晰，公式中向量符号（$\vec{}$）和导数点（$\dot{}$）标注规范，关键术语如"Frenet 标架"完整书写
- **空间关系**：各区域间留有适当空白，微分方程组在页面底部居中排版，方程编号与公式主体右对齐

<CTX>
{
   "topic": "曲线存在性定理与Frenet标架微分方程组",
   "keywords": ["曲线存在性定理", "Frenet标架", "常微分方程组", "曲率挠率重构"],
   "summary": "建立给定曲率挠率函数时曲线的存在唯一性定理，通过一阶常微分方程组实现几何量到曲线的重构",
   "pending_concepts": ["非弧长参数下的Frenet公式修正", "微分方程组解的存在唯一性证明细节"]
}
</CTX>

---

# Slide 29

## ①相互正交 ②右手标架 ③证 $\vec{e}_1$ 是单位切向量

### ①相互正交）
由常微分方程组解的理论  
∃唯一的一组解  
$$ \left. \{ \vec{r}(s); \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) \} \right|_{s=s_0} = \{ \vec{r}^0; \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0 \} $$  
再证 $\{ \vec{e}_i(s) \}$ 是 Frenet 标架  
先证 $\vec{e}_1, \vec{e}_2, \vec{e}_3$ 是相互正交  
$$ \frac{d \vec{e}_i}{ds} = a_{ij} \vec{e}_j \quad \{a_{ij}\} = \begin{pmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{pmatrix} $$  
$a_{ij} = -a_{ji}$，$a_{ij} + a_{ji} = 0$ 反对称  
假设 $g_{ij}(s) = \langle \vec{e}_i(s), \vec{e}_j(s) \rangle$  
$$ \frac{d g_{ij}}{ds} = \langle \dot{e}_i, e_j \rangle + \langle e_i, \dot{e}_j \rangle = \langle a_{ik} e_k, e_j \rangle + \langle e_i, a_{jk} e_k \rangle = a_{ik} g_{kj} + a_{jk} g_{ik} \quad (\times) $$  
$(\times)$ 是关于 $g_{ij}$ 的一阶齐次线性常微分方程组  
$g_{ij}(s)$ 是 $(\times)$ 一组解，$g_{ij}(s_0) = \delta_{ij}$  
$\delta_{ij}(s)$ 是 $(\times)$ 一组解，$\delta_{ij}(s_0) = \delta_{ij}$  
由常微分方程组解的唯一性可知  
$$ g_{ij}(s) \equiv \delta_{ij} = \langle \vec{e}_i(s), \vec{e}_j(s) \rangle $$  
即 $\{ \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) \}$ 是单位正交向量  

### ②右手标架
$$ ( \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0 ) = \langle \vec{e}_1^0 \wedge \vec{e}_2^0, \vec{e}_3^0 \rangle = 1 $$  
$( \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) )$  
由连续性，$| ( \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) ) | \equiv 1$  

## Figure & Layout Description
The image shows a handwritten mathematical derivation on a light yellow grid paper background. The content is organized in a top-to-bottom flow with clear section headings. At the very top, three numbered items are listed horizontally: "①相互正交", "②右手标架", "③证 $\vec{e}_1$ 是单位切向量". Below this, the main content starts with a large heading "①相互正交）" followed by explanatory text in Chinese. Mathematical formulas are interspersed throughout, including a large equation block showing the initial condition for the Frenet frame, a matrix representation of the coefficient tensor $\{a_{ij}\}$, and a derivation of the orthogonality condition using the metric tensor $g_{ij}(s)$. The text uses consistent black ink with varying stroke weights indicating handwritten emphasis. The second section "②右手标架" appears at the bottom with associated vector triple product formulas. Handwritten annotations include underlines for emphasis and marginal notes. The grid lines are light gray and form a regular square pattern (approximately 5mm spacing), providing structural alignment for the handwritten content. Some symbols near the bottom right corner (e.g., $\sum_{i=1}^{3}$) are partially obscured but identifiable. No colors other than black ink on yellow paper are present, and there are no diagrams or illustrations—only textual and formulaic content.

<CTX>
{
   "topic": "Frenet标架正交性与右手性证明",
   "keywords": ["Frenet标架", "常微分方程组", "正交性证明", "右手性", "单位切向量"],
   "summary": "通过一阶常微分方程组解的唯一性证明Frenet标架的正交性和右手性，完成曲线存在性定理的关键步骤",
   "pending_concepts": ["非弧长参数下的Frenet公式修正", "微分方程组解的存在唯一性证明细节", "曲率挠率函数的连续性要求"]
}
</CTX>

---

# Slide 30

$e_1(s) \wedge e_2(s) = e_3(s)$，是右手标架

③ 证$\vec{e_1}$是单位切向量，$\vec{e_2}$主法向量，$\vec{e_3}$副法向量

由1式知 $\frac{d\vec{r}}{ds} = \vec{e_1}$，$\left| \frac{d\vec{r}}{ds} \right| = |\vec{e_1}| = 1$

说明 $s$ 是弧长参数，故 $\frac{d\vec{r}}{ds} = \vec{e_1}$ 是单位切向量，记为 $\vec{t}(s)$

由2式知 $\left| \frac{d\vec{e_1}}{ds} \right| = |k \vec{e_2}| = k(s)$，$|\vec{e_1}| = k(s)$，$k(s)$ 是曲率

$\vec{n} = \frac{\vec{e_1}}{|\vec{e_1}|} = \frac{k \vec{e_2}}{k(s)} = \vec{e_2}$，$\vec{e_2}$ 是主法向量

$\vec{b} = \vec{t} \wedge \vec{n} = \vec{e_1} \wedge \vec{e_2} = \vec{e_3}$，$\vec{e_3}$ 是副法向量

4是Frenet公式，$k(s)$，$\tau(s)$ 分别是曲率挠率。

唯一性

由常微分方程组解的理论

$\exists$唯一的一组解

$$\left. \{ \vec{r}(s), \vec{e_1}(s), \vec{e_2}(s), \vec{e_3}(s) \} \right|_{s=s_0} = \{ \vec{r}^0; \vec{e_1}^0, \vec{e_2}^0, \vec{e_3}^0 \}$$

平面曲线基本定理：（一样证法）

## Figure & Layout Description
图片为浅米色网格纸背景的手写笔记，黑色墨水书写。整体布局分为上下两个逻辑区域：上半部分（约占2/3版面）为Frenet标架向量的定义与证明过程，包含带编号的推导步骤；下半部分（约占1/3版面）讨论唯一性证明。文字排列紧凑但层次分明，关键步骤用圆圈数字"③"标注。公式与文字交替出现，向量符号统一用箭头表示（如$\vec{e_1}$）。网格线为浅灰色正方形格子，文字基本居中对齐。无彩色标记或图形元素，纯手写体内容，字迹清晰但存在连笔现象（如"证"字与后续内容的衔接）。公式推导部分包含多层分式结构（如$\frac{d\vec{r}}{ds}$）和向量运算符号（$\wedge$），初始条件部分使用竖线标注限制条件（$|_{s=s_0}$）。

<CTX>
{
   "topic": "Frenet标架向量定义与唯一性证明",
   "keywords": ["Frenet标架", "单位切向量", "主法向量", "副法向量", "唯一性证明", "弧长参数"],
   "summary": "本页完成Frenet标架三个基本向量的严格定义，并通过常微分方程解的唯一性证明标架的确定性，建立曲线几何性质与参数方程的对应关系",
   "pending_concepts": ["平面曲线基本定理的具体表述", "曲率挠率函数的连续性条件", "非弧长参数下Frenet公式的转换方法"]
}
</CTX>

---

# Slide 31

e.g. $\mathbb{E}^3$中曲率挠率均为常数的分类

(1) $k=0$  
$$\frac{d\vec{t}}{ds}=k\vec{n}=0 \quad \vec{t}=\vec{c_1}$$  
$$\frac{d\vec{r}}{ds}=\vec{t}=\vec{c_1}$$  
$$\vec{r}=\vec{c_1}s + \vec{c_2}$$  
故是直线

(2) $k>0, \tau=0$，是圆  
不偏离平面

(3) $k>0, \tau>0$，圆柱螺旋线

## Figure & Layout Description
图片为方格纸背景的数学推导手稿，浅灰色细网格线构成标准坐标纸底纹。所有内容以黑色墨水手写呈现，整体布局呈纵向排列结构：
1. 顶部居中书写标题"e.g. $\mathbb{E}^3$中曲率挠率均为常数的分类"，采用较大字号的连笔手写体
2. 主体内容分为三个编号区块：
   - (1)区块位于左上区域，包含四行公式推导：首行并列书写"$k=0$"与"$\frac{d\vec{t}}{ds}=k\vec{n}=0$"，第二行独立公式"$\vec{t}=\vec{c_1}$"，第三行"$\frac{d\vec{r}}{ds}=\vec{t}=\vec{c_1}$"，第四行"$\vec{r}=\vec{c_1}s + \vec{c_2}$"，底部手写结论"故是直线"
   - (2)区块在中间区域，书写"$k>0, \tau=0$，是圆"，下方小字标注"不偏离平面"
   - (3)区块在底部区域，书写"$k>0, \tau>0$，圆柱螺旋线"
3. 所有向量符号均用箭头标注（如$\vec{t}$），常数项使用带下标的向量符号（如$\vec{c_1}$），公式与文字间保持标准手写间距，无特殊颜色或图形元素

<CTX>
{
   "topic": "$\\mathbb{E}^3$中曲率与挠率均为常数的曲线分类",
   "keywords": ["曲率常数", "挠率常数", "直线", "圆", "圆柱螺旋线", "Frenet标架应用"],
   "summary": "本页通过分析曲率和挠率的不同组合，系统分类了三维空间中具有常曲率和常挠率的曲线类型，完善了Frenet标架理论的实际应用案例",
   "pending_concepts": ["平面曲线基本定理的具体表述", "非圆柱螺旋线的其他常曲率挠率曲线类型", "曲率挠率函数的连续性条件"]
}
</CTX>

---

# Slide 32

# 第三章 曲面的局部理论

## §3.1 曲面的概念

$$
\vec{r}(x(u,v), y(u,v), z(u,v)) = \vec{r}(u,v)
$$

### 1. 曲面的概念

设 $D \subset \mathbb{E}^2$ 是区域（连通的开集）

定义 $\vec{r}: D \to \mathbb{E}^3$, $(u,v) \to (x(u,v), y(u,v), z(u,v))$

即 $\vec{r}(x(u,v), y(u,v), z(u,v))$

（坐标系示意图：左侧为 $uv$ 平面中的区域 $D$，右侧为三维空间中的曲面，中间箭头标注 $\vec{r}$）

显然若 $\vec{r} = \text{const}$ 是点不是曲面

所以作限制，若 $\vec{r}$ 满足

1. $\vec{r}(x(u,v), y(u,v), z(u,v)) \in C^\infty(D)$ 光滑

2. $\vec{r}_u(u,v) \wedge \vec{r}_v(u,v) \neq \vec{0}$，即 $\vec{r}_u, \vec{r}_v$ 线性无关（正则性）

则称 $\vec{r}$ 是 $\mathbb{E}^3$ 中的一个曲面片

**注**  
① 无奇点（$\bigcirc$ 不是）  
② $\vec{r} = \vec{a}$, $\vec{r}_u = 0$, $\vec{r}_v = 0$ 不正则  
正则性保证了 $\vec{r}$ 是一一映射

**e.g.**  
$z = f(x,y) \in C^\infty$  
$\vec{r}(x,y) = (x, y, f(x,y))$  
$\vec{r}_x = (1, 0, f_x)$

## Figure & Layout Description

页面采用米黄色方格纸背景，内容以橙色和黑色墨水手写呈现。顶部用较大橙色字体书写标题"第三章 曲面的局部理论"，其中"第三章"为艺术化手写体，"曲面的局部理论"为标准手写体。标题下方以黑色墨水书写二级标题"§3.1 曲面的概念"。

正文区域包含数学定义和公式，采用黑色手写体。左上方有手绘坐标系示意图：左侧为 $uv$ 平面直角坐标系，椭圆圈出区域 $D$；中间用箭头标注 $\vec{r}$ 表示映射关系；右侧为三维空间直角坐标系，绘制了平行四边形轮廓的曲面透视图，标注 $\vec{r}(u,v)$。

公式部分包含参数化映射定义、正则性条件等，关键条件用圆圈数字①②标注。注释部分以"注"开头分两点说明，示例部分以"e.g."开头展示显式曲面参数化。页面中存在多处手写修正痕迹，如"根无念"应为"概念"的笔误，以及用箭头指向特定公式进行强调。整体布局为左文右图结构，重要概念和公式通过下划线、圈注等方式突出显示。

<CTX>
{
   "topic": "曲面的参数化定义与正则性条件",
   "keywords": ["曲面参数化", "正则性条件", "C^∞光滑性", "线性无关偏导数", "曲面片"],
   "summary": "本页建立了三维空间中曲面的参数化定义框架，通过引入光滑性和正则性条件严格区分了曲面与退化情形，为后续讨论曲面几何性质奠定基础",
   "pending_concepts": ["曲面的第一基本形式", "切平面与法向量的严格定义", "参数变换下的不变性", "非显式曲面的参数化示例"]
}
</CTX>

---

# Slide 33

$$
\vec{r}_y = (0,1,f_y)
$$
$$
\vec{r}_x \wedge \vec{r}_y = \begin{vmatrix}
i & j & k \\
1 & 0 & f_x \\
0 & 1 & f_y
\end{vmatrix} = (-f_x, -f_y, 1) \neq \vec{0}
$$
$z = f(x,y)$ 是曲面

e.g.2 设 $F(x,y,z) \in C^\infty$, $S = \{(x,y,z) \mid F(x,y,z)=0\}$  
讨论：F是否是曲面  

A 若 $\nabla F(x,y,z) = (F_x, F_y, F_z)\big|_{(x_0,y_0,z_0)} \neq \vec{0}$  
　　当 $F_x|_{(x_0,y_0,z_0)} \neq 0$，$\exists$ 邻域 $U(y_0,z_0)$，使得 $x = f(y,z)$ $\left((y,z) \in U(y_0,z_0)\right)$  
　　当 $F_y|_{(x_0,y_0,z_0)} \neq 0$，$\exists$ 邻域 $U(x_0,z_0)$，使得 $y = f(x,z)$ $\left((x,z) \in U(x_0,z_0)\right)$  
　　当 $F_z|_{(x_0,y_0,z_0)} \neq 0$，$\exists$ 邻域 $U(x_0,y_0)$，使得 $z = f(x,y)$ $\left((x,y) \in U(x_0,y_0)\right)$  

由 e.g.1 $x = f(y,z)$, $y = f(x,z)$, $z = f(x,y)$  
　　各在局部是曲面片  

当 $\nabla F|_{(x_0,y_0,z_0)} \neq 0$，$S$ 在 $(x_0,y_0,z_0)$ 的邻域是一张曲面片  

B 当 $\nabla F|_{(x_0,y_0,z_0)} = 0$ ?  
e.g.2' 设 $F(x,y,z) = x^2 + y^2 - z^2 - c$, $S = \{(x,y,z) \mid F=0\}$  
$\nabla F = (2x, 2y, -2z)$  
$F=0 \Leftrightarrow x^2 + y^2 = z^2 + c$

## Figure & Layout Description
图片呈现方格纸背景上的黑色手写数学笔记，整体布局为纵向分层结构。顶部区域包含参数化曲面的向量推导（$\vec{r}_y$ 定义及叉乘计算），使用标准行列式符号展示切向量线性无关性。中间主体部分以"e.g.2"为起始，系统阐述隐函数定理在曲面判定中的应用，通过分段缩进和条件分支（A/B分类）构建逻辑层次：A部分用三行条件语句说明梯度非零时的局部参数化可能性，B部分讨论梯度为零的退化情形。底部右侧附有双叶锥体的简笔示意图，线条简洁但清晰呈现对称开口结构，与左侧代数方程 $x^2+y^2=z^2+c$ 形成几何-代数对应。文字排版采用手写体特有的非对齐风格，关键数学符号（如 $\nabla F$, $C^\infty$）通过加粗笔画强调，方格纸网格线作为隐式坐标系辅助公式对齐。

<CTX>
{
   "topic": "隐函数定理与曲面正则性条件",
   "keywords": ["隐函数定理", "梯度非零条件", "奇异点", "局部参数化", "曲面判定"],
   "summary": "本页通过隐函数定理建立曲面的隐式定义框架，严格区分正则点与奇异点，完善曲面存在的充分条件",
   "pending_concepts": ["奇异点的几何分类", "隐函数定理的证明细节", "退化曲面的拓扑结构", "参数化与隐式表示的等价性"]
}
</CTX>

---

# Slide 34

a. $c > 0$  
（单叶双曲面图示）  
$\nabla F = 0 \implies x = y = z = 0$，在此点不是曲面  

b. $c = 0$，$x^2 + y^2 = z^2$  
（锥面图示）  
在 $(0,0,0)$ 有角点，不是曲面  

c. $c < 0$，$x^2 + y^2 = z^2 + c$  
（双叶双曲面图示）  
此点平滑，无角点  
在 $(0,0,0)$ 不是曲面  
双叶双曲面  

e.g. 3 $F(x,y,z) = z^2$，$S: \{(x,y,z) \mid F(x,y,z) = 0\}$  
$\nabla F = (0,0,2z)$  
$z^2 = 0 \implies z = 0$（$xy$ 平面）  
令 $\nabla F = 0 \implies 2z = 0$  
在原点附近 $S$ 是曲面  

## Figure & Layout Description
手写笔记位于方格纸背景上，黑色墨水书写，整体纵向排列。页面分为四个主要区域：
1. **a部分**：左上角标注"a. $c > 0$"，右侧手绘单叶双曲面示意图（上下对称、中间收窄的旋转曲面），标注三维坐标轴$x,y,z$。下方文字说明$\nabla F = 0$的推导过程及"在此点不是曲面"的结论。
2. **b部分**：中部左侧标注"b. $c = 0$，$x^2 + y^2 = z^2$"，右侧手绘锥面示意图（顶点在原点、上下对称的圆锥体），坐标轴清晰标注。右侧文字标注"在$(0,0,0)$有角点，不是曲面"。
3. **c部分**：下部左侧标注"c. $c < 0$，$x^2 + y^2 = z^2 + c$"，右侧分两幅图：左侧为$x^2+y^2$平面示意图，右侧为双叶双曲面示意图（上下分离的两叶曲面），标注"此点平滑，无角点"。下方有"在$(0,0,0)$不是曲面"及"双叶双曲面"的文字说明。
4. **例题区域**：底部密集排列"e.g.3"内容，包含函数定义、梯度计算和推导过程，公式与文字混合书写，关键结论"在原点附近$S$是曲面"位于最下方。

所有图形均用简单线条勾勒，坐标轴采用标准右手系表示，文字注释紧邻对应图形，整体布局遵循从上至下的逻辑流。

<CTX>
{
   "topic": "隐函数定理与曲面正则性条件的实例验证",
   "keywords": ["隐函数定理", "梯度非零条件", "奇异点", "单叶双曲面", "锥面", "双叶双曲面"],
   "summary": "通过单叶双曲面、锥面、双叶双曲面等二次曲面实例，具体说明梯度为零时奇异点的几何表现及曲面正则性判定",
   "pending_concepts": ["奇异点的几何分类", "隐函数定理的证明细节", "退化曲面的拓扑结构", "参数化与隐式表示的等价性"]
}
</CTX>

---

# Slide 35

这点说明 $\nabla F \neq 0$ 一定是曲面  
$\nabla F = 0$ 不一定是曲面

给定两张曲面  
$\vec{r}_1: D \to E^3, \ (u, v) \to (x(u,v), y(u,v), z(u,v))$  
$\vec{r}_2: \bar{D} \to E^3, \ (\bar{u}, \bar{v}) \to (x(\bar{u},\bar{v}), y(\bar{u},\bar{v}), z(\bar{u},\bar{v}))$

若存在参数变换  
$\sigma: \bar{D} \to D, \ (\bar{u}, \bar{v}) \to (u(\bar{u}, \bar{v}), v(\bar{u}, \bar{v}))$  
使得 $\vec{r}_1(\bar{u}, \bar{v}) = \vec{r}_1 \circ \sigma (\bar{u}, \bar{v}) = \vec{r}_1(u(\bar{u}, \bar{v}), v(\bar{u}, \bar{v}))$  
与 $\vec{r}_2(\bar{u}, \bar{v})$ 是同一曲面  

则称 $r_1(u,v)$ 与 $r_2(\bar{u}, \bar{v})$ 是同一曲面的不同参数表示  

e.g. 球面 $x^2 + y^2 + z^2 = a^2$  

球面的直角坐标参数表示：  
$\vec{r}_1(x,y,z) = \left( x, y, \sqrt{a^2 - x^2 - y^2} \right)$

## Figure & Layout Description
图片为方格纸背景的数学笔记，整体布局为纵向排列的手写内容。背景为浅黄色方格纸，黑色墨水书写，字迹工整但带有手写特征。内容分为六个逻辑区块：
1. 顶部两行关于梯度条件的结论，使用较大字号书写，"∇F≠0"和"∇F=0"用符号突出显示
2. "给定两张曲面"作为小标题，下方连续两行参数方程，向量符号$\vec{r}_1$和$\vec{r}_2$手写明显，参数域$D$和$\bar{D}$用横线标注
3. "若存在参数变换"段落包含参数变换定义，$\sigma$符号书写清晰，箭头符号→用斜线表示
4. 等式推导部分用"使得"开头，包含复合映射符号$\circ$和三重等式
5. "则称"段落定义等价参数表示，使用"与...是同一曲面"的并列结构
6. 底部"e.g."示例部分包含球面方程和参数表示，根号表达式$\sqrt{a^2-x^2-y^2}$书写完整，括号使用标准数学符号

公式排版具有明显手写特征：向量符号用箭头表示，参数域横线标注，复合映射用圆圈符号，所有数学符号与汉字间距适中。段落间通过空行分隔，关键概念如"参数变换"、"等价"等词语有轻微加重书写。

<CTX>
{
   "topic": "曲面参数表示的等价性与参数变换",
   "keywords": ["参数变换", "等价参数表示", "球面参数化", "隐式与参数表示"],
   "summary": "本页引入曲面参数表示的等价性概念，通过参数变换定义不同参数化方法的等价关系，并以球面为例说明直角坐标参数表示的应用",
   "pending_concepts": ["参数变换的正则性条件", "隐式与参数表示的等价性证明", "非正则参数化的几何意义"]
}
</CTX>

---

# Slide 36

$(x,y) \in D = \{(x,y) : x^2 + y^2 < a\}$

$\vec{r_1}$ 表示上半球面

$\vec{r_2}(u,v) = (a\cos u \cos v, a\cos u \sin v, a\sin u)$

$(u,v) \in \bar{D} = \{(u,v) : -\frac{\pi}{2} < u < \frac{\pi}{2}, 0 < v < 2\pi\}$

$\vec{r_2}$ 表示 去掉南北极点和联结两极点的大圆弧的球面 球面 $\stackrel{\frown}{NB} + [N,B)$

作变换：  
$\sin u = \frac{z}{a} = \frac{\sqrt{a^2 - x^2 - y^2}}{a}$  
$\tan v = \frac{y}{x}$  
$u = \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a}$  
$v = \arctan \frac{y}{x}$

## Figure & Layout Description
页面背景为浅黄色方格纸，网格线为浅灰色细线。所有文字和图形均为手写体，主要使用黑色墨水。页面内容分为三个垂直区域：上部为参数定义区域，中部为几何图示，下部为参数变换公式。

上部区域包含四行数学表达式：第一行定义区域 $D$；第二行说明 $\vec{r_1}$ 的几何意义；第三行给出 $\vec{r_2}$ 的参数方程；第四行定义参数域 $\bar{D}$；第五行描述 $\vec{r_2}$ 的几何意义。文字为黑色手写体，字迹清晰，行间距均匀。

中部区域为球面几何图示：中心绘制一个三维球面，球面轮廓线为蓝色实线。赤道圆用橙色实线绘制，其他纬线用橙色虚线表示。坐标系标注：x轴指向左下方，y轴水平向右，z轴垂直向上，轴线为黑色实线。北极点标注为蓝色圆点并标记"N"，南极点标注为蓝色圆点并标记"B"。球面上有一条蓝色实线大圆弧连接N和B点，弧线上标注参数"u"表示余纬度角（从z轴正向测量），"v"表示经度角（在xy平面内从x轴测量）。图示中包含虚线辅助线表示空间几何关系。

下部区域包含"作变换："标题及四行参数变换公式，文字为黑色手写体，与上部区域字体风格一致。公式按行排列，每行独立。

整体布局层次分明：数学定义在上，几何可视化居中，变换公式在下。颜色使用具有明确功能区分：黑色用于文字和坐标轴，蓝色用于球面主轮廓，橙色用于赤道和纬线，蓝色圆点突出极点位置。图示与文字紧密关联，形成"理论-可视化-计算"的逻辑链条。

<CTX>
{
   "topic": "球面参数表示的具体实现与参数变换",
   "keywords": ["球面参数化", "参数变换", "上半球面", "去掉极点的球面", "隐式与参数表示"],
   "summary": "本页通过球面的具体例子，展示了上半球面和去掉极点的球面的参数表示，并给出了从直角坐标到参数坐标的变换公式，深化了参数表示的理解",
   "pending_concepts": ["参数变换的正则性条件", "球面参数化的覆盖范围", "非正则点的几何意义"]
}
</CTX>

---

# Slide 37

$$\delta: D \to \overline{D},\ (x,y) \to (u,v) = \left( \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a},\ \arctan \frac{y}{x} \right)$$

$$\vec{r}_2(x,y) = \vec{r}_2 \circ \delta(x,y) = \vec{r}_2\left(u(x,y), v(x,y)\right) =$$
$$= \vec{r}_2\left( \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a},\ \arctan \frac{y}{x} \right)$$

$\vec{r}_2$ 和 $\vec{r}_1$ 是否为同一曲面？

$$
\begin{aligned}
&\arcsin x \quad x^2 + y^2 \leq a^2 \Rightarrow \frac{\sqrt{a^2 - x^2 - y^2}}{a} \leq 1 \Rightarrow \arcsin \frac{\sqrt{a^2 - x^2 - y^2}}{a} \in \left[0, \frac{\pi}{2}\right] \\
&\Updownarrow \\
&u(x,y) \in \left[0, \frac{\pi}{2}\right]
\end{aligned}
$$

$$
\frac{y}{x} \in [-\infty, +\infty]
$$

$$
\arctan \frac{y}{x} \in \left[-\frac{\pi}{2}, \frac{\pi}{2}\right] \cup \left[\frac{\pi}{2}, \frac{3\pi}{2}\right] = [0, 2\pi]
$$

$$
u(x,y) \in [0, 2\pi]
$$

$\vec{r}_2(x,y)$ 表示完整的上半平面 $\left( \frac{y}{x} \text{ 扩充到 } -\infty \right)$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局呈纵向分层结构：
1. 顶部区域：用黑色墨水书写参数变换映射 $\delta$ 的定义，包含双变量函数表达式，其中 $\arcsin$ 和 $\arctan$ 项均以分数形式呈现，根号内为 $a^2 - x^2 - y^2$
2. 中上部：推导 $\vec{r}_2(x,y)$ 的复合函数表达式，分两行书写，第二行对参数进行展开
3. 中部：手写提问" $\vec{r}_2$ 和 $\vec{r}_1$ 是否为同一曲面？"，左侧配有 $\arcsin x$ 函数图像（坐标系中第一、三象限的S形曲线），右侧有简化的坐标轴示意图
4. 中下部：参数范围分析区域，包含三行推导：
   - 第一行展示 $x^2 + y^2 \leq a^2$ 的约束条件与 $\arcsin$ 取值范围的推导
   - 第二行标注 $y/x$ 的取值范围
   - 第三行分析 $\arctan$ 的取值范围合并过程
5. 底部：结论性陈述，包含 $\vec{r}_2(x,y)$ 的几何意义说明，其中"扩充到 $-\infty$"为手写补充说明
所有文字均为黑色手写体，公式符号与汉字混排，关键推导步骤用双向箭头（$\Updownarrow$）连接，部分区域有轻微涂改痕迹

<CTX>
{
   "topic": "球面参数化的覆盖范围与参数变换分析",
   "keywords": ["球面参数化", "参数变换", "上半球面", "参数范围", "覆盖范围"],
   "summary": "本页通过分析参数变换的取值范围，阐明了上半球面参数表示的完整覆盖特性及其与直角坐标的映射关系",
   "pending_concepts": ["参数连续性条件", "极点处的参数奇异性", "多参数片拼接机制"]
}
</CTX>

---

# Slide 38

球极投影坐标：

$$
x^2 + y^2 + z^2 = a^2
$$

① 用球面直角坐标参数 $(x,y,z)$ 表示平面 $(xoy)$

$$
\vec{r} = \vec{r_0} + \vec{v}t
$$

$$
(u,v,w) = (0,0,a) + t \overrightarrow{NP}
$$

其中 $\overrightarrow{NP} = (x,y,z-a)$

$$
= (tx, ty, a + t(z-a))
$$

$$
w=0 \Rightarrow t = \frac{a}{a-z}
$$

$$
u = \frac{ax}{a-z}, \quad v = \frac{ay}{a-z}
$$

$$
\vec{r}(x,y) = \left( \frac{ax}{a-z}, \frac{ay}{a-z}, 0 \right)
$$

$$
= \left( \frac{ax}{a-\sqrt{a^2-x^2-y^2}}, \frac{ay}{a-\sqrt{a^2-x^2-y^2}}, 0 \right)
$$

## Figure & Layout Description
图片背景为浅米色方格纸（1cm×1cm网格）。中央偏左区域绘制三维坐标系：黑色实线坐标轴（x轴指向左前方，y轴指向右方，z轴垂直向上），原点位于画面中心。橙色实线绘制半径为a的球体，球心在坐标原点；赤道线用橙色虚线表示。关键点标注：z轴正半轴顶点标记为$N(0,0,a)$（黑色文字），球面上任意点标记为$P(x,y,z)$（黑色文字），xy平面上的投影点标记为$Q(u,v,0)$（黑色文字）。从N点引出的黑色直线穿过P点并延伸至Q点，表示投影射线。文字内容分层排列：标题"球极投影坐标："位于图示上方；球面方程$x^2+y^2+z^2=a^2$在图示正下方；推导过程从"①"开始依次排列在方程下方，公式与文字交替出现，手写体清晰但部分笔画较轻（如$\overrightarrow{NP}$的箭头）。所有数学符号均使用标准印刷体书写，坐标轴标注（x,y,z）位于对应轴末端。

<CTX>
{
   "topic": "球极投影的坐标映射推导",
   "keywords": ["球极投影", "坐标映射", "参数变换", "投影公式", "极点奇异性"],
   "summary": "本页通过向量参数化方法严格推导了球面点到平面的球极投影坐标变换公式，揭示了投影关系的代数表达及分母奇异性来源",
   "pending_concepts": ["极点处的参数奇异性处理", "多参数片拼接机制", "投影连续性条件"]
}
</CTX>

---

# Slide 39

② 用球极投影坐标参数表示球面

$$
\vec{r} = \vec{r_0} + \vec{v}t
$$

$$
(x, y, z) = (0, 0, a) + (u, v, -a)t
$$
$$
= (ut, vt, a - at)
$$

$$
x^2 + y^2 + z^2 = a^2
$$

$$
u^2t^2 + v^2t^2 + a^2(1-t)^2 = a^2
$$

$$
(u^2 + v^2)t^2 + a^2(1 - 2t + t^2) = a^2
$$

$$
(u^2 + v^2 + a^2)t^2 - 2a^2t = 0
$$

$$
t\left(t - \frac{2a^2}{u^2 + v^2 + a^2}\right) = 0
$$

两个交点 $N$ 和 $P$，故 $P$ 点对应 $t = \frac{2a^2}{u^2 + v^2 + a^2}$

$$
(x, y, z) = \left( \frac{2a^2u}{u^2 + v^2 + a^2}, \frac{2a^2v}{u^2 + v^2 + a^2}, a\left(1 - \frac{2a^2}{u^2 + v^2 + a^2}\right) \right)
$$
$$
= \left( \frac{2a^2u}{u^2 + v^2 + a^2}, \frac{2a^2v}{u^2 + v^2 + a^2}, a \frac{u^2 + v^2 - a^2}{u^2 + v^2 + a^2} \right)
$$

去掉北极的球面表示

## Figure & Layout Description
图片为手写数学推导笔记，背景是浅米色方格纸（网格线为浅灰色，形成均匀正方形网格）。所有文字和公式均用黑色墨水书写，字迹工整清晰。内容从上至下垂直排列，分为7个逻辑区块：1) 序号"②"和标题"用球极投影坐标参数表示球面"（位于顶部，字体略大）；2) 向量形式的参数方程；3) 坐标展开表达式（含两行等式）；4) 球面方程约束条件；5) 代入后的代数推导过程（共4行递进式等式）；6) 交点分析与最终坐标参数表达式（含两行等式，第二行是简化形式）；7) 结论性语句"去掉北极的球面表示"（位于底部）。公式中的下标（如$u^2$）、分式结构（如$\frac{2a^2}{u^2+v^2+a^2}$）和向量符号（$\vec{r}$）均清晰可辨。整体布局严格遵循方格纸的网格对齐，无图形元素、无彩色标记，仅包含纯文本和数学符号。

<CTX>
{
   "topic": "球极投影坐标参数化的代数推导与奇异性分析",
   "keywords": ["球极投影", "坐标参数化", "代数推导", "投影公式", "分母奇异性", "北极点排除"],
   "summary": "本页完成球极投影显式参数表达式的严格代数推导，明确给出坐标映射公式并揭示分母奇异性对应北极点的几何排除机制",
   "pending_concepts": ["极点奇异性处理方案", "多参数片拼接的连续性条件", "投影映射的逆过程推导"]
}
</CTX>

---

# Slide 40

## 旋转曲面的参数表示

设 $(x(u), z(u))$ 是平面 $xoz$ 内一条曲线  
令 $x(u) = f(u)$, $z(u) = g(u)$  

让平面曲线 $(f(u), g(u))$ 绕 $z$ 轴旋转  
$$
\begin{aligned}
x &= f(u)\cos v \\
y &= f(u)\sin v \\
z &= g(u)
\end{aligned}
$$
$$
\vec{r}(u,v) = \bigl( f(u)\cos v,\ f(u)\sin v,\ g(u) \bigr)
$$

### 特例

(1) $f(u) = 1$, $g(u) = u$  
$$
\vec{r}(u,v) = (\cos v,\ \sin v,\ u) \quad \begin{cases} x^2 + y^2 = 1 \\ z = u \end{cases} \quad \text{圆柱面}
$$

(2) $f(u) = u$, $g(u) = u$  
$$
\vec{r}(u,v) = (u\cos v,\ u\sin v,\ u) \implies x^2 + y^2 = z^2 \quad \text{圆锥面}
$$

(3) $f(u) = R + r\cos u$, $g(u) = r\sin u$  
$$
\vec{r}(u,v) = \bigl( (R + r\cos u)\cos v,\ (R + r\cos u)\sin v,\ r\sin u \bigr)
$$
环

## Figure & Layout Description

页面背景为浅黄色方格纸，所有内容以手写形式呈现。主体文字使用黑色墨水书写，关键公式和坐标轴标注使用蓝色墨水。页面右侧包含三个示意图：  
1. 顶部为三维坐标系图，$z$ 轴垂直向上，$x$ 轴向左下方延伸，$y$ 轴向右下方延伸。蓝色曲线表示原始平面曲线 $(f(u), g(u))$，虚线圆环表示绕 $z$ 轴旋转形成的曲面轮廓，标注有旋转角 $v$。  
2. 中部右侧为圆柱面简图，显示一个标准直立圆柱体，底面和顶面为圆形，侧面垂直于底面。  
3. 底部右侧为环面简图，呈现圆环状结构，中心有空洞，标注坐标轴方向。  

文字内容按逻辑分层排列：标题 "e.g. 旋转曲面的参数表示" 位于顶部，推导过程在左侧纵向排列，特例部分通过编号 (1)(2)(3) 依次展开，每个特例右侧配有对应几何体的简图。公式部分使用蓝色墨水书写，与黑色文字形成视觉对比。坐标系图中，$x,y,z$ 轴用箭头明确指示方向，旋转曲面用虚线表示动态过程。

<CTX>
{
   "topic": "旋转曲面的参数表示方法与典型实例",
   "keywords": ["旋转曲面", "参数方程", "圆柱面", "圆锥面", "环面", "绕轴旋转"],
   "summary": "本页系统讲解旋转曲面的参数化方法，通过绕z轴旋转平面曲线推导一般参数方程，并给出圆柱面、圆锥面和环面的典型实例",
   "pending_concepts": ["旋转曲面的切平面与法向量计算", "参数化中的奇异性分析", "不同旋转轴的参数化差异"]
}
</CTX>

---

# Slide 41

④ $f(u) = \cos u$, $g(u) = \sin u$

$\vec{r}(u,v) = (\cos u \cos v, \cos u \sin v, \sin u)$

球面

## 2. 切平面和法向

考虑曲面 $S: \vec{r}(u,v) = (X(u,v), Y(u,v), Z(u,v)), (u,v) \in D$.

设 $P = P(u,v) \in S$

$P$ 点位置向量为 $\vec{r}(u,v)$

固定 $u = a$, 则 $\vec{r}(a,v)$ 是一条空间曲线

$\vec{r}(u,v)$ 在 $v = b$ 处的切向量为
$$\vec{r}_v(a,b) = \frac{\partial \vec{r}(u,v)}{\partial v}\bigg|_{v=b} = \frac{\partial \vec{r}}{\partial v}(a,b)$$
且与 $S$ 在点 $P_0$ 处相切 $P_0 = P(a,b)$

固定 $v = b$, 则 $\vec{r}(u,b)$ 是一条空间曲线, $u$ 变叫 $u$ 曲线

$\vec{r}(u,b)$ 在 $u = a$ 处的切向量为
$$\vec{r}_u(a,b) = \frac{\partial \vec{r}(u,b)}{\partial u}\bigg|_{u=a} = \frac{\partial \vec{r}}{\partial u}(a,b)$$
且与 $S$ 在点 $P_0$ 处相切 $P_0 = P(a,b)$

$\vec{r}_u$ 与 $\vec{r}_v$ 坐标切向量, $\vec{n} = \vec{r}_u \times \vec{r}_v$ 法向量, 所在直线 法线

正则即 $\vec{r}_u$ 与 $\vec{r}_v$ 线性无关, 张成切平面 $T_{P_0}S$

$\{P_0: \vec{r}_u, \vec{r}_v, \vec{r}_u \times \vec{r}_v\}$ 右手正交标架

## Figure & Layout Description

该PPT页面为手写数学笔记风格，背景为浅色方格纸。页面顶部左侧有带圈数字"④"，其右侧是关于球面参数方程的定义，包含函数$f(u)$和$g(u)$的表达式及向量函数$\vec{r}(u,v)$的完整表示，下方标注"球面"二字。

页面主体部分以"2. 切平面和法向"为二级标题，详细阐述曲面切平面与法向量的理论。文字内容为黑色手写体，公式清晰规范。右侧附有手绘曲面示意图，图中用黑色线条勾勒出曲面轮廓，蓝色标注"u=a, 称v曲线 $\vec{r}(a,v)$"，红色标注"v=b, 称为u曲线 $\vec{r}(u,b)$"。图中还用箭头标示了切向量$\vec{r}_u$、$\vec{r}_v$和法向量$\vec{n}=\vec{r}_u\times\vec{r}_v$，并标注"切平面"位置。示意图旁边有橙色手写注释"法向量"。

整体布局为左文右图结构，文字部分占据约2/3页面，图形部分占据右侧1/3。公式与文字混排，重要概念用不同颜色标注（右侧图示中的蓝色和红色标注），形成清晰的视觉层次。页面底部有"右手正交标架"的结论性描述。

<CTX>
{
   "topic": "曲面的切平面与法向量理论",
   "keywords": ["切平面", "法向量", "坐标切向量", "正则曲面", "右手正交标架"],
   "summary": "本页深入讲解曲面切平面与法向量的定义、计算方法及几何意义，阐述了坐标切向量与切平面的关系",
   "pending_concepts": ["曲面的第一基本形式", "高斯曲率与平均曲率", "曲面的第二基本形式", "参数化曲面的度量性质"]
}
</CTX>

---

# Slide 42

[无可见文本内容]

## Figure & Layout Description
图片为纯白色背景，覆盖有浅灰色的正方形网格线，形成规则的方格阵列。网格线均匀分布，横向与纵向线条数量大致相等（目测约15×20个方格），每个方格呈标准正方形，边长约1.5厘米。页面中无任何文字、公式、图形、图标或颜色填充区域，仅包含单一的浅灰色网格线作为视觉元素。布局上无标题区、内容区或页脚等典型PPT结构划分，整体呈现标准的坐标纸样式，无层级关系或重点突出区域。所有网格线粗细一致（约0.1毫米），颜色为浅灰色（RGB: #E0E0E0），与白色背景（RGB: #FFFFFF）形成低对比度视觉效果。

<CTX>
{
   "topic": "曲面的切平面与法向量理论",
   "keywords": ["切平面", "法向量", "坐标切向量", "正则曲面", "右手正交标架"],
   "summary": "本页为空白网格页，未提供新的内容或知识增量",
   "pending_concepts": ["曲面的第一基本形式", "高斯曲率与平均曲率", "曲面的第二基本形式", "参数化曲面的度量性质"]
}
</CTX>

---

# Slide 43

## Figure & Layout Description
页面为纯白色背景，覆盖由浅灰色细实线构成的均匀网格。网格线横向与纵向等距分布，形成规则的正方形小格，横向约20列，纵向约30行。无任何文字、图形、符号或装饰性元素，整体呈现标准坐标纸样式，适用于几何图形绘制或参数化曲面的可视化标注。网格线宽约0.5pt，颜色为#E0E0E0，与白色背景形成低对比度视觉层次。

<CTX>
{
   "topic": "曲面的切平面与法向量理论",
   "keywords": ["切平面", "法向量", "坐标切向量", "正则曲面", "右手正交标架"],
   "summary": "本页为空白网格页，未提供新的内容或知识增量",
   "pending_concepts": ["曲面的第一基本形式", "高斯曲率与平均曲率", "曲面的第二基本形式", "参数化曲面的度量性质"]
}
</CTX>

---

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

---

# Slide 45

## §3.3 曲面的第二基本形式

设曲面 $ S: \mathbf{r} = \mathbf{r}(u,v),\ (u,v) \in D \subset \mathbb{R}^2 $

$$
I = E \, du \, du + 2F \, du \, dv + G \, dv \, dv
$$

**平面**: $ \mathbf{r}(u,v) = (u, v, C) $

$$
I = du \, du + dv \, dv
$$

**柱面**: $ \mathbf{r}(x(u), y(u), v) $

$$
I = du \, du + dv \, dv
$$

$$
I = [x'^2 + y'^2] \, du \, du + dv \, dv
$$

$ u $ 是弧长参数，$ \mathbf{r}_u $ 单位向量  
简化 $ I(u,v) = du \, du + dv \, dv $

设曲面 $ S: \mathbf{r} = \mathbf{r}(u,v),\ (u,v) \in D $，$ \mathbf{r}_u, \mathbf{r}_v $ 是 $ S $ 的坐标切向量

$$
\vec{n} = \frac{\mathbf{r}_u \times \mathbf{r}_v}{|\mathbf{r}_u \times \mathbf{r}_v|} \quad \text{是 } S \text{ 的单位法向量}
$$

曲面第二基本形式定义为

$$
II = -\langle d\mathbf{r}, d\vec{n} \rangle = \langle d^2\mathbf{r}, \vec{n} \rangle
$$

## Figure & Layout Description

图片为手写数学笔记，背景为浅米色方格纸（1cm×1cm网格）。文字以黑色墨水书写，整体布局呈纵向排列，分为四个逻辑区块：

1. **标题区块**：顶部居中书写"§3.3 曲面的第二基本形式"，字体稍大且加粗，下方有横线分隔
2. **定义区块**：包含曲面参数化定义和第一基本形式通用表达式，公式采用居中排版，使用标准微分符号
3. **示例区块**：包含"平面"和"柱面"两个具体案例，每个案例包含参数化表达式和对应的第一基本形式计算，案例标题使用加粗字体
4. **理论区块**：底部详细定义第二基本形式，包含单位法向量公式和第二基本形式的两种等价表达式

文字书写工整但带有手写特征，部分连笔（如"柱面"的"柱"字），公式中微分符号"du"与"dv"间距均匀，向量符号使用箭头标注（如$\vec{n}$）。整体排版遵循"定义→示例→理论"的递进结构，关键公式均单独成行居中显示。

<CTX>
{
   "topic": "曲面的第二基本形式理论",
   "keywords": ["第二基本形式", "单位法向量", "坐标切向量", "曲面弯曲度量", "LME系数", "弧长参数"],
   "summary": "本页建立曲面第二基本形式的数学定义，通过单位法向量与二阶微分描述曲面弯曲特性，完善曲面微分几何的度量体系",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的测地线理论", "曲面的黎曼度量", "第二基本形式的几何意义"]
}
</CTX>

---

# Slide 46

How?

$\langle Y_u, \vec{n} \rangle = 0$ $\langle Y_v, \vec{n} \rangle = 0$

$\langle Y_{uu}, \vec{n} \rangle + \langle Y_u, \vec{n}_u \rangle = 0$ $\langle Y_{vv}, \vec{n} \rangle + \langle Y_v, \vec{n}_v \rangle = 0$

$\langle Y_{uv}, \vec{n} \rangle + \langle Y_u, \vec{n}_v \rangle = 0$ $\langle Y_{vv}, \vec{n} \rangle + \langle Y_v, \vec{n}_v \rangle = 0$

令 $L = \langle Y_{uu}, \vec{n} \rangle = -\langle Y_u, \vec{n}_u \rangle$

$M = \langle Y_{uv}, \vec{n} \rangle = -\langle Y_u, \vec{n}_v \rangle = -\langle Y_v, \vec{n}_u \rangle$

$N = \langle Y_{vv}, \vec{n} \rangle = -\langle Y_v, \vec{n}_v \rangle$

$$
\begin{aligned}
\mathrm{I\!I} &= -\langle d\mathbf{r}, d\mathbf{n} \rangle \\
&= -\langle Y_u du + Y_v dv, n_u du + n_v dv \rangle \\
&= -\langle Y_u, n_u \rangle du^2 - \left( \langle Y_u, n_v \rangle + \langle Y_v, n_u \rangle \right) du dv - \langle Y_v, n_v \rangle dv^2 \\
&= L du^2 + 2M du dv + N dv^2
\end{aligned}
$$

$L, M, N$ 是曲面 $S$ 第二基本量

$\mathrm{I\!I}(du, dv) = \mathrm{I\!I}(d\mathbf{r})$

**第二基本形式的几何意义**

设曲面 $S: \mathbf{r} = Y(u, v),\ (u, v) \in D$,
考虑 $\vec{Y}$ 在 $(u_0, v_0)$ 的 Taylor 展开

## Figure & Layout Description
图片背景为浅黄色方格纸，网格线为浅灰色细线。所有内容以黑色手写体呈现，字迹工整且具有教学板书特征。页面顶部左侧有手写体"How?"作为引导问题。主体内容由多组微分几何公式构成，分为三部分：第一部分是四个关于单位法向量 $\vec{n}$ 与坐标切向量内积的等式，左右对称排列；第二部分定义了第二基本量 $L, M, N$，采用"令"字引导的说明式结构；第三部分推导第二基本形式 $\mathrm{I\!I}$ 的展开式，包含四行递进的等式推导。关键项如 $Y_{uu}$ 和 $Y_{uv}$ 有波浪线标记强调，"第二基本形式的几何意义"标题使用下划线突出。公式中向量符号统一使用箭头标记（如 $\vec{n}$），微分符号 $du, dv$ 采用斜体排版。底部有中文注释说明曲面参数化和Taylor展开的应用场景，整体布局符合数学推导的逻辑递进结构。

<CTX>
{
   "topic": "曲面第二基本形式的几何意义",
   "keywords": ["第二基本形式", "单位法向量", "坐标切向量", "曲面弯曲度量", "LME系数", "Taylor展开"],
   "summary": "本页通过Taylor展开揭示第二基本形式的几何意义，建立曲面局部弯曲与二阶微分的直观联系",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的测地线理论", "曲面的黎曼度量", "曲面局部展开的几何应用"]
}
</CTX>

---

# Slide 47

$$
\Delta \vec{Y} = \vec{Y}(u_0 + \Delta u, v_0 + \Delta v) - \vec{Y}(u_0, v_0)
$$
$$
= Y_u \Delta u + Y_v \Delta v + \frac{1}{2} \left( Y_{uu} \Delta u^2 + 2 Y_{uv} \Delta u \Delta v + Y_{vv} \Delta v^2 \right) + O(P^2)
$$
$$
O(\Delta u^2 + \Delta v^2)
$$

$$
\langle \vec{n}(u_0, v_0), \Delta \vec{Y} \rangle = \langle \vec{n}, Y_u \rangle \Delta u + \langle \vec{n}, Y_v \rangle \Delta v 
$$
$$
+ \frac{1}{2} \left( \langle \vec{n}, Y_{uu} \rangle \Delta u^2 + 2 \langle \vec{n}, Y_{uv} \rangle \Delta u \Delta v + \langle \vec{n}, Y_{vv} \rangle \Delta v^2 \right)
$$
$$
+ \langle \vec{n}, O(\Delta u^2 + \Delta v^2) \rangle
$$

$$
\lim_{\Delta u^2 + \Delta v^2 \to 0} \frac{\langle \vec{n}, O(\Delta u^2 + \Delta v^2) \rangle}{\Delta u^2 + \Delta v^2} = 0 \quad \text{因为 } O(\Delta u^2 + \Delta v^2) \text{ 比 } \Delta u^2 + \Delta v^2 \text{ 更高阶}
$$
$$
\lim_{\Delta u^2 + \Delta v^2 \to 0} \frac{O(\Delta u^2 + \Delta v^2)}{\Delta u^2 + \Delta v^2} = 0
$$
$$
\text{故 } \langle \vec{n}, O(\Delta u^2 + \Delta v^2) \rangle = O(\Delta u^2 + \Delta v^2)
$$

## Figure & Layout Description

图片采用米黄色方格纸背景，整体布局分为上下两部分。上半部分为手写数学推导，下半部分为几何示意图。

**公式区域**（占据上半部分）：
- 顶部起始公式为 $\Delta \vec{Y} = \vec{Y}(u_0 + \Delta u, v_0 + \Delta v) - \vec{Y}(u_0, v_0)$
- 第二行展开式包含一阶项 $Y_u \Delta u + Y_v \Delta v$ 和二阶项 $\frac{1}{2} (Y_{uu} \Delta u^2 + 2 Y_{uv} \Delta u \Delta v + Y_{vv} \Delta v^2)$
- 第三行标注 $O(P^2)$，其中 $P$ 为斜体大写字母
- 第四行单独标注 $O(\Delta u^2 + \Delta v^2)$，垂直对齐于第三行下方

**几何示意图**（位于中部，占据图片中心区域）：
- 用黑色粗线绘制三维曲面，呈现碗状凹陷结构
- 曲面底部标注 $\vec{Y}(u_0, v_0)$，顶部边缘标注 $\vec{Y}(u_0 + \Delta u, v_0 + \Delta v)$
- 从曲面底部引出蓝色向量 $d\vec{Y}$ 指向顶部点
- 红色向量 $\Delta \vec{Y}$ 垂直于切平面，标注为"法向量"
- 黑色向量 $\vec{n}(u_0, v_0)$ 从曲面点垂直向上，标注"单位法向量"
- 蓝色平面标注为 $T_p S$（切平面），平面内有橙色小向量标注"切向量"
- 切平面与曲面交界处有橙色标注 $\frac{d\vec{Y}}{dt} dt$

**下部公式区域**：
- 以 $\langle \vec{n}(u_0, v_0), \Delta \vec{Y} \rangle$ 为起始的内积展开式
- 包含一阶项、二阶项和余项
- 余项极限分析部分包含两行极限表达式
- 最终结论行以"故"开头，推导出余项阶数关系

**颜色与标注**：
- 主要使用黑色墨水书写公式和轮廓
- 关键向量用蓝色（$d\vec{Y}$）和红色（$\Delta \vec{Y}$）突出
- 橙色标注用于"切向量"和微分符号
- 所有文字均为手写体，字迹清晰但带有书写痕迹

## Figure & Layout Description

<CTX>
{
   "topic": "第二基本形式的余项分析与法向分量提取",
   "keywords": ["第二基本形式", "单位法向量", "Taylor展开", "余项阶数", "曲面局部弯曲"],
   "summary": "本页通过法向量与位移向量的内积分析，严格证明第二基本形式中余项的高阶小量性质，揭示曲面弯曲度量的二阶微分本质",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的测地线理论", "曲面的黎曼度量", "曲面局部展开的几何应用"]
}
</CTX>

---

# Slide 48

故

$$ \langle \vec{n}_{(u_0,v_0)}, \Delta \vec{r} \rangle = \frac{1}{2} \left( \langle \vec{n}, \vec{r}_{uu} \rangle \Delta u^2 + 2 \langle \vec{n}, \vec{r}_{uv} \rangle \Delta u \Delta v + \langle \vec{n}, \vec{r}_{vv} \rangle \Delta v^2 \right) + O(\Delta u^2 + \Delta v^2) $$

设为 $\delta := \langle \vec{n}, \Delta \vec{r} \rangle$

$\delta$ 是到切平面的有向距离

$\delta > 0$, $\Delta \vec{r}$ 指向 $\vec{n}$ 同侧

$\delta < 0$, $\Delta \vec{r}$ 指离 $\vec{n}$ 同侧

$\Delta u^2 + \Delta v^2$ 充分小时

$$ \delta = \frac{1}{2} \left( L \, du \, du + 2M \, du \, dv + N \, dv \, dv \right) = \frac{1}{2} \text{II}(d\mathbf{r}) $$

几何意义：沿着某个方向，离开切平面的程度

e.g. 3.1

柱面 $\vec{r} = (x(u), y(u), v)$, $u$ 是弧长参数 $x_u^2 + y_u^2 = 1$

$\vec{r}_u = (x_u, y_u, 0)$  
$\vec{r}_v = (0, 0, 1)$  
$\vec{n} = \frac{\vec{r}_u \times \vec{r}_v}{|\vec{r}_u \times \vec{r}_v|} = \begin{vmatrix} i & j & k \\ x_u & y_u & 0 \\ 0 & 0 & 1 \end{vmatrix} = (y_u, -x_u, 0)$

$\vec{r}_{uu} = (x_{uu}, y_{uu}, 0)$  
$\vec{r}_{uv} = \vec{r}_{vu} = (0, 0, 0)$  
$\vec{r}_{vv} = (0, 0, 0)$

## Figure & Layout Description
图片为手写数学推导内容，背景是浅黄色方格纸（1cm×1cm网格）。文字以黑色墨水书写，关键符号"δ"用蓝色墨水突出标注。整体布局为垂直流式结构：顶部是"故"字引导的行间公式；其下是"设为"定义行，其中"δ"符号为蓝色；接着是四行文本说明，包含δ的几何意义和符号条件；随后是"Δu²+Δv²充分小时"的条件说明；再下方是第二行间公式；接着是"几何意义"的说明行；最后是"e.g. 3.1"示例部分，包含柱面参数化定义和多行向量计算。公式中的向量符号（如$\vec{n}$）均带有箭头标记，行列式使用标准三阶矩阵表示，所有下标（如$uu$, $uv$）清晰可辨。页面无标题栏或页脚，所有内容集中在方格纸中央区域，文字密度适中，行间距约1.5个网格高度。蓝色标注仅出现在"δ"符号处，用于强调核心变量，形成视觉焦点。

<CTX>
{
   "topic": "第二基本形式的几何意义与柱面实例验证",
   "keywords": ["第二基本形式", "有向距离", "法向分量", "柱面参数化", "曲面弯曲度量"],
   "summary": "本页通过有向距离δ的定义阐明第二基本形式的几何本质，并以柱面为例完成具体计算，验证了曲面局部弯曲的二阶微分特性",
   "pending_concepts": ["高斯曲率与平均曲率", "曲面的测地线理论", "曲面的黎曼度量", "曲面局部展开的几何应用"]
}
</CTX>

---

# Slide 49

$$
L = \langle \gamma_{uu}, \vec{n} \rangle = x_{uu}y_u - y_{uu}x_u = -k
$$
$$
M = \langle \gamma_{uv}, \vec{n} \rangle = 0
$$
$$
N = \langle \gamma_{vv}, \vec{n} \rangle = 0
$$
$$
\mathrm{II} = -k\,du^2
$$

圆柱面：$(x(u), y(u))$ 为圆 $k = \frac{1}{a}$  
$$
\mathrm{II} = -\frac{1}{a}\,du^2
$$

$$
\gamma(u,v) = (u, v, c)
$$
$$
\gamma_u = (1, 0, 0),\ \gamma_v = (0, 1, 0),\ \vec{n} = \frac{\gamma_u \times \gamma_v}{|\gamma_u \times \gamma_v|} = \frac{\begin{vmatrix} i & j & k \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{vmatrix}}{1} = (0, 0, 1)
$$
$$
\gamma_{uu} = 0,\ \gamma_{uv} = 0,\ \gamma_{vv} = 0
$$
$$
L = 0,\ M = 0,\ N = 0
$$
$$
\mathrm{II} = 0
$$

球面：$\gamma(\theta,\varphi) = (r\cos\theta\cos\varphi,\ r\cos\theta\sin\varphi,\ r\sin\theta)$  
$$
\gamma_\theta = (-r\sin\theta\cos\varphi,\ -r\sin\theta\sin\varphi,\ r\cos\theta)
$$
$$
\gamma_\varphi = (-r\cos\theta\sin\varphi,\ r\cos\theta\cos\varphi,\ 0)
$$

## Figure & Layout Description  
手写内容书写于浅黄色方格纸背景上，黑色墨水书写。内容按垂直顺序分为四个逻辑区块：  
1. 顶部区块：包含第二基本形式系数 $L, M, N$ 的定义式及 $\mathrm{II}$ 的表达式，公式以等号对齐方式排列，其中 $L$ 的定义式包含行列式展开结构  
2. 中上区块：标注"圆柱面："的标题行，后接圆周曲率 $k=1/a$ 的说明及对应的 $\mathrm{II}$ 表达式  
3. 中部区块：柱面参数化 $\gamma(u,v)$ 的向量表示，包含 $\gamma_u, \gamma_v$ 的坐标向量、法向量 $\vec{n}$ 的行列式计算过程（含矩阵表示）及二阶导数为零的结论  
4. 底部区块：标注"球面："的标题行，后接球面参数化表达式及 $\gamma_\theta, \gamma_\varphi$ 的偏导向量计算  
所有公式均采用手写体数学符号，下标通过位置偏移表示，向量符号用箭头标注。文字与公式混合排版，关键结论（如 $\mathrm{II}=0$）单独成行突出显示。

<CTX>
{
   "topic": "第二基本形式在柱面与球面的实例验证",
   "keywords": ["第二基本形式", "柱面参数化", "球面参数化", "曲率计算", "法向量推导"],
   "summary": "通过柱面和球面的具体参数化计算，验证了第二基本形式在不同曲面上的表现形式及曲率特性",
   "pending_concepts": ["球面的高斯曲率计算", "测地线方程推导", "曲面第一基本形式与第二基本形式的关联"]
}
</CTX>

---

# Slide 50

$$Y_\theta \wedge Y_\varphi = \left( r^2 \cos^2\theta \cos\varphi,\ r^2 \cos^2\theta \sin\varphi,\ -r^2 \sin\theta \cos\theta \cos^2\varphi - r^2 \sin\theta \cos\theta \sin^2\varphi - r^2 \sin\theta \cos\theta \right)$$

$$|Y_\theta \wedge Y_\varphi| = r^2 \cos\theta \sqrt{1} = r^2 \cos\theta$$

$$\vec{n} = \left( \cos\theta \cos\varphi,\ \cos\theta \sin\varphi,\ \sin\theta \right)$$

$$Y_\theta = \left( -r \sin\theta \cos\varphi,\ -r \sin\theta \sin\varphi,\ r \cos\theta \right)$$

$$Y_\varphi = \left( -r \cos\theta \sin\varphi,\ r \cos\theta \cos\varphi,\ 0 \right)$$

$$Y_{\theta\theta} = \left( -r \cos\theta \cos\varphi,\ -r \cos\theta \sin\varphi,\ -r \sin\theta \right)$$

$$Y_{\theta\varphi} = \left( r \sin\theta \sin\varphi,\ -r \sin\theta \cos\varphi,\ 0 \right)$$

$$Y_{\varphi\varphi} = \left( -r \cos\theta \cos\varphi,\ -r \cos\theta \sin\varphi,\ 0 \right)$$

$$L = \langle \vec{n}, Y_{\theta\theta} \rangle = -r \cos^2\theta \cos^2\varphi - r \cos^2\theta \sin^2\varphi - r \sin^2\theta = -r$$

$$M = \langle \vec{n}, Y_{\theta\varphi} \rangle = r \sin\theta \cos\theta \sin\varphi \cos\varphi - r \sin\theta \cos\theta \sin\varphi \cos\varphi = 0$$

$$N = \langle \vec{n}, Y_{\varphi\varphi} \rangle = -r \cos^2\theta \cos^2\varphi - r \cos^2\theta \sin^2\varphi = -r \cos^2\theta$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，所有内容以黑色墨水书写。公式从上至下垂直排列，共包含9组核心公式。其中$\vec{n}$向量表达式和$Y_{\theta\theta}$向量表达式下方有红色下划线标注重点。第一组公式展示叉乘结果，第二组计算其模长，第三组定义单位法向量，后续依次列出切向量、二阶偏导向量及第二基本形式系数计算。公式间存在分步推导关系，如模长计算先显示中间步骤再简化结果。手写体清晰但存在连笔现象，例如$\theta$与$\varphi$的区分需结合上下文判断。背景方格线为浅灰色，每行公式占据约2-3个方格高度，整体布局紧凑但层次分明。

<CTX>
{
   "topic": "球面第二基本形式系数的显式计算",
   "keywords": ["第二基本形式系数", "单位法向量", "二阶偏导向量", "曲面曲率计算"],
   "summary": "通过球面参数化显式计算出第二基本形式系数L=-r, M=0, N=-r cos²θ，为后续高斯曲率推导奠定基础",
   "pending_concepts": ["高斯曲率与第二基本形式的关系", "球面测地线的几何特性", "曲面嵌入欧氏空间的曲率性质"]
}
</CTX>

---

# Slide 51

$$ \text{II} = -r \, d\theta^2 + 0 - r \cos^2\theta \, d\phi^2. $$

**性质**：设 $ r(u,v) $ 和 $ r(\tilde{u},\tilde{v}) $ 是曲面 $ S $ 的两个不同参数表示，  
若 $ \sigma: (\tilde{u},\tilde{v}) \to (u,v) $ 是同向参数变换，则 $ \text{II}(d\tilde{u},d\tilde{v}) = \text{II}(du,dv) $.  
~ 反向 ~ ，则 $ \text{II}(d\tilde{u},d\tilde{v}) = -\text{II}(du,dv) $.

**证**：对于参数变换 $ \sigma: (\tilde{u},\tilde{v}) \to (u,v) $  
$$ r_{\tilde{u}} \wedge r_{\tilde{v}} = \frac{\partial(\tilde{u},\tilde{v})}{\partial(u,v)} \, r_u \wedge r_v $$

若 $ J > 0 $，  
$$ \vec{n}(u,v) = \vec{n}(\tilde{u},\tilde{v}) = \frac{r_u \wedge r_v}{|r_u \wedge r_v|} $$  
$$ \text{II}(du,dv) = -\langle dr(u,v), dn(u,v) \rangle $$  
$$ \quad = -\langle dr(\tilde{u},\tilde{v}), dn(\tilde{u},\tilde{v}) \rangle $$  
$$ \quad = \text{II}(d\tilde{u},d\tilde{v}) $$

若 $ J < 0 $，  
$$ \vec{n}(u,v) = -\vec{n}(\tilde{u},\tilde{v}) $$  
$$ \text{II}(du,dv) = -\langle dr(u,v), dn(u,v) \rangle $$  
$$ \quad = -\langle dr(\tilde{u},\tilde{v}), -dn(\tilde{u},\tilde{v}) \rangle $$  
$$ \quad = -\text{II}(d\tilde{u},d\tilde{v}) $$

## Figure & Layout Description
图片为方格纸背景的手写数学笔记，整体布局为自上而下的垂直排列结构。顶部是第二基本形式的显式表达式，使用黑色墨水书写，公式中包含希腊字母 $ \theta $、$ \phi $ 及三角函数 $ \cos^2\theta $。中部为"性质"段落，用中文说明参数变换对第二基本形式的影响，其中"同向"和"反向"两词被波浪线标注强调。下部为"证"明部分，分为两栏逻辑推导：左侧为雅可比行列式关系式，右侧通过条件分支（$ J>0 $ 和 $ J<0 $）展开证明，包含向量外积符号 $ \wedge $、内积符号 $ \langle \cdot, \cdot \rangle $ 及法向量 $ \vec{n} $ 的方向变化。所有公式与文字均采用手写体，字迹清晰，部分符号（如 $ \tilde{u} $）使用波浪线标注，整体排版紧凑但层次分明，关键推导步骤通过等号对齐保持视觉连贯性。

<CTX>
{
   "topic": "第二基本形式的参数变换性质",
   "keywords": ["参数变换", "同向/反向", "雅可比行列式", "单位法向量方向"],
   "summary": "阐述第二基本形式在参数变换下的符号变化规律，建立曲面几何量的坐标变换理论基础",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>

---

# Slide 52

性质 2：设曲面 $S: \mathbf{r} = \mathbf{r}(u,v), (u,v) \in D$，  
↑: 合同变换  
↑ 把 $S$ 变为 $\tilde{S}: \tilde{\mathbf{r}}(u,v) = \tilde{T} \circ \mathbf{r}(u,v) = \mathbf{r}(u,v)T + P_0$  
记 $II$ 和 $\tilde{II}$ 分别是 $S$ 和 $\tilde{S}$ 的第二基本形式  
若 $\tilde{T}$ 是刚体运动，$II = \tilde{II}$  
若 $\tilde{T}$ 是反向刚体运动，$II = -\tilde{II}$  
$\tilde{II} = -\langle d\tilde{\mathbf{r}}, d\tilde{\mathbf{n}} \rangle$  
证：$\tilde{\mathbf{r}}_u = \mathbf{r}_u T$, $\tilde{\mathbf{r}}_v = \mathbf{r}_v T$, $\tilde{T}_0(x) = xT$  
$\tilde{\mathbf{r}}_u \wedge \tilde{\mathbf{r}}_v = \mathbf{r}_u T \wedge \mathbf{r}_v T = \tilde{T}_0(\mathbf{r}_u) \wedge \tilde{T}_0(\mathbf{r}_v)$  
$= \det(T) \tilde{T}_0(\mathbf{r}_u \wedge \mathbf{r}_v)$  
$= \det(T) (\mathbf{r}_u \wedge \mathbf{r}_v) T$  
$|\tilde{\mathbf{r}}_u \wedge \tilde{\mathbf{r}}_v| = |\det(T) (\mathbf{r}_u \wedge \mathbf{r}_v) T|$  
$= |(\mathbf{r}_u \wedge \mathbf{r}_v) T| = \sqrt{\langle (\mathbf{r}_u \wedge \mathbf{r}_v)T, (\mathbf{r}_u \wedge \mathbf{r}_v)T \rangle}$  
$= (\mathbf{r}_u \wedge \mathbf{r}_v) T T^\top (\mathbf{r}_u \wedge \mathbf{r}_v)^\top$  
$= (\mathbf{r}_u \wedge \mathbf{r}_v) (\mathbf{r}_u \wedge \mathbf{r}_v)^\top = |\mathbf{r}_u \wedge \mathbf{r}_v|$

## Figure & Layout Description
手写笔记内容书写在浅米色方格纸背景上，网格线为浅灰色细线。文字以黑色墨水书写，整体呈竖直排列结构。顶部以较大字号书写"性质2："作为标题，其后接曲面定义公式。中间部分用"↑"符号引导的两行说明合同变换操作，字体略小于标题但大于正文。核心结论部分使用标准字号，分两行说明刚体运动与反向刚体运动对第二基本形式的影响。证明部分从"证："开始，采用多行对齐格式，每行公式通过等号对齐，其中向量符号$\mathbf{r}$和变换符号$T$保持统一书写风格。所有公式中的外积符号"$\wedge$"清晰可辨，行列式符号"$\det$"书写完整。证明过程末尾的范数计算步骤占据页面下半部分，通过多行推导展示模长不变性。整体布局呈现典型的课堂笔记特征：重点内容通过字号差异突出，推导过程按逻辑顺序垂直排列，无额外图形元素。

<CTX>
{
   "topic": "第二基本形式在合同变换下的符号变化规律",
   "keywords": ["合同变换", "刚体运动", "反向刚体运动", "雅可比行列式", "外积模长"],
   "summary": "阐明第二基本形式在刚体运动下保持不变、在反向刚体运动下符号取反的特性，并通过外积推导验证模长不变性",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>

---

# Slide 53

$$\tilde{n} = \frac{\tilde{Y}_u \wedge \tilde{Y}_v}{|\tilde{Y}_u \wedge \tilde{Y}_v|} = \det(T) \frac{(Y_u \wedge Y_v)T}{|Y_u \wedge Y_v|} = \det T \cdot n^T$$

$$d\tilde{n} = \det T \cdot dn^T$$

$$d\tilde{r} = dr^T$$

$$\tilde{II} = -\langle d\tilde{r}, d\tilde{n} \rangle$$
$$= -\langle dr^T, \det T \cdot dn^T \rangle$$
$$= -\det T \langle dr^T, dn^T \rangle$$
$$= -\det T \ dr^T T^T dn^T$$
$$= -\det T \ dr \ dn^T$$
$$= -\det T \ \langle dr, dn \rangle$$
$$= \det T \ II$$

故 $\det T = 1 \cdots$

$\det T = -1 \cdots$

## Figure & Layout Description
图片展示了一张浅黄色方格纸背景的手写数学推导，方格线为浅灰色，形成规则的网格布局。所有内容以黑色手写体呈现，字迹工整清晰。推导内容从上到下垂直排列，共包含12行数学表达式，分为四个逻辑区块：第一行是单位法向量的变换公式，第二、三行分别描述法向量微分和位置向量微分的变换关系，第四至第十行是第二基本形式的详细推导过程（包含7个等式步骤），最后两行是结论性陈述。公式中的向量符号（如$\tilde{n}$）带有波浪线标记，矩阵转置使用上标T表示，内积使用尖括号$\langle \cdot, \cdot \rangle$表示。整个推导过程左对齐，每行等号对齐形成清晰的逻辑链条，无额外图形或彩色标注。

<CTX>
{
   "topic": "第二基本形式在合同变换下的符号变化规律的数学推导",
   "keywords": ["合同变换", "刚体运动", "反向刚体运动", "雅可比行列式", "外积模长", "第二基本形式"],
   "summary": "通过向量外积和内积的严格推导，证明了第二基本形式在合同变换下满足$\\tilde{II} = \\det T \\cdot II$的变换规律，从而在刚体运动下保持不变，在反向刚体运动下符号取反",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>

---

