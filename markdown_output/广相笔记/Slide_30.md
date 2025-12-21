# Slide 30

$$\epsilon^{\mu_1\mu_2\cdots\mu_n} a_{\mu_1\nu_1} a_{\mu_2\nu_2} \cdots a_{\mu_n\nu_n} \bar{a} = \epsilon_{\lambda_1\lambda_2\cdots\lambda_n} (a^{\lambda_1\mu_1} a_{\mu_1\nu_1}) (a^{\lambda_2\mu_2} a_{\mu_2\nu_2}) \cdots (a^{\lambda_n\mu_n} a_{\mu_n\nu_n})$$

$$= \epsilon_{\lambda_1\lambda_2\cdots\lambda_n} \delta_{\nu_1}^{\lambda_1} \delta_{\nu_2}^{\lambda_2} \cdots \delta_{\nu_n}^{\lambda_n}$$

$$\epsilon^{\mu_1\mu_2\cdots\mu_n} a_{\mu_1\nu_1} a_{\mu_2\nu_2} \cdots a_{\mu_n\nu_n} \bar{a} = \epsilon_{\nu_1\nu_2\cdots\nu_n}$$

$$\epsilon_{\nu_1\nu_2\cdots\nu_n} a \bar{a} = \epsilon_{\nu_1\nu_2\cdots\nu_n}$$

$$a\bar{a} = 1$$

$$\bar{a} = \frac{1}{a}$$

## 1.3 余因子（即伴随矩阵）

定义 $A^{\mu\nu} = \frac{1}{n!} \epsilon^{\mu\mu_2\cdots\mu_n} \epsilon^{\nu\nu_1\cdots\nu_n} a_{\mu_2\nu_2} \cdots a_{\mu_n\nu_n}$

可证 $A^{\mu\nu} a_{\mu\lambda} = \frac{1}{n} a \delta_\lambda^\nu$：

$$A^{\mu\nu} a_{\mu\lambda} = \frac{1}{n!} \epsilon^{\mu\mu_2\cdots\mu_n} \epsilon^{\nu\nu_1\cdots\nu_n} a_{\mu\lambda} a_{\mu_2\nu_2} \cdots a_{\mu_n\nu_n}$$

$$= \frac{1}{n!} \epsilon^{\nu\nu_1\cdots\nu_n} \cdot a \cdot \epsilon_{\lambda\nu_2\cdots\nu_n}$$

$$= \frac{1}{n!} a \cdot \delta_\lambda^\nu (n-1)!$$

## Figure & Layout Description
图片呈现为手写笔记形式，背景为浅米色方格纸（网格线为浅灰色细线）。内容由黑色墨水书写，包含多组数学公式和中文说明。顶部区域有两行Levi-Civita符号相关的推导公式，字体大小适中，公式排版紧凑。中间部分有一条橙色手绘下划线（略带波浪形）横跨第三行公式，下划线末端连接一个橙色向下箭头，指向下方公式。在"可证"部分的推导过程中，有一条蓝色手绘下划线标记了关键步骤。文字内容包括中文标题"1.3 余因子（即伴随矩阵）"及多处数学符号，其中希腊字母和上下标清晰可辨。整体布局为垂直排列的推导过程，公式从上至下依次展开，层次分明，无边框或特殊装饰元素。手写笔迹流畅，部分公式中的下标和上标间距紧凑但可辨认。

<CTX>
{
   "topic": "余因子与伴随矩阵的定义及性质推导",
   "keywords": ["余因子", "伴随矩阵", "Levi-Civita符号", "行列式", "逆矩阵"],
   "summary": "本页系统推导了余因子（伴随矩阵）的定义及其与Levi-Civita符号的内在联系，并证明了伴随矩阵与原矩阵乘积的关键性质",
   "pending_concepts": ["余因子在矩阵求逆中的具体应用步骤", "伴随矩阵与逆矩阵的完整关系表达式", "行列式导数的协变形式在弯曲时空中的实现"]
}
</CTX>