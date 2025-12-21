# Slide 8

$$= \partial_\nu \partial_\mu \phi + \phi^6 \partial_\nu \Gamma^\lambda_{\mu 6} + \Gamma^\lambda_{\mu 6} \partial_\nu \phi^6 + \Gamma^\lambda_{\nu \alpha} \partial_\mu \phi^\alpha + \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu 6} \phi^6 - \Gamma^\beta_{\nu \mu} \partial_\beta \phi - \Gamma^\beta_{\nu \mu} \Gamma^\lambda_{\beta 6} \phi^6$$

$$\nabla_\nu \nabla_\mu \phi^\lambda = \partial_\nu \partial_\mu \phi^\lambda + \phi^6 \left( \partial_\nu \Gamma^\lambda_{\mu 6} + \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu 6} - \Gamma^\beta_{\nu \mu} \Gamma^\lambda_{\beta 6} \right) + \Gamma^\lambda_{\mu 6} \partial_\nu \phi^6 + \Gamma^\lambda_{\nu \alpha} \partial_\mu \phi^\alpha - \Gamma^\beta_{\nu \mu} \partial_\beta \phi^\lambda$$

$$\nabla_\mu \nabla_\nu \phi^\lambda = \partial_\mu \partial_\nu \phi^\lambda + \phi^6 \left( \partial_\mu \Gamma^\lambda_{\nu 6} + \Gamma^\lambda_{\mu \alpha} \Gamma^\alpha_{\nu 6} - \Gamma^\beta_{\mu \nu} \Gamma^\lambda_{\beta 6} \right) + \Gamma^\lambda_{\nu 6} \partial_\mu \phi^6 + \Gamma^\lambda_{\mu \alpha} \partial_\nu \phi^\alpha - \Gamma^\beta_{\mu \nu} \partial_\beta \phi^\lambda$$

$$\left( \nabla_\mu \nabla_\nu - \nabla_\nu \nabla_\mu \right) \phi^\lambda = \phi^6 \left( \partial_\mu \Gamma^\lambda_{\nu 6} - \partial_\nu \Gamma^\lambda_{\mu 6} + \Gamma^\lambda_{\mu \alpha} \Gamma^\alpha_{\nu 6} - \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu 6} + \Gamma^\lambda_{\beta 6} \left( \Gamma^\beta_{\nu \mu} - \Gamma^\beta_{\mu \nu} \right) \right)$$

相消 $+ \Gamma^\lambda_{\nu 6} \partial_\mu \phi^6 - \Gamma^\lambda_{\mu 6} \partial_\nu \phi^6 + \Gamma^\lambda_{\mu \alpha} \partial_\nu \phi^\alpha - \Gamma^\lambda_{\nu \alpha} \partial_\mu \phi^\alpha + \left( \Gamma^\beta_{\nu \mu} - \Gamma^\beta_{\mu \nu} \right) \partial_\beta \phi^\lambda$

$$= \phi^6 \left( \partial_\mu \Gamma^\lambda_{\nu 6} - \partial_\nu \Gamma^\lambda_{\mu 6} + \Gamma^\lambda_{\mu \alpha} \Gamma^\alpha_{\nu 6} - \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu 6} \right) \equiv R^\lambda_{\theta \mu \nu}$$

$$+ \left( \Gamma^\beta_{\nu \mu} - \Gamma^\beta_{\mu \nu} \right) \left( \partial_\beta \phi^\lambda + \phi^6 \Gamma^\lambda_{\beta 6} \right)$$

$$\equiv -T^\beta_{\mu \nu} \quad \nabla_\beta \phi^\lambda$$

于是 $\left( \nabla_\mu \nabla_\nu - \nabla_\nu \nabla_\mu \right) \phi^\lambda = R^\lambda_{\theta \mu \nu} \phi^\theta - T^\sigma_{\mu \nu} \nabla_\sigma \phi^\lambda$

$$R^\lambda_{\theta \mu \nu} = \partial_\mu \Gamma^\lambda_{\nu \theta} - \partial_\nu \Gamma^\lambda_{\mu \theta} + \Gamma^\lambda_{\mu \alpha} \Gamma^\alpha_{\nu \theta} - \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu \theta} \quad \text{易看出关于}\mu\nu\text{反对称}$$

$$T^\theta_{\mu \nu} = \Gamma^\theta_{\mu \nu} - \Gamma^\theta_{\nu \mu} \quad \text{关于}\mu\nu\text{反对称}$$

$$\left( \nabla_\mu \nabla_\nu - \nabla_\nu \nabla_\mu \right) \phi^\lambda = \phi^\theta \left( \partial_\mu \Gamma^\lambda_{\nu \theta} - \partial_\nu \Gamma^\lambda_{\mu \theta} + \Gamma^\lambda_{\mu \alpha} \Gamma^\alpha_{\nu \theta} - \Gamma^\lambda_{\nu \alpha} \Gamma^\alpha_{\mu \theta} \right)$$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体布局呈纵向公式链结构。主要使用黑色墨水书写，关键项用彩色标记：
- 蓝色标记：$\phi^6$、$\Gamma^\lambda_{\mu 6}$等特定张量分量
- 红色标记：包含"相消"文字标注、关键表达式下划线、$R^\lambda_{\theta \mu \nu}$和$T^\theta_{\mu \nu}$的定义式
- 橙色波浪线：标记需要抵消的交叉项（如$\Gamma^\lambda_{\nu 6} \partial_\mu \phi^6 - \Gamma^\lambda_{\mu 6} \partial_\nu \phi^6$）
- 红色双下划线：突出曲率张量$R^\lambda_{\theta \mu \nu}$的定义核心部分
- 红色箭头：指示推导流程方向
- 红色"≡"符号：强调等价定义关系
公式按推导逻辑分层排列，从顶部的协变导数展开到底部的曲率张量定义。底部有红色手写注释"易看出关于μν反对称"和"关于μν反对称"。存在少量橙色修正标记（如"∇_βφ^λ"旁的修正符号）。

<CTX>
{
   "topic": "协变导数交换性与曲率张量的推导",
   "keywords": ["协变导数交换子", "黎曼曲率张量", "挠率张量", "联络系数反对称性", "张量微分算子"],
   "summary": "本页完成协变导数交换子的完整推导，建立曲率张量与挠率张量的数学表达式，揭示联络系数反对称性对曲率结构的影响",
   "pending_concepts": ["曲率张量的几何意义", "挠率张量的物理诠释", "测地线方程与曲率的关系", "无挠流形的特殊性质", "曲率张量的代数恒等式"]
}
</CTX>