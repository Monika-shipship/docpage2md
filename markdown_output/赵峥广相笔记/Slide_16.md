# Slide 16

$$ \delta^\mu_\nu = \begin{cases} 1 & \mu=\nu \\ 0 & \mu\neq\nu \end{cases} $$

$$ \delta^\alpha_\beta = \begin{cases} 1 & \alpha=\beta \\ 0 & \alpha\neq\beta \end{cases} $$

$$ \frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\beta}{\partial x'^\nu} \delta^\alpha_\beta = \frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\alpha}{\partial x'^\nu} = \frac{\partial x'^\mu}{\partial x'^\nu} = \begin{cases} 1 & \mu=\nu \\ 0 & \mu\neq\nu \end{cases} $$

$ \delta^\alpha_\beta $ 是 (1,1) 阶张量  
逆协

## §2.3 张量代数

张量是逐点定义的，运算在同一点进行

一、加法  
$ C^{\mu\nu}_{e\mu} = A^{\mu\nu}_{e\mu} + B^{\mu\nu}_{e\mu} $ 同一点，同阶

二、乘法  
$ A^\mu_{\alpha\beta} B^\nu_\gamma = C^{\mu\nu}_{\alpha\beta\gamma} $ 乘法（矩阵乘法）

## Figure & Layout Description
图片呈现浅米色方格纸背景，网格线为浅灰色细线，形成均匀的正方形网格（约 20×30 个单元格）。所有文字和公式均以橙色手写体书写，笔迹清晰流畅，具有自然的书写倾斜度（约 5-10 度右倾）。内容按垂直顺序排列：  
1. 顶部区域：两行分段函数定义（克罗内克符号），使用大括号结构，上标/下标位置精准（如 $\delta^\mu_\nu$ 中 $\mu$ 为上标、$\nu$ 为下标）  
2. 中部区域：连续的偏导数推导公式，等号对齐形成逻辑链，偏导数符号 $\partial$ 书写规范  
3. 中下部：文字说明 "$ \delta^\alpha_\beta $ 是 (1,1) 阶张量" 采用常规字体，下方附有小字标注"逆协"（字号约为主文本 70%）  
4. 核心标题：**§2.3 张量代数** 使用加粗手写体（笔画宽度比正文宽 30%），作为视觉焦点  
5. 底部区域：分两点阐述代数规则，"一、"和"二、"编号左对齐，公式与文字说明横向排列（公式在左，说明文字在右）  
整体层级通过书写大小和位置区分：标题 > 公式 > 说明文字，无颜色变化但通过笔画粗细实现视觉层次。公式中所有希腊字母（μ, ν, α, β, γ）和拉丁字母（x, e）均清晰可辨，上下标位置符合数学规范。

<CTX>
{
   "topic": "张量代数运算规则与同点定义特性",
   "keywords": ["张量代数", "同点运算", "张量加法", "张量乘法", "矩阵乘法", "阶数约束"],
   "summary": "阐明张量在同一点进行的代数运算规则，包括同阶张量加法和指标外积乘法，强调运算需满足同点同阶条件",
   "pending_concepts": ["混合张量的物理实例解析", "傀偶指标在具体场论中的操作规范", "非整数阶张量的可能性", "指标升降操作的几何解释", "矩阵乘法表述与张量外积的本质区别"]
}
</CTX>