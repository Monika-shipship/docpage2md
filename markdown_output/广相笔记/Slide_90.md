# Slide 90

$ds^2 = -c^2 e^\nu dt^2 + e^\lambda dr^2 + r^2 (d\theta^2 + \sin^2\theta d\phi^2).$

中的 $r$ 不是 0 到 $r$ 处的固有长度。  
固有长度是 $dt=0$ 同时测，$L = \int ds = \sqrt{e^\lambda} \, dr$，  
如史瓦西解 $ds^2 = -\left(1 - \frac{2GM}{rc^2}\right) c^2 dt^2 + \frac{1}{1 - \frac{2GM}{rc^2}} dr^2$，

由此计算 Einstein 张量  
metric → connection → curvature  
$$R^\lambda_{\mu\sigma\nu} = \partial_\sigma \Gamma^\lambda_{\nu\mu} - \partial_\nu \Gamma^\lambda_{\sigma\mu} + \Gamma^\lambda_{\sigma\alpha} \Gamma^\alpha_{\nu\mu} - \Gamma^\lambda_{\nu\alpha} \Gamma^\alpha_{\sigma\mu}.$$

缩并 13 得 Ricci 张量  
$$R_{\mu\nu} = R^\lambda_{\mu\lambda\nu} = \partial_\lambda \Gamma^\lambda_{\mu\nu} - \partial_\nu \Gamma^\lambda_{\lambda\mu} + \Gamma^\lambda_{\lambda\alpha} \Gamma^\alpha_{\mu\nu} - \Gamma^\lambda_{\nu\alpha} \Gamma^\alpha_{\lambda\mu}.$$  
是对称张量。  
$$R^0_0 = g^{\mu\sigma} R_{\sigma 0} = g^{\mu\sigma} \left[ \partial_\lambda \Gamma^\lambda_{\sigma 0} - \partial_0 \Gamma^\lambda_{\lambda \sigma} + \Gamma^\lambda_{\lambda\alpha} \Gamma^\alpha_{\sigma 0} - \Gamma^\lambda_{0\alpha} \Gamma^\alpha_{\lambda \sigma} \right]$$  
$$R^0_0 = g^{00} \left( \partial_\lambda \Gamma^\lambda_{00} - \partial_0 \Gamma^\lambda_{\lambda 0} + \Gamma^\lambda_{\lambda\alpha} \Gamma^\alpha_{00} - \Gamma^\lambda_{0\alpha} \Gamma^\alpha_{\lambda 0} \right)$$  
0分量为  
$$= g^{00} \left( \partial_\lambda \Gamma^\lambda_{00} - \partial_0 \Gamma^\lambda_{\lambda 0} + \Gamma^\lambda_{\lambda\alpha} \Gamma^\alpha_{00} - \Gamma^\lambda_{0\alpha} \Gamma^\alpha_{\lambda 0} \right)$$  
$$= -\frac{1}{e^\nu} \left[ \left( \partial_0 (\frac{1}{2c} \dot{\nu}) + \partial_r (\frac{1}{2c} \nu' e^{\nu - \lambda}) \right) - \partial_0 \left( \frac{1}{2c} (\dot{\nu} + \lambda) \right) + \left( \frac{1}{2c} (\nu + \lambda) \frac{1}{2c} \dot{\nu} + \left( \frac{1}{r} + \frac{1}{2c} (\nu + \lambda) \right) \frac{1}{2c} \nu' e^{\nu - \lambda} \right) - \left( \frac{1}{2c} \dot{\nu} \frac{1}{2c} \dot{\nu} + \frac{1}{2c} \nu' \cdot \frac{1}{2c} \nu' e^{\nu - \lambda} + \frac{1}{2c} \nu' e^{\nu - \lambda} \frac{1}{2c} \nu' + \frac{1}{2c} \lambda \frac{1}{2c} \nu' \right) \right]$$

## Figure & Layout Description
图片为手写数学推导内容，书写在浅黄色方格纸上（方格线为浅灰色），整体布局为纵向排列。文字和公式使用黑色墨水书写，字迹清晰但存在部分连笔和涂改痕迹。内容从上至下分为四个主要区域：1) 顶部为球对称度规的表达式，使用较大字体书写；2) 中上部为关于坐标r物理意义的中文解释及史瓦西解的度规形式；3) 中部为Einstein张量计算流程说明及黎曼曲率张量的定义公式，其中"metric → connection → curvature"用箭头符号连接；4) 底部为Ricci张量缩并过程及R^0_0分量的具体展开式，包含多行复杂偏导数运算。公式中存在大量希腊字母（ν, λ, Γ等）和上下标，部分符号因手写体存在辨识难度（如∂_0与∂_r的区分）。页面无彩色元素，仅黑白手写内容，整体呈现典型的理论物理手稿风格。

<CTX>
{
   "topic": "曲率张量的具体计算与Ricci张量分量推导",
   "keywords": ["曲率张量", "Ricci张量", "Einstein张量", "指标缩并", "度规函数求导"],
   "summary": "本页完成了从黎曼曲率张量到Ricci张量的指标缩并过程，并推导出R^0_0分量的具体表达式，为建立Einstein场方程提供必要数学基础",
   "pending_concepts": ["Einstein场方程的完整形式", "R^0_0表达式中各项的物理意义", "Schwarzschild解的边界条件应用", "度规函数ν和λ的确定方法"]
}
</CTX>