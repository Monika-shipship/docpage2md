# Slide 19

上式乘 $g^{\alpha\lambda}$  
$$g^{\alpha\lambda} \nabla_{\lambda} R_{\alpha\sigma} + g^{\alpha\lambda} \nabla_{\mu} R^{\mu}_{\ \ \alpha\sigma\lambda} = g^{\alpha\lambda} \nabla_{\sigma} R_{\alpha\lambda}$$  
由前假设 $\nabla_{\mu} g^{\alpha\lambda} = 0$，$g$ 和 $\nabla$ 可交换  
$$\nabla_{\lambda} \left( g^{\alpha\lambda} R_{\alpha\sigma} \right) + \nabla_{\mu} \left( g^{\alpha\lambda} R^{\mu}_{\ \ \alpha\sigma\lambda} \right) = \nabla_{\sigma} \left( g^{\alpha\lambda} R_{\alpha\lambda} \right)$$  
定义 $R^{\lambda}_{\sigma} = g^{\alpha\lambda} R^{\mu}_{\ \ \alpha\sigma\lambda}$ $\quad \downarrow$  
$\quad R$  
则  
$$\nabla_{\lambda} \left( R^{\lambda}_{\sigma} \right) + \nabla_{\mu} \left( R^{\mu}_{\sigma} \right) = \nabla_{\sigma} \left( R \right)$$  
$$2 \nabla_{\mu} R^{\mu}_{\sigma} = \nabla_{\sigma} R$$  
$$\nabla_{\mu} R^{\mu}_{\sigma} = \frac{1}{2} \nabla_{\sigma} R = \frac{1}{2} g^{\mu}_{\sigma} \nabla_{\mu} R$$  
$$\nabla_{\mu} \left( R^{\mu}_{\sigma} - \frac{1}{2} g^{\mu}_{\sigma} R \right) = 0$$  
$\quad \underbrace{\qquad \qquad \qquad \qquad}_{\downarrow}$  
$\quad G^{\mu}_{\sigma}$，Einstein 张量  
故 $\nabla_{\mu} G^{\mu}_{\sigma}$，协变散度为 $0$.

## Figure & Layout Description
手写内容以黑色墨水书写于浅米色方格纸背景上，方格线为浅灰色细线构成均匀网格。文字内容垂直排列，共12行，包含数学公式与中文说明。公式部分使用标准张量符号，包含希腊字母（$\alpha, \lambda, \mu, \sigma$）、协变导数符号（$\nabla$）、度规张量（$g$）和曲率张量（$R$）。关键推导步骤间用箭头（$\downarrow$）连接逻辑关系，最后一行公式下方有蓝色手绘波浪线标注重点。文字书写工整但带有自然的手写倾斜，部分下标（如$R^{\mu}_{\ \ \alpha\sigma\lambda}$）通过空格区分多层指标。公式与中文说明交替出现，形成"推导步骤-解释-新推导"的递进结构。

<CTX>
{
   "topic": "Einstein张量协变散度为零的推导",
   "keywords": ["Einstein张量", "协变散度", "曲率标量缩并", "度规相容性", "Bianchi恒等式应用"],
   "summary": "通过度规缩并和Bianchi恒等式推导出Einstein张量的协变散度为零，为爱因斯坦场方程的协变性奠定数学基础",
   "pending_concepts": ["曲率标量的物理意义", "共形曲率张量的分解方法", "能量-动量张量的协变守恒"]
}
</CTX>