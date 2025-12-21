# Slide 88

② $\mu,\nu=i,j\ 1,2,3$  
$$P^2_{ij} = \frac{1}{2} g^{zz} \left( \partial_i g_{zj} + \partial_j g_{zz} - \partial_z g_{ij} \right)$$  
$g_{zi}\ g_{zj}\ g_{ij}\ \quad \theta?$  

**A** $i=j$  
$$P^2_{ii} = \frac{1}{2} g^{zz} \left( -\partial_z g_{ii} \right)$$  
$g_{ii}$中只有 $g_{33}$ 与 $\theta$ 有关  
故 $P^2_{11}=0,\ P^2_{22}=0,\ P^2_{33} = \frac{1}{2} \cdot \frac{1}{r^2} \left( -\partial_\theta r^2 \sin^2\theta \right) = \frac{1}{2} \left( -2\sin\theta \cos\theta \right) = -\sin\theta \cos\theta$  

**B** $i=2$ 且 $j=2$ (选一个)  
$$P^2_{i2} = \frac{1}{2} g^{zz} \left( \partial_i g_{zz} \right) \quad g_{zz} = r^2$$  
只有 $i=1$ 才非 0  
$$P^2_{32}=0,\ P^2_{12}=P^2_{21} = \frac{1}{2} \cdot \frac{1}{r^2} \left( \partial_r r^2 \right) = \frac{1}{r}$$  

$\Lambda=3$ 时，$\sigma=3$ 才有 0.  
$$P^3_{\mu\nu} = \frac{1}{2} g^{33} \left( \partial_\mu g_{3\nu} + \partial_\nu g_{3\mu} - \partial_3 g_{\mu\nu} \right)$$  
$$P^3_{00} = \frac{1}{2} g^{33} \left( -\partial_3 g_{00} \right) = 0.$$  
下轮 $\mu,\nu \to i,j\ \ 1,2,3$  
$$P^3_{ij} = \frac{1}{2} g^{33} \left( \partial_i g_{3j} + \partial_j g_{3i} - \partial_3 g_{ij} \right)$$

## Figure & Layout Description
图片为浅黄色方格纸背景的手写数学推导，黑色墨水书写。内容分为三个逻辑区块：  
1. 顶部以带圈数字"②"开头，标注指标范围$\mu,\nu=i,j\ 1,2,3$，其下是联络分量$P^2_{ij}$的通用公式，公式后列出$g_{zi},g_{zj},g_{ij}$并标注"$\theta?$"疑问符号  
2. 中间区块以加粗字母"A"标识，包含$i=j$时的特例推导，分三行书写：第一行为$P^2_{ii}$表达式，第二行说明$g_{33}$与$\theta$的依赖关系，第三行通过等式链推导出$P^2_{33}=-\sin\theta\cos\theta$  
3. 下方区块以"B"标识，包含$i=2,j=2$情形的推导，左侧为$P^2_{i2}$公式和$g_{zz}=r^2$条件，右侧标注"只有$i=1$才非0"的注释，下方列出$P^2_{32}$和$P^2_{12}$的具体结果  
4. 底部以希腊字母"$\Lambda=3$"开头，推导$P^3_{\mu\nu}$的表达式，包含$P^3_{00}=0$的结论和下轮指标替换说明  
所有公式均采用手写体数学符号，偏导数用$\partial$表示，分数用水平线书写，关键推导步骤通过等号对齐排列，部分文字如"选一个"、"只有...才非0"作为解题注释穿插在公式间。

<CTX>
{
   "topic": "球对称度规下黎曼联络各分量的显式计算（具体分量推导）",
   "keywords": ["联络分量推导", "度规参数求导", "球坐标系应用", "指标对称性", "参数化度规", "具体分量表达式"],
   "summary": "本页完成球对称度规下所有非零黎曼联络分量的具体计算，推导出$P^2_{33}$、$P^2_{12}$等关键分量的显式表达式并验证其物理意义",
   "pending_concepts": ["曲率张量各分量的具体计算步骤", "Einstein场方程在球对称情形的简化形式", "边界条件对λ和ν函数的约束条件", "Schwarzschild解的唯一性证明"]
}
</CTX>