# Slide 22

## 1.8 微分形式与外积

### 1.8.1 $dx^\mu$ 的外积

先定义内积：  
$<\phi|\psi> = g_{\mu\nu}\phi^\mu\psi^\nu$

若 $\psi = \phi$，$<\phi,\phi> = g_{\mu\nu}\phi^\mu\phi^\nu$.

外积：$dx^\mu \wedge dx^\nu$

定义对易 $dx^\mu \wedge dx^\nu = -dx^\nu \wedge dx^\mu$.

是叉乘的推广.

### 1.8.2 1-形式

协变矢量可定义 1-形式 (1-form)  
$a = a_\mu dx^\mu$.

其外微分：$da = \partial_\mu a_\nu dx^\mu \wedge dx^\nu$  
原指标对换 $= \partial_\nu a_\mu dx^\nu \wedge dx^\mu$

$$
da = \frac{1}{2} \left( \partial_\mu a_\nu dx^\mu \wedge dx^\nu + \partial_\nu a_\mu dx^\nu \wedge dx^\mu \right)
$$

$$
= \frac{1}{2} \left( \partial_\mu a_\nu dx^\mu \wedge dx^\nu - \partial_\nu a_\mu dx^\mu \wedge dx^\nu \right)
$$

$$
da = \frac{1}{2} \left( \partial_\mu a_\nu - \partial_\nu a_\mu \right) dx^\mu \wedge dx^\nu.
$$

令 $F_{\mu\nu} = \partial_\mu a_\nu - \partial_\nu a_\mu$

$$
da = \frac{1}{2} F_{\mu\nu} dx^\mu \wedge dx^\nu \text{ 称为 } a_\mu \text{ 的旋度张量}.
$$

## Figure & Layout Description
图片为手写笔记风格，背景是浅黄色方格纸（类似数学练习本），方格线为浅灰色。文字和公式全部用黑色墨水书写，字迹工整清晰。整体内容分为两个主要章节：1.8.1 和 1.8.2，标题"1.8 微分形式与外积"位于页面左上角，使用较大字号。1.8.1 部分首先定义内积，接着讨论外积的对易关系；1.8.2 部分从 1-形式的定义开始，逐步推导外微分的表达式，包含多步公式推导，每步公式均左对齐排列。公式中使用了希腊字母（μ, ν）、偏导符号（∂）、楔积符号（∧）等数学符号，下标和上标书写规范。页面右侧有较大空白区域，无其他图形或装饰元素。整体排版层次分明，逻辑推导过程清晰可见，具有典型的课堂笔记特征。

<CTX>
{
   "topic": "微分形式与外积的基本概念",
   "keywords": ["微分形式", "外积", "1-形式", "外微分", "旋度张量"],
   "summary": "本页介绍了微分形式与外积的基础知识，包括内积定义、外积对易关系以及1-形式的外微分计算，为后续曲率张量和Gauss-Bonnet-Chern定理的数学表述提供工具基础",
   "pending_concepts": ["外微分的坐标无关性", "更高阶微分形式的构造", "外积与内积的统一框架", "旋度张量在物理中的具体应用"]
}
</CTX>