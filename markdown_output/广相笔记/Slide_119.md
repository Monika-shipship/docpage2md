# Slide 119

故  
$$ C t(b \to r) = I_1 + 2\beta b I_2 + \beta b^3 I_3 $$  
$$ = \sqrt{r^2 - b^2} + 2\beta b \ln\left(r + \sqrt{r^2 - b^2}\right) + \beta b^3 \frac{1}{b^2} \left. \frac{\sqrt{r^2 - b^2}}{r} \right|_b^r $$  
$$ = \sqrt{r^2 - b^2} + 2\beta b \ln\left( \frac{r + \sqrt{r^2 - b^2}}{b} \right) + \beta b \frac{\sqrt{r^2 - b^2}}{r} $$  

$$ \bar{T} = t(b \to r_1) + t(b \to r_2) $$  
$$ = \frac{1}{c} \left[ \sqrt{r_1^2 - b^2} + \sqrt{r_2^2 - b^2} + 2\beta b \ln\left( \frac{(r_1 + \sqrt{r_1^2 - b^2})(r_2 + \sqrt{r_2^2 - b^2})}{b^2} \right) + \beta b \left( \frac{\sqrt{r_1^2 - b^2}}{r_1} + \frac{\sqrt{r_2^2 - b^2}}{r_2} \right) \right] $$  

$$ T_{\text{all}} = 2\bar{T} \quad \text{, 使用近似 } r_1, r_2 \gg b \text{ 有 } \ln(1+x) = x - \frac{x^2}{2} $$  
$$ T_{\text{all}} = \frac{2}{c} \left[ r_1 + r_2 + 2\beta b \ln \frac{2r_1 \cdot 2r_2}{b^2} + 2\beta b \right] $$  
$$ = \frac{2}{c} \left[ r_1 + r_2 + 2\beta b \left(1 + \ln \frac{4r_1 r_2}{b^2} \right) \right] $$  

无相对论时 $ T_{\text{all}} = \frac{2}{c}(r_1 + r_2) \quad \beta = \frac{GM}{c^2 b} $  
$$ \Delta T = \frac{4\beta b}{c} \left(1 + \ln \frac{4r_1 r_2}{b^2} \right) $$  
$$ = \frac{4GM}{c^3} \left(1 + \ln \frac{4r_1 r_2}{b^2} \right) $$  
水星 $ \Delta T = 240 \mu s = 2.4 \times 10^{-4} s $

## Figure & Layout Description  
图像为米黄色方格纸背景，浅灰色细线构成均匀网格（约5mm×5mm）。所有内容以黑色墨水手写，文字与公式垂直排列，占据画面主要区域。顶部左侧有汉字"故"作为段落起始标记。公式分七组水平排列，每组公式通过等号对齐，部分长公式分多行书写（如$\bar{T}$表达式跨两行）。积分上下限用竖线标注（如$\left. \frac{\sqrt{r^2 - b^2}}{r} \right|_b^r$），对数函数参数用括号明确范围。关键变量$r_1, r_2, b$均带有下标，希腊字母$\beta$清晰可辨。底部有"水星"字样及具体数值计算，单位符号$\mu s$用标准字体书写。整体布局无颜色区分，仅通过公式层级和间距体现逻辑结构，无图形或表格元素。

<CTX>
{
   "topic": "雷达回波延迟的广义相对论计算",
   "keywords": ["雷达回波延迟", "广义相对论验证", "冲击参数", "度规方程", "时间延迟积分", "β一阶近似", "积分分解", "时间延迟解析解", "β参数代入"],
   "summary": "本页完成雷达信号时间延迟的最终解析表达式推导，通过β参数代入得到含GM/c³的显式延迟公式并给出水星观测实例",
   "pending_concepts": ["4r₁r₂/b²的物理意义解释", "水星数据的具体观测条件", "与光线偏折角计算的数学关联性", "γ符号与径向坐标r的对应关系"]
}
</CTX>