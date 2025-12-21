# Slide 7

$$\frac{\partial}{\partial x^\alpha}\left( \frac{\partial x^\beta}{\partial x'^\mu} \frac{\partial x'^\nu}{\partial x^\beta} \right) = \frac{\partial}{\partial x^\alpha} (\delta_\mu^\nu) = 0$$

$\Gamma_{\mu\nu}^{\lambda}$ 称为联络 (Connection)，不是张量  
可延联络满足 $\Gamma_{\mu\nu}^{\lambda} = \bar{A}_{\mu}^{\alpha} \bar{A}_{\nu}^{\beta} A_{\gamma}^{\lambda} \Gamma_{\alpha\beta}^{\gamma} + \bar{A}_{\mu}^{\alpha} A_{\beta}^{\lambda} \frac{\partial \bar{A}_{\gamma}^{\beta}}{\partial x^{\alpha}}$ (坐标依赖的张量)  
*some how*

$D_{\mu}\phi = \partial_{\mu}\phi$  
$D_{\mu}\phi^{\rho} = \partial_{\mu}\phi^{\rho} + \Gamma_{\mu\alpha}^{\rho}\phi^{\alpha}$  
$D_{\mu}\phi_{\rho} = \partial_{\mu}\phi_{\rho} - \Gamma_{\mu\rho}^{\alpha}\phi_{\alpha}$  
$D_{\mu}\phi_{\sigma}^{\rho} = \partial_{\mu}\phi_{\sigma}^{\rho} + \Gamma_{\mu\alpha}^{\rho}\phi_{\sigma}^{\alpha} - \Gamma_{\mu\sigma}^{\beta}\phi_{\beta}^{\rho}$  
$D_{\lambda}\phi^{\mu\nu} = \partial_{\lambda}\phi^{\mu\nu} + \Gamma_{\lambda\alpha}^{\mu}\phi^{\alpha\nu} + \Gamma_{\lambda\beta}^{\nu}\phi^{\mu\beta}$

联络变分？  
$g^{\mu\nu}D_{\mu} = D^{\nu}$ 有些书定义  
$D_{\mu}D_{\nu}\phi^{\lambda} \overset{?}{=} D_{\nu}D_{\mu}\phi^{\lambda}$  
$\neq !$

令 $\phi_{;\mu}^{\lambda} = \partial_{\mu}\phi^{\lambda} + \Gamma_{\mu\alpha}^{\lambda}\phi^{\alpha}$  
$\phi_{;\nu}^{\lambda} = \partial_{\nu}\phi^{\lambda} + \Gamma_{\nu\mu}^{\lambda}\phi^{\mu}$

$D_{\nu}D_{\mu}\phi^{\lambda} = D_{\nu}\phi_{;\mu}^{\lambda} = \partial_{\nu}\phi_{;\mu}^{\lambda} + \Gamma_{\nu\alpha}^{\lambda}\phi_{;\mu}^{\alpha} - \Gamma_{\nu\mu}^{\beta}\phi_{;\beta}^{\lambda}$  
$D_{\mu}D_{\nu}\phi^{\lambda} = D_{\mu}\phi_{;\nu}^{\lambda} = \partial_{\mu}\phi_{;\nu}^{\lambda} + \Gamma_{\mu\alpha}^{\lambda}\phi_{;\nu}^{\alpha} - \Gamma_{\mu\nu}^{\beta}\phi_{;\beta}^{\lambda}$

$$D_{\nu}D_{\mu}\phi^{\lambda} = D_{\nu}\phi_{;\mu}^{\lambda} = \partial_{\nu}\left( \partial_{\mu}\phi^{\lambda} + \Gamma_{\mu\alpha}^{\lambda}\phi^{\alpha} \right) + \Gamma_{\nu\alpha}^{\lambda} \left( \partial_{\mu}\phi^{\alpha} + \Gamma_{\mu\beta}^{\alpha}\phi^{\beta} \right) - \Gamma_{\nu\mu}^{\beta} \left( \partial_{\beta}\phi^{\lambda} + \Gamma_{\beta\gamma}^{\lambda}\phi^{\gamma} \right)$$

## Figure & Layout Description
手写笔记式PPT页面，背景为浅米色方格纸（1cm×1cm网格）。内容以黑色墨水书写，部分公式符号用蓝色标记。页面布局分为三个主要区域：

1. **右上区域**：包含一个独立的行间公式，用黑色手写体书写，公式右侧有"=0"结尾，字体略大于正文。

2. **中上部主体区域**：
   - 首行定义"Γ_{μν}^λ 称为联络"，其中"Connection"用英文括号标注
   - 其下为可延联络的变换公式，右侧有中文注释"(坐标依赖的张量)"和英文"some how"（手写体较小）
   - 协变导数系列公式垂直排列，包含5个不同张量阶数的协变导数表达式

3. **中下部区域**：
   - 以"联络变分？"作为小标题
   - 包含g^{μν}D_μ=D^ν的定义说明
   - 协变导数交换性讨论，包含"≠!"符号和两个协变导数作用的展开式
   - 最后一个大型行间公式用蓝色标记了Γ_{μβ}^α和Γ_{βγ}^λ中的β指标

页面整体为手写风格，公式排版紧凑，部分希腊字母（如Γ）书写较大，下标/上标位置准确。蓝色标记仅出现在最后一个公式的部分指标上，形成视觉焦点。

<CTX>
{
   "topic": "协变导数的计算规则与联络变分分析",
   "keywords": ["协变导数", "联络系数", "克氏符", "张量微分", "坐标变换不变性", "联络变分", "协变导数交换性"],
   "summary": "本页详细推导了不同张量类型的协变导数表达式，验证联络的非张量变换性质，并开始探讨协变导数的交换性问题与联络变分的数学形式",
   "pending_concepts": ["联络变分的物理意义", "协变导数不对易与曲率张量的关系", "测地线方程的推导过程", "挠率张量的物理诠释", "黎曼曲率张量的构造逻辑"]
}
</CTX>