# Slide 20

## 1. 平移定义

①  
$$A'_{\mu}(p \to \theta) = \left( \frac{\partial x^{\alpha}}{\partial x'^{\mu}} \right)_{\alpha} A_{\alpha}(p \to \theta)$$

②  
$$\delta A_{\mu}(p) = A_{\mu}(p \to \theta) - A_{\mu}(p) = \Gamma^{\lambda}_{\mu\nu}(p) \cdot A_{\lambda}(p) dx^{\nu}$$

## 2. 联络的变换规律

$$A'_{\mu}(p \to \theta) = A'_{\mu}(p) + F^{\lambda}_{\mu\nu}(p) \cdot A'_{\lambda}(p) dx'^{\nu}$$

$$A_{\alpha}(p \to \theta) = A_{\alpha}(p) + E^{B}_{\alpha\gamma}(p) \, A_{\beta}(p) dx^{\gamma}$$

$$f_{\alpha} = f_{p} + \frac{\partial f}{\partial x^{\mu}} dx^{\mu}$$

$$\left( \frac{\partial x^{\alpha}}{\partial x'^{\mu}} \right)_{\alpha} = \left( \frac{\partial x^{\alpha}}{\partial x'^{\mu}} \right)_{p} + \left[ \frac{\partial}{\partial x'^{\nu}} \left( \frac{\partial x^{\alpha}}{\partial x'^{\mu}} \right)_{p} \right] dx'^{\nu}$$
$$= \left( \frac{\partial x^{\alpha}}{\partial x'^{\mu}} \right)_{p} + \left( \frac{\partial^{2} x^{\alpha}}{\partial x'^{\nu} \partial x'^{\mu}} \cdot \frac{\partial x'^{\nu}}{\partial x^{\delta}} \right)_{p} dx^{\delta}$$

## Figure & Layout Description

图片背景为浅米色方格纸，文字以橙色手写体为主，部分符号用蓝色标记。整体布局分为上下两个主要区域：

1. **顶部区域**：标题"1. 平移定义"位于左上角，下方有编号①和②的两个公式。公式①中$A'_{\mu}$下方有蓝色波浪线标记，等号右侧的雅可比矩阵表达式下方有黑色下划线，右侧有蓝色箭头指向$A_{\alpha}$。公式②中$\delta A_{\mu}$左侧有蓝色三角形标记。

2. **中部区域**：标题"2. 联络的变换规律"位于页面中部，下方排列三个公式。第一个公式中$A'_{\mu}$下方有蓝色波浪线标记，$F^{\lambda}_{\mu\nu}$下方有黑色下划线。第二个公式中$E^{B}_{\alpha\gamma}$下方有黑色下划线，左侧有蓝色三角形标记。

3. **底部区域**：包含雅可比矩阵的展开式，分两行书写。第一行等号左侧的雅可比矩阵表达式下方有黑色双下划线，第二行展开式中二阶导数部分有括号强调。

所有公式中的张量指标（如$\mu,\nu,\lambda$）均以标准上下标形式呈现，微分符号$dx$的上标使用手写体风格。页面右侧留有约1/4空白区域，无内容。

<CTX>
{
   "topic": "仿射空间与联络理论基础",
   "keywords": ["仿射空间", "坐标变换", "联络", "平移", "雅可比矩阵", "联络变换", "绝对微分"],
   "summary": "明确定义平移操作的数学表达式，推导联络在坐标变换下的具体变换规律，建立坐标微分与联络系数的关联机制",
   "pending_concepts": ["联络变换的物理意义", "F和E符号的几何解释", "二阶导数项在联络变换中的作用", "平移操作与测地线的关系", "联络系数对称性的物理含义"]
}
</CTX>