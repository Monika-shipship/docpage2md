# Slide 29

## ①相互正交 ②右手标架 ③证 $\vec{e}_1$ 是单位切向量

### ①相互正交）
由常微分方程组解的理论  
∃唯一的一组解  
$$ \left. \{ \vec{r}(s); \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) \} \right|_{s=s_0} = \{ \vec{r}^0; \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0 \} $$  
再证 $\{ \vec{e}_i(s) \}$ 是 Frenet 标架  
先证 $\vec{e}_1, \vec{e}_2, \vec{e}_3$ 是相互正交  
$$ \frac{d \vec{e}_i}{ds} = a_{ij} \vec{e}_j \quad \{a_{ij}\} = \begin{pmatrix} 0 & k & 0 \\ -k & 0 & \tau \\ 0 & -\tau & 0 \end{pmatrix} $$  
$a_{ij} = -a_{ji}$，$a_{ij} + a_{ji} = 0$ 反对称  
假设 $g_{ij}(s) = \langle \vec{e}_i(s), \vec{e}_j(s) \rangle$  
$$ \frac{d g_{ij}}{ds} = \langle \dot{e}_i, e_j \rangle + \langle e_i, \dot{e}_j \rangle = \langle a_{ik} e_k, e_j \rangle + \langle e_i, a_{jk} e_k \rangle = a_{ik} g_{kj} + a_{jk} g_{ik} \quad (\times) $$  
$(\times)$ 是关于 $g_{ij}$ 的一阶齐次线性常微分方程组  
$g_{ij}(s)$ 是 $(\times)$ 一组解，$g_{ij}(s_0) = \delta_{ij}$  
$\delta_{ij}(s)$ 是 $(\times)$ 一组解，$\delta_{ij}(s_0) = \delta_{ij}$  
由常微分方程组解的唯一性可知  
$$ g_{ij}(s) \equiv \delta_{ij} = \langle \vec{e}_i(s), \vec{e}_j(s) \rangle $$  
即 $\{ \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) \}$ 是单位正交向量  

### ②右手标架
$$ ( \vec{e}_1^0, \vec{e}_2^0, \vec{e}_3^0 ) = \langle \vec{e}_1^0 \wedge \vec{e}_2^0, \vec{e}_3^0 \rangle = 1 $$  
$( \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) )$  
由连续性，$| ( \vec{e}_1(s), \vec{e}_2(s), \vec{e}_3(s) ) | \equiv 1$  

## Figure & Layout Description
The image shows a handwritten mathematical derivation on a light yellow grid paper background. The content is organized in a top-to-bottom flow with clear section headings. At the very top, three numbered items are listed horizontally: "①相互正交", "②右手标架", "③证 $\vec{e}_1$ 是单位切向量". Below this, the main content starts with a large heading "①相互正交）" followed by explanatory text in Chinese. Mathematical formulas are interspersed throughout, including a large equation block showing the initial condition for the Frenet frame, a matrix representation of the coefficient tensor $\{a_{ij}\}$, and a derivation of the orthogonality condition using the metric tensor $g_{ij}(s)$. The text uses consistent black ink with varying stroke weights indicating handwritten emphasis. The second section "②右手标架" appears at the bottom with associated vector triple product formulas. Handwritten annotations include underlines for emphasis and marginal notes. The grid lines are light gray and form a regular square pattern (approximately 5mm spacing), providing structural alignment for the handwritten content. Some symbols near the bottom right corner (e.g., $\sum_{i=1}^{3}$) are partially obscured but identifiable. No colors other than black ink on yellow paper are present, and there are no diagrams or illustrations—only textual and formulaic content.

<CTX>
{
   "topic": "Frenet标架正交性与右手性证明",
   "keywords": ["Frenet标架", "常微分方程组", "正交性证明", "右手性", "单位切向量"],
   "summary": "通过一阶常微分方程组解的唯一性证明Frenet标架的正交性和右手性，完成曲线存在性定理的关键步骤",
   "pending_concepts": ["非弧长参数下的Frenet公式修正", "微分方程组解的存在唯一性证明细节", "曲率挠率函数的连续性要求"]
}
</CTX>