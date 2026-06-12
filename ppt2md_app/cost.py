def calculate_image_tokens(image_path):
    """
    根据 Qwen3-VL 官方规则计算图像 Token:
    Token = (H_bar * W_bar) / (32 * 32) + 2
    """
    from PIL import Image

    try:
        with Image.open(image_path) as img:
            height = img.height
            width = img.width

            h_bar = round(height / 32) * 32
            w_bar = round(width / 32) * 32

            return int((h_bar * w_bar) / 1024) + 2
    except Exception:
        return 2000


def estimate_price(model_type, input_tokens, output_tokens):
    """
    根据阶梯计费估算价格，单位为元。
    """
    cost = 0.0

    if model_type == "qwen3-vl-plus":
        if input_tokens <= 32000:
            cost += (input_tokens / 1000) * 0.001
        elif input_tokens <= 128000:
            cost += (input_tokens / 1000) * 0.0015
        else:
            cost += (input_tokens / 1000) * 0.003

        if output_tokens <= 32000:
            cost += (output_tokens / 1000) * 0.01
        elif output_tokens <= 128000:
            cost += (output_tokens / 1000) * 0.015
        else:
            cost += (output_tokens / 1000) * 0.03

    elif model_type == "qwen-plus":
        if input_tokens <= 128000:
            cost += (input_tokens / 1000) * 0.0008
        elif input_tokens <= 256000:
            cost += (input_tokens / 1000) * 0.0024
        else:
            cost += (input_tokens / 1000) * 0.0048

        cost += (output_tokens / 1000) * 0.002

    return cost


def estimate_flat_price(input_tokens, output_tokens, input_price_per_million, output_price_per_million):
    if input_price_per_million is None or output_price_per_million is None:
        return None
    return (
        (input_tokens / 1_000_000) * input_price_per_million
        + (output_tokens / 1_000_000) * output_price_per_million
    )


def show_cost_estimation(console, tasks_config, config):
    from rich.table import Table

    table = Table(title="💰 任务成本预估 (仅供参考)", show_header=True, header_style="bold magenta")
    table.add_column("PPT 任务", style="cyan")
    table.add_column("页数", justify="right")
    table.add_column("预估 Token (M)", justify="right")
    table.add_column("预估费用 (元)", justify="right", style="green")

    total_cost = 0.0
    total_tokens = 0

    with console.status("[bold green]正在计算成本预估...[/]"):
        for ppt_name, task_config in tasks_config.items():
            images = task_config["images"]
            start = task_config["range_start"]
            end = task_config["range_end"]
            target_images = images[start:end]

            sample_images = target_images[:5]
            if sample_images:
                sum_tokens = sum(calculate_image_tokens(img) for img in sample_images)
                avg_img_tokens = int(sum_tokens / len(sample_images))
            else:
                avg_img_tokens = 2000

            num_slides = len(target_images)

            s1_input = avg_img_tokens + 300
            s1_output = 500
            s1_unit_cost = estimate_flat_price(
                s1_input,
                s1_output,
                config.vision_input_price_per_million,
                config.vision_output_price_per_million,
            )
            if s1_unit_cost is None:
                s1_unit_cost = estimate_price(config.model_vision, s1_input, s1_output)
            s1_cost = s1_unit_cost * num_slides
            s1_tokens = (s1_input + s1_output) * num_slides

            s2_input = 3500
            s2_output = 800
            s2_unit_cost = estimate_flat_price(
                s2_input,
                s2_output,
                config.brain_input_price_per_million,
                config.brain_output_price_per_million,
            )
            if s2_unit_cost is None:
                s2_unit_cost = estimate_price(config.model_brain, s2_input, s2_output)
            s2_cost = s2_unit_cost * num_slides
            s2_tokens = (s2_input + s2_output) * num_slides

            ppt_cost = s1_cost + s2_cost
            ppt_tokens = s1_tokens + s2_tokens

            total_cost += ppt_cost
            total_tokens += ppt_tokens

            table.add_row(
                ppt_name,
                str(num_slides),
                f"{ppt_tokens / 1000000:.2f} M",
                f"¥ {ppt_cost:.2f}",
            )

    table.add_row("总计", "", f"{total_tokens / 1000000:.2f} M", f"¥ {total_cost:.2f}", style="bold red")
    console.print(table)
    console.print(
        "[dim]"
        f"注：预估基于当前选择 Vision={config.vision_provider}:{config.model_vision}, "
        f"Brain={config.brain_provider}:{config.model_brain} 的本地价格表或自定义价格。"
        "实际计费以服务商账单为准。"
        "[/]\n"
    )
