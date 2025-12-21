# Slide 28

## 1.9.3 广义协变 Gauss 积分定理

设矢量 $j^\mu$ 的普通散度为 $\partial_\mu j^\mu$，

$n$ 维欧氏空间 $M$ 上高斯定理为：

$\sim \int_\Sigma \nabla \cdot \vec{a}  dV = \int_{\partial \Sigma} \vec{a} \cdot d\vec{S}$

$\sim \int_M \partial_\mu j^\mu d^n x = \int_{\partial M} j^\mu dS_\mu$

$dS_\mu$ 为 $(n-1)$ 维面元。

设 $J^\mu$ 为黎曼流形上的逆变矢量  
$$
\Gamma^\lambda_{\mu\lambda} = \frac{1}{2} g^{\lambda\nu} \partial_\mu (g_{\lambda\nu}) = \partial_\mu (\ln \sqrt{g}) = \frac{1}{\sqrt{g}} \partial_\mu (\sqrt{g})
$$

其协变散度为 $D_\mu J^\mu = \frac{1}{\sqrt{g}} \partial_\mu (\sqrt{g} J^\mu)$

$$
D_\mu \phi^\mu = \partial_\mu \phi^\mu + \Gamma^\mu_{\mu\lambda} \phi^\lambda = \partial_\mu \phi^\mu + \frac{1}{\sqrt{g}} \partial_\lambda (\sqrt{g}) \phi^\lambda = \frac{1}{\sqrt{g}} \partial_\mu (\sqrt{g} \phi^\mu)
$$

$$
\int_M (D_\mu J^\mu) \sqrt{g} d^n x = \int_{\partial M} \sqrt{g} J^\mu dS_\mu
$$

$\sqrt{g} dS_\mu$ 为协变面元.

## Figure & Layout Description

图片为米黄色方格纸背景的手写笔记，黑色墨水书写。标题"1.9.3 广义协变 Gauss 积分定理"位于左上角，使用较大字号且字迹工整。正文分为四个逻辑段落：

1. 第一段（标题下方）说明矢量 $j^\mu$ 的普通散度定义，字体中等，末尾逗号清晰
2. 第二段介绍 $n$ 维欧氏空间高斯定理，包含两个带波浪线前缀的积分等式，公式左对齐，积分符号与上下限标注明确，$\vec{a}$ 与 $d\vec{S}$ 均带箭头符号
3. 第三段定义面元 $dS_\mu$，字体略小，位于公式下方
4. 第四段引入黎曼流形概念，右侧有大括号包含的 $\Gamma^\lambda_{\mu\lambda}$ 推导过程（分两行书写），等号对齐；协变散度定义部分包含三行公式推导，每行等号严格对齐，最后一行公式下方标注"协变面元"说明

整体布局为左对齐结构，公式与文字混合排布，关键变量如 $\sqrt{g}$、$d^n x$ 等符号书写规范，积分区域 $\Sigma$ 与 $\partial \Sigma$ 标注清晰。右侧推导区域与主公式形成视觉呼应，体现从普通散度到协变散度的逻辑递进。

<CTX>
{
   "topic": "广义协变Gauss积分定理与协变散度的几何表述",
   "keywords": ["协变散度", "高斯积分定理", "黎曼流形", "协变面元", "度规行列式"],
   "summary": "本页推导了黎曼流形上协变形式的高斯积分定理，通过引入协变面元$\\sqrt{g}dS_\\mu$建立弯曲时空中的散度定理，为后续曲率积分与拓扑不变量研究奠定基础",
   "pending_concepts": ["协变散度在引力场方程中的物理诠释", "边界项$\\partial M$的拓扑分类", "协变体积元与Hodge对偶的关联"]
}
</CTX>