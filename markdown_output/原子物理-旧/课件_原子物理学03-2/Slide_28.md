# Slide 28

# 单电子(H)原子-H原子中电子的概率分布

> 氢原子(类氢离子)处在束缚态 $u_{nlm}(r, \theta, \varphi)$，则在 $(r, \theta, \varphi)$ 点附近 $d\tau$ 体积元内电子出现的概率为：

$$\rho_{nlm}(r,\theta,\varphi)d\tau = |u_{nlm}(r,\theta,\varphi)|^2 r^2 \sin\theta drd\theta d\varphi$$
$$= R_{nl}^2(r)r^2 dr |Y_{lm}(\theta,\varphi)|^2 d\Omega$$

- 黄色椭圆标注：$R_{nl}^2(r)r^2 dr$ → **径向分布**
- 绿色椭圆标注：$|Y_{lm}(\theta,\varphi)|^2 d\Omega$ → **角向分布**

## 角向分布函数 $W_{lm}(\theta, \varphi)$

$$W_{lm}(\theta,\varphi)d\Omega = \left[\int_0^\infty |u_{nlm}(r,\theta,\varphi)|^2 r^2 dr\right] \sin\theta d\theta d\varphi$$
$$= \left[\int_0^\infty R_{nl}^2(r)r^2 dr\right] |Y_{lm}(\theta,\varphi)|^2 \sin\theta d\theta d\varphi$$
$$= |Y_{lm}(\theta,\varphi)|^2 d\Omega$$

右侧坐标系图旁公式：
$$d\tau = dr \cdot rd\theta \cdot r\sin\theta d\varphi$$
$$= r^2 dr \frac{dS}{r^2} = r^2 dr d\Omega$$

## Figure & Layout Description
页面顶部是黑色粗体标题"单电子(H)原子-H原子中电子的概率分布"，下方有一条深蓝色水平分割线。主体内容分为左右两部分：左侧是理论说明与公式推导，右侧是三维坐标系示意图。左侧内容以蓝色右向箭头符号开头，引出氢原子束缚态概率分布的定义。核心公式分为两行，第一行展示概率密度表达式，第二行分解为径向部分和角向部分。其中，径向部分$R_{nl}^2(r)r^2 dr$被黄色椭圆形框高亮，下方用蓝色文字标注"径向分布"；角向部分$|Y_{lm}(\theta,\varphi)|^2 d\Omega$被绿色椭圆形框高亮，下方用蓝色文字标注"角向分布"，两个标注均有橙色箭头指向对应部分。"角向分布函数"标题使用红色字体突出显示。右侧的三维坐标系图展示了直角坐标系(x,y,z)与球坐标系(r,θ,φ)的转换关系，包含坐标轴、角度标记和位置矢量，图中用红色标记了角度θ和φ的定义。坐标系图下方有体积元$d\tau$的分解公式。整个页面采用白底黑字为主，关键概念使用彩色高亮和标注，公式排版清晰，层次分明。

<CTX>
{
   "topic": "氢原子电子概率分布的径向与角向分解",
   "keywords": ["概率分布", "径向分布", "角向分布", "球谐函数", "体积元", "角向分布函数"],
   "summary": "本页阐述了氢原子电子概率分布如何分解为径向分布和角向分布，并引入了角向分布函数的概念，明确了球坐标系下概率密度的数学表达",
   "pending_concepts": ["径向分布函数的物理意义", "角向分布与原子轨道形状的关系", "概率密度与电子云模型的联系", "不同量子数对应的概率分布特征"]
}
</CTX>