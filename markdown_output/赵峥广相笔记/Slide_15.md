# Slide 15

## 2. 广相中的张量

**标量**：在广义坐标变换下不变的量  
$U'(x') = U(x)$

**变矢量**：在广义坐标变换下与坐标微分元一样变的量  
$dx'^\mu = \frac{\partial x'^\mu}{\partial x^\alpha} dx^\alpha \quad dx^\alpha = \frac{\partial x^\alpha}{\partial x'^\mu} dx'^\mu$  
$V'^\mu = \frac{\partial x'^\mu}{\partial x^\alpha} V^\alpha$

**协变矢量**  
$V'_\mu = \frac{\partial x^\alpha}{\partial x'^\mu} V_\alpha$

**逆变张量**  
$T'^{\mu\nu} = \frac{\partial x'^\mu}{\partial x^\alpha} \frac{\partial x'^\nu}{\partial x^\beta} T^{\alpha\beta}$

**协变**  
$T'_{\mu\nu} = \frac{\partial x^\alpha}{\partial x'^\mu} \frac{\partial x^\beta}{\partial x'^\nu} T_{\alpha\beta}$

**混合张量**  
$T'^{\mu_1 \mu_2 \mu_3 \cdots \mu_p}_{\nu_1 \nu_2 \nu_3 \cdots \nu_q} = \frac{\partial x'^{\mu_1}}{\partial x^{\alpha_1}} \frac{\partial x'^{\mu_2}}{\partial x^{\alpha_2}} \cdots \frac{\partial x'^{\mu_p}}{\partial x^{\alpha_p}} \frac{\partial x^{\beta_1}}{\partial x'^{\nu_1}} \frac{\partial x^{\beta_2}}{\partial x'^{\nu_2}} \cdots \frac{\partial x^{\beta_q}}{\partial x'^{\nu_q}} T^{\alpha_1 \alpha_2 \cdots \alpha_p}_{\beta_1 \beta_2 \cdots \beta_q}$

$(p, q)$  
逆协  

傀偶指标不代表阶数，只能一上一下求和

## Figure & Layout Description

图片为手写风格的学术笔记，背景是浅米色方格纸（1cm×1cm网格线），文字以橙色手写体呈现。内容垂直排列于左侧区域，占据页面约三分之二宽度，右侧三分之一为空白网格区域。标题"2. 广相中的张量"位于左上角，字号最大且加粗。各概念以"**概念名**"作为小标题，使用加粗手写体，下方紧接公式推导。公式采用分式结构，偏导数符号清晰，上下标位置规范。文字行间距均匀，每行公式与对应说明文字保持紧密对齐。底部有手写注释"傀偶指标..."，字体略小但清晰可辨。整体布局呈现典型的课堂笔记特征：逻辑分层明确、公式推导连贯、无装饰性元素，仅保留核心数学表达式和概念定义。

<CTX>
{
   "topic": "广义相对论中的张量分类与坐标变换规则",
   "keywords": ["标量", "变矢量", "协变矢量", "逆变张量", "混合张量", "傀偶指标"],
   "summary": "系统阐述了标量、协/逆变矢量及混合张量在广义坐标变换下的具体变换规则，明确了上下指标的物理意义与求和约束",
   "pending_concepts": ["混合张量的物理实例解析", "傀偶指标在具体场论中的操作规范", "非整数阶张量的可能性", "指标升降操作的几何解释"]
}
</CTX>