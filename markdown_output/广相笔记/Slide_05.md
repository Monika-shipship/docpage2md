# Slide 5

## 坐标变换与张量定义

### 坐标变换关系
- 两个坐标系的示意图（$x$ 与 $\bar{x}$ 坐标系，标注"两坐标"）

### 定义变换矩阵
- $A = [A^\mu_\nu]$, $A^\mu_\nu = \frac{\partial \bar{x}^\mu}{\partial x^\nu}$ 的正变换
- $d\bar{x}^\mu = A^\mu_\nu dx^\nu$
- $\sim \frac{\partial \bar{x}^\mu}{\partial x^\nu} dx^\nu$ $\quad$ $x$ 是标量函数！坐标不是矢量，坐标微分是矢量

### Jacobian 行列式
- $\det A \equiv J(\bar{x}/x)$ 称为 Jacobian 行列式
- $dx^\mu = \frac{\partial x^\mu}{\partial \bar{x}^\nu} d\bar{x}^\nu$ 即 $dx^\mu = \tilde{A}^\mu_\nu d\bar{x}^\nu$

### 逆变换条件
- 若 $J \neq 0$，则有逆变换 $x^\mu = x^\mu(\bar{x}^1, \bar{x}^2, \cdots, \bar{x}^n)$, $x^\mu \equiv \bar{x}^\mu$
- 可定义 $\tilde{A}^\nu_\mu = \frac{\partial x^\nu}{\partial \bar{x}^\mu}$
- $\frac{\partial x^\mu}{\partial \bar{x}^\nu} = \delta^\mu_\nu$ 且 $\frac{\partial \bar{x}^\mu}{\partial x^\nu} \frac{\partial x^\nu}{\partial \bar{x}^\rho} = \delta^\mu_\rho$
- 可知 $\tilde{A} = [\tilde{A}^\nu_\mu]$ 为 $A$ 的逆矩阵 $\quad \tilde{A} = A^{-1}$, $A\tilde{A} = \tilde{A}A = I$

### 张量变换规则
- $\frac{dx^\mu}{ds}$, $u^\mu = \frac{dx^\mu}{ds}$ 切矢量
- 指标在上？逆变, contravariant $\quad dx^\mu = \frac{\partial x^\mu}{\partial \bar{x}^\nu} d\bar{x}^\nu = A^\mu_\nu d\bar{x}^\nu$
- 下协变 (covariant) $\quad d\bar{x}_\mu = \frac{\partial \bar{x}^\nu}{\partial x^\mu} dx_\nu = \tilde{A}^\nu_\mu dx_\nu$

### 核心规律
- **上逆下协**

### 张量分类
- **切？余切？**

#### 定义张量：
1. **零阶张量，标量**  
   $\phi'(\bar{x}) = \phi(x)$  
   在坐标变换下不变

2. **一阶张量，矢量**  
   - **A. 协变矢量**  
     $\phi'_\mu(\bar{x}) = \tilde{A}^\nu_\mu \phi_\nu(x) = \frac{\partial x^\nu}{\partial \bar{x}^\mu} \phi_\nu(x)$  
     e.g. 令 $\phi_\mu(x) = \frac{\partial \phi(x)}{\partial x^\mu}$, $\phi'_\mu(\bar{x}) = \frac{\partial \phi'(\bar{x})}{\partial \bar{x}^\mu} = \frac{\partial \phi(x)}{\partial x^\nu} \frac{\partial x^\nu}{\partial \bar{x}^\mu} = \frac{\partial x^\nu}{\partial \bar{x}^\mu} \phi_\nu(x)$  
     $\phi'_\mu(\bar{x}) = \tilde{A}^\nu_\mu \phi_\nu(x)$

   - **B. 逆变矢量**  
     $\phi'^\mu(\bar{x}) = A^\mu_\nu \phi^\nu(x) = \frac{\partial \bar{x}^\mu}{\partial x^\nu} \phi^\nu(x)$  
     e.g. $x^\mu = x^\mu(x^1, \cdots, x^n)$  
     则 $dx^\mu = \frac{\partial \bar{x}^\mu}{\partial x^\nu} dx^\nu = A^\mu_\nu dx^\nu$

#### 曲线参数化说明
- 其中 $C$ 为流形上曲线，参数 $x^\mu = x^\mu(s)$  
  $s$ 为弧长，在 $\bar{x}$ 中为 $\bar{x}^\mu = \bar{x}^\mu(s')$  
- 规定 $ds' = ds$ 弧长  
  则 $\frac{d\bar{x}^\mu}{ds'} = A^\mu_\nu \frac{dx^\nu}{ds}$  
- 定义切矢量 $u^\mu(x) = \frac{dx^\mu}{ds}$  
  则 $u'^\mu(\bar{x}) = A^\mu_\nu u^\nu(x)$

## Figure & Layout Description
该页面采用方格纸背景，整体布局为垂直排列的手写笔记风格。顶部包含一个简笔坐标系示意图：左侧标注 $x$ 坐标系，右侧标注 $\bar{x}$ 坐标系，两坐标系间有椭圆形曲线连接，下方标注"两坐标"。正文内容以黑色手写体呈现，包含大量数学公式和中文注释。关键概念"上逆下协"被蓝色矩形框高亮标记，位于页面中下部。公式中的张量指标严格区分上下位置，微分符号如 $dx^\mu$ 采用上标表示。页面右侧有空白网格区域，整体呈现典型的课堂板书特征，文字密度较高且逻辑层次清晰，通过公式推导与文字说明交替展开坐标变换理论。

<CTX>
{
   "topic": "坐标变换与张量定义",
   "keywords": ["坐标变换", "Jacobian行列式", "协变张量", "逆变张量", "切矢量", "标量不变性"],
   "summary": "本页详细阐述坐标变换规则下张量的定义方法，明确区分协变与逆变张量的变换性质，建立流形上曲线参数化与切矢量的关系",
   "pending_concepts": ["克氏符的引入与几何意义", "测地线方程的推导过程", "联络系数在张量微分中的应用", "挠率张量的物理诠释"]
}
</CTX>