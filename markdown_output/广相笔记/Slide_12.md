# Slide 12

而 $g^{\lambda\nu} g_{\nu\lambda} = \frac{1}{n} g^\lambda_\lambda = g$

$$
\frac{\partial g}{\partial x^\mu} = g^{\lambda\nu} \frac{\partial g_{\lambda\nu}}{\partial x^\mu} + \frac{\partial g^{\lambda\nu}}{\partial x^\mu} g_{\lambda\nu} \quad || \ 0
$$

? 待补充

$$
\frac{\partial g}{\partial x^\mu} = n \, g^{\lambda\nu} \frac{\partial g_{\lambda\nu}}{\partial x^\mu}
$$
$$
= g \, g^{\lambda\nu} \frac{\partial g_{\lambda\nu}}{\partial x^\mu}
$$
$$
\frac{1}{g} \frac{\partial g}{\partial x^\mu} = \frac{\partial \ln g}{\partial x^\mu} = g^{\lambda\nu} \frac{\partial g_{\lambda\nu}}{\partial x^\mu}
$$

$$
\Gamma^\lambda_{\mu\lambda} = \frac{1}{2} g^{\sigma\lambda} \partial_\mu g_{\sigma\lambda}
$$
$$
= \frac{1}{2} \frac{1}{g} \frac{\partial g}{\partial x^\mu}
$$
$$
\Gamma^\lambda_{\mu\lambda} = \frac{\partial \ln \sqrt{g}}{\partial x^\mu}
$$

$$
\frac{1}{\sqrt{g}} \frac{1}{2\sqrt{g}} \frac{\partial g}{\partial x^\mu} = \frac{1}{\sqrt{g}} \frac{\partial \sqrt{g}}{\partial x^\mu} = \partial \ln \sqrt{g}
$$

用处：$\nabla_\mu \phi^\lambda = \partial_\mu \phi^\lambda + \Gamma^\lambda_{\mu\alpha} \phi^\alpha$

协变散度：$\mu \to \lambda$
$$
\nabla_\lambda \phi^\lambda = \partial_\lambda \phi^\lambda + \Gamma^\lambda_{\lambda\alpha} \phi^\alpha
$$
$$
= \partial_\lambda \phi^\lambda + \frac{\partial \ln \sqrt{g}}{\partial x^\lambda} \phi^\lambda
$$
$$
\lambda \to \lambda
$$

## Figure & Layout Description

图片为方格纸背景的手写数学推导，整体布局呈纵向排列。顶部起始公式为"而 $g^{\lambda\nu} g_{\nu\lambda} = \frac{1}{n} g^\lambda_\lambda = g$"，采用黑色墨水书写。第二行是偏导数展开式，右侧标注"|| 0"表示第二项为零。中间区域有红色手写文字"? 待补充"，下方接续推导过程。

关键公式$\frac{1}{g} \frac{\partial g}{\partial x^\mu} = \frac{\partial \ln g}{\partial x^\mu} = g^{\lambda\nu} \frac{\partial g_{\lambda\nu}}{\partial x^\mu}$被红色波浪线完整下划，作为视觉焦点。克氏联络表达式$\Gamma^\lambda_{\mu\lambda} = \frac{1}{2} g^{\sigma\lambda} \partial_\mu g_{\sigma\lambda}$及其等价形式垂直排列于中下部，右侧有独立推导分支显示$\frac{1}{\sqrt{g}} \frac{1}{2\sqrt{g}} \frac{\partial g}{\partial x^\mu}$的简化过程。

底部区域包含"用处"说明和协变散度推导，公式间存在逻辑递进关系。所有公式均采用手写体数学符号，下标/上标位置精确，部分希腊字母（如$\Gamma$、$\nu$）书写清晰。整体排版保持物理公式推导的典型垂直流式结构，无表格或图形元素。

<CTX>
{
   "topic": "克氏联络与度规行列式的关系推导及协变散度表达式",
   "keywords": ["克氏联络", "度规相容条件", "指标轮换", "度规行列式", "协变散度", "克氏降指标", "黎曼联络唯一性"],
   "summary": "本页通过度规行列式与克氏联络的关联推导，建立了协变散度的显式表达式，补充了度规相容性条件在张量场散度计算中的具体应用",
   "pending_concepts": ["曲率张量的显式计算", "测地线方程的推导", "联络系数的物理意义", "克氏联络在弯曲时空中的应用"]
}
</CTX>