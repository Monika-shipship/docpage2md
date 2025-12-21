# Slide 19

## 仿射空间（一般化）

仿射 ～ 线性

$\vec{A} + \vec{B}$ 仿矢量  
$\lambda \vec{A}$ 仿矢量  
$0$ 没定义  

$x'^\mu = x'^\mu(x^\nu) \quad \nu=1,2,3,4$  
$$dx'^\mu = \left. \frac{\partial x'^\mu}{\partial x^\alpha} \right|_P dx^\alpha$$  
$\det \neq 0, \infty$  

有逆  
$$dx^\alpha = \frac{\partial x^\alpha}{\partial x'^\mu} dx'^\mu$$  
分量 $4^n$  

### 2.4 平移与联络  
$$\frac{A_\mu(P) - A_\mu(Q)}{ox^\mu} \quad \xrightarrow[\alpha x^\mu]{} \frac{A_\mu(P \to Q)}{A_\mu(\alpha)}$$  
$$A'_\mu(P) = \left. \left( \frac{\partial x^\alpha}{\partial x'^\mu} \right) \right|_P A_\alpha(P)$$  
$$\frac{A_\mu(P) - A_\mu(Q)}{ox^\mu} \quad \text{无定义}$$

## Figure & Layout Description
图片为方格纸背景的手写笔记，文字以橙色墨水书写。整体布局分为上下两部分：  
1. **上半部分**（占页面2/3）：  
   - 标题"仿射空间（一般化）"居左，字体较大且加粗  
   - 下方列出"仿射～线性"核心关系，其下分四行说明：  
     * 两行矢量运算规则（$\vec{A}+\vec{B}$和$\lambda\vec{A}$）  
     * "0没定义"单独成行  
     * 两组坐标变换公式（含微分形式），其中$dx'^\mu$公式为行间公式，用竖线标注点$P$  
     * "det≠0,∞"和"有逆"作为独立行  
     * 逆变换公式为行间公式，下方标注"分量$4^n$"  
2. **下半部分**（占页面1/3）：  
   - 以"§ 2.4 平移与联络"为小节标题  
   - 包含三个核心公式：  
     * 左侧分式表达式（分子为$A_\mu(P)-A_\mu(Q)$，分母为$ox^\mu$）  
     * 右侧联络变换公式$A'_\mu(P)=...$（行间公式）  
     * 底部重复分式并标注"无定义"  
3. **视觉特征**：  
   - 所有公式均手写，部分符号连笔（如"仿射"的"射"字）  
   - 坐标指标$\mu,\nu,\alpha$均用希腊字母  
   - "ox^\mu"中的"o"为小写字母（非零）  
   - 方格线为浅灰色，间距均匀  

<CTX>
{
   "topic": "仿射空间与联络理论基础",
   "keywords": ["仿射空间", "坐标变换", "联络", "平移", "雅可比矩阵"],
   "summary": "从仿射空间的线性性质出发，建立坐标变换的微分规则，引出联络概念以解决平移操作的数学定义问题",
   "pending_concepts": ["联络的具体数学定义", "仿射空间与黎曼几何的关系", "平移操作的物理意义", "坐标变换中雅可比矩阵的几何解释", "联络与绝对微分的衔接机制"]
}
</CTX>