from pathlib import Path

import pytest
from rich.console import Console

from docpage2md_app.config import AppConfig
from docpage2md_app.cost import (
    QWEN_VISION_DEFAULT_MAX_PIXELS,
    calculate_image_tokens,
    estimate_deepseek_chat_tokens,
    estimate_deepseek_text_tokens,
    show_cost_estimation,
    smart_resize_dimensions,
)
from docpage2md_app.deepseek_tokenizer import encode_text


def test_deepseek_tokenizer_counts_basic_text():
    assert encode_text("Hello!") == [19923, 3]
    assert estimate_deepseek_text_tokens("Hello!") == 2
    assert estimate_deepseek_chat_tokens([{"role": "user", "content": "Hello!"}]) == 5
    assert estimate_deepseek_text_tokens("群论笔记") == 4


def test_qwen_image_smart_resize_default_max_pixels():
    resized_h, resized_w, max_pixels = smart_resize_dimensions(4096, 4096)

    assert (resized_h, resized_w) == (1600, 1600)
    assert max_pixels == QWEN_VISION_DEFAULT_MAX_PIXELS


def test_qwen_image_token_count_uses_real_dimensions(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    image = tmp_path / "crop.png"
    Image.new("RGB", (100, 100), "white").save(image)

    assert calculate_image_tokens(image) == 11


def test_qwen_image_token_count_scales_tiny_images_to_minimum(tmp_path):
    pytest.importorskip("PIL")
    from PIL import Image

    image = tmp_path / "tiny.png"
    Image.new("RGB", (1, 1), "white").save(image)

    assert calculate_image_tokens(image) == 6


def test_cli_cost_table_splits_vision_and_brain_tokens_by_context_radius(tmp_path):
    tasks = {
        "sample": {
            "images": [str(tmp_path / "missing_1.png"), str(tmp_path / "missing_2.png")],
            "range_start": 0,
            "range_end": 2,
        }
    }
    small_console = Console(record=True, width=180)
    large_console = Console(record=True, width=180)

    show_cost_estimation(small_console, tasks, AppConfig(brain_context_radius=0))
    show_cost_estimation(large_console, tasks, AppConfig(brain_context_radius=5))

    small = small_console.export_text()
    large = large_console.export_text()
    for header in ("Vision输入(M)", "Vision输出(M)", "Brain输入(M)", "Brain输出(M)", "Vision费用", "Brain费用"):
        assert header in small
    assert "0.007" in small
    assert "0.023" in large
