# Slide 27

## 2.5 协变微分

### 1. 标量场的协变微分

标量场的普通微分 $U_{,\mu} = \frac{\partial U(x)}{\partial x^\mu}$

协变  
这是一个矢量，证明：$U(x) = U'(x')$

$$U'_{,\mu} = \frac{\partial U'(x')}{\partial x'^\mu} = \frac{\partial U'(x')}{\partial x^\alpha} \frac{\partial x^\alpha}{\partial x'^\mu} = \frac{\partial U(x)}{\partial x^\alpha} \frac{\partial x^\alpha}{\partial x'^\mu} = U_{,\alpha} \frac{\partial x^\alpha}{\partial x'^\mu}$$

即 $U_{;\mu} = U_{,\mu}$  
协变微分 = 普通微分

### 2. 协变矢量场的协变微分

$$A_{\mu;\nu} \equiv \frac{\partial A_\mu}{\partial x^\nu} \equiv \lim_{Q \to P} \frac{A_\mu(Q) - A_\mu(P)}{\Delta x^\nu}$$

$$A_{\mu;\nu} \equiv \lim_{Q \to P} \frac{A_\mu(Q) - A_\mu(P \to Q)}{\Delta x^\nu} \equiv \lim_{Q \to P} \frac{A_\mu(Q) - [A_\mu(P) + \Gamma^\lambda_{\mu\nu}\Delta x^\nu A_\lambda]}{\Delta x^\nu}$$

$$= \lim_{Q \to P} \frac{A_\mu(Q) - A_\mu(P)}{\Delta x^\nu} - \Gamma^\lambda_{\mu\nu} A_\lambda$$

$$A_{\mu;\nu} = A_{\mu,\nu} - \Gamma^\lambda_{\mu\nu} A_\lambda$$

## Figure & Layout Description

这张PPT页面采用手写笔记风格，背景为浅米色方格纸样式，模拟了在方格笔记本上书写的视觉效果。所有文字和公式均以橙色手写体呈现，字体大小不一，体现手写笔记的自然感。

页面顶部是标题"2.5 协变微分"，使用较大字号的橙色手写体。内容分为两个主要部分，分别以"1. 标量场的协变微分"和"2. 协变矢量场的协变微分"作为小标题。

第一部分包含标量场普通微分的定义公式，以及协变性质的证明过程。公式推导过程清晰，包含多个等号连接的变换步骤，每个步骤间有适当间距以便阅读。在推导过程中，有"协变"、"这是一个矢量，证明："等手写注释文字，用以解释推导的物理意义。

第二部分主要展示协变矢量场的协变微分定义。右侧有一个简图，显示点P到点Q的位移向量$\Delta x^\nu$，以及在P点、Q点和P点平行移动到Q点的矢量$A_\mu(P)$、$A_\mu(Q)$和$A_\mu(P \to Q)$。图中用箭头连接这些矢量，直观展示了协变微分的几何意义。

公式中的希腊字母、下标和上标均清晰可辨，包括$\mu$、$\nu$、$\alpha$、$\lambda$等。极限符号$\lim_{Q \to P}$和偏导数符号$\frac{\partial}{\partial x^\mu}$书写规范。联络系数$\Gamma^\lambda_{\mu\nu}$的上下标位置准确，上标$\lambda$在右上方，下标$\mu\nu$在右下方。

页面布局呈纵向排列，内容从上至下依次展开，公式推导部分占据主要空间。整体视觉层次分明，标题、小标题、公式和注释通过字号和位置区分，便于阅读和理解协变微分的概念。

<CTX>
{
   "topic": "协变微分的定义与计算方法",
   "keywords": ["协变微分", "标量场", "协变矢量场", "联络系数", "微分算子", "平行移动"],
   "summary": "本页详细介绍了标量场和协变矢量场的协变微分定义及计算方法，揭示了协变微分与普通微分的区别，以及联络系数在协变微分中的关键作用",
   "pending_concepts": ["协变张量场的协变微分", "协变微分的几何意义", "协变微分与曲率的关系", "高阶张量的协变微分"]
}
</CTX>