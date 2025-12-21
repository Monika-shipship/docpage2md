# Slide 17

## 2.3 $E^3$ 的曲线

在 $E^3$ 中，设 $\vec{r}(t) = (x(t), y(t), z(t))$，$t \in (a,b)$，正则曲线  
$$S(t) = \int_0^t |\vec{r}'(u)| \, du$$  
$$\frac{dS}{dt} = |\vec{r}'(t)| > 0,\ S \text{ 严格增}$$  
存在反函数 $t = t(s)$，则  
$$\vec{r}(s) = (x(s), y(s), z(s))$$  
$$\vec{t} = \dot{\vec{r}}(s)$$  

法向量：垂直于 $\vec{t}$ 的向量称为法向量  
所有法线构成了法平面  
$$\langle \vec{t}, \vec{t} \rangle = 1 \quad \text{求导} \quad \langle \dot{\vec{t}}, \vec{t} \rangle = 0 \quad \dot{\vec{t}} \perp \vec{t}$$  
$\Rightarrow \dot{\vec{t}}$ 是 $\vec{r}(s)$ 的一个法向量，但 $\dot{\vec{t}}$ 和 $\vec{n}$ 不一定平行！  

定义 **空间曲率**  
$$\kappa(s) = |\dot{\vec{t}}| = |\ddot{\vec{r}}| = \sqrt{\ddot{x}^2 + \ddot{y}^2 + \ddot{z}^2} \quad (\dot{\vec{t}} \neq 0)$$  
一定大于 0！  
$$\vec{n} = \frac{\dot{\vec{t}}}{|\dot{\vec{t}}|} = \frac{\dot{\vec{t}}}{\kappa} \quad \text{称主法向量}$$  

定义副法向量 $\vec{b} = \vec{t} \times \vec{n}$  

有标架 $\{\vec{r}(s);\ \vec{t}(s),\ \vec{n}(s),\ \vec{b}(s)\}$  
称空间曲线的 Frenet 标架，正交标架，活动标架  

## Figure & Layout Description

页面为浅黄色方格纸背景的手写笔记，整体布局为纵向排版。标题"2.3 $E^3$的曲线"位于页面顶部左侧，使用黑色手写字体。正文内容以黑色墨水书写，公式与文字混合排布，关键术语通过颜色区分：

1. **颜色标记**：
   - "空间曲率"四字用蓝色墨水书写
   - 主法向量公式 $\vec{n} = \frac{\dot{\vec{t}}}{|\dot{\vec{t}}|}$ 旁有红色箭头指向右侧
   - "主法向量"三字下方有波浪线标记

2. **图形元素**：
   - 页面右下角有手绘曲线示意图，包含：
     * 一段向上弯曲的黑色曲线
     * 曲线上标注点 $O$ 和 $\vec{r}(s)$ 矢量
     * 从 $O$ 点引出三个向量：切向量 $\vec{t}$、主法向量 $\vec{n}$、副法向量 $\vec{b}$
     * 向量用带箭头的线段表示，$\vec{n}$ 与 $\vec{t}$ 垂直，$\vec{b}$ 与前两者构成右手系

3. **文字层级**：
   - 标题为一级结构
   - 定义性语句（"定义空间曲率"等）使用加粗处理
   - 推导过程按逻辑顺序分行排列，关键步骤（如"求导"）用中文标注
   - 公式与文字混合排版，部分公式使用行间格式突出显示

4. **特殊标记**：
   - "但 $\dot{\vec{t}}$ 和 $\vec{n}$ 不一定平行！"后有手写感叹号
   - "不一定平行"四字旁有手绘叉号标记
   - 积分公式中的积分限和微分符号清晰可见

<CTX>
{
   "topic": "三维空间曲线的Frenet标架体系与曲率定义",
   "keywords": ["Frenet标架", "主法向量", "副法向量", "空间曲率", "活动标架"],
   "summary": "建立三维曲线的Frenet标架体系，明确定义切向量、主法向量和副法向量的几何关系，给出空间曲率的严格数学表达",
   "pending_concepts": ["挠率的几何意义与数学表达", "Frenet-Serret公式的完整推导"]
}
</CTX>