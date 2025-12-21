# Slide 56

$$
\frac{d^2 x^i}{ds^2} = \frac{\partial}{\partial t} \left[ \frac{1}{c} \frac{dx^i}{dt} \frac{1}{\sqrt{1-h_{00}}} \right] \frac{dt}{ds}
$$

$$
+ \frac{\partial}{\partial x^j} \left[ \frac{1}{c} \frac{1}{\sqrt{1-h_{00}}} \right] \frac{dx^i}{dt} \frac{dx^j}{ds}
$$

$$
\frac{dt}{ds} = \frac{1}{c} \frac{1}{\sqrt{1-h_{00}}}, \quad \text{且} \quad \frac{1}{c} \frac{dx^i}{dt} \ll 1
$$

第二项略去

$$
\frac{d^2 x^i}{ds^2} = \frac{\partial}{\partial t} \left[ \frac{1}{c} \frac{dx^i}{dt} \frac{1}{\sqrt{1-h_{00}}} \right] \frac{1}{c} \frac{1}{\sqrt{1-h_{00}}}
$$

$$
= \left[ \frac{1}{c} \frac{d^2 x^i}{dt^2} \frac{1}{\sqrt{1-h_{00}}} + \frac{1}{c} \frac{dx^i}{dt} \partial_t \frac{1}{\sqrt{1-h_{00}}} \right] \frac{1}{c} \frac{1}{\sqrt{1-h_{00}}}
$$

$$
\frac{d^2 x^i}{ds^2} = \frac{1}{c^2} \frac{d^2 x^i}{dt^2} \frac{1}{1-h_{00}}
$$

## Figure & Layout Description
图像为方格纸背景的手写推导过程，所有内容以黑色墨水书写，关键项用蓝色笔划去。页面顶部为第一组公式，包含两个主要项，第二项被蓝色斜线划掉。中间区域有中文注释"第二项略去"，其上方有"dt/ds"的表达式和条件"1/c dxⁱ/dt <<1"。下方为推导的中间步骤，包含展开后的括号项，其中时间导数项被蓝色下划线标记为"≈0"。最底部为最终简化结果。公式中的下标（如h₀₀）使用标准手写体，平方根符号完整，分数线清晰。所有数学符号（∂, d, √）均符合物理文献规范，蓝色标记仅用于强调被忽略的高阶项。

<CTX>
{
   "topic": "弱场近似下空间测地线二阶导数的简化推导",
   "keywords": ["弱场近似", "h_{00}展开", "高阶小量忽略", "空间加速度", "测地线方程简化"],
   "summary": "通过忽略速度相关高阶小量，将空间坐标二阶协变导数简化为仅含h_{00}的显式表达式，建立与牛顿力学的直接联系",
   "pending_concepts": ["h_{00}的具体物理形式", "时间导数项被忽略的严格条件", "与泊松方程的衔接逻辑"]
}
</CTX>