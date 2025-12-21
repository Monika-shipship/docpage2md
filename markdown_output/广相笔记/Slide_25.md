# Slide 25

## 1.9.1 Levi-Civita 张量

$\forall g_{\mu\nu} \text{张量}, \ a = \det(g_{\mu\nu})$

$$
\varepsilon_{\mu_1\mu_2\cdots\mu_n} \ a = \varepsilon^{\nu_1\nu_2\cdots\nu_n} \ g_{\mu_1\nu_1} g_{\mu_2\nu_2} \cdots g_{\mu_n\nu_n}
$$

所以，令 $g = \det(g_{\mu\nu})$

$$
g \ \varepsilon_{\nu_1\nu_2\cdots\nu_n} = \varepsilon^{\mu_1\mu_2\cdots\mu_n} \ g_{\mu_1\nu_1} g_{\mu_2\nu_2} \cdots g_{\mu_n\nu_n}
$$

$$
(\sqrt{g})^2 = g
$$

$$
\sqrt{g} \ \varepsilon_{\nu_1\nu_2\cdots\nu_n} = \frac{\varepsilon^{\mu_1\mu_2\cdots\mu_n}}{\sqrt{g}} \ g_{\mu_1\nu_1} g_{\mu_2\nu_2} \cdots g_{\mu_n\nu_n}
$$

$$
\frac{\varepsilon^{\mu_1\mu_2\cdots\mu_n}}{\sqrt{g}} : \text{n阶单位逆变张量}
$$

$$
\sqrt{g} \ \varepsilon_{\nu_1\nu_2\cdots\nu_n} : \text{n阶单位协变张量}
$$

对于二维曲面，曲率张量：$R_{\lambda\sigma\mu\nu}, \ \lambda\sigma\mu\nu = \{1,2\}$

单位面积元：$\frac{\varepsilon^{\mu\nu}}{\sqrt{g}}, \ \sqrt{g} \ \varepsilon_{\mu\nu}$

## Figure & Layout Description

图片为手写笔记形式，背景为浅黄色方格纸，网格线为浅灰色，每个方格约1cm×1cm。文字与公式以黑色墨水书写，笔迹清晰，字迹工整。页面顶部居中位置写有章节标题"1.9.1 Levi-Civita 张量"，字体略大于正文。正文内容自上而下分段排列，每段包含数学公式与中文注释。公式部分采用上下标结构，张量指标使用下标（如$g_{\mu\nu}$）和上标（如$\varepsilon^{\mu\nu}$）表示，行列式用$\det$符号。关键推导步骤以中文短句连接，如"所以，令$g = \det(g_{\mu\nu})$"。页面中下部包含两行中文注释，分别定义"n阶单位逆变张量"和"n阶单位协变张量"。底部有针对二维曲面的特殊说明，涉及曲率张量和单位面积元的表达式。整体布局层次分明，公式与文字交替排列，逻辑流程清晰，符合数学推导笔记的典型特征。

<CTX>
{
   "topic": "Levi-Civita张量与度规行列式的关系及其在微分几何中的应用",
   "keywords": ["Levi-Civita张量", "度规行列式", "单位逆变张量", "单位协变张量", "体积元"],
   "summary": "本页系统阐述了Levi-Civita张量与度规行列式的关系，定义了协变/逆变单位张量，并推导出适用于任意维度的体积元表达式，为后续Stokes定理的坐标无关性证明提供几何基础",
   "pending_concepts": ["体积元在Stokes定理中的具体应用", "Levi-Civita张量与外微分算子的关联", "二维曲面中曲率张量的完整表达式", "Hodge对偶与单位面积元的几何意义"]
}
</CTX>