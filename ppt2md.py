import os
import re
import time
from pathlib import Path
from dashscope import MultiModalConversation
import dashscope

# ================= 配置区域 =================
# 建议配置环境变量，或者在此处填入
# dashscope.api_key = "sk-xxxxxxxxxxxx"

MODEL_NAME = "qwen3-vl-plus"
INPUT_FOLDER = "./ppt_images"      
OUTPUT_FOLDER = "./markdown_output" 
FINAL_FILE = "FULL_PRESENTATION.md" 

# 思考预算 (Token)
THINKING_BUDGET = 2048 

# === 修复后的 Prompt 模板 (关键：找回了 CTX 标签要求) ===
USER_PROMPT_TEMPLATE = r"""
你将收到一张PPT页面截图（单页）。请把该页内容转换为“尽可能保持原结构”的 Markdown。

硬性格式要求：
1) 公式：行内使用 $...$；行间使用
$$
...
$$
不要用 \(...\) 或 \[...\]。
2) 如果页面有表格，用 Markdown 表格表达；如果是复杂表格，允许拆分并解释合并单元格关系。
3) 对该页中所有图形/照片/示意图/流程图/坐标图/标注关系，必须提供“足够细粒度”的图像描述：
   - 元素有哪些（形状/箭头/颜色/相对位置/坐标轴/标注文字/连接关系）
   - 视觉层级与布局（左/右/上/下分区，主标题位置，图与文字对应关系）
   - 若图可被复刻（如TikZ/Visio），描述应可直接指导复刻。
4) OCR时保持专有名词、符号、变量名（如 X_m、k^2(x)）的大小写与下标。
5) 不要编造不存在的内容；不确定处请用“[无法辨认]”标记。

输出结构（必须遵守）：
- 顶部：# Slide {slide_no}
- 然后依次给出该页的文本内容（用合适的 Markdown 标题层级/列表/引用/代码块等）
- 然后单独给出一个二级标题：## Figure & Layout Description
  在这里写对该页视觉信息的细粒度描述。
- 最后输出一个隐藏的上下文块，用于跨页连贯（必须存在且为合法JSON，必须包含在 <CTX> 标签中）：
  当前页面信息：
- 幻灯片编号: {slide_no}
- 上一页传递的上下文 (Context): 
  {context_block}

请开始分析：
"""

def get_sorted_images(folder):
    """获取并排序图片"""
    p = Path(folder)
    if not p.exists():
        os.makedirs(folder, exist_ok=True)
        print(f"警告: 文件夹 {folder} 不存在。")
        return []
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    # 按文件名智能排序
    return sorted([f for f in p.iterdir() if f.suffix.lower() in exts], 
                  key=lambda x: x.name)

def extract_context(text):
    """提取 内容"""
    # === 修复点：填回了正则表达式 ===
    pattern = r"<CTX>(.*?)</CTX>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No context from previous page."

def safe_get_content(choice):
    """安全地从 choice 中提取 text"""
    text = ""
    if isinstance(choice, dict):
        message = choice.get('message', {})
    else:
        message = getattr(choice, 'message', None)
    
    if not message:
        return ""

    content = None
    if isinstance(message, dict):
        content = message.get('content')
    else:
        content = getattr(message, 'content', None)

    if content:
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    text += item.get('text', '')
                elif isinstance(item, str):
                    text += item
        elif isinstance(content, str):
            text = content
    return text

def check_is_thinking(choice):
    """检查当前是否在输出思考内容"""
    if isinstance(choice, dict):
        message = choice.get('message', {})
        return bool(message.get('reasoning_content'))
    else:
        message = getattr(choice, 'message', None)
        return bool(getattr(message, 'reasoning_content', False))

def merge_markdowns(output_dir, final_filename):
    """合并文件"""
    p = Path(output_dir)
    final_path = p.parent / final_filename
    md_files = sorted(p.glob("Slide_*.md"), key=lambda x: x.name)
    
    if not md_files:
        return

    print(f"\n正在合并 {len(md_files)} 个文件 -> {final_path.name}")
    with open(final_path, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# 演示文稿内容汇总\n\n> 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")
    print(f"合并完成！")

def process_ppt_stream():
    images = get_sorted_images(INPUT_FOLDER)
    if not images:
        print("未找到图片，请检查 ppt_images 文件夹")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    current_context = "This is the first slide."
    
    print(f"=== 任务启动: {len(images)} 张幻灯片 | 模型: {MODEL_NAME} ===")
    print(f"=== 策略: 串行(Context) + 思考(Thinking) + 流式(Stream) ===")

    for idx, img_path in enumerate(images):
        slide_no = idx + 1
        print(f"\n[{slide_no}/{len(images)}] 处理中: {img_path.name}")
        
        filled_prompt = USER_PROMPT_TEMPLATE.format(
            slide_no=slide_no,
            context_block=current_context
        )
        
        messages = [{
            "role": "user",
            "content": [
                {"image": f"file://{img_path.absolute()}"},
                {"text": filled_prompt}
            ]
        }]

        full_text = ""
        is_thinking_printed = False
        
        # 重试循环
        for attempt in range(3):
            try:
                responses = MultiModalConversation.call(
                    model=MODEL_NAME,
                    messages=messages,
                    stream=True,
                    incremental_output=True,
                    enable_thinking=True,        
                    thinking_budget=THINKING_BUDGET 
                )
                
                print("  >> 状态: ", end="", flush=True)
                
                for chunk in responses:
                    if chunk.status_code != 200:
                        continue
                    if not chunk.output or not chunk.output.choices:
                        continue
                    
                    choice = chunk.output.choices[0]
                    
                    # 状态指示
                    if check_is_thinking(choice):
                        if not is_thinking_printed:
                            print("正在深度思考...", end="", flush=True)
                            is_thinking_printed = True
                        continue 
                    
                    # 获取正文
                    text_chunk = safe_get_content(choice)
                    if text_chunk:
                        if is_thinking_printed:
                            print("\n  >> 生成: ", end="", flush=True)
                            is_thinking_printed = False
                        print(text_chunk, end="", flush=True)
                        full_text += text_chunk
                
                print("\n  >> 完成")
                break 
            except Exception as e:
                print(f"\n  !! 异常 (重试 {attempt+1}): {e}")
                time.sleep(1)

        if full_text:
            save_name = f"Slide_{slide_no:02d}.md"
            with open(Path(OUTPUT_FOLDER) / save_name, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            # 提取下文 Context
            ctx = extract_context(full_text)
            # 只有当提取到有效内容时才更新上下文
            if "No context" not in ctx:
                current_context = ctx
        else:
            print("  !!警告: 本页未生成有效内容")

    merge_markdowns(OUTPUT_FOLDER, FINAL_FILE)

if __name__ == "__main__":
    process_ppt_stream()