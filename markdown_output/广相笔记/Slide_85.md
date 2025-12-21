# Slide 85

则 $[g_{\mu\nu}] = \begin{bmatrix} -e^{\nu} & & & \\ & e^{\lambda} & & \\ & & r^2 & \\ & & & r^2 \sin^2\theta \end{bmatrix}$

$g^{\mu\nu} = [g^{\mu\nu}] = \begin{bmatrix} -e^{-\nu} & & & \\ & e^{-\lambda} & & \\ & & \frac{1}{r^2} & \\ & & & \frac{1}{r^2 \sin^2\theta} \end{bmatrix}$

Metric ansatz 假设  
这正是假设度规的形式。

$g = \det(g_{\mu\nu}) = -r^4 \sin^2\theta \, e^{\nu + \lambda}$

$\sqrt{-g} = r^2 \sin\theta \, e^{\frac{\nu + \lambda}{2}}$

Metric $\rightarrow$ Connection $\rightarrow$ Curvature

### 3.1.2 黎曼联络 $\Gamma^{\lambda}_{\mu\nu}$

在 Riemann 几何中 $\Gamma^{\lambda}_{\mu\nu} = g^{\lambda\sigma} \left( \partial_{\mu} g_{\sigma\nu} + \partial_{\nu} g_{\mu\sigma} - \partial_{\sigma} g_{\mu\nu} \right)$.

## Figure & Layout Description
手写内容呈现在浅黄色方格纸背景上，方格线为浅灰色。整体布局分为四个纵向区域：  
1. **顶部区域**：两个4×4对角矩阵并列排布，上方矩阵表示协变度规 $g_{\mu\nu}$，下方矩阵表示逆变度规 $g^{\mu\nu}$，均以黑色墨水手写，矩阵元素沿主对角线分布，非对角元素留空；  
2. **中部区域**：左侧手写英文"Metric ansatz"及中文"假设"，下方接中文说明"这正是假设度规的形式"，文字为黑色墨水，字迹工整；  
3. **中下区域**：两个行列式公式垂直排列，包含 $g = \det(g_{\mu\nu})$ 和 $\sqrt{-g}$ 的表达式，公式中指数项和三角函数符号清晰；  
4. **底部区域**：流程说明"Metric → Connection → Curvature"用箭头连接，下方标注小节标题"3.1.2 黎曼联络 $\Gamma^{\lambda}_{\mu\nu}$"，并附带黎曼联络的完整公式，公式中协变导数符号 $\partial$ 和度规逆张量 $g^{\lambda\sigma}$ 书写规范。  
整体文字与公式分布疏密得当，关键数学符号（如 $\nu, \lambda, \theta$）均使用斜体手写，与普通文字形成视觉区分。

<CTX>
{
   "topic": "度规假设形式与黎曼联络的推导",
   "keywords": ["度规假设", "行列式计算", "黎曼联络", "度规逆阵", "球对称度规"],
   "summary": "本页通过设定球对称度规的假设形式，推导了行列式表达式，并引入黎曼联络的计算公式，为曲率张量和引力场方程的求解建立数学基础",
   "pending_concepts": ["Schwarzschild解的具体形式", "联络系数的显式计算", "曲率张量与Einstein场方程的关联", "边界条件与度规参数的确定"]
}
</CTX>