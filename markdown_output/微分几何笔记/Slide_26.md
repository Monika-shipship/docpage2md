# Slide 26

③ 曲率，挠率和容许参数无关

容许参数：正则曲线对应参数 要求 $\frac{ds}{du} > 0$

Frenet 公式  
$$\dot{\vec{t}} = k(s) \vec{n}$$  
$$\dot{\vec{n}} = -k(s)\vec{t} + \tau(s) \vec{b}$$  
$$\dot{\vec{b}} = -\tau(s)\vec{n}$$  

定义：  
$\vec{t}(s) = \dot{\vec{r}}(s)$  
$\vec{n} = \frac{\ddot{\vec{r}}}{|\ddot{\vec{r}}|} = \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|}$  
$\dot{\vec{n}} = \frac{d}{ds} \left( \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|} \right)$  
$\vec{b} = \vec{t} \wedge \vec{n} = \dot{\vec{r}}(s) \wedge \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|}$  
$\dot{\vec{b}} = \frac{d}{ds} \left( \dot{\vec{r}}(s) \wedge \frac{\ddot{\vec{r}}(s)}{|\ddot{\vec{r}}(s)|} \right)$  

所以 Frenet 标架只和 $\dot{\vec{r}}(s)$ 和 $\ddot{\vec{r}}(s)$ 有关

现只用证 $\dot{\vec{r}}(s)$ 与容许参数无关

设 $s_1$ 和 $s_2$：  
$s_1 = s_2 + C$  
$\frac{d\vec{r}}{ds_1} = \frac{d\vec{r}}{d(s_2 + C)} = \frac{d\vec{r}}{ds_2}$  
$\frac{d}{ds_1} \left( \frac{d\vec{r}}{ds_1} \right) = \frac{d}{ds_2} \left( \frac{d\vec{r}}{ds_2} \right)$  

所以 $\dot{\vec{r}}(s)$ 与 $s$ 的选取无关

设 $t$ 是 $\vec{r}(u)$ 的容许参数  
$S(t) = \int_0^t |\vec{r}'(u)| du$  
$S'(t) = |\vec{r}'(u)| > 0$（$S$ 严格增）  
存在反函数 $t = t(s)$  

所以与容许参数无关

## Figure & Layout Description
手写笔记呈现于米黄色方格纸背景上，网格线为浅灰色细线。内容以黑色墨水书写，整体分为三个逻辑区域：顶部为标题区（"③ 曲率，挠率和容许参数无关"及容许参数定义），中部为Frenet公式列表与推导过程（包含6组向量公式），底部为参数无关性证明（含积分表达式和反函数推导）。文字布局呈纵向排列，公式间通过等号对齐形成视觉层次。关键结论"所以Frenet标架只和..."使用下划线强调，"S严格增"旁有手写箭头标注。部分符号如$\vec{r}$、$\dot{\vec{t}}$等向量符号书写清晰，积分上下限和导数符号完整。左侧有手写"n阶"标记，疑似章节编号。

<CTX>
{
   "topic": "Frenet标架与容许参数的无关性证明",
   "keywords": ["曲率", "挠率", "Frenet标架", "弧长参数", "参数变换不变性"],
   "summary": "证明Frenet标架仅依赖弧长参数，与容许参数选择无关，建立几何不变量与参数化的本质联系",
   "pending_concepts": ["挠率的几何意义", "非弧长参数下的Frenet公式修正"]
}
</CTX>