import json

from .config import AppConfig
from .files import scan_ppt_folders


def load_session(config: AppConfig):
    for session_file in (config.session_path, config.legacy_session_path):
        if not session_file.exists():
            continue
        try:
            with session_file.open("r", encoding="utf-8") as f:
                session_data = json.load(f)
        except Exception:
            continue

        if session_file == config.legacy_session_path and not config.session_path.exists():
            save_session(config, session_data)
        return session_data

    return None


def save_session(config: AppConfig, tasks_config):
    config.session_dir.mkdir(parents=True, exist_ok=True)
    with config.session_path.open("w", encoding="utf-8") as f:
        json.dump(tasks_config, f, indent=2, ensure_ascii=False)


def parse_range_string(range_str, max_len):
    if not range_str or range_str.lower() == "all":
        return 0, max_len

    try:
        if "-" in range_str:
            start, end = range_str.split("-")
            start = int(start) - 1
            if end.lower() == "end":
                end = max_len
            else:
                end = int(end)
            return max(0, start), min(end, max_len)

        idx = int(range_str) - 1
        return max(0, idx), min(idx + 1, max_len)
    except Exception:
        return 0, max_len


def interactive_setup(console, api_key, config: AppConfig):
    from rich.panel import Panel

    console.print(
        Panel.fit(
            f"🔍 扫描中... (会话: [bold magenta]{config.session_name}[/])",
            style="bold blue",
        )
    )

    all_tasks = scan_ppt_folders(config.input_folder)
    if not all_tasks:
        console.print(f"[bold red]❌ 未在 {config.input_folder} 中发现子文件夹。[/]")
        return None

    ppt_names = list(all_tasks.keys())
    old_session = load_session(config)
    if old_session:
        console.print("\n[bold yellow]📢 发现断点记录！[/]")
        choice = input("👉 是否继续？(y/n) [默认为 y]: ").strip().lower()
        if choice != "n":
            return old_session

    console.print("\n[bold green]📂 发现以下文档页图片任务:[/]")
    for i, name in enumerate(ppt_names):
        count = len(all_tasks[name])
        console.print(f"  [[bold cyan]{i + 1}[/]] {name} ([yellow]{count} 页[/])")

    selection = input("\n👉 选择任务 (如 1,3 | a): ").strip()
    selected_names = []
    if selection.lower() == "a":
        selected_names = ppt_names
    else:
        try:
            for idx in [int(x) for x in selection.split(",") if x.strip()]:
                if 1 <= idx <= len(ppt_names):
                    selected_names.append(ppt_names[idx - 1])
        except Exception:
            return None

    if not selected_names:
        return None

    final_config = {}
    console.print("\n⚙️  [bold]配置范围 (回车=全选):[/]")
    for name in selected_names:
        total = len(all_tasks[name])
        range_input = input(f"   📘 [{name}] (共{total}页): ").strip()
        start, end = parse_range_string(range_input, total)
        final_config[name] = {
            "images": all_tasks[name],
            "range_start": start,
            "range_end": end,
            "task_id": None,
        }

    save_session(config, final_config)
    return final_config
