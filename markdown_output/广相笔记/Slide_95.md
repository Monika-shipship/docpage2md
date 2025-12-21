# Slide 95

$$
(e^{-\lambda} - 1)r = \alpha
$$
$$
e^{-\lambda} = 1 + \frac{\alpha}{r}
$$
所以 $e^{\nu} = e^{-\lambda} = 1 + \frac{\alpha}{r}$

$$
ds^2 = -\left(1 + \frac{\alpha}{r}\right)c^2 dt^2 + \frac{dr^2}{1 + \frac{\alpha}{r}} + r^2 \left(d\theta^2 + \sin^2\theta d\phi^2\right)
$$

方程独立性？比安基恒等式结果

确定常数 $\alpha$：

Newton近似有 $g_{00} = -\left(1 - \frac{2GM}{rc^2}\right)$

所以 $\alpha = -\frac{2GM}{c^2}$

即得史瓦西解  
Einstein 中心对称真空解

$$
ds^2 = -\left(1 - \frac{2GM}{rc^2}\right)c^2 dt^2 + \frac{dr^2}{1 - \frac{2GM}{rc^2}} + r^2 d\theta^2 + r^2 \sin^2\theta d\phi^2
$$

记 $r_s = \frac{2GM}{c^2}$，太阳 $M_0 = 2 \times 10^{33} \text{g}$，$r_0 = 695700 \text{km}$  
$r_s = 2.95 \text{km}$  
$\frac{r_s}{r_0} \sim 4.2 \times 10^{-6}$ 很小（相对）

## Figure & Layout Description
图片为浅米色方格纸背景的手写笔记，黑色墨水书写。内容垂直排列，分为四个逻辑区块：  
1. 顶部区域：三行微分方程推导，包含指数函数关系式，手写字体工整，公式间通过"所以"连接  
2. 中上区域：Schwarzschild度规的初始形式，公式跨三行书写，分母项$1+\alpha/r$有明显分数结构，右侧括号内包含球坐标项  
3. 中下区域：用中文标注"方程独立性？"并手写下划线，下方分步骤推导积分常数$\alpha$，含Newton近似与度规分量$g_{00}$的对应关系  
4. 底部区域：最终Schwarzschild度规表达式（跨两行），下方附太阳参数计算实例，包含$M_0$、$r_0$、$r_s$的数值比较  
所有公式均采用手写体数学符号，下标清晰可见（如$g_{00}$），数值计算部分包含单位标注（km, g），最后一行比值用波浪号表示数量级关系。

<CTX>
{
   "topic": "Schwarzschild解的完整推导与积分常数确定",
   "keywords": ["Schwarzschild半径", "牛顿近似", "度规函数积分常数", "中心对称真空解", "坐标奇点"],
   "summary": "本页通过牛顿近似确定度规函数积分常数，完整导出Schwarzschild度规并给出太阳系统的数值验证",
   "pending_concepts": ["Schwarzschild半径的物理意义", "坐标奇点与视界的数学关联", "比安基恒等式在场方程中的具体应用"]
}
</CTX>