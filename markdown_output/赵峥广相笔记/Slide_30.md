# Slide 30

$$T^{\mu}_{\nu;\lambda} A_{\mu} B^{\nu} - T^{\mu}_{\nu} B^{\nu} \Gamma^{\delta}_{\mu\lambda} A_{\delta} + T^{\mu}_{\nu} A_{\mu} \Gamma^{\nu}_{\delta\lambda} B^{\delta} = T^{\mu}_{\nu,\lambda} A_{\mu} B^{\nu}$$

$$T^{\mu}_{\nu;\lambda} A_{\mu} B^{\nu} = T^{\mu}_{\nu,\lambda} A_{\mu} B^{\nu} + T^{\mu}_{\nu} B^{\nu} \Gamma^{\delta}_{\mu\lambda} A_{\delta} - T^{\mu}_{\nu} A_{\mu} \Gamma^{\nu}_{\delta\lambda} B^{\delta}$$

## 坐标转换

$$T^{\mu}_{\nu;\lambda} A_{\mu} B^{\nu} = T^{\mu}_{\nu,\lambda} A_{\mu} B^{\nu} + T^{\delta}_{\nu} B^{\nu} \Gamma^{\mu}_{\delta\lambda} A_{\mu} - T^{\mu}_{\delta} A_{\mu} \Gamma^{\delta}_{\nu\lambda} B^{\nu}$$  
（蓝色标注：$\delta\mu$互换，$\delta\nu$互换）

$$T^{\mu}_{\nu;\lambda} = T^{\mu}_{\nu,\lambda} + \Gamma^{\mu}_{\delta\lambda} T^{\delta}_{\nu} - \Gamma^{\delta}_{\nu\lambda} T^{\mu}_{\delta}$$

$$A_{\nu;\lambda} = A_{\nu,\lambda} - \Gamma^{\kappa}_{\nu\lambda} A_{\kappa}$$

$$B^{\mu}_{;\lambda} = B^{\mu}_{,\lambda} + \Gamma^{\mu}_{\delta\lambda} B^{\delta}$$

$$\Gamma^{\mu}_{\delta\lambda} T^{\delta}_{\nu}$$

$$T^{\beta}_{\alpha;\lambda} = T^{\beta}_{\alpha,\lambda} + \Gamma^{\beta}_{\delta\lambda} T^{\delta}_{\alpha} - \Gamma^{\delta}_{\alpha\lambda} T^{\beta}_{\delta}$$

$$T_{\mu\nu;\lambda} = T_{\mu\nu,\lambda} - \Gamma^{\delta}_{\mu\lambda} T_{\delta\nu} - \Gamma^{\delta}_{\nu\lambda} T_{\mu\delta}$$

$$T^{\mu\nu}_{;\lambda} = T^{\mu\nu}_{,\lambda} + \Gamma^{\mu}_{\delta\lambda} T^{\delta\nu} + \Gamma^{\nu}_{\delta\lambda} T^{\mu\delta}$$

## Figure & Layout Description

图片为手写数学公式稿纸，背景为浅米色方格纸（网格线为浅灰色）。所有公式和文字以橙色墨水手写，部分关键标注用蓝色墨水书写。内容按垂直顺序排列，共分7个逻辑区块：

1. **顶部公式区**：两行橙色公式，占据图片上1/4区域。第一行公式包含三项，以等号连接；第二行公式以等号开头，结构与第一行互补。
2. **标题区**：位于中上部，橙色手写汉字"坐标转换"（"坐"字略带连笔），字体大小比公式略大，居中对齐。
3. **核心公式区**：标题下方有两行公式。第一行公式右侧有两处蓝色标注："δμ互换"和"δν互换"，其中"δμ"和"δν"为蓝色希腊字母，"互换"为蓝色汉字；第二行公式为协变微商的标准表达式。
4. **矢量场公式区**：包含两个独立公式，分别描述协变矢量场 $A_{\nu}$ 和逆变矢量场 $B^{\mu}$ 的协变微分，垂直排列。
5. **中间项公式**：单行公式 $\Gamma^{\mu}_{\delta\lambda} T^{\delta}_{\nu}$，居中显示，作为过渡。
6. **混合张量公式**：单行公式 $T^{\beta}_{\alpha;\lambda} = \cdots$，展示混合张量的协变微分。
7. **底部张量公式区**：最后两行公式，分别描述协变二阶张量 $T_{\mu\nu}$ 和逆变二阶张量 $T^{\mu\nu}$ 的协变微分，垂直排列。

整体布局呈垂直流式结构，公式间行距均匀（约1.5倍行高）。关键符号（如 $\Gamma$）手写清晰，下标/上标位置准确。蓝色标注仅出现在第三区块，与橙色主公式形成视觉对比。右下角有手写箭头指向最后一行公式，但箭头后内容被截断，标记为"[无法辨认]"。

<CTX>
{
   "topic": "协变微分的坐标变换与具体张量表达式",
   "keywords": ["坐标变换", "协变微商", "联络系数", "逆变矢量场", "协变矢量场", "高阶张量"],
   "summary": "本页推导协变微分在坐标变换下的形式，给出逆变/协变矢量场及二阶张量的协变微分显式表达式",
   "pending_concepts": ["协变微分的几何意义", "协变微分与曲率的关系", "联络系数的物理诠释"]
}
</CTX>