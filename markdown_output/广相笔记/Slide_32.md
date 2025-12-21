# Slide 32

## 1.4 偏微分

已知 $a = \frac{1}{n!} \epsilon^{\mu_1 \mu_2 \dots \mu_n} \epsilon^{\nu_1 \nu_2 \dots \nu_n} a_{\mu_1 \nu_1} a_{\mu_2 \nu_2} \dots a_{\mu_n \nu_n}$

$$
\partial_\lambda (a) = \frac{1}{n!} \epsilon^{\mu_1 \mu_2 \dots \mu_n} \epsilon^{\nu_1 \nu_2 \dots \nu_n} \sum_{k=1}^n \left[ \partial_\lambda \left( a_{\mu_k \nu_k} \right) a_{\mu_1 \nu_1} \dots a_{\mu_{k-1} \nu_{k-1}} a_{\mu_{k+1} \nu_{k+1}} \dots a_{\mu_n \nu_n} \right]
$$

哑标，交换使得每个和中 $\mu_k \leftrightarrow \mu$, $\nu_k \leftrightarrow \nu$,

所以
$$
\partial_\lambda a = \frac{1}{n!} \epsilon^{\mu_1 \mu_2 \dots \mu_n} \epsilon^{\nu_1 \nu_2 \dots \nu_n} \color{red}{n} \cdot \partial_\lambda (a_{\mu_1 \nu_1}) a_{\mu_2 \nu_2} \dots a_{\mu_n \nu_n}
$$
$$
= \frac{1}{(n-1)!} \epsilon^{\mu_1 \mu_2 \dots \mu_n} \epsilon^{\nu_1 \nu_2 \dots \nu_n} \partial_\lambda (a_{\mu_1 \nu_1}) a_{\mu_2 \nu_2} \dots a_{\mu_n \nu_n}
$$
$$
\color{blue}{\mu_1 \to \mu \quad \nu_1 \to \nu}
$$
$$
= \frac{1}{(n-1)!} \epsilon^{\mu \mu_2 \dots \mu_n} \epsilon^{\nu \nu_2 \dots \nu_n} \partial_\lambda (a_{\mu \nu}) a_{\mu_2 \nu_2} \dots a_{\mu_n \nu_n}
$$
$$
= n! \, A^{\mu \nu}
$$

## Figure & Layout Description

图像为手写数学推导内容，书写在方格纸背景上。整体布局为纵向排列的数学公式与文字说明：

1. **标题区域**：左上角手写"1.4 偏微分"作为章节标题，黑色墨水书写，字体较大
2. **公式区域**：
   - 第一行公式为已知条件 $a = \frac{1}{n!} \epsilon^{\mu_1 \mu_2 \dots \mu_n} \epsilon^{\nu_1 \nu_2 \dots \nu_n} a_{\mu_1 \nu_1} a_{\mu_2 \nu_2} \dots a_{\mu_n \nu_n}$
   - 第二行开始是偏导数推导，包含多行公式，其中关键步骤用不同颜色标注
   - 红色墨水标注了系数 $n$，突出其在推导中的重要性
   - 蓝色墨水用于下划线标记关键替换步骤 $\mu_1 \to \mu \quad \nu_1 \to \nu$，并在最后一步标注 $= n! \, A^{\mu \nu}$
3. **文字说明**：中间穿插"哑标，交换使得每个和中 $\mu_k \leftrightarrow \mu$, $\nu_k \leftrightarrow \nu$"的推导说明，黑色手写体
4. **视觉层次**：
   - 主推导流程从上至下垂直排列
   - 颜色编码区分关键步骤：红色强调系数，蓝色标记变量替换
   - 公式中的求和符号 $\sum$ 展开为显式项，展示完整的乘积结构
5. **书写特征**：手写体带有明显笔锋，公式符号清晰但存在连笔现象（如 $\epsilon$ 符号的连写），部分下标存在轻微倾斜

## Figure & Layout Description

<CTX>
{
   "topic": "伴随矩阵的偏微分性质与行列式导数",
   "keywords": ["偏微分", "Levi-Civita符号", "余因子展开", "行列式导数", "伴随矩阵元素"],
   "summary": "本页推导出伴随矩阵元素与行列式偏导数的关系式 $\\partial_\\lambda a = n! \\, A^{\\mu\\nu}$，建立行列式微分与余因子矩阵的显式联系",
   "pending_concepts": ["协变微分在行列式导数中的应用", "非对称矩阵情形下的修正项推导", "高阶偏导数与矩阵不变量的关联"]
}
</CTX>