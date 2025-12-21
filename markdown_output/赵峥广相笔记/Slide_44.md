# Slide 44

# 2. 等效原理的数学基础

## 2.10 短程线（实质为极值）可能最长、最小、常值

$$S = \int_A^B ds$$

$$\delta S = \delta \int_A^B ds = 0$$

$$ds^2 = g_{\alpha\beta} dx^\alpha dx^\beta \quad \text{（注：} g_{\alpha\beta} = g_{\alpha\beta}(x^\mu)\text{）}$$

$$ds = \sqrt{g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta} d\lambda \quad \left( \dot{x}^\alpha \triangleq \frac{dx^\alpha}{d\lambda}, \ x^\alpha = x^\alpha(\lambda) \right)$$

$$\delta \int_A^B \sqrt{g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta} d\lambda$$

$$\frac{\partial L}{\partial x^\nu} - \frac{d}{d\lambda} \frac{\partial L}{\partial \dot{x}^\nu} = 0$$

$$\frac{\partial L}{\partial x^\nu} = \frac{1}{2} \frac{1}{\sqrt{g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta}} \frac{\partial g_{\alpha\beta}}{\partial x^\nu} \dot{x}^\alpha \dot{x}^\beta$$

$$\frac{\partial L}{\partial \dot{x}^\nu} = \frac{1}{2} \frac{1}{\sqrt{g_{\alpha\beta} \dot{x}^\alpha \dot{x}^\beta}} \left[ g_{\alpha\beta} \dot{x}^\beta \delta^\alpha_\nu + g_{\alpha\beta} \dot{x}^\alpha \delta^\beta_\nu \right]$$

## Figure & Layout Description

页面采用浅米色方格纸背景，方格线为浅灰色，间距均匀。所有文字和公式以橙色手写体呈现，笔迹流畅但带有明显手写特征。顶部第一行是标题"2. 等效原理的数学基础"，字体较大且加粗，位于页面上部中央区域。第二行开始为子标题"2.10 短程线（实质为极值）可能最长、最小、常值"，其中"实质为极值"被括号包围且括号为手写弧线。公式区域占据页面主体，从第三行开始垂直排列，每行公式独立成行，行间距适中。公式中存在多处手写注释：在$g_{\alpha\beta}$右侧有手写小字"（注：$g_{\alpha\beta} = g_{\alpha\beta}(x^\mu)$）"；在$\dot{x}^\alpha$定义处有括号注释包含导数定义和参数化说明。公式中出现两个手绘圆圈符号（分别标记为圈A和圈B），位于$g_{\alpha\beta}$和$\dot{x}^\alpha$附近，可能用于强调关键变量。整体布局遵循自上而下的逻辑流，标题-子标题-核心公式-推导步骤的层次结构清晰，无额外图形或颜色标记。

<CTX>
{
   "topic": "短程线方程的变分推导",
   "keywords": ["短程线", "极值问题", "测地线方程", "拉格朗日量", "变分原理"],
   "summary": "本页通过变分原理推导短程线方程，建立了曲线极值问题与度规张量的微分关系，为等效原理提供几何化数学表述",
   "pending_concepts": ["极值问题的物理意义（最长/最短/常值）", "参数化选择对短程线的影响", "测地线方程与克氏符的显式关联", "度规张量对坐标的显式依赖性验证"]
}
</CTX>