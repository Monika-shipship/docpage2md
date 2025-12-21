# Slide 49

$$
L = \langle \gamma_{uu}, \vec{n} \rangle = x_{uu}y_u - y_{uu}x_u = -k
$$
$$
M = \langle \gamma_{uv}, \vec{n} \rangle = 0
$$
$$
N = \langle \gamma_{vv}, \vec{n} \rangle = 0
$$
$$
\mathrm{II} = -k\,du^2
$$

圆柱面：$(x(u), y(u))$ 为圆 $k = \frac{1}{a}$  
$$
\mathrm{II} = -\frac{1}{a}\,du^2
$$

$$
\gamma(u,v) = (u, v, c)
$$
$$
\gamma_u = (1, 0, 0),\ \gamma_v = (0, 1, 0),\ \vec{n} = \frac{\gamma_u \times \gamma_v}{|\gamma_u \times \gamma_v|} = \frac{\begin{vmatrix} i & j & k \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{vmatrix}}{1} = (0, 0, 1)
$$
$$
\gamma_{uu} = 0,\ \gamma_{uv} = 0,\ \gamma_{vv} = 0
$$
$$
L = 0,\ M = 0,\ N = 0
$$
$$
\mathrm{II} = 0
$$

球面：$\gamma(\theta,\varphi) = (r\cos\theta\cos\varphi,\ r\cos\theta\sin\varphi,\ r\sin\theta)$  
$$
\gamma_\theta = (-r\sin\theta\cos\varphi,\ -r\sin\theta\sin\varphi,\ r\cos\theta)
$$
$$
\gamma_\varphi = (-r\cos\theta\sin\varphi,\ r\cos\theta\cos\varphi,\ 0)
$$

## Figure & Layout Description  
手写内容书写于浅黄色方格纸背景上，黑色墨水书写。内容按垂直顺序分为四个逻辑区块：  
1. 顶部区块：包含第二基本形式系数 $L, M, N$ 的定义式及 $\mathrm{II}$ 的表达式，公式以等号对齐方式排列，其中 $L$ 的定义式包含行列式展开结构  
2. 中上区块：标注"圆柱面："的标题行，后接圆周曲率 $k=1/a$ 的说明及对应的 $\mathrm{II}$ 表达式  
3. 中部区块：柱面参数化 $\gamma(u,v)$ 的向量表示，包含 $\gamma_u, \gamma_v$ 的坐标向量、法向量 $\vec{n}$ 的行列式计算过程（含矩阵表示）及二阶导数为零的结论  
4. 底部区块：标注"球面："的标题行，后接球面参数化表达式及 $\gamma_\theta, \gamma_\varphi$ 的偏导向量计算  
所有公式均采用手写体数学符号，下标通过位置偏移表示，向量符号用箭头标注。文字与公式混合排版，关键结论（如 $\mathrm{II}=0$）单独成行突出显示。

<CTX>
{
   "topic": "第二基本形式在柱面与球面的实例验证",
   "keywords": ["第二基本形式", "柱面参数化", "球面参数化", "曲率计算", "法向量推导"],
   "summary": "通过柱面和球面的具体参数化计算，验证了第二基本形式在不同曲面上的表现形式及曲率特性",
   "pending_concepts": ["球面的高斯曲率计算", "测地线方程推导", "曲面第一基本形式与第二基本形式的关联"]
}
</CTX>