import os
import re
import time
import json
import logging
import datetime
import argparse
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
import queue

# === 尝试导入 rich ===
try:
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn, MofNCompleteColumn
    )
    from rich.live import Live
    from rich.panel import Panel
    from rich.console import Console
except ImportError:
    print("❌ 缺少依赖库 [rich]。请运行: pip install rich")
    exit(1)

import dashscope
from dashscope import MultiModalConversation

# ================= 配置区域 =================
MODEL_NAME = "qwen3-vl-plus"
INPUT_FOLDER = "./ppt_images"      
OUTPUT_FOLDER = "./markdown_output" 
LOG_FOLDER = "./log"

# 并发控制
MAX_WORKERS = 15  
THINKING_BUDGET = 2048 

# === 命令行参数解析 ===
parser = argparse.ArgumentParser(description="PPT转Markdown工具")
parser.add_argument("-n", "--name", type=str, default="default", help="任务会话名称")
parser.add_argument("-o", "--output", type=str, default="./markdown_output", help="输出目录路径")
args = parser.parse_args()

SESSION_FILE = f"session_{args.name}.json"
CURRENT_SESSION_NAME = args.name
# 强制转为绝对路径
OUTPUT_FOLDER = str(Path(args.output).resolve())
INPUT_FOLDER_ABS = str(Path(INPUT_FOLDER).resolve())

# === Prompt 模板 ===
USER_PROMPT_TEMPLATE = r"""
你是一个专业的 PPT 转 Markdown 助手。你将收到一张 PPT 页面截图（单页）。

【上一页传递的知识状态 Context】:
{context_block}

---
【当前任务】
请分析当前 PPT 图片，将其转换为 Markdown。

【硬性格式要求】
1. **公式**：行内用 $...$；行间用 $$...$$。禁止使用 \(...\) 或 \[...\]。
2. **表格**：使用 Markdown 表格。
3. **视觉描述**：必须包含二级标题 `## Figure & Layout Description`，详细描述图片的视觉元素（布局、颜色、形状、层级），描述应细致到可指导复刻。
4. **OCR**：精确识别文字、符号下标。
5. **真实性**：不确定的内容标记为“[无法辨认]”。

【输出结构（必须严格遵守）】
输出必须包含以下三部分，顺序不能乱：

1. **幻灯片头部**
   # Slide {slide_no}

2. **正文内容**
   (这里是识别出的 PPT 文本内容，保持原级结构)

3. **视觉描述**
   ## Figure & Layout Description
   (这里是视觉描述)

4. **上下文更新 (Hidden Block)**
   请根据“上一页的知识状态”和“当前页内容”，生成一个新的、扁平的 JSON 状态块。
   *注意*：不要把上一页的 JSON 直接嵌套进来！你需要消化信息，输出合并后的当前状态。
   
   格式必须如下（必须包含在 <CTX> 标签中）：
   <CTX>
   {{
      "topic": "当前页的核心主题",
      "keywords": ["关键词1", "关键词2"],
      "summary": "一句话概括本页对于整体课程的知识增量",
      "pending_concepts": ["尚未解释清楚的概念..."]
   }}
   </CTX>
"""

# ================= 辅助函数 =================

def setup_logger(session_name):
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_FOLDER, f"log_{session_name}_{timestamp}.log")
    logger = logging.getLogger(f"PPT2MD_{session_name}")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - [%(processName)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger, log_file

def check_env():
    # 优先读取环境变量
    api_key = os.getenv("DASHSCOPE_API_KEY")
    # 如果环境变量没有，再看代码里有没有硬编码
    if not api_key and dashscope.api_key is None:
        return None, "❌ 未检测到 API Key。请设置环境变量 DASHSCOPE_API_KEY。"
    
    # 返回获取到的 key (如果代码没硬编码，api_key就是环境变量的值)
    final_key = api_key if api_key else dashscope.api_key
    
    if not os.path.exists(INPUT_FOLDER):
        try:
            os.makedirs(INPUT_FOLDER)
            return None, f"⚠️ 输入文件夹 {INPUT_FOLDER} 不存在，已创建。"
        except:
            return None, f"❌ 无法创建文件夹 {INPUT_FOLDER}。"
            
    return final_key, "环境检查通过"

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s.name)]

def scan_ppt_folders(root_folder):
    root = Path(root_folder)
    if not root.exists(): return {}
    tasks = {}
    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
    for entry in root.iterdir():
        if entry.is_dir():
            images = [f for f in entry.iterdir() if f.suffix.lower() in exts]
            if images:
                images.sort(key=natural_sort_key)
                tasks[entry.name] = [str(img.absolute()) for img in images]
    return tasks

def extract_context(text):
    pattern = r"<CTX>(.*?)</CTX>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).replace("```json", "").replace("```", "").strip()
    return "No context from previous page."

def read_context_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            ctx = extract_context(content)
            if "No context" not in ctx:
                return ctx
    except:
        pass
    return "Resumed session. Context lost from previous file."

def safe_get_content(choice):
    text = ""
    msg = choice.get('message', {}) if isinstance(choice, dict) else getattr(choice, 'message', None)
    if not msg: return ""
    content = msg.get('content') if isinstance(msg, dict) else getattr(msg, 'content', None)
    if content:
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict): text += item.get('text', '')
                elif isinstance(item, str): text += item
        elif isinstance(content, str): text = content
    return text

def check_is_thinking(choice):
    msg = choice.get('message', {}) if isinstance(choice, dict) else getattr(choice, 'message', None)
    if not msg: return False
    return bool(msg.get('reasoning_content') if isinstance(msg, dict) else getattr(msg, 'reasoning_content', False))

def merge_markdowns(ppt_output_dir, ppt_name):
    p = Path(ppt_output_dir)
    final_path = p / f"{ppt_name}_FULL.md"
    md_files = sorted(p.glob("Slide_*.md"), key=natural_sort_key)
    if not md_files: return
    with open(final_path, 'w', encoding='utf-8') as outfile:
        outfile.write(f"# {ppt_name} 汇总\n\n> 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")

# ================= 交互与状态管理 =================

def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    return None

def save_session(tasks_config):
    with open(SESSION_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks_config, f, indent=2, ensure_ascii=False)

def parse_range_string(range_str, max_len):
    if not range_str or range_str.lower() == 'all':
        return 0, max_len
    try:
        if '-' in range_str:
            start, end = range_str.split('-')
            start = int(start) - 1 
            if end.lower() == 'end': end = max_len
            else: end = int(end)
            return max(0, start), min(end, max_len)
        else:
            idx = int(range_str) - 1
            return max(0, idx), min(idx + 1, max_len)
    except:
        return 0, max_len

def interactive_setup(console, api_key):
    console.print(Panel.fit(f"🔍 扫描中... (会话: [bold magenta]{CURRENT_SESSION_NAME}[/])", style="bold blue"))
    all_tasks = scan_ppt_folders(INPUT_FOLDER)
    
    if not all_tasks:
        console.print(f"[bold red]❌ 未在 {INPUT_FOLDER} 中发现子文件夹。[/]")
        return None

    ppt_names = list(all_tasks.keys())
    
    old_session = load_session()
    if old_session:
        console.print("\n[bold yellow]📢 发现当前会话有未完成的任务！[/]")
        console.print(f"   包含: [cyan]{', '.join(old_session.keys())}[/]")
        choice = input("👉 是否继续？(y/n) [默认为 y]: ").strip().lower()
        if choice != 'n':
            # 恢复任务时，也要把当前的 api_key 注入进去
            for k in old_session:
                old_session[k]["api_key"] = api_key
            return old_session

    console.print("\n[bold green]📂 发现以下 PPT:[/]")
    for i, name in enumerate(ppt_names):
        count = len(all_tasks[name])
        console.print(f"  [[bold cyan]{i+1}[/]] {name} ([yellow]{count} 页[/])")
    
    console.print("\n👉 [bold]选择要处理的 PPT:[/]")
    console.print("   输入序号(如 1,3) | 输入 'a' 全选")
    
    selection = input("   您的选择: ").strip()
    
    selected_names = []
    if selection.lower() == 'a':
        selected_names = ppt_names
    else:
        try:
            indices = [int(x.strip()) for x in selection.split(',') if x.strip()]
            for idx in indices:
                if 1 <= idx <= len(ppt_names):
                    selected_names.append(ppt_names[idx-1])
        except:
            console.print("[bold red]❌ 输入无效[/]")
            return None

    if not selected_names: return None

    final_config = {}
    console.print("\n⚙️  [bold]配置页码范围 (回车=全选):[/]")
    
    for name in selected_names:
        total = len(all_tasks[name])
        range_input = input(f"   📘 [{name}] (共{total}页) 范围: ").strip()
        start, end = parse_range_string(range_input, total)
        
        final_config[name] = {
            "images": all_tasks[name],
            "range_start": start,
            "range_end": end,
            "task_id": None,
            "api_key": api_key  # 关键：把 Key 存进配置传给子进程
        }
    
    save_session(final_config)
    return final_config

# ================= 核心工作线程 =================

def process_single_ppt_task(ppt_name, config, msg_queue):
    """子进程：执行任务"""
    
    # === 关键：子进程初始化 API Key ===
    # 优先使用配置里的 key，如果没有（旧存档），再尝试 os.getenv
    task_key = config.get("api_key")
    if task_key:
        dashscope.api_key = task_key
    else:
        # 兜底：尝试读环境
        dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    
    images_paths = config["images"]
    start_idx = config["range_start"]
    end_idx = config["range_end"]
    task_id = config["task_id"]
    
    target_images = images_paths[start_idx:end_idx]
    
    ppt_output_dir = Path(OUTPUT_FOLDER) / ppt_name
    os.makedirs(ppt_output_dir, exist_ok=True)
    msg_queue.put(("log", f"[{ppt_name}] 输出目录: {ppt_output_dir}"))
    
    msg_queue.put(("init_task", task_id, len(target_images)))
    
    current_context = "Starting processing. No prior context."
    first_target_slide_no = start_idx + 1 
    
    if first_target_slide_no > 1:
        prev_slide_no = first_target_slide_no - 1
        prev_md_path = ppt_output_dir / f"Slide_{prev_slide_no:02d}.md"
        if prev_md_path.exists():
            current_context = read_context_from_file(prev_md_path)
    
    msg_queue.put(("log", f"[{ppt_name}] 启动范围 P{first_target_slide_no}-P{end_idx}"))

    for i, img_path_str in enumerate(target_images):
        actual_slide_no = start_idx + i + 1
        save_name = f"Slide_{actual_slide_no:02d}.md"
        output_path = ppt_output_dir / save_name
        
        # 1. 断点检测
        if output_path.exists() and output_path.stat().st_size > 100:
            msg_queue.put(("status", task_id, f"P{actual_slide_no} 跳过"))
            current_context = read_context_from_file(output_path)
            msg_queue.put(("advance", task_id, 1))
            continue

        # 2. 准备
        filled_prompt = USER_PROMPT_TEMPLATE.format(
            slide_no=actual_slide_no,
            context_block=current_context
        )
        
        messages = [{
            "role": "user",
            "content": [
                {"image": f"file://{img_path_str}"},
                {"text": filled_prompt}
            ]
        }]

        full_text = ""
        msg_queue.put(("status", task_id, f"P{actual_slide_no} 分析中..."))
        
        # 3. 调用 API
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
                
                msg_queue.put(("status", task_id, f"P{actual_slide_no} 生成中..."))
                
                for chunk in responses:
                    if chunk.status_code != 200:
                        msg_queue.put(("log", f"[{ppt_name}] P{actual_slide_no} Err: {chunk.code} {chunk.message}"))
                        continue
                    if not chunk.output or not chunk.output.choices: continue
                    choice = chunk.output.choices[0]
                    
                    if check_is_thinking(choice):
                        msg_queue.put(("status", task_id, f"P{actual_slide_no} 深度思考..."))
                        continue 
                    
                    text_chunk = safe_get_content(choice)
                    if text_chunk:
                        full_text += text_chunk
                
                msg_queue.put(("log", f"[{ppt_name}] P{actual_slide_no} 完成"))
                break 
            except Exception as e:
                msg_queue.put(("log", f"[{ppt_name}] P{actual_slide_no} 异常: {str(e)}"))
                msg_queue.put(("status", task_id, f"P{actual_slide_no} 重试..."))
                time.sleep(2)

        # 4. 保存
        if full_text:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            ctx = extract_context(full_text)
            if "No context" not in ctx:
                current_context = ctx
        else:
            msg_queue.put(("log", f"[{ppt_name}] P{actual_slide_no} 失败(空)"))

        msg_queue.put(("advance", task_id, 1))

    msg_queue.put(("status", task_id, "合并中..."))
    merge_markdowns(ppt_output_dir, ppt_name)
    msg_queue.put(("log", f"[{ppt_name}] 全部完成"))
    return f"{ppt_name} Done"

# ================= 主程序入口 =================
def main():
    console = Console()
    
    # 1. 环境检查与 Key 获取
    final_key, msg = check_env()
    if not final_key:
        console.print(msg)
        return

    # 2. 日志
    logger, log_file_path = setup_logger(CURRENT_SESSION_NAME)
    console.print(Panel(f"""[bold]运行环境信息[/]
    会话名称: [magenta]{CURRENT_SESSION_NAME}[/]
    API Key (前8位): {final_key[:8]}...
    输入目录: {INPUT_FOLDER_ABS}
    输出目录: {OUTPUT_FOLDER}
    日志文件: {log_file_path}
    """, title="配置检查", border_style="green"))

    # 3. 交互设置 (传入 key)
    tasks_config = interactive_setup(console, final_key)
    if not tasks_config:
        return

    # 4. 初始化
    m = Manager()
    msg_queue = m.Queue()

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.fields[ppt_name]}", justify="right"),
        BarColumn(),
        TaskProgressColumn(),      
        MofNCompleteColumn(),      
        TimeElapsedColumn(),       
        TimeRemainingColumn(),     
        TextColumn("[yellow]{task.fields[status]}"), 
    )

    print("\n")
    
    # 5. 启动
    with Live(progress, console=console, refresh_per_second=10):
        for ppt_name in tasks_config:
            tid = progress.add_task(
                f"waiting...", 
                total=100, 
                ppt_name=ppt_name, 
                status="准备中..."
            )
            tasks_config[ppt_name]["task_id"] = tid

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = []
            for ppt_name, config in tasks_config.items():
                futures.append(executor.submit(process_single_ppt_task, ppt_name, config, msg_queue))
            
            finished_tasks = 0
            total_tasks = len(tasks_config)
            
            while finished_tasks < total_tasks:
                try:
                    while not msg_queue.empty():
                        msg_type, *args = msg_queue.get_nowait()
                        
                        if msg_type == "init_task":
                            tid, total = args
                            progress.update(tid, total=total)
                        elif msg_type == "advance":
                            tid, steps = args
                            progress.advance(tid, steps)
                        elif msg_type == "status":
                            tid, text = args
                            progress.update(tid, status=text)
                        elif msg_type == "log":
                            log_msg = args[0]
                            logger.info(log_msg)
                            
                    done_count = sum(1 for f in futures if f.done())
                    if done_count > finished_tasks:
                        finished_tasks = done_count
                    
                    if finished_tasks == total_tasks and msg_queue.empty():
                        break
                    time.sleep(0.1)
                except queue.Empty:
                    pass
                except Exception as e:
                    logger.error(f"Main Loop Error: {e}")
                    break

    console.print(Panel(f"[bold green]✨ 所有任务处理完毕！[/]", expand=False))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断。")