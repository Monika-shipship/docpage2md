# Slide 16

**A:**  
$$ = \frac{1}{2} \left( \partial_\mu \partial_\sigma g_{\tau\nu} + \partial_\nu \partial_\tau g_{\mu\sigma} - \partial_\nu \partial_\sigma g_{\tau\mu} - \partial_\mu \partial_\tau g_{\nu\sigma} \right) $$

**B:**  
$$ + \Gamma^\lambda_{\mu\sigma} \Gamma^\beta_{\lambda,\nu\tau} - \Gamma^\lambda_{\nu\sigma} \Gamma^\beta_{\lambda,\mu\tau} $$  
$$ = g_{\lambda\beta} \Gamma^\lambda_{\nu\tau} \Gamma^\beta_{\mu\sigma} - g_{\lambda\beta} \Gamma^\lambda_{\mu\tau} \Gamma^\beta_{\nu\sigma} $$  
$$ \lambda \to \beta $$  
$$ = g_{\alpha\beta} \Gamma^\alpha_{\nu\tau} \Gamma^\beta_{\mu\sigma} - g_{\alpha\beta} \Gamma^\alpha_{\mu\tau} \Gamma^\beta_{\nu\sigma} $$

故 $ R_{\tau\sigma\mu\nu} = $  
$$ \frac{1}{2} \left( \partial_\mu \partial_\sigma g_{\tau\nu} + \partial_\nu \partial_\tau g_{\mu\sigma} - \partial_\nu \partial_\sigma g_{\tau\mu} - \partial_\mu \partial_\tau g_{\nu\sigma} \right) + g_{\alpha\beta} \left( \Gamma^\alpha_{\nu\tau} \Gamma^\beta_{\mu\sigma} - \Gamma^\alpha_{\mu\tau} \Gamma^\beta_{\nu\sigma} \right) $$

可验证与下式一致：$ \tau \leftrightarrow \lambda $

---

将 Christoffel 代入可得  
$$ R_{\lambda\sigma\mu\nu} = \frac{1}{2} \left( \partial_\sigma \partial_\nu g_{\lambda\mu} + \partial_\lambda \partial_\mu g_{\sigma\nu} - \partial_\sigma \partial_\mu g_{\lambda\nu} - \partial_\lambda \partial_\nu g_{\sigma\mu} \right) + g_{\alpha\beta} \left( \Gamma^\alpha_{\lambda\mu} \Gamma^\beta_{\sigma\nu} - \Gamma^\alpha_{\lambda\nu} \Gamma^\beta_{\sigma\mu} \right) $$

## Figure & Layout Description
页面为浅米色方格纸背景，手写内容以黑色为主，关键标识符使用彩色标注：  
1. **颜色编码**：  
   - "A:" 以红色手写体标注，位于页面左上角  
   - "B:" 以蓝色手写体标注，位于A部分下方  
   - "λ→β" 替换规则以蓝色手写体标注  
   - 底部公式框上方有深红色水平粗线（约2px）作为分隔线  
2. **布局结构**：  
   - 顶部为A部分的曲率张量第一项展开（4项偏导组合）  
   - 中部为B部分的克氏联络二次项展开，包含两行推导和指标替换过程  
   - 下部以"故"字引导最终曲率张量表达式，分两行书写  
   - 最底部为带红色分隔线的印刷体公式框，包含标准黎曼曲率张量表达式  
3. **手写特征**：  
   - 偏导符号∂书写为倾斜手写体  
   - 克氏联络Γ的上下标存在手写连笔现象（如Γ^λ_{μσ}中上标λ与下标μσ的间距较紧凑）  
   - 指标替换规则"λ→β"中箭头为手绘斜线  
4. **层级关系**：  
   - 手写推导内容占据页面80%区域，按从上到下逻辑流排列  
   - 印刷体公式框位于页面底部15%区域，与手写内容有明确视觉分隔  

<CTX>
{
   "topic": "黎曼曲率张量的显式展开与度规相容性验证",
   "keywords": ["曲率张量展开", "度规相容性应用", "指标替换规则", "抵消项分析", "克氏联络代入"],
   "summary": "通过将克氏联络显式代入曲率张量并执行指标替换，验证了曲率张量协变形式与标准表达式的一致性，揭示了度规导数项与联络二次项的组合机制",
   "pending_concepts": ["曲率张量的对称性质", "Ricci曲率的计算方法", "曲率标量的物理意义", "Bianchi恒等式的推导"]
}
</CTX>