from dataclasses import dataclass
import re
from typing import Dict, Iterable, Optional, Tuple
import urllib.request


ROLE_VISION = "vision"
ROLE_BRAIN = "brain"


@dataclass(frozen=True)
class ModelPrice:
    input_per_million: Optional[float] = None
    output_per_million: Optional[float] = None
    cached_input_per_million: Optional[float] = None
    currency: str = "CNY"
    source: str = "local"
    note: str = ""


@dataclass(frozen=True)
class ModelSpec:
    provider: str
    model_id: str
    display_name: str
    roles: Tuple[str, ...]
    supports_vision: bool
    supports_thinking: bool
    price: ModelPrice
    context_tokens: Optional[int] = None
    max_output_tokens: Optional[int] = None
    rpm: Optional[int] = None
    tpm: Optional[int] = None
    note: str = ""

    @property
    def key(self):
        return make_model_key(self.provider, self.model_id)


def make_model_key(provider, model_id):
    return f"{provider}:{model_id}"


def get_default_catalog():
    specs = [
        ModelSpec(
            provider="dashscope",
            model_id="qwen3-vl-plus",
            display_name="Qwen3-VL-Plus",
            roles=(ROLE_VISION,),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(1.0, 10.0, 0.2, source="百炼控制台粘贴文本"),
            context_tokens=256_000,
            max_output_tokens=32_000,
            rpm=3000,
            tpm=5_000_000,
            note="当前默认视觉模型，适合 OCR/图形分析。",
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3-vl-flash-2026-01-22",
            display_name="Qwen3-VL-Flash",
            roles=(ROLE_VISION,),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(0.15, 1.5, 0.03, source="百炼控制台粘贴文本"),
            context_tokens=256_000,
            max_output_tokens=32_000,
            rpm=3000,
            tpm=5_000_000,
            note="便宜快速；控制台文本提示将于 2026-09-08 下线。",
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.7-plus",
            display_name="Qwen3.7-Plus",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(2.0, 8.0, 0.4, source="百炼控制台粘贴文本", note="控制台显示有限时折扣，估算按原价保守计算。"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=5_000_000,
            note="多模态智能体基座，精度和价格折中。",
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.7-max-2026-06-08",
            display_name="Qwen3.7-Max 2026-06-08",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(12.0, 36.0, 2.4, source="百炼控制台粘贴文本"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=600,
            tpm=1_000_000,
            note="最高档多模态快照；成本明显更高。",
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.7-max",
            display_name="Qwen3.7-Max",
            roles=(ROLE_BRAIN,),
            supports_vision=False,
            supports_thinking=True,
            price=ModelPrice(12.0, 36.0, 2.4, source="百炼控制台粘贴文本", note="控制台显示有限时折扣，估算按原价保守计算。"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=5_000_000,
            note="控制台文本称当前开放纯文本能力，适合作为 Brain。",
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.6-plus",
            display_name="Qwen3.6-Plus",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(2.0, 12.0, source="百炼控制台粘贴文本"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=5_000_000,
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.6-flash",
            display_name="Qwen3.6-Flash",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(1.2, 7.2, source="百炼控制台粘贴文本"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=10_000_000,
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.5-plus",
            display_name="Qwen3.5-Plus",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(0.8, 4.8, source="百炼控制台粘贴文本"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=5_000_000,
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen3.5-flash",
            display_name="Qwen3.5-Flash",
            roles=(ROLE_VISION, ROLE_BRAIN),
            supports_vision=True,
            supports_thinking=True,
            price=ModelPrice(0.2, 2.0, source="百炼控制台粘贴文本"),
            context_tokens=1_000_000,
            max_output_tokens=64_000,
            rpm=30_000,
            tpm=10_000_000,
        ),
        ModelSpec(
            provider="dashscope",
            model_id="qwen-plus",
            display_name="Qwen-Plus",
            roles=(ROLE_BRAIN,),
            supports_vision=False,
            supports_thinking=True,
            price=ModelPrice(0.8, 2.0, source="README 原有估算"),
            note="原默认 Brain 模型，作为无 DeepSeek Key 时的稳妥回退。",
        ),
        ModelSpec(
            provider="deepseek",
            model_id="deepseek-v4-flash",
            display_name="DeepSeek V4 Flash",
            roles=(ROLE_BRAIN,),
            supports_vision=False,
            supports_thinking=True,
            price=ModelPrice(1.0, 2.0, 0.02, source="DeepSeek 官方价格页"),
            context_tokens=1_000_000,
            max_output_tokens=384_000,
            rpm=2500,
            note="便宜、并发高；推荐作为 Brain。",
        ),
        ModelSpec(
            provider="deepseek",
            model_id="deepseek-v4-pro",
            display_name="DeepSeek V4 Pro",
            roles=(ROLE_BRAIN,),
            supports_vision=False,
            supports_thinking=True,
            price=ModelPrice(3.0, 6.0, 0.025, source="DeepSeek 官方价格页"),
            context_tokens=1_000_000,
            max_output_tokens=384_000,
            rpm=500,
            note="更强但更贵，适合高质量重组。",
        ),
    ]
    return {spec.key: spec for spec in specs}


def refresh_catalog_best_effort(catalog):
    refreshed = dict(catalog)
    try:
        refreshed.update(_fetch_deepseek_pricing())
    except Exception:
        pass
    return refreshed


def _fetch_deepseek_pricing():
    url = "https://api-docs.deepseek.com/zh-cn/quick_start/pricing"
    with urllib.request.urlopen(url, timeout=5) as response:
        html = response.read().decode("utf-8", errors="replace")

    hit_prices = re.search(r"缓存命中[^0-9]*(0\.\d+)\s*元\s*(0\.\d+)\s*元", html)
    miss_prices = re.search(r"缓存未命中[^0-9]*(\d+(?:\.\d+)?)\s*元\s*(\d+(?:\.\d+)?)\s*元", html)
    output_prices = re.search(r"tokens输出[^0-9]*(\d+(?:\.\d+)?)\s*元\s*(\d+(?:\.\d+)?)\s*元", html)
    concurrency = re.search(r"并发限制(?:\(\d+\))?[^0-9]*(\d+)\s*(\d+)", html)

    if not (hit_prices and miss_prices and output_prices):
        return {}

    flash = _deepseek_spec(
        model_id="deepseek-v4-flash",
        display_name="DeepSeek V4 Flash",
        input_price=float(miss_prices.group(1)),
        output_price=float(output_prices.group(1)),
        cached_price=float(hit_prices.group(1)),
        rpm=int(concurrency.group(1)) if concurrency else 2500,
    )
    pro = _deepseek_spec(
        model_id="deepseek-v4-pro",
        display_name="DeepSeek V4 Pro",
        input_price=float(miss_prices.group(2)),
        output_price=float(output_prices.group(2)),
        cached_price=float(hit_prices.group(2)),
        rpm=int(concurrency.group(2)) if concurrency else 500,
    )
    return {flash.key: flash, pro.key: pro}


def _deepseek_spec(model_id, display_name, input_price, output_price, cached_price, rpm):
    return ModelSpec(
        provider="deepseek",
        model_id=model_id,
        display_name=display_name,
        roles=(ROLE_BRAIN,),
        supports_vision=False,
        supports_thinking=True,
        price=ModelPrice(
            input_per_million=input_price,
            output_per_million=output_price,
            cached_input_per_million=cached_price,
            source="DeepSeek 官方价格页（启动时刷新）",
        ),
        context_tokens=1_000_000,
        max_output_tokens=384_000,
        rpm=rpm,
    )


def models_for_role(catalog: Dict[str, ModelSpec], role: str) -> Iterable[ModelSpec]:
    return [spec for spec in catalog.values() if role in spec.roles]


def get_model(catalog: Dict[str, ModelSpec], provider: str, model_id: str) -> Optional[ModelSpec]:
    return catalog.get(make_model_key(provider, model_id))


def price_label(spec: ModelSpec):
    price = spec.price
    if price.input_per_million is None or price.output_per_million is None:
        return "价格未知"
    return f"¥{price.input_per_million:g}/M in, ¥{price.output_per_million:g}/M out"
