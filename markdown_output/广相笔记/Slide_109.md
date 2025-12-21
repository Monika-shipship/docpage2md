# Slide 109

## 3.3 光线在恒星附近的偏折

### 3.3.1 光在引力场中如何传播

设一粒子静质量 $m_0$，其 4 动量为  
$$ p^\mu = m_0 c u^\mu, \quad u^\mu = \frac{dx^\mu}{ds} = \frac{1}{c} \frac{dx^\mu}{d\tau} \quad (\tau \text{ 为固有时}) $$

选取 $g_{\mu\nu}u^\mu u^\nu = -1$，则  
$$ g_{\mu\nu}u^\mu u^\nu = g_{\mu\nu} \frac{dx^\mu}{ds} \frac{dx^\nu}{ds} = \frac{ds^2}{ds \cdot ds} = \frac{-(cd\tau)^2}{cd\tau \cdot cd\tau} = -1. $$

故  
$$ p^2 = g_{\mu\nu}p^\mu p^\nu = -m_0^2 c^2 $$  
$$ p^2 + m_0^2 c^2 = 0. $$

粒子在弯曲时空中运动，$u^\mu$ 自平行：  
$$ \frac{dV^\lambda}{ds} = 0 \Rightarrow \frac{\partial V^\lambda}{\partial x^\mu} \frac{dx^\mu}{ds} = 0 \quad \xrightarrow[\text{Riemann}]{} \partial \to \nabla $$  
$$ \nabla_\mu (V^\lambda) u^\mu = 0. $$

即  
$$ \nabla_\mu (V^\lambda) u^\mu = 0 $$

取 $V$ 为切矢 $u$，则测地线方程：  
$$ \nabla_\mu (u^\lambda) u^\mu = 0, \quad u^\mu = \frac{dx^\mu}{ds}. $$  
$$ p^\mu \propto u^\mu, \text{ 即 } \nabla_\mu (p^\lambda) p^\mu = 0. $$

对光子，$m_0 = 0$，$p^\mu = m_0 c \frac{dx^\mu}{ds}$ 不能用。

## Figure & Layout Description

图片为方格纸背景的手写笔记，文字为黑色墨水，布局清晰分层。顶部居中书写主标题“3.3 光线在恒星附近的偏折”，字体较大且加粗。其下为小节标题“3.3.1 光在引力场中如何传播”，左侧缩进书写。正文内容按逻辑分段排列：第一段定义粒子静质量与4动量，包含两行公式；第二段推导度规条件与动量平方关系，公式链式排列且等号对齐；第三段讨论弯曲时空运动，左侧有手写箭头标注“三维”，右侧标注“Riemann ∂→∇”；最后讨论光子特殊情况，末尾标注“不能用”。整体排版为左对齐，公式与文字穿插，部分符号有涂改痕迹（如“V”被多次修改），关键推导步骤间留有适当行距以增强可读性。

<CTX>
{
   "topic": "光线在引力场中的偏折与测地线方程",
   "keywords": ["测地线方程", "四动量", "光子静质量", "引力偏折", "协变导数"],
   "summary": "本页推导了弯曲时空中粒子的测地线方程，并阐明光子（零静质量）情况下四动量的特殊处理方式及其与经典路径的关联",
   "pending_concepts": ["光子测地线方程的具体解法", "引力偏折角度的计算步骤", "协变导数在弱场近似下的简化形式"]
}
</CTX>