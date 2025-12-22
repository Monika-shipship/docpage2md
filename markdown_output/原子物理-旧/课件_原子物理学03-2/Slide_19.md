# Slide 19

# 单电子(H)原子-中心力场薛定谔方程

- 分离变量

$$ u(\mathbf{r}) = u(r, \theta, \varphi) = R(r) Y(\theta, \varphi) $$

*径向波函数*  
*角向波函数*

$$ \frac{1}{R} \frac{d}{dr} \left( r^2 \frac{dR}{dr} \right) + \frac{2mr^2}{\hbar^2} [E - V(r)] = -\frac{1}{Y \sin\theta} \frac{\partial}{\partial\theta} \left( \sin\theta \frac{\partial Y}{\partial\theta} \right) - \frac{1}{Y \sin^2\theta} \frac{\partial^2 Y}{\partial\varphi^2} = \text{常数} \lambda $$

$$
\begin{cases}
\frac{1}{r^2} \frac{d}{dr} \left( r^2 \frac{dR}{dr} \right) + \left[ \frac{2m}{\hbar^2} (E - V(r)) - \frac{\lambda}{r^2} \right] R = 0 & \text{径向方程} \\
-\frac{1}{\sin\theta} \frac{\partial}{\partial\theta} \left( \sin\theta \frac{\partial Y}{\partial\theta} \right) - \frac{1}{\sin^2\theta} \frac{\partial^2 Y}{\partial\varphi^2} = \lambda Y & \text{角向方程}
\end{cases}
$$

## Figure & Layout Description

PPT页面顶部是黑色粗体标题"单电子(H)原子-中心力场薛定谔方程"，下方有一条深灰色水平分割线。标题下方左侧有红色文字"分离变量"，前面配有一个蓝色右向三角符号。中间区域显示波函数分离变量公式 $u(\mathbf{r}) = u(r, \theta, \varphi) = R(r) Y(\theta, \varphi)$，其中"R(r)"下方用红色文字标注"径向波函数"，"Y(θ, φ)"下方用红色文字标注"角向波函数"，并有两条蓝色箭头分别从公式指向这两个标注。右侧是一个原子结构示意图：球体中心有带正号的圆圈表示质子（标注"m_p"），球体表面有小圆点表示电子（标注"m_e"），标有径向距离"r"、极角"θ"和方位角"φ"；θ角由垂直虚线和黑色箭头表示，φ角由水平虚线和黑色箭头表示，球体用实线和虚线勾勒出三维结构。中间偏下位置有一个大型蓝色右向箭头，指向分离后的方程表达式，等号后标注"= 常数λ"。最下方是一个大括号，包含两个方程：上半部分是径向方程，右侧用蓝色文字标注"径向方程"；下半部分是角向方程，右侧用蓝色文字标注"角向方程"。整体布局为左文右图结构，文字部分以黑色为主，关键术语用红色突出，数学符号使用标准物理符号规范。

<CTX>
{
   "topic": "单电子原子薛定谔方程的分离变量法实现",
   "keywords": ["分离变量法", "径向波函数", "角向波函数", "径向方程", "角向方程", "球坐标系"],
   "summary": "本页详细展示了中心力场薛定谔方程通过分离变量法分解为径向方程和角向方程的具体数学过程，明确了波函数的径向-角向分离形式及分离常数λ的引入",
   "pending_concepts": ["分离常数λ的物理意义与量子数关联", "径向方程的具体求解方法", "角向方程与球谐函数的关系", "量子化条件的数学推导"]
}
</CTX>