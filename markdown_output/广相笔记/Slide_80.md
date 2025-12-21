# Slide 80

$$\nabla \cdot \vec{A} = 0 \implies \nabla^2 \phi = -\frac{\rho}{\varepsilon_0}, \quad \nabla^2 \vec{A} - \frac{1}{c^2}\frac{\partial^2 \vec{A}}{\partial t^2} = \mu_0 \vec{J}$$
$$\nabla^2 \phi - \frac{1}{c^2}\frac{\partial^2 \phi}{\partial t^2} = -\frac{\rho}{\varepsilon_0}$$
$$\Box \vec{A} = -\mu_0 \vec{J}_\mu$$

$$\nabla \cdot \vec{A} + \frac{1}{c}\frac{\partial \phi}{\partial t} = 0$$
$$\vec{A} = \begin{pmatrix} \vec{A} \\ i\frac{\phi}{c} \end{pmatrix}$$
$$\partial_\mu A^\mu = 0$$

类比，选不同规范 方程不一样，  
合适规范可简化方程。

$$g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}, \quad \partial_\mu \partial^\mu = \partial_z \partial_z - \partial_0^2 = \nabla^2 - \frac{1}{c^2}\frac{\partial^2}{\partial t^2}$$
$$\Box h_{\mu\nu} = T_{\mu\nu} \quad \Box = g^{\mu\nu}\partial_\mu \partial_\nu \text{ 达朗贝尔算子}$$

弱场近似下， $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu} \quad |h_{\mu\nu}| \ll 1$

$$R_{\mu\nu} - \frac{1}{2}R g_{\mu\nu} = \frac{8\pi G}{c^3}$$

## Figure & Layout Description
图片为浅黄色方格纸背景，网格线为浅灰色细线构成1cm×1cm正方形网格。所有内容为黑色手写体，分为四个逻辑区块：
1. 顶部区域：三行电磁学方程，包含向量算符∇、拉普拉斯算子∇²、达朗贝尔算子□，公式间用逗号分隔，最后一行单独列出□A=-μ₀J_μ
2. 中上区域：规范条件相关公式，包含四维势A的矩阵表示（2×1列向量），使用分段函数形式书写
3. 中部区域：两行中文注释，"类比..."与"合适规范..."分两行书写，字体略大于公式
4. 底部区域：引力场方程部分，包含度规分解g=η+h、达朗贝尔算子定义、弱场近似条件及爱因斯坦场方程
所有公式均手写在网格交点处，字符高度约0.5cm，中文注释行高约0.7cm。部分公式存在上标/下标（如μν）和分数结构，手写体存在连笔现象但关键符号清晰可辨。

<CTX>
{
   "topic": "规范条件与坐标条件的类比：电磁学与引力场",
   "keywords": ["谐和坐标条件", "Fock", "规范条件", "gauge", "电磁势", "达朗贝尔算子", "弱场近似", "度规扰动", "爱因斯坦场方程"],
   "summary": "本页通过电磁学规范条件与引力场坐标条件的类比，阐明规范选择对场方程形式的影响，并引入弱场近似下的线性化引力理论",
   "pending_concepts": ["弱场近似下引力波的解", "规范条件与坐标条件的数学等价性证明", "达朗贝尔算子在弯曲时空中的推广", "8πG/c³系数的量纲分析", "h_μν扰动的物理意义"]
}
</CTX>