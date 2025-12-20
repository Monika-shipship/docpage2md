# Slide 5

# 单电子(H)原子-中心力场薛定谔方程

- **分离变量**  
  $u(\mathbf{r}) = u(r, \theta, \varphi) = R(r) Y(\theta, \varphi)$  
  <span style="color:red">径向波函数</span> &nbsp;&nbsp;&nbsp;&nbsp; <span style="color:red">角向波函数</span>

  $$
  \frac{1}{R} \frac{d}{dr} \left( r^2 \frac{dR}{dr} \right) + \frac{2mr^2}{\hbar^2} [E - V(r)] = -\frac{1}{Y \sin \theta} \frac{\partial}{\partial \theta} \left( \sin \theta \frac{\partial Y}{\partial \theta} \right) - \frac{1}{Y \sin^2 \theta} \frac{\partial^2 Y}{\partial \varphi^2} \equiv \text{常数} \lambda
  $$

  $$
  \begin{cases}
  \frac{1}{r^2} \frac{d}{dr} \left( r^2 \frac{dR}{dr} \right) + \left[ \frac{2m}{\hbar^2} (E - V(r)) - \frac{\lambda}{r^2} \right] R = 0 & \text{径向方程} \\
  \\
  -\frac{1}{\sin \theta} \frac{\partial}{\partial \theta} \left( \sin \theta \frac{\partial Y}{\partial \theta} \right) - \frac{1}{\sin^2 \theta} \frac{\partial^2 Y}{\partial \varphi^2} = \lambda Y & \text{角向方程}
  \end{cases}
  $$

## Figure & Layout Description

页面顶部是黑色粗体一级标题"单电子(H)原子-中心力场薛定谔方程"，下方有一条细灰线分隔。左侧区域以红色项目符号"▶"开头，标注"分离变量"（红色字体）。其下方是波函数分离公式 $u(\mathbf{r}) = u(r, \theta, \varphi) = R(r) Y(\theta, \varphi)$，公式中有两条蓝色箭头分别指向下方的红色文字"径向波函数"和"角向波函数"。中间区域展示一个大型等式，左侧为径向部分，右侧为角向部分，等号右侧标注"≡常数λ"。该等式下方有一个大型蓝色右向箭头，指向由大括号括起的两个方程组。右侧区域是一个球坐标系示意图：中心为带"+"号的原子核（标注"mₚ"），外围有电子轨道（标注"mₑ"），用黑色实线和虚线表示球面，标注球坐标变量"r"（径向矢量）、"θ"（极角）和"φ"（方位角）。底部两个方程中，"径向方程"和"角向方程"以蓝色字体标注在对应方程右侧。整体布局为左文右图结构，公式区域使用标准数学排版，关键术语通过颜色（红/蓝）和箭头实现视觉强调。

<CTX>
{
  "topic": "单电子原子薛定谔方程的分离变量解法",
  "keywords": ["薛定谔方程", "球坐标系", "分离变量", "径向波函数", "角向波函数", "库仑势"],
  "summary": "本页详细阐述了通过分离变量法将单电子原子薛定谔方程分解为径向方程和角向方程的数学过程，明确了波函数的径向与角向组成部分。",
  "pending_concepts": ["常数λ的物理意义", "径向/角向方程的具体求解方法"]
}
</CTX>