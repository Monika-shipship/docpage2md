# Slide 39

## 2.1.2 GR中的黎曼度规

在 SR 中：$ds^2 = -c^2 dt^2 + \left[ (dx^1)^2 + (dx^2)^2 + (dx^3)^2 \right]$.

SR: $ds^2 = -c^2 dt^2 + \left[ (dx^1)^2 + (dx^2)^2 + (dx^3)^2 \right]$.

$ds^2 = \eta_{\mu\nu} dx^\mu dx^\nu \quad \mu,\nu = 0,1,2,3, \quad x^0 = ct$

$$
\begin{bmatrix}
\eta_{\mu\nu}
\end{bmatrix}
=
\begin{bmatrix}
-1 & & & \\
& 1 & & \\
& & 1 & \\
& & & 1
\end{bmatrix}
\quad \det \eta = -1
$$

GR: $ds^2 = g_{\mu\nu} dx^\mu dx^\nu$

Riemann流形和欧氏空间局部同胚

故可在每个时空点的邻域内作坐标变换：

$$
\eta_{\mu\nu} = \frac{\partial x'^\lambda}{\partial x^\mu} \frac{\partial x'^\sigma}{\partial x^\nu} g_{\lambda\sigma}
$$

将 Riemann 的 $g_{\mu\nu}$ 变到平直时空的 $\eta_{\mu\nu}$:

$\eta$ 的行列式：

$$
\eta = \frac{1}{n!} \varepsilon^{\mu_1 \mu_2 \cdots \mu_n} \varepsilon^{\nu_1 \nu_2 \cdots \nu_n} \eta_{\mu_1 \nu_1} \eta_{\mu_2 \nu_2} \cdots \eta_{\mu_n \nu_n}
$$

$$
= \frac{1}{n!} \varepsilon^{\mu_1 \mu_2 \cdots \mu_n} \varepsilon^{\nu_1 \nu_2 \cdots \nu_n} \frac{\partial x'^{\lambda_1}}{\partial x^{\mu_1}} \frac{\partial x'^{\sigma_1}}{\partial x^{\nu_1}} g_{\lambda_1 \sigma_1} \frac{\partial x'^{\lambda_2}}{\partial x^{\mu_2}} \frac{\partial x'^{\sigma_2}}{\partial x^{\nu_2}} g_{\lambda_2 \sigma_2} \cdots \frac{\partial x'^{\lambda_n}}{\partial x^{\mu_n}} \frac{\partial x'^{\sigma_n}}{\partial x^{\nu_n}} g_{\lambda_n \sigma_n}
$$

$$
= \frac{1}{n!} \left[ \varepsilon^{\mu_1 \mu_2 \cdots \mu_n} \frac{\partial x'^{\lambda_1}}{\partial x^{\mu_1}} \frac{\partial x'^{\lambda_2}}{\partial x^{\mu_2}} \cdots \frac{\partial x'^{\lambda_n}}{\partial x^{\mu_n}} \right] \left[ \varepsilon^{\nu_1 \nu_2 \cdots \nu_n} \frac{\partial x'^{\sigma_1}}{\partial x^{\nu_1}} \frac{\partial x'^{\sigma_2}}{\partial x^{\nu_2}} \cdots \frac{\partial x'^{\sigma_n}}{\partial x^{\nu_n}} \right] g_{\lambda_1 \sigma_1} g_{\lambda_2 \sigma_2} \cdots g_{\lambda_n \sigma_n}
$$

## Figure & Layout Description

图片为手写笔记形式，背景是浅黄色方格纸，文字主要用黑色墨水书写。页面顶部有二级标题"2.1.2 GR中的黎曼度规"。正文内容按逻辑顺序排列，包含SR（狭义相对论）和GR（广义相对论）的度规表达式、矩阵表示、坐标变换公式及行列式推导。

关键视觉元素包括：
1. 两处手写公式被彩色笔标记：蓝色波浪线框住公式左侧的Levi-Civita符号与雅可比矩阵部分，红色波浪线框住右侧的偏导数乘积部分
2. 矩阵表示使用方括号，以"-"符号表示对角线元素，非对角线位置留白
3. 公式中的下标/上标清晰可辨（如$dx^1$、$\eta_{\mu\nu}$）
4. 行列式展开式分三行书写，第三行包含彩色标记区域
5. 所有数学符号保持手写风格，但符号结构完整（如$\varepsilon$符号、偏导数符号）
6. 页面右侧有少量空白网格，无额外内容

<CTX>
{
   "topic": "黎曼度规的局部平坦化与行列式变换",
   "keywords": ["度规张量", "Riemann流形", "局部惯性系", "度规行列式", "坐标变换"],
   "summary": "本页详细推导了如何在Riemann流形的每个时空点邻域内通过坐标变换将弯曲时空度规局部化为平直时空度规，并给出度规行列式在坐标变换下的具体变换关系",
   "pending_concepts": ["局部惯性系的具体构造方法", "行列式变换的物理意义", "Levi-Civita符号在度规变换中的几何解释"]
}
</CTX>