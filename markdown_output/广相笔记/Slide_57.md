# Slide 57

## 正文内容

短程线方程：  
$$\frac{d^2 x^\lambda}{ds^2} + \Gamma^\lambda_{\alpha\beta} \frac{dx^\alpha}{ds} \frac{dx^\beta}{ds} = 0.$$

代入 Newton 近似：  
$$\frac{1}{c^2} \frac{d^2 x^\lambda}{dt^2} \frac{1}{1-h_{00}} + \Gamma^\lambda_{\alpha\beta} \frac{dx^\alpha}{ds} \frac{dx^\beta}{ds} = 0.$$

一次项有：  
$$\frac{dx^0}{ds} = \frac{1}{\sqrt{1-h_{00}}}, \quad \frac{d^2 x^0}{ds^2} \to 0.$$  
$$\frac{dx^i}{ds} = \frac{1}{c} \frac{dx^i}{dt} \frac{1}{\sqrt{1-h_{00}}} \ll 1$$

起 $\Gamma^\lambda_{\alpha\beta}$ 只有 $0$ 时不为小量  
$\lambda$ 为 $0$ 时小量，$\lambda$ 取 $i=1,2,3$.  
$$\frac{1}{c^2} \frac{d^2 x^i}{dt^2} \frac{1}{1-h_{00}} + \Gamma^i_{00} \frac{dx^0}{ds} \frac{dx^0}{ds} = 0.$$

## Figure & Layout Description

图片为方格纸背景的手写数学推导内容，整体布局为纵向分段式结构。文字与公式均以黑色墨水书写，字体为工整的手写体，部分符号带有轻微连笔。内容分为四个逻辑区块：

1. **标题区块**：位于页面顶部，手写"短程线方程："作为标题，字体略大于正文。
2. **主方程区块**：标题下方为测地线方程的完整表达式，包含二阶导数项和Christoffel符号项，公式居中书写且占两行。
3. **近似代入区块**：标注"代入 Newton 近似"，下方为引入$1/c^2$和$1/(1-h_{00})$因子的修正方程，公式中$dt^2$项被特别标注。
4. **项分析区块**：包含"一次项有："引导的三组条件式，其中速度项$\frac{dx^i}{ds}$旁标注$\ll 1$，并有中文注释说明Christoffel符号的非小量条件，最后给出空间分量的简化方程。

页面左侧留有约1cm空白边距，公式中的$h_{00}$下标清晰可辨，所有分式均采用水平分数线书写，$c^2$、$dt^2$等符号的上标格式规范。部分中文注释（如"起"、"取"）存在手写连笔现象，但通过上下文可明确语义。

<CTX>
{
   "topic": "牛顿近似下测地线方程空间分量的显式推导",
   "keywords": ["测地线方程代入", "速度项忽略条件", "空间加速度表达式", "Christoffel符号简化"],
   "summary": "通过代入牛顿近似并分析一次项量级，将测地线方程空间分量简化为仅含h_{00}和时间导数的显式加速度方程",
   "pending_concepts": ["h_{00}与引力势的具体关系", "时间导数项被忽略的严格数学条件", "空间加速度与牛顿引力场的直接对应形式"]
}
</CTX>