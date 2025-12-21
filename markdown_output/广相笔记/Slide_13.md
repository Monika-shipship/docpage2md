# Slide 13

$$
\nabla_\lambda \phi^\lambda = \partial_\lambda \phi^\lambda + \frac{1}{\sqrt{g}} \frac{\partial \sqrt{g}}{\partial x^\lambda} \phi^\lambda
$$
$$
= \frac{1}{\sqrt{g}} \partial_\lambda (\sqrt{g} \phi^\lambda)
$$
故 $\nabla_\lambda \phi^\lambda = \frac{1}{\sqrt{g}} \partial_\lambda (\sqrt{g} \phi^\lambda)$

黎曼曲率张量：
$$
R^\lambda_{\sigma\mu\nu} = \partial_\mu \Gamma^\lambda_{\nu\sigma} - \partial_\nu \Gamma^\lambda_{\mu\sigma} + \Gamma^\lambda_{\mu\alpha} \Gamma^\alpha_{\nu\sigma} - \Gamma^\lambda_{\nu\alpha} \Gamma^\alpha_{\mu\sigma}
$$

中的联络为克氏符时有
$$
\Gamma^\sigma_{\mu\nu} = \frac{1}{2} g^{\sigma\lambda} \left( \partial_\mu g_{\lambda\nu} + \partial_\nu g_{\lambda\mu} - \partial_\lambda g_{\mu\nu} \right)
$$
$$
\Gamma^\sigma_{\mu\nu} = \Gamma^\sigma_{\nu\mu}, \quad g_{\lambda\sigma} \Gamma^\sigma_{\mu\nu} = \Gamma_{\lambda,\mu\nu} = \frac{1}{2} \left( \partial_\mu g_{\lambda\nu} + \partial_\nu g_{\lambda\mu} - \partial_\lambda g_{\mu\nu} \right)
$$
则称 $R^\lambda_{\sigma\mu\nu}$ 为 Riemann 曲率

观察 $R^\lambda_{\sigma\mu\nu} = \partial_\mu \Gamma^\lambda_{\nu\sigma} - \partial_\nu \Gamma^\lambda_{\mu\sigma} + \Gamma^\lambda_{\mu\alpha} \Gamma^\alpha_{\nu\sigma} - \Gamma^\lambda_{\nu\alpha} \Gamma^\alpha_{\mu\sigma}$

$\mu\nu$ 交换反对称 $R^\lambda_{\sigma\mu\nu} = -R^\lambda_{\sigma\nu\mu}$

$R^\lambda_{\sigma\mu\nu}$ 降下来，全协变 $g_{\tau\lambda} R^\lambda_{\sigma\mu\nu} = R_{\tau\sigma\mu\nu}$

## Figure & Layout Description
图片为方格纸背景的手写笔记，浅米色底纹配灰色网格线。内容以黑色墨水书写，包含多组数学公式和中文说明文字。公式按逻辑顺序自上而下排列：顶部是协变散度推导（3行公式），中间是"黎曼曲率张量"标题及对应公式（4行），下方是克氏联络表达式（含红色波浪下划线标注），再往下是对称性说明和曲率性质推导。关键公式中的克氏联络表达式被红色波浪线重点标记，形成视觉焦点。文字与公式混合排布，中文说明使用简体字，数学符号书写规范但带有手写特征（如$\Gamma$符号略似"P"形）。整体布局呈现典型的课堂推导笔记特征，公式行间距适中，重要结论通过换行和空格分隔。

<CTX>
{
   "topic": "黎曼曲率张量的显式定义与克氏联络表达式",
   "keywords": ["克氏联络", "度规相容条件", "黎曼曲率张量", "曲率反对称性", "全协变曲率张量", "指标轮换"],
   "summary": "本页通过克氏联络的度规表达式导出黎曼曲率张量的显式形式，阐明其在指标交换下的反对称性质及协变形式转换规则",
   "pending_concepts": ["曲率张量的 Bianchi 恒等式", "测地线偏离方程", "Ricci 曲率的物理意义", "爱因斯坦场方程中的曲率项"]
}
</CTX>