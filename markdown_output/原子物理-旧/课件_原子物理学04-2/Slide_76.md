# Slide 76

## 阻尼的贡献

$$\frac{d\mathbf{m}}{dt} = -\gamma \mathbf{m} \times \mathbf{H}_{\text{eff}} + \mathbf{m} \times \left( \alpha \frac{d\mathbf{m}}{dt} \right)$$

- 绿色背景项：$-\gamma \mathbf{m} \times \mathbf{H}_{\text{eff}}$  
- 黄色背景项：$\mathbf{m} \times \left( \alpha \frac{d\mathbf{m}}{dt} \right)$  

向量图示：  
- 红色箭头：$\mathbf{H}_{\text{eff}}$（垂直向上）  
- 蓝色箭头：$\mathbf{M}$（与$\mathbf{H}_{\text{eff}}$成锐角）  
- 绿色箭头：$-\gamma \mathbf{M} \times \mathbf{H}_{\text{eff}}$（垂直于$\mathbf{M}$和$\mathbf{H}_{\text{eff}}$平面）  
- 橙色箭头：$\frac{\alpha}{M_s} \left( \mathbf{M} \times \frac{d\mathbf{M}}{dt} \right)$（与绿色箭头垂直）  
- 标注角度：$90^\circ$  

时间演化图表：  
- 横轴：$t(2\pi/\omega_0)$（范围0-10）  
- 纵轴：$M_x(t)/M_x(0)$（范围-1.0至1.0）  
- 曲线：振荡衰减波形，标注$\alpha = 0.2$和$1/\alpha$  

球体进动图：  
- 球面：虚线网格表示单位球  
- 黑色粗箭头：$\mathbf{M}$（从球心指向表面）  
- 轨迹：螺旋虚线（从赤道向北极收敛）  
- 顶部箭头：$H$（垂直向上）  
- 文字说明：Precession of the magnetization in a field showing the effect of damping.  

共振谱线图：  
- 左图：$P$ vs $f$，高斯型曲线，标注$\Delta f$（红色虚线框）  
- 右图：$\frac{dP}{dH}$ vs $H$，导数型曲线，标注$\Delta H$（红色虚线框）  

阻尼参数公式：  
$$\alpha = \frac{\gamma \Delta H}{2\omega}$$

## Figure & Layout Description

页面顶部是黑色粗体标题"阻尼的贡献"，下方有一条深灰色水平分隔线。内容区域分为四个主要区块：  
1. **左上区域**：展示LLG方程，方程中$-\gamma \mathbf{m} \times \mathbf{H}_{\text{eff}}$项被浅绿色矩形背景突出，$\mathbf{m} \times \left( \alpha \frac{d\mathbf{m}}{dt} \right)$项被浅黄色矩形背景突出。  
2. **左中区域**：三维向量示意图，包含：  
   - 红色垂直箭头标注$\mathbf{H}_{\text{eff}}$  
   - 蓝色箭头标注$\mathbf{M}$，与红色箭头夹角约30°  
   - 绿色箭头标注$-\gamma \mathbf{M} \times \mathbf{H}_{\text{eff}}$，垂直指向观察者方向  
   - 橙色箭头标注$\frac{\alpha}{M_s} \left( \mathbf{M} \times \frac{d\mathbf{M}}{dt} \right)$，与绿色箭头成90°  
   - 蓝色椭圆虚线表示进动轨迹，标注$90^\circ$角  
3. **右上区域**：二维折线图，坐标轴带网格线：  
   - 横轴标签$t(2\pi/\omega_0)$，刻度0-10  
   - 纵轴标签$M_x(t)/M_x(0)$，刻度-1.0至1.0  
   - 黑色曲线呈指数衰减振荡，图例框标注$\alpha = 0.2$和$1/\alpha$  
4. **右侧区域**：三维球体示意图：  
   - 球面由虚线网格构成，中心点有黑色粗线表示$H$方向（垂直向上）  
   - 黑色粗箭头$\mathbf{M}$从球心指向表面，轨迹为螺旋虚线（从赤道向北极收敛）  
   - 球体下方有英文说明文字  
5. **底部区域**：并排两个二维图表：  
   - 左图：$P$纵轴 vs $f$横轴，蓝色高斯曲线，红色虚线框标注$\Delta f$  
   - 右图：$\frac{dP}{dH}$纵轴 vs $H$横轴，蓝色导数曲线，红色虚线框标注$\Delta H$  
   - 两图下方居中显示阻尼参数公式$\alpha = \frac{\gamma \Delta H}{2\omega}$  

整体布局采用网格化设计，文字与图形交错排列；关键数学符号使用标准向量表示（粗体）；颜色编码用于区分方程中的不同物理项（绿色=进动项，黄色=阻尼项）。

<CTX>
{
   "topic": "阻尼项在LLG方程中的物理实现与线宽表征",
   "keywords": ["阻尼参数α", "共振线宽ΔH", "磁化进动阻尼", "LLG方程", "有效磁场"],
   "summary": "本页通过LLG方程的阻尼项解析、磁化进动可视化及共振谱线分析，建立了阻尼参数α与共振线宽ΔH的定量关系，并阐明阻尼对磁化动力学的影响机制",
   "pending_concepts": ["阻尼参数α的微观物理起源", "线宽ΔH与磁损耗功率的直接关联", "有效磁场H_eff的具体组成成分", "不同材料中α值的实验测定方法"]
}
</CTX>