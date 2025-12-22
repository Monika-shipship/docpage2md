# Slide 88

## 主要结论

磁场探测的量子极限（原子磁强计）约为 $\Delta B_{SQL} \approx 7 \times 10^{-14} (t[\text{s}])^{-1}$ G

利用该方法得到的探测精度**优于量子极限3个量级**！

### 原因分析：

#### 通常的探测极限
- **不确定原理** $\Delta S_y \Delta S_z \geq \frac{\hbar}{2} |\langle S_x \rangle| \approx \frac{\hbar^2 N}{2}$
- **上页公式** $\phi = \Omega t = g\mu_B B t / \hbar \approx \frac{S_y}{S_x} \approx \frac{S_y}{N\hbar}$
- $\Delta S_y \approx \Delta S_z$ $\rightarrow$ $\Delta \phi \approx \frac{1}{\sqrt{N}}$

#### 磁针的探测极限
- $(\delta S_y)^2 \approx \frac{V}{g^2 \mu_B^2} \frac{2k_B T}{\omega} \chi''(\omega)$
- $\chi''(\omega) \approx N\hbar \alpha \frac{g^2 \mu_B^2}{V} \frac{\omega}{\omega_0^2}$
- $(\delta S_y)^2 \approx N\hbar \frac{2\alpha k_B T}{\omega_0^2}$ $\rightarrow$ $\Delta \phi_Q \approx \frac{\delta S_y}{S_x} \frac{1}{\sqrt{t}} \approx \sqrt{\frac{2\alpha k_B T}{N\hbar \omega_0^2 t}}$ $\rightarrow$ $\Delta B_Q \approx \frac{\hbar}{g\mu_B} \sqrt{\frac{2\alpha k_B T}{\hbar \omega_0^2}} \frac{1}{\sqrt{N t^3}}$
- T~0.1K, N~$3 \times 10^{12}$, $\alpha$=0.01, $\Omega$=100s$^{-1}$时 $\Delta B_Q \approx 10^{-20} (t[\text{s}])^{-3/2}$ G

D. F. Jackson Kimball, et al. Phys. Rev. Lett. 116, 190801 (2016).

## Figure & Layout Description

PPT页面整体采用白色背景，布局结构清晰。顶部是黑色粗体一级标题"主要结论"，下方有一条深灰色水平分割线。

主体内容分为左右两部分：
- 左侧占约2/3页面，包含文字和公式内容。首先是一段黑色正文描述磁场探测的量子极限，其中"优于量子极限3个量级"使用红色粗体突出显示。下方是"原因分析："标题，接着是两个带蓝色圆角矩形边框的区域。
  - 上方蓝色边框区域左侧有垂直排列的黑色文字"通常的探测极限"，内部包含不确定原理公式、上页公式推导，以及一个蓝色右向箭头连接$\Delta S_y \approx \Delta S_z$与$\Delta \phi \approx \frac{1}{\sqrt{N}}$。
  - 下方蓝色边框区域左侧有垂直排列的黑色文字"磁针的探测极限"，内部包含多行公式推导，使用蓝色右向箭头连接各推导步骤，最后是参数条件和结果公式。
- 右侧占约1/3页面，显示一个科学图表。图表具有对数坐标轴：X轴为"Time (s)"，范围从0.001到1000；Y轴为"Magnetic field uncertainty (G)"，范围从$10^{-20}$到$10^{-12}$。图表包含三条曲线：
  - 虚线标注为"$\Delta B_{SQL}$ ($T_{rel} = 0$)"
  - 实线标注为"$\Delta B_{det}$"
  - 点线标注为"$\Delta B_Q$"
  - 图表右下区域有文字"gas collisions"标注

页面底部右侧是蓝色引用文字"D. F. Jackson Kimball, et al. Phys. Rev. Lett. 116, 190801 (2016)."，字体较小。

<CTX>
{
   "topic": "磁场探测精度与量子极限的比较及理论解释",
   "keywords": ["LLG方程", "噪声背底", "相位导出", "SQUID探测", "角度分辨率", "等效磁场", "测试不确定度", "拉莫尔进动", "量子极限", "原子磁强计", "磁针探测极限", "不确定原理"],
   "summary": "本页总结了原子磁强计的磁场探测量子极限，指出实际探测精度优于量子极限3个量级，并通过不确定原理和磁针探测模型解释了原因，阐明了时间与探测精度的3/2次方关系",
   "pending_concepts": ["长径比优化的具体数学表达式", "磁屏蔽技术的实现方案", "g因子在铁磁材料中的实际取值依据", "LLG方程的具体形式", "SQUID工作原理的细节", "原子磁强计的工作原理", "磁针探测模型的具体推导"]
}
</CTX>