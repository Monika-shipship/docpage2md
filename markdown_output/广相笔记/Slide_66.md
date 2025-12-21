# Slide 66

$$
R_0^0 = \frac{8\pi G}{c^4} \left( -\frac{1}{2} \rho c^2 \right)
$$

$$
R_0^0 = -\frac{4\pi G}{c^2} \rho
$$

Ricci张量：

$$
R_{\mu\nu} = R^\lambda_{\mu\lambda\nu} = \partial_\lambda \Gamma^\lambda_{\nu\mu} - \partial_\nu \Gamma^\lambda_{\lambda\mu} + \Gamma^\lambda_{\lambda\alpha} \Gamma^\alpha_{\nu\mu} - \Gamma^\lambda_{\nu\alpha} \Gamma^\alpha_{\lambda\mu}
$$

$$
h_{00} = -\frac{2\phi}{c^2}
$$

$$
g_{00} = -\left(1 - h_{00}\right) = -\left(1 + \frac{2\phi}{c^2}\right) \quad g_{ij} = \delta_{ij} \quad g_{i0} = g_{0i} = 0
$$

$$
g^{00} = -\left( \frac{1}{1 - h_{00}} \right) = -\left(1 + h_{00}\right) = -\left(1 - \frac{2\phi}{c^2}\right)
$$

$$
g^{ij} = \delta^{ij} \quad g^{i0} = g^{0i} = 0
$$

联结不为 0 的项为

$$
\Gamma^i_{00} = -\frac{1}{2} \partial_i h_{00} = \frac{1}{c^2} \partial_i \phi
$$

$$
\Gamma^0_{0i} = \Gamma^0_{i0} = \frac{1}{c^2} \partial_i \phi
$$

全代入 $R_{\mu\nu}$ 得

## Figure & Layout Description

图片为手写体数学推导内容，背景为浅米色方格纸（网格线为浅灰色，间距约5mm）。文字和公式以黑色墨水书写，整体布局呈垂直分块结构：

1. **顶部区域**：包含两个独立行间公式，分别占据第一、二行，公式间距较大，字体清晰工整，使用标准数学符号（如分数线、括号等）。

2. **中部区域**：
   - 第三行以中文"Ricci张量："作为小标题，后接多行展开的Ricci张量定义式，公式分为两行书写，第二行缩进对齐第一行运算符
   - 下方依次排列$h_{00}$定义式、度规分量$g_{\mu\nu}$及其逆张量$g^{\mu\nu}$的表达式，每组公式独立成行
   - 公式中出现希腊字母（如$\Gamma$）、偏导符号$\partial$、克罗内克δ符号等

3. **底部区域**：
   - "联结不为 0 的项为"作为子标题
   - 下方两行书写Christoffel符号非零分量表达式
   - 最底行以"全代入 $R_{\mu\nu}$ 得"结束，暗示推导过程的延续性

整体书写风格为物理学家典型的手稿风格，公式排版符合张量运算的规范逻辑，关键变量（如$\phi$、$c$、$G$）多次重复出现形成视觉焦点。手写笔迹流畅，但部分符号（如$\Gamma$）因连笔稍显潦草，需结合上下文推断。

<CTX>
{
   "topic": "静态引力场中度规扰动与Ricci张量的显式计算：从牛顿势到曲率分量的完整推导",
   "keywords": ["Ricci张量", "度规扰动", "Christoffel符号", "牛顿势", "张量分量代入"],
   "summary": "本页完成度规扰动项$h_{00}$代入Ricci张量的具体计算，建立牛顿引力势φ与时空曲率的直接数学映射关系",
   "pending_concepts": ["Christoffel符号非零分量的物理意义", "度规扰动项$h_{00}$的符号约定依据", "为何仅保留一阶小量项"]
}
</CTX>