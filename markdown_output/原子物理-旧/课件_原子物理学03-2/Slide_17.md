# Slide 17

# 单电子(H)原子-中心力场薛定谔方程

## Cartesian coordinates
$(x, y, z)$

$$x = r \sin\theta \cos\varphi$$
$$y = r \sin\theta \sin\varphi$$
$$z = r \cos\theta$$

## Spherical coordinates
$(r, \theta, \varphi)$

$$r = \sqrt{x^2 + y^2 + z^2}$$
$$\theta = \arccos\left( \frac{z}{\sqrt{x^2 + y^2 + z^2}} \right)$$
$$\varphi = \arctan\left( \frac{y}{x} \right)$$

## Figure & Layout Description
页面采用左右对称布局结构，中央由蓝色双向箭头连接两个坐标系区域。左侧区域顶部有浅蓝色背景的"Cartesian coordinates"标题（红色文字），下方标注坐标表示$(x, y, z)$。包含三维直角坐标系示意图：X-Axis（蓝色文字）指向左下方，Y-Axis（蓝色文字）指向右方，Z-Axis（蓝色文字）指向上方，坐标轴均为蓝色实线；坐标点"Point (x,y,z)"用紫色虚线连接到各坐标轴，形成三维投影结构。

右侧区域顶部有浅蓝色背景的"Spherical coordinates"标题（红色文字），下方标注坐标表示$(r, \theta, \varphi)$。包含球坐标系示意图：原点处引出蓝色向量$\mathbf{r}$（标注"r"），向量末端为黄色圆点；红色弧线标注极角$\theta$（与z轴夹角）和方位角$\varphi$（xy平面内与x轴夹角）；x、y、z轴用黑色实线表示，其中x轴指向左下方，y轴指向右方，z轴指向上方；向量$\mathbf{r}$在各坐标轴的投影$r_x$、$r_y$、$r_z$用黑色虚线表示。

两个区域下方分别列出坐标变换公式，文字为黑色标准字体。左侧公式展示球坐标到直角坐标的转换，右侧公式展示直角坐标到球坐标的转换，所有数学符号均采用标准印刷体。

<CTX>
{
   "topic": "直角坐标系与球坐标系的转换关系",
   "keywords": ["中心力场", "球坐标系", "坐标变换", "径向距离", "角度变量", "分离变量法"],
   "summary": "本页详细展示直角坐标系与球坐标系的数学转换关系，为在中心力场中应用分离变量法求解薛定谔方程奠定坐标变换基础",
   "pending_concepts": ["球坐标系下的分离变量法", "径向方程的求解步骤", "量子数的物理意义", "本征函数的球谐函数表示"]
}
</CTX>