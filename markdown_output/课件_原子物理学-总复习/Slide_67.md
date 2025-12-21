# Slide 67

## 电子组态能级

### 中心力场近似

$$\hat{H} = \hat{H}_0 + \hat{H}_1$$

$$\hat{H}_0 = \sum_{i=1}^{N} \left( -\frac{\hbar^2}{2m_e} \nabla_i^2 - \frac{Ze^2}{4\pi\varepsilon_0 r_i} + S(r_i) \right) = \sum_{i=1}^{N} \left( -\frac{\hbar^2}{2m_e} \nabla_i^2 + V(r_i) \right)$$

$$\hat{H}_1 = \sum_{i<j=1}^{N} \cancel{\frac{e^2}{4\pi\varepsilon_0 r_{ij}}} - \sum_{i=1}^{N} S(r_i) \quad \text{剩余静电势}$$

### 修正：

(1) 剩余静电势

$$\hat{H}_1 = \sum_{i<j=1}^{N} \frac{e^2}{4\pi\varepsilon_0 r_{ij}} - \sum_{i=1}^{N} S(r_i)$$

(2) 自旋轨道相互作用

$$\hat{H}_2 = \sum_{i=1}^{N} \xi(r_i) \mathbf{l}_i \cdot \mathbf{s}_i \quad \text{其中} \quad \xi(r_i) = \frac{1}{2m_e^2 c^2} \frac{1}{r_i} \frac{dV(r_i)}{dr_i}$$

## Figure & Layout Description

幻灯片顶部有黑色粗体标题"电子组态能级"，下方有一条深灰色水平分割线。标题下方是蓝色子标题"中心力场近似"。正文包含多行公式：第一行是哈密顿量分解式$\hat{H} = \hat{H}_0 + \hat{H}_1$；第二行$\hat{H}_0$的展开式包含从$i=1$到$N$的求和，内部有动能项、库仑势项和$S(r_i)$项，等号右侧简化为有效势$V(r_i)$；第三行$\hat{H}_1$的原始表达式中，$\frac{e^2}{4\pi\varepsilon_0 r_{ij}}$项被红色圆圈加斜线标记（表示修正），右侧标注"剩余静电势"黑色文字。下方蓝色标题"修正："后分两点：(1)修正后的剩余静电势公式，(2)自旋轨道相互作用公式，其中$\xi(r_i)$的定义式以"其中"引出。公式中的符号如$\hbar$、$\nabla^2$、$\varepsilon_0$等均准确呈现，下标和求和范围清晰可见。整体布局采用左对齐方式，重要修正项通过颜色和符号进行视觉强调。

<CTX>
{
   "topic": "电子组态能级与中心力场近似",
   "keywords": ["中心力场近似", "剩余静电势", "自旋轨道相互作用", "有效势", "哈密顿量分解"],
   "summary": "本页介绍了电子组态能级计算中的中心力场近似方法，通过分解哈密顿量并修正剩余静电势与自旋轨道耦合项建立更精确的模型",
   "pending_concepts": ["S(r_i)的具体物理意义", "中心力场近似的误差分析", "自旋轨道耦合对能级分裂的具体影响"]
}
</CTX>