# Slide 22

在 $E^3$ 中，求正则曲线的曲率和挠率

$$
S(t) = \int_0^t |\vec{r}'(u)| \, du
$$

$$
\frac{dS}{dt} = |\vec{r}'(u)| > 0
$$

$$
\vec{T}(s) = \frac{d\vec{r}}{ds} = \frac{d\vec{r}}{dt} \frac{dt}{ds}
$$

$$
\vec{T}' = k \vec{n}, \quad k(s) = |\vec{T}'(s)|
$$

$$
\frac{d\vec{T}(s)}{ds} = \frac{d}{ds} \left( \frac{d\vec{r}}{dt} \frac{dt}{ds} \right) = \frac{d}{dt} \left( \frac{d\vec{r}}{dt} \frac{dt}{ds} \right) \frac{dt}{ds}
$$

$$
= \left( \frac{d^2\vec{r}}{dt^2} \frac{dt}{ds} + \frac{d\vec{r}}{dt} \frac{d}{dt} \left( \frac{dt}{ds} \right) \right) \frac{dt}{ds}
$$

$$
= \left( [无法辨认] + \frac{d\vec{r}}{dt} \frac{d}{ds} \left( \frac{dt}{ds} \right) \frac{ds}{dt} \right) \frac{dt}{ds}
$$

$$
= \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2t}{ds^2}
$$

$$
\vec{b} = \vec{t} \wedge \vec{n}, \quad \vec{n} = \frac{\vec{T}'}{|\vec{T}'|} = \frac{\vec{T}'}{k(s)}
$$

$$
\vec{b} = \vec{t} \wedge \frac{\vec{T}'}{k} = (\vec{t} \wedge \vec{T}') \frac{1}{k}
$$

$$
|\vec{b}| = |\vec{t} \wedge \vec{T}'| \frac{1}{k} \implies k = |\vec{t} \wedge \vec{T}'|
$$

$$
\vec{t} \wedge \vec{T}' = \frac{d\vec{r}}{dt} \frac{dt}{ds} \wedge \left( \frac{d^2\vec{r}}{dt^2} \left( \frac{dt}{ds} \right)^2 + \frac{d\vec{r}}{dt} \frac{d^2t}{ds^2} \right)
$$

$$
= \left( \frac{dt}{ds} \right)^3 \vec{r}' \wedge \vec{r}'' + 0
$$

$$
|\vec{t} \wedge \vec{T}'| = \left| \left( \frac{dt}{ds} \right)^3 \right| |\vec{r}' \wedge \vec{r}''|
$$

$$
= \left( \frac{dt}{ds} \right)^3 |\vec{r}' \wedge \vec{r}''|
$$

$$
k(s) = \frac{|\vec{r}' \wedge \vec{r}''|}{|\vec{r}'|^3} \sim \rho = \frac{v^3}{|\vec{r}' \wedge \vec{r}''|}
$$

## Figure & Layout Description

图片呈现为方格纸背景的手写数学推导，整体为单页PPT布局。文字为黑色墨水书写，排版呈纵向分步推导结构。顶部第一行是中文标题"在E³中，求正则曲线的曲率和挠率"，字体略大于正文。下方依次排列15行数学公式，公式间有逻辑递进关系，通过等号对齐形成视觉流。关键公式如$S(t)$定义、$\frac{dS}{dt}$、$\vec{T}(s)$等使用较大字号，推导步骤中的中间过程字体稍小。部分公式存在手写修正痕迹：第8行"= ( [无法辨认] + ..."处有明显空白，第12行"$\vec{b} = \vec{t} \wedge \frac{\vec{T}'}{k}$"中分数线较粗，第15行末尾"$\rho = \frac{v^3}{|\vec{r}' \wedge \vec{r}''|}$"的分母部分有下划线强调。所有向量符号均用箭头标注（如$\vec{r}$），叉乘符号统一使用$\wedge$。背景方格线为浅灰色，间距约0.5cm，公式文字与网格线形成清晰的坐标参考系。

<CTX>
{
   "topic": "曲率和挠率的向量计算公式推导",
   "keywords": ["曲率计算", "挠率公式", "Frenet标架", "向量叉乘", "弧长参数化"],
   "summary": "通过向量微分运算推导出曲率k=|r'∧r''|/|r'|³和挠率ρ=v³/|r'∧r''|的显式表达式，建立速度加速度与几何特征量的直接联系",
   "pending_concepts": ["挠率的具体计算步骤", "三维曲线可视化示例", "曲率与挠率在运动学中的物理意义"]
}
</CTX>