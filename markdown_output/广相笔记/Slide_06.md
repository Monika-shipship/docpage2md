# Slide 6

协变微分（增加协变指标）  
对逆变矢量有 $ \phi'^\lambda(x') = A^\lambda_\nu \phi^\nu(x) = \frac{\partial x'^\lambda}{\partial x^\nu} \phi^\nu(x) $  
由于 $ A^\lambda_\nu $ 是 $ x $ 的函数，若直接求导 $ \frac{\partial \phi^\lambda}{\partial x^\mu} $ 不再是张量 $ \frac{\partial \phi'^\lambda}{\partial x'^\mu} $  

引入协变算符  
$$ D_\mu \phi^\lambda = \partial_\mu \phi^\lambda + \Gamma^\lambda_{\mu\nu} \phi^\nu $$  
这是张量  
$$ D'_\mu \phi'^\lambda = \bar{A}^\alpha_\mu \bar{A}^\lambda_\beta D_\alpha \phi^\beta $$  
即 $ \left( \partial'_\mu \phi'^\lambda + \Gamma'^\lambda_{\mu\nu} \phi'^\nu \right) = \bar{A}^\alpha_\mu \bar{A}^\lambda_\beta \left( \partial_\alpha \phi^\beta + \Gamma^\beta_{\alpha\delta} \phi^\delta \right) $  
$$ \bar{A}^\lambda_\mu \partial_\nu (A^\nu_\gamma \phi^\gamma) + \Gamma'^\lambda_{\mu\nu} A^\nu_\kappa \phi^\kappa = \bar{A}^\alpha_\mu A^\lambda_\beta \partial_\alpha \phi^\beta + \bar{A}^\alpha_\mu A^\lambda_\beta \Gamma^\beta_{\alpha\delta} \phi^\delta $$  
$$ \bar{A}^\lambda_\mu \phi^\gamma \partial_\nu A^\nu_\gamma + \bar{A}^\lambda_\mu A^\nu_\gamma \partial_\nu \phi^\gamma + \Gamma'^\lambda_{\mu\nu} A^\nu_\kappa \phi^\kappa = \bar{A}^\alpha_\mu A^\lambda_\beta \partial_\alpha \phi^\beta + \bar{A}^\alpha_\mu A^\lambda_\beta \Gamma^\beta_{\alpha\delta} \phi^\delta $$  

$$ \bar{A}^\alpha_\mu \phi^\beta \partial_\alpha A^\nu_\beta + \color{blue}{\bar{A}^\alpha_\mu A^\nu_\beta \partial_\alpha \phi^\beta} + \Gamma'^\lambda_{\mu\nu} A^\nu_\beta \phi^\beta = \color{blue}{\bar{A}^\alpha_\mu A^\nu_\beta \partial_\alpha \phi^\beta} + \bar{A}^\alpha_\mu A^\nu_\beta \Gamma^\beta_{\alpha\delta} \phi^\delta $$  
$$ \Gamma'^\lambda_{\mu\nu} A^\nu_\beta = \bar{A}^\alpha_\mu A^\delta_\beta \Gamma^\lambda_{\alpha\delta} - \bar{A}^\alpha_\mu \partial_\alpha A^\nu_\beta $$  
$$ \Gamma'^\lambda_{\mu\nu} A^\nu_\beta \bar{A}^\beta_\gamma = \bar{A}^\beta_\gamma \bar{A}^\alpha_\mu A^\delta_\beta \Gamma^\lambda_{\alpha\delta} - \bar{A}^\beta_\gamma \bar{A}^\alpha_\mu \partial_\alpha A^\nu_\beta $$  
$$ \Gamma'^\lambda_{\mu\gamma} = \Gamma'^\lambda_{\mu\nu} \delta^\nu_\gamma = \bar{A}^\beta_\gamma \bar{A}^\alpha_\mu A^\delta_\beta \Gamma^\lambda_{\alpha\delta} + \bar{A}^\alpha_\mu A^\nu_\beta \partial_\alpha \bar{A}^\beta_\gamma $$  
$$ \bar{A}^\beta_\gamma \partial_\alpha (A^\nu_\beta) = - A^\nu_\beta \partial_\alpha (\bar{A}^\beta_\gamma) $$  
$$ \frac{\partial x^\beta}{\partial x'^\gamma} \frac{\partial}{\partial x^\alpha} \left( \frac{\partial x'^\nu}{\partial x^\beta} \right) = - \frac{\partial x'^\nu}{\partial x^\beta} \frac{\partial}{\partial x^\alpha} \left( \frac{\partial x^\beta}{\partial x'^\gamma} \right) $$  

## Figure & Layout Description
图片为方格纸背景的手写笔记，文字以黑色墨水书写，部分公式用蓝色荧光笔高亮（位于中下部区域，包含 $ \bar{A}^\alpha_\mu A^\nu_\beta \partial_\alpha \phi^\beta $ 等表达式），底部有红色下划线标记。公式中存在彩色标注：橙色文字 "t→β" 和 "Y→α" 位于推导步骤旁，黑色手写体包含大量张量指标运算。整体布局为纵向排列的推导流程，从坐标变换规则逐步展开到协变导数的定义与性质验证，关键等式通过等号对齐形成逻辑链。右下角有部分公式被截断，标记为 [无法辨认]。

<CTX>
{
   "topic": "协变微分与联络系数的引入",
   "keywords": ["协变导数", "联络系数", "克氏符", "张量微分", "坐标变换不变性"],
   "summary": "本页通过协变导数的定义解决普通导数在坐标变换下的非张量性问题，推导联络系数的显式表达式并验证其张量变换性质",
   "pending_concepts": ["测地线方程的推导过程", "挠率张量的物理诠释", "黎曼曲率张量的构造逻辑", "协变微分在物理场论中的具体应用"]
}
</CTX>