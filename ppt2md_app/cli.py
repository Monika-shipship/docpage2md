import argparse
import queue
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager
from pathlib import Path

from .config import AppConfig


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="PPT2MD-V10 (Parallel Brain & Stream Fixed)")
    parser.add_argument("-n", "--name", type=str, default="default", help="任务会话名称")
    parser.add_argument("-o", "--output", type=str, default="./markdown_output", help="输出目录路径")
    return parser.parse_args(argv)


def ensure_dependencies():
    required = [
        ("rich", "rich"),
        ("PIL", "Pillow"),
        ("dashscope", "dashscope"),
    ]
    for module_name, package_name in required:
        try:
            __import__(module_name)
        except ImportError:
            print(f"❌ 缺少依赖库 [{package_name}]。请运行: pip install {package_name}")
            return False
    return True


def build_config(args):
    return AppConfig(
        session_name=args.name,
        output_folder=str(Path(args.output).resolve()),
    )


def configure_stdio():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main(argv=None):
    configure_stdio()
    args = parse_args(argv)
    if not ensure_dependencies():
        return 1

    from rich.console import Console
    from rich.live import Live
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        MofNCompleteColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
    )

    from .cost import show_cost_estimation
    from .files import check_env, setup_logger
    from .model_settings import configure_models
    from .pipeline import process_single_ppt_task
    from .session import interactive_setup

    config = build_config(args)
    console = Console()

    final_key, msg = check_env(config)
    if not final_key:
        console.print(msg)
        return 1

    config = configure_models(console, config)
    logger, log_file_path = setup_logger(config)
    console.print(
        Panel(
            f"""[bold]V10 终极版 (Parallel Brain / Raw Context)[/]
    会话: [magenta]{config.session_name}[/] | API Key: 已设置
    -------------------------------------------------------
    Step 1 引擎: [cyan]{config.vision_provider}:{config.model_vision}[/] (并发: {config.vision_batch_workers})
    Step 2 引擎: [green]{config.brain_provider}:{config.model_brain}[/] (并发: {config.brain_batch_workers})
    -------------------------------------------------------
    输出: {config.output_folder}
    日志: {log_file_path}
    """,
            title="配置确认",
            border_style="green",
        )
    )

    tasks_config = interactive_setup(console, final_key, config)
    if not tasks_config:
        return 0

    show_cost_estimation(console, tasks_config, config)
    if input("👉 确认开始任务吗？(y/n) [默认为 y]: ").strip().lower() == "n":
        print("已取消。")
        return 0

    msg_manager = Manager()
    msg_queue = msg_manager.Queue()

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.fields[ppt_name]}", justify="right"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[status]}"),
    )

    print("\n")

    with Live(progress, console=console, refresh_per_second=10):
        for ppt_name in tasks_config:
            task_id = progress.add_task(
                "waiting...",
                total=100,
                ppt_name=ppt_name,
                status="准备中...",
            )
            tasks_config[ppt_name]["task_id"] = task_id

        with ProcessPoolExecutor(max_workers=config.max_ppt_workers) as executor:
            futures = [
                executor.submit(process_single_ppt_task, ppt_name, task_config, msg_queue, config)
                for ppt_name, task_config in tasks_config.items()
            ]

            finished_tasks = 0
            total_tasks = len(tasks_config)

            while finished_tasks < total_tasks:
                try:
                    while not msg_queue.empty():
                        msg_type, *message_args = msg_queue.get_nowait()

                        if msg_type == "init_task":
                            task_id, total = message_args
                            progress.update(task_id, total=total)
                        elif msg_type == "advance":
                            task_id, steps = message_args
                            progress.advance(task_id, steps)
                        elif msg_type == "status":
                            task_id, text = message_args
                            progress.update(task_id, status=text)
                        elif msg_type == "log":
                            logger.info(message_args[0])

                    done_count = sum(1 for future in futures if future.done())
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

    console.print(Panel("[bold green]✨ 所有双阶段思考任务处理完毕！[/]", expand=False))
    return 0
