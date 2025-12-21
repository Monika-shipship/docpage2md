# Slide 114

λ 是 $ \lambda^2 + 1 $ 之根，$ \sin^2\phi = \frac{1 - \cos 2\phi}{2} $  
$ \cos 2\phi = 1 - 2\sin^2\phi $  
所以无重根。  
$ u_1 \sim \cos 2\phi + \text{const} \sim \sin^2\phi + \text{const} $  
设 $ u_1 = A \sin^2\phi + B $  
$ u_1' = 2A \sin\phi \cos\phi = A \sin 2\phi $  
$ u_1'' = 2A \cos 2\phi = 2A(1 - 2\sin^2\phi) = 2A - 4A \sin^2\phi $  
$ u_1'' + u_1 = 2A + B - 3A \sin^2\phi \sim \frac{1}{b^2} \sin^2\phi $  
$ \Rightarrow A = -\frac{1}{3b^2}, \quad B = -2A = \frac{2}{3b^2} $  
故 $ u_1 = \frac{1}{3b^2} (-\sin^2\phi + 2) $  
$ u = u_0 + \delta u_1 $  
$ = \frac{1}{b} \sin\phi + \frac{\alpha}{3b^2} (2 - \sin^2\phi) $  
$ = \frac{1}{b} \sin\phi + \frac{3GM}{3c^2 b^2} (2 - \sin^2\phi) $  
令 $ \beta = \frac{GM}{c^2 b} = \frac{\alpha}{3b} $，$ \frac{GM}{c^2 b} \sim \beta $  
$ u = \frac{1}{b} \sin\phi + \frac{\beta}{b} (2 - \sin^2\phi) $  
当 $ r \to \infty $ 时，$ u = 0 $，可解出  
$ \sin\phi + \beta (2 - \sin^2\phi) = 0 $

## Figure & Layout Description
图片为单页手写数学推导，背景为浅黄色方格纸（网格线为浅灰色，间距约5mm）。文字和公式全部用黑色墨水书写，笔迹清晰但略带倾斜（向右倾斜约10-15度）。内容从左上角开始，按行排列，共16行手写内容，每行高度约8-10mm。公式部分使用标准手写数学符号（如积分号、分数线、希腊字母），其中关键推导步骤（如"设 $ u_1 = A \sin^2\phi + B $"）占两行高度，以突出显示。推导流程分为四层：1) 初始三角恒等式（第1-2行）；2) 一阶修正项假设（第3-4行）；3) 逐阶求导与方程代入（第5-8行）；4) 参数求解与最终表达式（第9-16行）。页面右下角有轻微墨迹晕染，但不影响文字辨识。整体布局紧凑，行间距均匀，符合学术笔记的典型特征。

<CTX>
{
   "topic": "史瓦西度规中一阶修正项u₁的显式求解与边界条件推导",
   "keywords": ["一阶修正项求解", "弱场近似", "光线偏折边界条件", "三角恒等式应用", "微扰参数代换"],
   "summary": "本页完成一阶修正项u₁的显式求解，得到u = (1/b)sinφ + (β/b)(2 - sin²φ)的完整表达式，并推导出r→∞时的光线偏折边界条件方程",
   "pending_concepts": ["光线偏折角的最终计算步骤", "冲击参数b的物理定义与测量方法", "边界条件sinφ + β(2 - sin²φ)=0的几何解释"]
}
</CTX>