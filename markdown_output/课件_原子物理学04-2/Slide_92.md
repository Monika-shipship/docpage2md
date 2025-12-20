# Slide 92

# 基于悬浮实验的分辨率极限

*PHYSICAL REVIEW LETTERS 127, 070801 (2021)*

## Surpassing the Energy Resolution Limit with Ferromagnetic Torque Sensors

Andrea Vinante$^{1,2}$, Chris Timberlake$^{2}$, Dmitry Budker$^{3,4,5}$, Derek F. Jackson Kimball$^{6}$, Alexander O. Sushkov$^{7,8,9}$, and Hendrik Ulbricht$^{2}$

$^{1}$Istituto di Fotonica e Nanotecnologie CNR and Fondazione Bruno Kessler, I-38123 Povo, Trento, Italy  
$^{2}$Department of Physics and Astronomy, University of Southampton, Southampton SO17 1BJ, United Kingdom  
$^{3}$Johannes Gutenberg-Universität Mainz, 55128 Mainz, Germany  
$^{4}$Helmholtz-Institut, GSI Helmholtzzentrum für Schwerionenforschung, 55128 Mainz, Germany  
$^{5}$Department of Physics, University of California at Berkeley, Berkeley, California 94720-7300, USA  
$^{6}$Department of Physics, California State University-East Bay, Hayward, California 94542-3084, USA  
$^{7}$Department of Physics, Boston University, Boston, Massachusetts 02215, USA  
$^{8}$Department of Electrical and Computer Engineering, Boston University, Boston, Massachusetts 02215, USA  
$^{9}$Photonics Center, Boston University, Boston, Massachusetts 02215, USA  

FIG. 1. (a) Model and conventions adopted. A ferromagnet with spin $S$ and magnetic moment $\mu = -\gamma S$ is trapped along the $z$ axis. It can harmonically librate around $z$ by an angle $\alpha$ and around $y$ by an angle $\beta$. Application of an oscillating magnetic field $B$ along $y$ will produce a torque $\tau = \mu \times B$ along $z$, driving the librational motion in the $\alpha$ degree of freedom. (b) Scheme of a ferromagnet above an infinite superconducting plane (gray region) in the Meissner regime. In this implementation, harmonic confinement of the $\beta$ angle arises naturally due to the interaction with an image dipole $\mu'$.

FIG. 2. (a) Magnetic field sensitivity as a function of frequency for a levitated NdFeB magnetic sphere with radius $R = 30\ \mu$m, $f_0 = 1.88$ Hz: ERL (blue dotted line), thermal noise at $Q = 10^7$, $T = 4.2$ K (red dashed-dotted) and at $T = 50$ mK, $Q = 10^9$ (red dashed), SQL on mechanical torque (green solid), spin-projection noise for independent spins (thin black dotted). The vertical line represents the Einstein-de Haas frequency $f_{EH} = 0.1f_0$. (b) Sub-resonant magnetic field sensitivity as a function of radius $R$, with $f_0 = 10f_{EH}$. Lines corresponding to ERL, thermal, SQL, and spin-projection as in (a). The vertical line marks the radius used in (a). Horizontal lines correspond to effective magnetic fields corresponding to relativistic frame dragging effects, as discussed in Ref. [5]: de Sitter effect (purple dashed), Lense-Thirring effect (orange solid).

FIG. 3. Exclusion plot from a hypothetical experiment searching for spin-spin interactions between electrons mediated by an exotic boson. The $x$ axis is the mass of the exchanged boson, and the $y$ axis is the dimensionless spin-spin coupling [6]. We assume a levitated micromagnet with radius $R = 0.2$ mm, a rotating polarized sphere actuator of radius 2 mm placed at distance 4 mm underneath the levitated magnet, and measurement time $10^6$ s. Blue solid (red dashed) lines: theoretical bound assuming thermal noise at $T = 4.2$ K, $Q = 10^7$ (SQL noise). Black line and shaded region: exclusion plot from the best experiment in the literature [25].

ERL：经典能量分辨极限  
SQL：力矩测量标准量子极限  
Spin-P:文献1中的噪声背底  

**y方向的B会引起s在z方向的力矩，  
给出力矩探测的量子极限为：**  
$$S_{\tau,\text{SQL}} \geq 2\hbar|\chi(\omega)|^{-1} = 2\hbar I\left[(-\omega^2 + \omega_0^2)^2 + \left(\frac{\omega\omega_0}{Q}\right)^2\right]^{1/2}$$

**磁体体积越大，探测极限越低**  
**在精密测量中的应用前景**

## Figure & Layout Description

页面顶部是大号黑色粗体标题"基于悬浮实验的分辨率极限"，下方有一条灰色水平分割线。页面整体采用三栏布局：左侧为论文基本信息和图1，中间为图2和公式，右侧为图3和解释性文字。

左侧区域：
- 顶部显示期刊信息"PHYSICAL REVIEW LETTERS 127, 070801 (2021)"
- 论文标题"Surpassing the Energy Resolution Limit with Ferromagnetic Torque Sensors"以加粗字体显示
- 作者列表和机构信息按编号排列，字体较小
- FIG. 1包含两个子图：(a)为三维坐标系示意图，显示x、y、z轴及磁矩S的方向；(b)为灰色平面(超导体)上方悬浮磁体的示意图
- FIG. 1下方有详细英文说明文字

中间区域：
- 顶部是图2，包含两个子图：(a)为频率-磁场灵敏度曲线图，横轴为Frequency (Hz)，纵轴为Magnetic field noise (T/Hz^(1/2))，标注"30μm半径磁球"；(b)为半径-磁场灵敏度曲线图，横轴为Radius (m)，纵轴为Magnetic field noise (T/Hz^(1/2))
- 图2下方有英文说明文字
- 中间偏下位置有红色边框包围的公式区域，内含量子极限公式
- 底部有黑色加粗文字"磁体体积越大，探测极限越低"

右侧区域：
- 顶部有三个定义：ERL、SQL、Spin-P的中文解释
- 中部是FIG. 3，为玻色子质量-自旋耦合强度的排除图，横轴为Boson mass (eV)，纵轴为(g^2)/(4πħc)
- FIG. 3下方有英文说明文字
- 底部有红色边框包围的文字"在精密测量中的应用前景"

图线颜色说明：
- 图2(a)中：ERL为蓝色点线，thermal noise为红色点划线和虚线，SQL为绿色实线，spin-projection noise为黑色细点线
- 图2(b)中：包含多条彩色曲线，包括紫色虚线(de Sitter effect)和橙色实线(Lense-Thirring effect)
- 图3中：蓝色实线和红色虚线表示理论界限，黑色实线和阴影区域表示文献中的最佳实验结果

页面元素层级：标题 > 分割线 > 三栏内容 > 底部强调文字，整体采用学术论文风格，图表与文字紧密配合，重点内容用红色边框突出显示。

<CTX>
{
   "topic": "悬浮实验的分辨率极限与量子探测理论",
   "keywords": ["分辨率极限", "量子极限", "力矩探测", "磁体体积", "ERL", "SQL", "自旋-玻色子相互作用", "磁通钉扎", "精密测量"],
   "summary": "本页深入分析了悬浮实验中的分辨率极限理论，揭示了力矩探测的量子极限公式及磁体体积对探测灵敏度的影响机制",
   "pending_concepts": ["磁通钉扎与量子极限的具体关联机制", "ERL与SQL在悬浮实验中的实际测量差异", "自旋-玻色子相互作用实验的具体实施条件", "不同温度条件下热噪声对探测极限的影响量化"]
}
</CTX>