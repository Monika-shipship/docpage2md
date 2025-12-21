# Slide 29

## 附录一：矩阵 & det

$\hat{A} = [a_{\mu\nu}]$ 矩阵，$n \times n$.

$\hat{A}^{-1}\hat{A} = \hat{A}\hat{A}^{-1} = \mathbb{I}$.

$\hat{A}^{-1} = [a^{\mu\nu}]$

$a^{\mu\nu}a_{\nu\lambda} = \delta^\mu_\lambda$, $a_{\mu\lambda}a^{\lambda\nu} = \delta_\mu^\nu$.

2. det

记 $a = \det(a_{\mu\nu})$

定义 $\epsilon_{\nu_1\nu_2\cdots\nu_n} a = \epsilon^{\mu_1\mu_2\cdots\mu_n} a_{\mu_1\nu_1}a_{\mu_2\nu_2}\cdots a_{\mu_n\nu_n}$

由于 $\epsilon_{\nu_1\nu_2\cdots\nu_n} \epsilon^{\nu_1\nu_2\cdots\nu_n} = n!$

$n! a = \epsilon_{\nu_1\nu_2\cdots\nu_n} \epsilon^{\mu_1\mu_2\cdots\mu_n} a_{\mu_1\nu_1}a_{\mu_2\nu_2}\cdots a_{\mu_n\nu_n}$

$a = \frac{1}{n!} \epsilon_{\nu_1\nu_2\cdots\nu_n} \epsilon^{\mu_1\mu_2\cdots\mu_n} a_{\mu_1\nu_1}a_{\mu_2\nu_2}\cdots a_{\mu_n\nu_n}$

记 $\tilde{a} = \det(a^{\mu\nu})$

$\epsilon^{\mu_1\mu_2\cdots\mu_n} \tilde{a} = \epsilon_{\lambda_1\lambda_2\cdots\lambda_n} a^{\lambda_1\mu_1}a^{\lambda_2\mu_2}\cdots a^{\lambda_n\mu_n}$

同样 $a_{\mu_1\nu_1}a_{\mu_2\nu_2}\cdots a_{\mu_n\nu_n}$

## Figure & Layout Description
页面背景为浅米色方格纸，网格线为浅灰色正方形格子。所有文字为黑色手写体，字迹清晰工整。标题"附录一：矩阵 & det"位于页面左上角，使用较大字号书写。正文内容分为两个主要部分：第一部分以"1."开头，包含矩阵定义、逆矩阵性质及逆矩阵元素关系式；第二部分以"2. det"开头，详细推导行列式定义及Levi-Civita符号相关公式。公式按行排列，每行公式间有适当行距，关键符号（如$\delta$、$\epsilon$）使用标准数学符号书写，上下标位置准确。页面无图形元素，纯文字与公式排版，整体结构呈纵向层级分布，重点公式通过换行分隔增强可读性。手写文字存在轻微倾斜，但不影响内容识别。

<CTX>
{
   "topic": "矩阵与行列式的协变形式基础",
   "keywords": ["矩阵", "行列式", "Levi-Civita符号", "逆矩阵", "度规行列式"],
   "summary": "本页补充了黎曼几何所需的矩阵与行列式基础理论，重点推导了协变/逆变指标下的行列式定义及其与Levi-Civita符号的关系",
   "pending_concepts": ["行列式在协变导数中的具体应用", "度规行列式与体积元的直接关联", "Levi-Civita符号在弯曲时空中的协变性质"]
}
</CTX>