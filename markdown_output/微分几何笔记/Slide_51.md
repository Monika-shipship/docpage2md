# Slide 51

$$ \text{II} = -r \, d\theta^2 + 0 - r \cos^2\theta \, d\phi^2. $$

**性质**：设 $ r(u,v) $ 和 $ r(\tilde{u},\tilde{v}) $ 是曲面 $ S $ 的两个不同参数表示，  
若 $ \sigma: (\tilde{u},\tilde{v}) \to (u,v) $ 是同向参数变换，则 $ \text{II}(d\tilde{u},d\tilde{v}) = \text{II}(du,dv) $.  
~ 反向 ~ ，则 $ \text{II}(d\tilde{u},d\tilde{v}) = -\text{II}(du,dv) $.

**证**：对于参数变换 $ \sigma: (\tilde{u},\tilde{v}) \to (u,v) $  
$$ r_{\tilde{u}} \wedge r_{\tilde{v}} = \frac{\partial(\tilde{u},\tilde{v})}{\partial(u,v)} \, r_u \wedge r_v $$

若 $ J > 0 $，  
$$ \vec{n}(u,v) = \vec{n}(\tilde{u},\tilde{v}) = \frac{r_u \wedge r_v}{|r_u \wedge r_v|} $$  
$$ \text{II}(du,dv) = -\langle dr(u,v), dn(u,v) \rangle $$  
$$ \quad = -\langle dr(\tilde{u},\tilde{v}), dn(\tilde{u},\tilde{v}) \rangle $$  
$$ \quad = \text{II}(d\tilde{u},d\tilde{v}) $$

若 $ J < 0 $，  
$$ \vec{n}(u,v) = -\vec{n}(\tilde{u},\tilde{v}) $$  
$$ \text{II}(du,dv) = -\langle dr(u,v), dn(u,v) \rangle $$  
$$ \quad = -\langle dr(\tilde{u},\tilde{v}), -dn(\tilde{u},\tilde{v}) \rangle $$  
$$ \quad = -\text{II}(d\tilde{u},d\tilde{v}) $$

## Figure & Layout Description
图片为方格纸背景的手写数学笔记，整体布局为自上而下的垂直排列结构。顶部是第二基本形式的显式表达式，使用黑色墨水书写，公式中包含希腊字母 $ \theta $、$ \phi $ 及三角函数 $ \cos^2\theta $。中部为"性质"段落，用中文说明参数变换对第二基本形式的影响，其中"同向"和"反向"两词被波浪线标注强调。下部为"证"明部分，分为两栏逻辑推导：左侧为雅可比行列式关系式，右侧通过条件分支（$ J>0 $ 和 $ J<0 $）展开证明，包含向量外积符号 $ \wedge $、内积符号 $ \langle \cdot, \cdot \rangle $ 及法向量 $ \vec{n} $ 的方向变化。所有公式与文字均采用手写体，字迹清晰，部分符号（如 $ \tilde{u} $）使用波浪线标注，整体排版紧凑但层次分明，关键推导步骤通过等号对齐保持视觉连贯性。

<CTX>
{
   "topic": "第二基本形式的参数变换性质",
   "keywords": ["参数变换", "同向/反向", "雅可比行列式", "单位法向量方向"],
   "summary": "阐述第二基本形式在参数变换下的符号变化规律，建立曲面几何量的坐标变换理论基础",
   "pending_concepts": ["高斯曲率在参数变换下的不变性", "测地线方程的参数无关性", "曲面嵌入欧氏空间的内蕴几何性质"]
}
</CTX>