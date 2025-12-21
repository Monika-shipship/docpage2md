# Slide 46

$$g_{\mu\nu,\beta}\dot{x}^\mu\dot{x}^\beta = \frac{1}{2}g_{\mu\nu,\beta}\dot{x}^\mu\dot{x}^\beta + \frac{1}{2}g_{\beta\nu,\mu}\dot{x}^\mu\dot{x}^\beta$$

但 $g_{\mu\nu,\beta}\dot{x}^\mu\dot{x}^\beta = \frac{1}{2}(g_{\mu\nu,\beta} + g_{\beta\nu,\mu})\dot{x}^\mu\dot{x}^\beta$

$$\delta \int \dot{x}^\mu\dot{x}_\mu ds + \frac{1}{2}g^{\mu\nu}\left(g_{\mu\nu,\beta} + g_{\beta\nu,\mu} - g_{\alpha\beta,\nu}\right)\dot{x}^\alpha\dot{x}^\beta = 0$$

$$\ddot{x}^\mu + \Gamma^\mu_{\alpha\beta}\dot{x}^\alpha\dot{x}^\beta = 0 \quad \frac{d^2x^\mu}{ds^2} + \Gamma^\mu_{\alpha\beta}\frac{dx^\alpha}{ds}\frac{dx^\beta}{ds} = 0$$

↓  
克氏符  
广相中测地线和短程线同一性  
这个方程只对亚光速有效  

§ 2.11 曲率张量（黎曼空间中，无挠用克氏符）  

$$R^\rho_{\lambda\mu\nu} = \Gamma^\rho_{\lambda\nu,\mu} - \Gamma^\rho_{\lambda\mu,\nu} + \Gamma^\rho_{\sigma\mu}\Gamma^\sigma_{\lambda\nu} - \Gamma^\rho_{\sigma\nu}\Gamma^\sigma_{\lambda\mu}$$

(1) 对后一对反称 $R^\rho_{\lambda\mu\nu} = -R^\rho_{\lambda\nu\mu}$  
$\lambda\mu\nu \quad \nu\lambda\mu \quad \mu\nu\lambda$  
$\lambda\nu,\mu \leftrightarrow \lambda\mu,\nu$  

(2) 两种缩并  
1.2 $A_{\mu\nu} = R^\rho_{\mu\rho\nu}$  
$\nu\mu,\lambda \leftrightarrow \nu\lambda,\mu$  
1.3 $A_{\lambda\nu} = R^\rho_{\lambda\rho\nu}$  
$\mu\lambda,\nu \leftrightarrow \mu\nu,\lambda$

## Figure & Layout Description
图片为浅米色网格背景的手写笔记，文字与公式均以橙色墨水书写。整体布局为纵向排列的数学推导与中文注释混合结构：顶部为度规张量导数相关的变分推导（4行公式），中间部分包含测地线方程的两种表达形式（带箭头指示的"克氏符"标注），随后是3行中文说明文字。下半部分以"§ 2.11"为标题开启新章节，包含曲率张量的定义公式及对称性说明。公式中使用标准微分几何符号（$\Gamma$, $\dot{x}$, $R$等），下标清晰但部分希腊字母存在手写连笔。中文注释采用与公式相同的橙色字体，字号略小于公式。整体排版紧凑，行间距较小，符合课堂笔记特征。所有公式均未使用编号，通过换行自然分隔。

<CTX>
{
   "topic": "曲率张量的定义与对称性性质",
   "keywords": ["曲率张量", "黎曼空间", "克氏符", "里奇缩并", "对称性条件"],
   "summary": "本页引入黎曼空间中曲率张量的显式定义，展示其与克氏符的导数关系，并阐明后一对指标的反称性及两种重要缩并形式",
   "pending_concepts": ["曲率张量的几何意义解释", "无挠条件对克氏符的具体约束", "两种缩并结果的物理诠释"]
}
</CTX>