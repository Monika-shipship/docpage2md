# Slide 110

并且 $ds=0$，不能用 $S$ 作参数 $X^\mu = X^\mu(S)$  
引入一任意参数 $\lambda$  
定义光切矢 $K^\mu = \frac{dx^\mu}{d\lambda}$，$X^\mu = X^\mu(\lambda)$，  
光切 $ds^2=0$，有 $K^2 = g_{\mu\nu} K^\mu K^\nu = 0$。  

切矢 $K^\mu$ 在传播路径上平行，即  
$$K^\mu \nabla_\mu K^\lambda = 0.$$  
$$K^\mu \left( \partial_\mu K^\lambda + \Gamma^\lambda_{\mu\nu} K^\nu \right) = 0.$$  
$$\frac{dx^\mu}{d\lambda} \frac{\partial K^\lambda}{\partial x^\mu} + \Gamma^\lambda_{\mu\nu} K^\nu K^\mu = 0$$  
$$\frac{dK^\lambda}{d\lambda} + \Gamma^\lambda_{\mu\nu} K^\nu K^\mu = 0,$$  
$$K^\lambda = \frac{dx^\lambda}{d\lambda}$$  
$$\frac{d^2 x^\lambda}{d\lambda^2} + \Gamma^\lambda_{\mu\nu} \frac{dx^\mu}{d\lambda} \frac{dx^\nu}{d\lambda} = 0. \text{ 即光的测地线方程，}$$

## Figure & Layout Description
图片为方格纸背景的单页手写内容，整体布局为纵向排列的数学推导过程。文字与公式以黑色墨水书写，字迹清晰但略带手写体特征。背景为浅米色方格纸，网格线为浅灰色，每格约1cm×1cm。内容从上至下分为七行主要推导段落，每段包含中文说明与数学公式。第一行文字起始于左上角，后续段落依次向下排列，行间距适中。公式中使用了希腊字母（如 $\lambda$、$\mu$、$\nu$）、张量符号（如 $K^\mu$、$g_{\mu\nu}$）及微分算符（如 $\frac{dx^\mu}{d\lambda}$）。部分公式包含多行展开，如协变导数展开过程分为三行递进式表达。文字与公式混合排版，中文说明与数学符号间无明显分隔，但通过上下文逻辑保持连贯性。无彩色元素或图形插图，仅包含纯文本与数学表达式。

<CTX>
{
   "topic": "光子测地线方程的参数化推导与协变形式",
   "keywords": ["光切矢", "参数化测地线", "零测地线条件", "协变导数展开", "测地线方程"],
   "summary": "本页通过引入任意参数λ重新参数化光子路径，推导出零测地线条件下协变形式的测地线方程，并明确其与经典测地线方程的数学等价性",
   "pending_concepts": ["弱场近似下测地线方程的显式解", "参数λ与物理时间的对应关系", "克里斯托费尔符号在具体度规中的展开方法"]
}
</CTX>