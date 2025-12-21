# Slide 118

$$ c \, dt = dr \left(1 + \frac{2\beta b}{\gamma}\right) \sqrt{1 + \frac{b^2}{\gamma^2 - b^2} \left(1 + \frac{2\beta b}{\gamma}\right)} $$

$$ \sqrt{1 + \frac{b^2}{\gamma^2 - b^2} + \frac{b^2}{\gamma^2 - b^2} \cdot \frac{2\beta b}{\gamma}} $$

$$ \sqrt{\frac{\gamma^2}{\gamma^2 - b^2} + \frac{b^2}{\gamma^2 - b^2} \cdot \frac{2\beta b}{\gamma}} $$

$$ \sqrt{\frac{\gamma^2}{\gamma^2 - b^2} \left(1 + \frac{b^2}{\gamma^2} \cdot \frac{2\beta b}{\gamma}\right)} $$

$$ c \, dt = dr \left(1 + \frac{2\beta b}{\gamma}\right) \frac{\gamma}{\sqrt{\gamma^2 - b^2}} \left(1 + \frac{2\beta b^3}{2\gamma^3}\right) $$

$$ = \frac{\gamma \, dr}{\sqrt{\gamma^2 - b^2}} \left(1 + \frac{2\beta b}{\gamma} + \frac{\beta b^3}{\gamma^3}\right) $$

$$ c \, dt = \frac{\gamma \, dr}{\sqrt{\gamma^2 - b^2}} + 2\beta b \frac{dr}{\sqrt{\gamma^2 - b^2}} + \beta b^3 \frac{dr}{\gamma^2 \sqrt{\gamma^2 - b^2}} $$

$$ \underbrace{\hspace{1.5cm}}_{I_1} \quad \underbrace{\hspace{1.5cm}}_{I_2} \quad \underbrace{\hspace{3.5cm}}_{I_3} $$

$$ I_1 = \frac{\frac{1}{2} d\gamma^2}{\sqrt{\gamma^2 - b^2}} = \frac{1}{2} \cdot \frac{1}{1 - \frac{1}{2}} (\gamma^2 - b^2)^{\frac{1}{2}} = \sqrt{\gamma^2 - b^2} $$

$$ \text{令 } y = \sqrt{\gamma^2 - b^2} \quad \gamma^2 - y^2 = b^2 \quad 2\gamma d\gamma = y dy \implies \frac{d\gamma}{y} = \frac{dy}{\gamma} = \frac{d(\gamma + y)}{\gamma + y} = d\ln(\gamma + y) $$

$$ I_2 = \int \frac{dr}{\sqrt{\gamma^2 - b^2}} = \int \frac{dy}{y} = \ln(\gamma + y) = \ln\left(\gamma + \sqrt{\gamma^2 - b^2}\right) $$

$$ I_3 = \int \frac{dr}{\gamma^2 \sqrt{\gamma^2 - b^2}} = \int \frac{dr}{\gamma^2 y} = \int \frac{dy}{\gamma^3} = \frac{1}{b^2} \cdot \frac{y}{\gamma} = \frac{1}{b^2} \cdot \frac{\sqrt{\gamma^2 - b^2}}{\gamma} $$

$$ \frac{dy}{\gamma} = \frac{\gamma^2 d\left(\frac{y}{\gamma}\right)}{b^2} \implies \frac{dy}{\gamma^3} = \frac{1}{b^2} d\left(\frac{y}{\gamma}\right) $$

## Figure & Layout Description
图片为方格纸背景的手写数学推导，整体采用黑色墨水书写。公式按自上而下的逻辑顺序排列，共分6个主要推导阶段：1) 初始延迟表达式；2) 平方根内展开；3) 分式化简；4) 一阶近似展开；5) 积分项分解（标记为I₁/I₂/I₃）；6) 各积分项详细计算。关键步骤使用波浪线标注积分项，变量替换部分用"令"字引导。公式中存在手写修正痕迹，如第二行平方根内分式结构有重写调整。推导过程包含微分运算(dγ, dy)、对数变换(ln)和根式化简，最后两行有微分关系的推导说明。整体布局紧凑但层次清晰，每行公式高度约1.5个方格单位，关键等号对齐。

<CTX>
{
   "topic": "雷达回波延迟的广义相对论计算",
   "keywords": ["雷达回波延迟", "广义相对论验证", "冲击参数", "度规方程", "时间延迟积分", "β一阶近似", "积分分解"],
   "summary": "本页通过积分分解法完成雷达信号时间延迟的解析推导，将延迟表达式分解为三个可计算积分项并给出具体解析解",
   "pending_concepts": ["雷达延迟实验的具体观测数据", "b/(4β)的物理意义解释", "与光线偏折角计算的关联性", "β参数的具体物理含义", "γ符号与径向坐标r的对应关系"]
}
</CTX>