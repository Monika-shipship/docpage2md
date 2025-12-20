# Slide 87

## 噪声背底的导出---从LLG方程出发

相位可通过以下方法得出  
$\phi = \Omega t = g\mu_B B t / \hbar \approx \frac{S_y}{S_x} \approx \frac{S_y}{N\hbar}$

可通过测试$S_y$分量来决定$\phi$的大小（$S_y$可通过SQUID等测出）

SQUID离针10μm时，推算出其对磁通变化量的探测极限为  
$10^{-13} \text{G} \cdot \text{cm}^2 / \sqrt{\text{Hz}}$。参考磁通$10^{-4} \text{G} \cdot \text{cm}^2$，其角度分辨率可达  
$\delta\phi_{\text{det}} \approx \delta\Phi / \Phi \lesssim 10^{-9} \text{ rad} / \sqrt{\text{Hz}}$

等效磁场大小为  
$\Delta B_{\text{det}} \approx 10^{-16} (t[\text{s}])^{-3/2} \text{ G}$

时间t的3/2次方关系来源于测试不确定度。

D. F. Jackson Kimball, et al. *Phys. Rev. Lett.* 116, 190801 (2016).

## Figure & Layout Description
页面采用白底黑字设计，整体布局为左文右图结构。顶部有主标题"噪声背底的导出---从LLG方程出发"，使用加粗黑体字，下方有一条深灰色水平分割线。左侧区域包含5个段落文本：第一段为"相位可通过以下方法得出"引导的公式；第二段说明$S_y$分量测试方法；第三段描述SQUID探测极限并包含角度分辨率公式；第四段给出等效磁场公式；第五段解释时间关系。所有公式均以标准LaTeX格式呈现，变量使用斜体，单位符号使用正体。右侧区域包含两个科学示意图：上方为Fig. 1，展示铁磁针在磁场中的进动模型，包含三维坐标系（x,y,z轴）、椭圆形铁磁针（标注S）、磁场B方向箭头（沿z轴）、进动频率Ω的环形箭头，以及环绕的磁力线；下方为拾取线圈结构图，显示"Pick-up coil"线圈、"Conducting slab"导电板层、"approximate dimensions of needle"针体尺寸标注及垂直距离t。页面右下角有蓝色字体的文献引用信息。文字层级清晰，标题最大，正文次之，公式与说明文字大小一致，图形与文字区域比例约为1:2。

<CTX>
{
   "topic": "基于LLG方程的铁磁针磁力计噪声背底理论推导",
   "keywords": ["LLG方程", "噪声背底", "相位导出", "SQUID探测", "角度分辨率", "等效磁场", "测试不确定度", "拉莫尔进动"],
   "summary": "本页通过LLG方程导出噪声背底，推导了相位、SQUID探测极限及等效磁场表达式，阐明了时间与测试不确定度的3/2次方关系",
   "pending_concepts": ["长径比优化的具体数学表达式", "磁屏蔽技术的实现方案", "g因子在铁磁材料中的实际取值依据", "LLG方程的具体形式", "SQUID工作原理的细节"]
}
</CTX>