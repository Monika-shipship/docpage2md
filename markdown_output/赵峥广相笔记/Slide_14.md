# Slide 14

电磁四矢 $A = (A_1, A_2, A_3, A_4)$  
$A_4 = \frac{1}{c}\phi$ 从静电  

$F_{\mu\nu}$  

## §2.2 广相中的张量  

$x'^\mu = x'^\mu(x^1, x^2, x^3, x^4)$  

$x_0 = ct \quad x_4 = ict$  

$dx'^\mu = \left. \frac{\partial x'^\mu}{\partial x^\alpha} \right|_P dx^\alpha$  

$dx'^3 = \left. \frac{\partial x'^3}{\partial x^1} \right|_P dx^1 + \left. \frac{\partial x'^3}{\partial x^2} \right|_P dx^2 + \cdots$  

$\det \left| \frac{\partial x'^\mu}{\partial x^\alpha} \right| \neq 0 \text{ or } \infty$ 有逆变换  

$dx^\alpha = \frac{\partial x^\alpha}{\partial x'^\mu} dx'^\mu$  

$\frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\alpha}{\partial x'^\nu} = \frac{\partial x'^\mu}{\partial x'^\nu} = \delta^\mu_\nu = \begin{cases} 1 & \mu=\nu \\ 0 & \mu \neq \nu \end{cases}$ 克罗内克符号  

$\frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x^\alpha}{\partial x'^\nu} = I_{\mu\nu}$  

## Figure & Layout Description  
图片为方格纸背景的手写笔记，文字与公式以橙色墨水书写。整体布局分为三个垂直区域：  
1. **顶部区域**：横向排列电磁四矢定义公式，$A_4$ 的表达式右侧有“从静电”字样，末尾被截断。  
2. **中部区域**：包含二级标题“§2.2 广相中的张量”，其下按逻辑顺序排列坐标变换公式：  
   - 坐标变换的函数表示 $x'^\mu = x'^\mu(...)$  
   - 时空坐标定义 $x_0=ct$ 与 $x_4=ict$ 并列书写  
   - 微分变换公式分两行展示，第二行以省略号结尾  
   - 雅可比行列式条件与“有逆变换”注释并列  
3. **底部区域**：包含逆变换公式、克罗内克符号的分段定义（含矩阵形式说明），以及最终的恒等式。  
所有公式严格对齐方格线，关键符号（如 $\partial$, $\delta$）书写工整，下标/上标位置清晰。部分文字（如“克罗内克符号”）以中文标注在公式右侧，形成“公式-注释”对照结构。

<CTX>
{
   "topic": "广义相对论中的坐标变换与四维张量表示",
   "keywords": ["电磁四维势", "坐标微分变换", "雅可比矩阵", "克罗内克符号", "逆变换条件"],
   "summary": "本页将坐标变换理论扩展至四维时空，通过电磁四维势示例说明物理量在广义坐标系中的变换规则，为后续度规张量分析提供操作基础",
   "pending_concepts": ["A₄与φ的完整物理对应关系", "ict虚时间坐标的现代诠释", "雅可比矩阵行列式条件的物理意义", "克罗内克符号在非正交系中的修正形式"]
}
</CTX>