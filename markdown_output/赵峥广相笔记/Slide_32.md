# Slide 32

## §2.6 测地线的仿射参量  
测地线 ②自平行线  

### 曲线空间的曲线参数方程 $x^\mu = x^\mu(\lambda)$  
切矢 $A^\mu = \frac{dx^\mu}{d\lambda}$  

$A^\mu(P) \xrightarrow{\alpha} A^\mu(0)$  
$P(\lambda)$ $\quad$ $x^\mu + dx^\mu$  

要求 $A^\mu|_{P \to 0} \parallel A^\mu|_0$  

$$
\frac{A'^i(0)}{A'^i(P \to 0)} = \cdots = \frac{A'^n(0)}{A'^n(P \to 0)} = F(\lambda + d\lambda)
$$

$A^\mu(0) = A^\mu(P \to 0) \, F(\lambda + d\lambda)$  
$A^\mu(0) = A^\mu(P \to 0) \left[ F(\lambda) + \frac{dF}{d\lambda} d\lambda \right]$  
$\quad \downarrow$  
取一定为 $1$ $\quad F(\lambda) = 1$  

令 $\frac{dF}{d\lambda} = f(\lambda)$  
$A^\mu(0) = (1 + f(\lambda) d\lambda) \, A^\mu(P \to 0)$  

用 $P$ 表达 $\quad$ 定切矢  
$A^\mu(0) = A^\mu(P) + dA^\mu(P)$  
$\quad = \frac{dx^\mu}{d\lambda} + d\left[\frac{dx^\mu}{d\lambda}\right] d\lambda$  
$\quad = \frac{dx^\mu}{d\lambda} + \frac{d^2 x^\mu}{d\lambda^2} d\lambda$  

$$
A^\mu(P \to 0) = A^\mu(P) - P^\mu_{\alpha\beta} A^\alpha(P) \, dx^\beta
$$
$$
= \frac{dx^\mu}{d\lambda} - P^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} d\lambda
$$

$$
\frac{dx^\mu}{d\lambda} + \frac{d^2 x^\mu}{d\lambda^2} d\lambda = (1 + f(\lambda) d\lambda) \left[ \frac{dx^\mu}{d\lambda} - P^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} d\lambda \right]
$$

$$
\frac{dx^\mu}{d\lambda} + \frac{d^2 x^\mu}{d\lambda^2} d\lambda = \frac{dx^\mu}{d\lambda} - P^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} d\lambda + \frac{dx^\mu}{d\lambda} f(\lambda) d\lambda
$$

## Figure & Layout Description  
图片为方格纸背景的手写笔记，文字颜色统一为橙色。顶部标题行分为三部分：左侧为"§2.6 测地线的仿射参量"，中间为"测地线"，右侧为"②自平行线"。主体内容分为左右两列：  
- 左列从"曲线空间的曲线参数方程"开始，依次推导切矢定义、平行移动条件、比例系数关系，包含箭头标注（$A^\mu(P) \xrightarrow{\alpha} A^\mu(0)$）和点标注（$P(\lambda)$、$x^\mu + dx^\mu$）  
- 右列聚焦"自平行线"条件，展示比例系数 $F(\lambda)$ 的展开推导，含多层括号嵌套和注释"取一定为1"  
- 中下部为关键等式推导，左侧展示切矢微分展开式，右侧展示含 $P^\mu_{\alpha\beta}$ 的联络项表达式  
- 底部为最终等式展开，通过等号对齐呈现左右两侧的完全展开形式  
所有公式均以手写体呈现，部分符号（如 $P^\mu_{\alpha\beta}$）采用上标+双下标结构，推导过程通过箭头和缩进体现逻辑层级。方格纸网格线清晰可见，文字严格沿网格线书写，无额外图形元素。

<CTX>
{
   "topic": "测地线的仿射参量与自平行线条件推导",
   "keywords": ["仿射参量", "自平行线条件", "测地线方程", "联络系数"],
   "summary": "本页通过切矢平行移动条件推导出测地线方程，明确仿射参量下自平行线的数学表达式，建立联络系数与曲线二阶导数的联系",
   "pending_concepts": ["仿射参量的物理意义", "联络系数与引力场的对应关系", "测地线方程在弯曲时空中的具体应用"]
}
</CTX>