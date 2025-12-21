# Slide 27

1.9.2 不变体积元

$dx^\mu$ 是逆变矢量  
$$dx'^\mu = \Lambda^\mu_\nu dx^\nu \quad \Lambda^\mu_\nu = \frac{\partial x'^\mu}{\partial x^\nu}$$

$n$维流形上的体积元记作 $d^n x$。  
定义：$d^n x = dx^1 \wedge dx^2 \wedge \cdots \wedge dx^n$，  
不是标量，  
但 $\frac{1}{n!} \sqrt{g} \epsilon_{\mu_1 \mu_2 \cdots \mu_n} dx^{\mu_1} \wedge dx^{\mu_2} \wedge \cdots \wedge dx^{\mu_n}$  
（是不变体积元）  
$$= \sqrt{g} dx^1 \wedge dx^2 \wedge \cdots \wedge dx^n$$  
$$= \sqrt{g} d^n x$$

$n!$？因为 $\epsilon_{\mu_1 \mu_2 \cdots \mu_n}$ 重复计数了 $n \times (n-1) \times \cdots \times 1 = n!$ 次。

## Figure & Layout Description
图片为浅黄色方格纸背景的手写笔记，文字以黑色墨水书写。内容从左上角开始纵向排列：
1. 标题"1.9.2 不变体积元"位于页面顶部偏左位置，字体略大且加粗
2. 核心公式区域占据页面中上部，包含两组行间公式：第一组为坐标变换关系式，第二组为体积元定义
3. 文字说明部分采用左对齐方式，关键结论"是不变体积元"被手写圆圈标记，并有向下箭头指向后续推导步骤
4. 所有公式中的外积符号"∧"均以手写形式呈现，Levi-Civita符号$\epsilon$的下标清晰标注
5. 页面底部有$n!$的解释性文字，末尾"次"字后有手写句号
6. 整体布局保持数学推导的逻辑顺序，重要结论通过符号标记（圆圈、箭头）进行视觉强调

<CTX>
{
   "topic": "不变体积元的坐标不变性与Levi-Civita张量应用",
   "keywords": ["不变体积元", "Levi-Civita张量", "度规行列式", "外微分形式", "坐标变换"],
   "summary": "本页通过Levi-Civita张量和度规行列式推导出n维流形上不变体积元的表达式，证明其在坐标变换下的不变性，为Gauss-Bonnet定理的积分形式提供几何基础",
   "pending_concepts": ["体积元在弯曲时空中的物理意义", "Hodge对偶算子与体积元的关系", "边界项对体积元积分的影响"]
}
</CTX>