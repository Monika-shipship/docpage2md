import json
from dataclasses import replace
from typing import Dict, Optional

from rich.table import Table

from .config import AppConfig
from .env import get_deepseek_api_key
from .model_catalog import (
    ROLE_BRAIN,
    ROLE_VISION,
    ModelPrice,
    ModelSpec,
    get_default_catalog,
    models_for_role,
    price_label,
    refresh_catalog_best_effort,
)


def configure_models(console, config: AppConfig):
    console.print("[dim]正在刷新可用模型价格（DeepSeek 官方页为尽力刷新，失败会使用本地表）...[/]")
    catalog = refresh_catalog_best_effort(get_default_catalog())
    saved = load_model_settings(config)
    if saved:
        saved_config = apply_model_settings(config, saved)
        console.print(
            "[bold cyan]模型配置[/]: "
            f"Vision={saved_config.model_vision} | "
            f"Brain={saved_config.brain_provider}:{saved_config.model_brain}"
        )
        choice = input("👉 是否沿用上次模型配置？(y/n) [默认为 y]: ").strip().lower()
        if choice != "n":
            return saved_config

    vision_config = choose_model(
        console=console,
        config=config,
        catalog=catalog,
        role=ROLE_VISION,
        title="Step 1 视觉模型",
        default_provider=config.vision_provider,
        default_model=config.model_vision,
    )
    final_config = choose_model(
        console=console,
        config=vision_config,
        catalog=catalog,
        role=ROLE_BRAIN,
        title="Step 2 Brain 模型",
        default_provider="deepseek" if get_deepseek_api_key() else config.brain_provider,
        default_model="deepseek-v4-flash" if get_deepseek_api_key() else config.model_brain,
    )

    if final_config.brain_provider == "deepseek" and not get_deepseek_api_key():
        console.print("[bold yellow]未检测到 DEEPSEEK_API_KEY，DeepSeek Brain 会失败。[/]")
        fallback = input("👉 改用 qwen-plus 吗？(y/n) [默认为 y]: ").strip().lower()
        if fallback != "n":
            final_config = replace(
                final_config,
                brain_provider="dashscope",
                model_brain="qwen-plus",
                brain_input_price_per_million=None,
                brain_output_price_per_million=None,
            )

    save_model_settings(config, final_config)
    return final_config


def choose_model(console, config, catalog, role, title, default_provider, default_model):
    specs = list(models_for_role(catalog, role))
    default_index = _find_default_index(specs, default_provider, default_model)

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("#", justify="right")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Price")
    table.add_column("Note")

    for i, spec in enumerate(specs, start=1):
        marker = " *" if i == default_index else ""
        table.add_row(
            f"{i}{marker}",
            spec.provider,
            spec.display_name,
            price_label(spec),
            spec.note or "",
        )
    table.add_row("c", "custom", "自定义模型", "可手动填价格", "适合官方新模型还没进内置目录时使用")
    console.print(table)

    selected = input(f"👉 选择 {title} [默认 {default_index}]: ").strip().lower()
    if not selected:
        selected = str(default_index)

    if selected == "c":
        return _custom_model_config(config, role)

    try:
        index = int(selected)
    except ValueError:
        index = default_index

    if not 1 <= index <= len(specs):
        index = default_index

    return _apply_spec(config, role, specs[index - 1])


def load_model_settings(config: AppConfig):
    if not config.model_settings_path.exists():
        return None
    try:
        with config.model_settings_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_model_settings(base_config: AppConfig, selected_config: AppConfig):
    base_config.log_path.mkdir(parents=True, exist_ok=True)
    data = {
        "vision_provider": selected_config.vision_provider,
        "model_vision": selected_config.model_vision,
        "vision_input_price_per_million": selected_config.vision_input_price_per_million,
        "vision_output_price_per_million": selected_config.vision_output_price_per_million,
        "brain_provider": selected_config.brain_provider,
        "model_brain": selected_config.model_brain,
        "brain_input_price_per_million": selected_config.brain_input_price_per_million,
        "brain_output_price_per_million": selected_config.brain_output_price_per_million,
    }
    with base_config.model_settings_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def apply_model_settings(config: AppConfig, settings: Dict):
    return replace(
        config,
        vision_provider=settings.get("vision_provider", config.vision_provider),
        model_vision=settings.get("model_vision", config.model_vision),
        vision_input_price_per_million=settings.get("vision_input_price_per_million"),
        vision_output_price_per_million=settings.get("vision_output_price_per_million"),
        brain_provider=settings.get("brain_provider", config.brain_provider),
        model_brain=settings.get("model_brain", config.model_brain),
        brain_input_price_per_million=settings.get("brain_input_price_per_million"),
        brain_output_price_per_million=settings.get("brain_output_price_per_million"),
    )


def _find_default_index(specs, provider, model_id):
    for i, spec in enumerate(specs, start=1):
        if spec.provider == provider and spec.model_id == model_id:
            return i
    return 1


def _apply_spec(config, role, spec: ModelSpec):
    if role == ROLE_VISION:
        return replace(
            config,
            vision_provider=spec.provider,
            model_vision=spec.model_id,
            vision_input_price_per_million=spec.price.input_per_million,
            vision_output_price_per_million=spec.price.output_per_million,
        )

    return replace(
        config,
        brain_provider=spec.provider,
        model_brain=spec.model_id,
        brain_input_price_per_million=spec.price.input_per_million,
        brain_output_price_per_million=spec.price.output_per_million,
    )


def _custom_model_config(config, role):
    provider_default = "dashscope" if role == ROLE_VISION else "deepseek"
    provider = input(f"   Provider ({provider_default}/dashscope/deepseek): ").strip().lower()
    if not provider:
        provider = provider_default
    if role == ROLE_VISION and provider != "dashscope":
        print("   当前 Vision 阶段只支持 dashscope，已自动改为 dashscope。")
        provider = "dashscope"
    model_id = input("   模型 ID: ").strip()
    if not model_id:
        model_id = config.model_vision if role == ROLE_VISION else config.model_brain

    input_price = _read_optional_float("   输入价格 元/百万 tokens (未知可回车): ")
    output_price = _read_optional_float("   输出价格 元/百万 tokens (未知可回车): ")

    if role == ROLE_VISION:
        return replace(
            config,
            vision_provider=provider,
            model_vision=model_id,
            vision_input_price_per_million=input_price,
            vision_output_price_per_million=output_price,
        )

    return replace(
        config,
        brain_provider=provider,
        model_brain=model_id,
        brain_input_price_per_million=input_price,
        brain_output_price_per_million=output_price,
    )


def _read_optional_float(prompt):
    raw = input(prompt).strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def get_configured_price(config: AppConfig, role: str):
    if role == ROLE_VISION:
        return ModelPrice(
            input_per_million=config.vision_input_price_per_million,
            output_per_million=config.vision_output_price_per_million,
        )
    return ModelPrice(
        input_per_million=config.brain_input_price_per_million,
        output_per_million=config.brain_output_price_per_million,
    )
