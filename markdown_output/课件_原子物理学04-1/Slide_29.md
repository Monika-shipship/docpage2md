# Slide 29

# 电子自旋

## [例3.1] 经典的电子陀螺

电子经典半径  
$$r_e = \frac{e^2}{4\pi\varepsilon_0 m_e c^2} = \frac{1.44 \text{eV} \cdot \text{nm}}{0.511 \times 10^6 \text{eV}} \doteq 2.8 \times 10^{-15} \text{m}$$

电子陀螺的角动量：  
$$\int_0^{r_e} \rho(4\pi r^2) dr \cdot rv = \int_0^{r_e} \rho(4\pi r^2) dr \cdot r\omega r$$
$$= \int_0^{r_e} 4\pi \rho \omega r^4 dr = 4\pi \rho \omega \frac{1}{5} r_e^5$$
$$= 4\pi \frac{m_e}{4\pi r_e^3 / 3} \omega \frac{1}{5} r_e^5$$
$$= \frac{3}{5} m_e \omega r_e^5$$
$$= \frac{\hbar}{2}$$

$$v_{\text{sur}} = \omega r_e = \frac{5\hbar}{6 m_e r_e} = \frac{5\hbar c \cdot c}{6 m_e c^2 r_e} = \frac{5}{6} \frac{197 \text{eV} \cdot \text{nm} \cdot 3 \times 10^8 \text{m} \cdot \text{s}^{-1}}{0.511 \times 10^6 \text{eV} \cdot 2.8 \times 10^{-15} \text{m}}$$
$$\sim 3.5 \times 10^{10} \text{m} \cdot \text{s}^{-1} \gg c$$

<span style="color:red">荒谬结论</span>

## Figure & Layout Description

页面顶部左侧为黑色粗体标题"电子自旋"，下方有一条深灰色水平分割线。主体内容分为左右两部分：

1. **左侧文本区域**：
   - 蓝色标题"[例3.1] 经典的电子陀螺"作为二级标题
   - 黑色正文依次排列：
     * "电子经典半径"文字说明及公式
     * "电子陀螺的角动量："说明文字及多行积分推导公式
     * 表面速度公式推导，最终结果标注红色"荒谬结论"
   - 左侧底部有一个蓝色右向箭头图标指向表面速度公式

2. **右侧图形区域**：
   - 灰色渐变球体示意图，中心有蓝色竖直转轴
   - 球体表面有两组蓝色同心圆虚线，标注"r, r+dr"
   - 转轴顶部有红色向上箭头标注"S"，旁边红色弧形箭头标注"ω"
   - 球体右侧有红色水平箭头指向外侧，标注"rₑ"

3. **颜色与排版**：
   - 标题文字：黑色（主标题）、蓝色（例题标题）
   - 公式文字：黑色（主体）、红色（关键参数rₑ、ω、S及结论）
   - 图形元素：灰色球体、蓝色线条/箭头、红色标注
   - 层级关系：标题→例题说明→公式推导→结论，右侧图形与左侧公式对应

<CTX>
{
   "topic": "经典电子模型与量子自旋的本质矛盾",
   "keywords": ["电子经典半径", "经典电子陀螺", "表面速度超光速", "经典模型局限性", "量子自旋必要性"],
   "summary": "通过经典电子陀螺模型推导，揭示电子表面速度远超光速的荒谬结论，证明经典模型无法解释电子自旋现象",
   "pending_concepts": ["量子自旋的正确理论表述", "狄拉克方程对电子自旋的解释", "相对论效应对经典模型的修正", "自旋本质的非经典性特征"]
}
</CTX>