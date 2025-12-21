# Slide 33

$$
\frac{d^2 x^\mu}{d\lambda^2} d\lambda = -\Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} d\lambda + \frac{dx^\mu}{d\lambda} f(\lambda) d\lambda
$$

$$
\frac{d^2 x^\mu}{d\lambda^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\lambda} \frac{dx^\beta}{d\lambda} = f(\lambda) \frac{dx^\mu}{d\lambda}
$$

测地线方程（$x^\mu = x^\mu(\lambda)$，$\frac{dx^\mu}{d\lambda}$ 切矢）

简化：

作变换 $\lambda = \lambda(\sigma)$

$$
\frac{dx^\mu}{d\lambda} = \frac{dx^\mu}{d\sigma} \frac{d\sigma}{d\lambda}
$$

$$
\frac{d^2 x^\mu}{d\lambda^2} = \frac{d^2 x^\mu}{d\sigma^2} \left( \frac{d\sigma}{d\lambda} \right)^2 + \frac{dx^\mu}{d\sigma} \frac{d^2 \sigma}{d\lambda^2}
$$

$$
\frac{d^2 x^\mu}{d\sigma^2} \left( \frac{d\sigma}{d\lambda} \right)^2 + \frac{dx^\mu}{d\sigma} \frac{d^2 \sigma}{d\lambda^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\sigma} \frac{dx^\beta}{d\sigma} \left( \frac{d\sigma}{d\lambda} \right)^2 = f(\lambda) \frac{dx^\mu}{d\sigma} \frac{d\sigma}{d\lambda}
$$

$$
\left( \frac{d^2 x^\mu}{d\sigma^2} + \Gamma^\mu_{\alpha\beta} \frac{dx^\alpha}{d\sigma} \frac{dx^\beta}{d\sigma} \right) \left( \frac{d\sigma}{d\lambda} \right)^2 = \frac{dx^\mu}{d\sigma} \left[ f(\lambda) \frac{d\sigma}{d\lambda} - \frac{d^2 \sigma}{d\lambda^2} \right]
$$

当 $f(\lambda) \frac{d\sigma}{d\lambda} - \frac{d^2 \sigma}{d\lambda^2} = 0$ 时（由于 $\lambda = \lambda(\sigma)$ 不确定）

## Figure & Layout Description

图片背景为浅米色方格纸纹理，所有内容以橙色手写体呈现。页面布局分为三个垂直区域：左上区域展示原始测地线方程推导，包含两行核心公式；中间区域标注"测地线方程"说明文字，右侧有手绘括号连接切矢说明；左下区域为"简化"推导过程，包含参数变换的链式法则展开。公式中存在明显的层级关系：第一行公式通过等号连接三项，第二行公式为整理后的标准形式。推导过程中使用了弯曲箭头连接右侧的切矢说明，箭头起始于"切矢"文字指向方程右侧项。所有微分符号（如$d^2x^\mu/d\lambda^2$）均采用分数形式书写，联络系数$\Gamma^\mu_{\alpha\beta}$的上下标位置清晰。页面右下角存在未完成的推导步骤，末尾公式被截断但关键条件式完整可见。文字与公式混合排布，关键术语"测地线方程"用中文标注，数学符号与汉字说明交替出现。

<CTX>
{
   "topic": "测地线方程的参数变换与仿射参量条件",
   "keywords": ["仿射参量", "自平行线条件", "测地线方程", "联络系数", "参数变换"],
   "summary": "本页完成测地线方程的参数变换推导，明确当参数变换满足特定微分条件时可消除附加项，确立仿射参量的数学判据",
   "pending_concepts": ["参数变换的物理意义", "仿射参量与固有时的关系", "非仿射参量下的测地线修正项"]
}
</CTX>