# Slide 41

$$L = \int_{\sigma_1}^{\sigma_2} \sqrt{-ds^2}\ ,\ \text{记}\ \dot{x}^\mu = \frac{dx^\mu}{d\sigma}$$
$$= \int_{\sigma_1}^{\sigma_2} \sqrt{-g_{\mu\nu}\dot{x}^\mu\dot{x}^\nu}\cdot d\sigma$$

L 取极值时，称 L 为短程线

$$\delta L = 0 \Rightarrow \begin{cases} 
\text{极大} \\ 
\text{极小} \\ 
\text{平稳} 
\end{cases}$$

测地线不一定最短！

记 $F = F(x,\dot{x}) = \sqrt{-g_{\mu\nu}\dot{x}^\mu\dot{x}^\nu}$

$\delta\int F\,d\sigma = 0$ 求 $x^\mu = x^\mu(\sigma)$ 路径，

用欧-拉方程 $\frac{d}{d\sigma}\left(\frac{\partial F}{\partial\dot{x}^\mu}\right) - \frac{\partial F}{\partial x^\mu} = 0$

$F = \sqrt{-g_{\alpha\beta}\dot{x}^\alpha\dot{x}^\beta}$

$$\frac{d}{d\sigma}\left(\frac{\partial F}{\partial\dot{x}^\mu}\right) = \frac{d}{d\sigma}\left(\frac{1}{2\sqrt{-g_{\alpha\beta}\dot{x}^\alpha\dot{x}^\beta}}\cdot\frac{\partial}{\partial\dot{x}^\mu}(-g_{\alpha\beta}\dot{x}^\alpha\dot{x}^\beta)\right)$$

## Figure & Layout Description
图片为手写数学推导内容，背景是浅米色方格纸（网格线为浅灰色，间距均匀），文字和公式以黑色墨水书写。内容从上至下垂直排列，包含多行公式和文字说明。第一行是测地线长度L的定义公式，包含积分符号和度规张量项；第二行是L的展开形式，显示了度规张量与切矢量乘积的平方根积分。第三部分是关于L取极值的文字说明，"短程线"三字被特别强调。第四部分是变分条件δL=0的分类说明，使用大括号括起三个选项（极大、极小、平稳），其中"极小"旁有对勾标记。第五行是醒目的感叹句"测地线不一定最短！"，字体略大且末尾有感叹号强调。接下来是函数F的定义及变分原理应用说明，最后两行是欧拉-拉格朗日方程的具体展开，包含复杂的偏导数和链式求导表达式。整体布局清晰，公式与文字交替出现，关键概念和结论有视觉强调。

<CTX>
{
   "topic": "测地线方程的变分推导",
   "keywords": ["测地线", "变分原理", "欧拉-拉格朗日方程", "短程线", "仿射参量"],
   "summary": "本页通过变分法推导测地线方程，阐明了测地线作为短程线的数学本质及变分条件",
   "pending_concepts": ["测地线方程的具体解法", "仿射参量的物理意义", "类时/类空测地线的区分条件"]
}
</CTX>