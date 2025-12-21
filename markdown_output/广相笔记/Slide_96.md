# Slide 96

## 3.2 行星轨道进动

### 3.2.1 Newton引力下

$$
\frac{d^2 \vec{r}}{dt^2} = -\frac{GM}{r^2} \vec{e_r}
$$

选轨道面 $\theta = \frac{\pi}{2}$（球坐标系中）

有三个结论

1. **面速度守恒**

   $$
   dA = \frac{1}{2} r \cdot r d\phi = \frac{1}{2} r^2 d\phi
   $$
   $$
   \frac{dA}{dt} = \frac{1}{2} r^2 \dot{\phi}
   $$
   而角动量守恒 $m \dot{\phi} r^2 = L \Rightarrow \dot{\phi} r^2 = \frac{L}{m} \equiv h$
   
   故 $\frac{dA}{dt} = \frac{h}{2} = \frac{L}{2m}$ 是守恒量

2. 
   $$
   \ddot{\vec{r}} = -\frac{GM}{r^2} \vec{e_r}
   $$
   $$
   \Rightarrow \begin{cases}
   \ddot{r} - \dot{\phi}^2 r = -\frac{GM}{r^2} \Rightarrow \text{Binet方程} \\
   \ddot{\phi} r + 2\dot{\phi}\dot{r} = 0 \Rightarrow \frac{d}{dt}(\dot{\phi} r^2) = 0 \Rightarrow \text{角动量守恒}
   \end{cases}
   $$

   作换元 $u = \frac{1}{r}$
   
   可得比内方程 $\frac{d^2 u}{d\phi^2} + u = -\frac{r^2 F_r}{m h^2} = \frac{GM}{h^2}$
   
   解为 $u = \frac{1}{p}(1 + e \cos \phi)$

## Figure & Layout Description

手写笔记内容呈现在浅米色方格纸背景上，文字为黑色墨水手写体。整体布局为纵向排列的数学推导过程：

1. 顶部左侧书写主标题"3.2 行星轨道进动"，字迹较大且加粗
2. 其下左侧书写子标题"3.2.1 Newton引力下"
3. 中间区域包含核心运动方程，使用标准微分符号和向量箭头
4. 左侧中部有一个手绘椭圆轨道示意图，椭圆内标有"A"点和"dφ"角度标记，线条为黑色椭圆轮廓
5. 右侧对应示意图区域是面积速度守恒的推导公式，包含微分表达式和守恒量推导
6. 下方分两点列出结论，每个结论前有带圈数字编号
7. 第二个结论部分包含大括号分组的联立方程组，右侧有中文注释说明
8. 最底部是变量替换和比内方程的推导过程，最终给出轨道方程解

所有公式和文字均按教学笔记的逻辑顺序排列，重要结论用下划线或加粗方式强调（通过手写加粗实现）。方格纸的网格线作为背景参考，但不影响文字内容的可读性。

<CTX>
{
   "topic": "牛顿引力框架下行星轨道运动与开普勒定律的推导",
   "keywords": ["开普勒第二定律", "Binet方程", "比内方程", "角动量守恒", "面积速度"],
   "summary": "本页推导了牛顿引力下的行星轨道运动方程，通过角动量守恒和Binet方程验证开普勒定律并得到椭圆轨道解",
   "pending_concepts": ["相对论修正对轨道进动的影响", "Schwarzschild度规与牛顿近似的对应关系", "轨道参数p和e的物理意义"]
}
</CTX>