# Slide 91

$$R_0^0 = -\frac{1}{2} e^{-\lambda} \left( \nu'' + \frac{1}{2} \nu'^2 - \frac{1}{2} \nu' \lambda' + \frac{2}{r} \nu' \right) + \frac{1}{2c^2} e^{-\nu} \left( \ddot{\lambda} - \frac{1}{2} \dot{\lambda} \dot{\nu} + \frac{1}{2} \dot{\lambda}^2 \right).$$

$$R_1^1 = R_1^0 = -\frac{1}{2} e^{-\lambda} \left( \nu'' + \frac{1}{2} \nu'^2 - \frac{1}{2} \nu' \lambda' - \frac{2}{r} \lambda' \right) + \frac{e^{-\nu}}{2c^2} \left( \ddot{\lambda} - \frac{1}{2} \dot{\nu} \dot{\lambda} + \frac{1}{2} \dot{\lambda}^2 \right).$$

$$R_2^2 = R_3^3 = \frac{1 - e^{-\lambda}}{r^2} + \frac{1}{2} \frac{e^{-\lambda}}{r} (\lambda' - \nu')$$

$$R = R^\mu_\mu = \frac{2}{r^2}(1 - e^{-\lambda}) - \frac{1}{2} e^{-\lambda} (2\nu'' + \nu'^2 - \lambda' \nu') - \frac{2e^{-\lambda}}{r} (\nu' - \lambda') + \frac{e^{-\nu}}{c^2} \left( \ddot{\lambda} - \frac{1}{2} \dot{\lambda} \dot{\nu} + \frac{1}{2} \dot{\lambda}^2 \right).$$

$$P_0^1 = \frac{1}{cr} e^{-\lambda} \dot{\lambda}$$

再算 Einstein 张量  
$$G^\mu_\nu = R^\mu_\nu - \frac{1}{2} g^\mu_\nu R$$

由中心球对称情况的 $\Gamma^\lambda_{\mu\nu}$ 可计算 Einstein 张量  
$$G^\mu_\nu = R^\mu_\nu - \frac{1}{2} \delta^\mu_\nu R \tag{23}$$

$$\begin{aligned}
G_0^0 &: R_0^0 - \frac{1}{2} R = e^{-\lambda} \left[ \frac{1}{r^2} - \frac{1}{r} \lambda' \right] - \frac{1}{r^2} \\
G_1^1 &: R_1^1 - \frac{1}{2} R = e^{-\lambda} \left( \frac{1}{r} \nu' + \frac{1}{r^2} \right) - \frac{1}{r^2} \\
G_2^2 &: R_2^2 - \frac{1}{2} R = R_3^3 - \frac{1}{2} R \\
&= \frac{1}{2} e^{-\lambda} \left[ \nu'' + \frac{1}{2} (\nu')^2 - \frac{1}{2} \nu' \lambda' + \frac{1}{r} (\nu' - \lambda') \right] \\
&\quad - \frac{e^{-\nu}}{2c^2} \left[ \ddot{\lambda} + \frac{1}{2} (\dot{\lambda})^2 - \frac{1}{2} \dot{\lambda} \dot{\nu} \right] \tag{24} \\
G_0^1 &: R_0^1 = \frac{1}{cr} e^{-\lambda} \dot{\lambda}
\end{aligned}$$

## Figure & Layout Description
图片采用方格纸背景（浅灰色网格线），整体为手写数学推导内容。主要区域由黑色墨水书写，包含5组核心公式和1段中文说明。公式从上至下排列：第一行是$R_0^0$表达式，第二行是$R_1^1=R_1^0$表达式，第三行是$R_2^2=R_3^3$表达式，第四行是标量曲率$R$的完整展开式，第五行是$P_0^1$表达式。中部有手写中文"再算Einstein张量"及对应张量定义式。底部嵌入一个白色矩形框（模拟打印体），内含标题"由中心球对称情况的$\Gamma^\lambda_{\mu\nu}$可计算Einstein张量"，下方列出(23)(24)编号公式，其中(24)包含多行对齐公式。所有公式均使用标准手写体数学符号，部分导数符号（如$\ddot{\lambda}$）带有明显连笔特征。白色框与手写内容形成视觉对比，框内文字为黑色印刷体，公式编号右对齐。

<CTX>
{
   "topic": "Einstein张量的具体表达式推导与中心球对称情况应用",
   "keywords": ["曲率张量", "Ricci张量", "Einstein张量", "指标缩并", "度规函数求导", "中心球对称度规"],
   "summary": "本页完成了Einstein张量$G^\\mu_\\nu$在中心球对称度规下的具体分量表达式推导，建立了Ricci张量与标量曲率的组合关系",
   "pending_concepts": ["Einstein场方程与物质分布的对应关系", "度规函数ν和λ的物理约束条件", "Schwarzschild解的推导路径", "Einstein张量各分量的物理意义阐释"]
}
</CTX>