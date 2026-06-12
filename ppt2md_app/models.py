import json
import time
import urllib.error
import urllib.request

import dashscope
from dashscope import Generation, MultiModalConversation

from .config import AppConfig
from .env import get_dashscope_api_key, get_deepseek_api_key
from .prompts import PROMPT_STAGE_1_VISION, PROMPT_STAGE_2_BRAIN


def run_stage_1_vision(img_path, slide_no, ppt_name, msg_queue, config: AppConfig):
    """
    Step 1 Worker: 调用 VL 模型提取 Raw Data。
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"image": f"file://{img_path}"},
                        {"text": PROMPT_STAGE_1_VISION},
                    ],
                }
            ]

            responses = MultiModalConversation.call(
                model=config.model_vision,
                messages=messages,
                enable_thinking=True,
                thinking_budget=config.thinking_budget_vision,
                stream=True,
                incremental_output=True,
            )

            full_content = ""
            full_reasoning = ""

            for chunk in responses:
                if chunk.status_code == 200:
                    try:
                        if not hasattr(chunk.output, "choices") or not chunk.output.choices:
                            continue

                        message = chunk.output.choices[0].message

                        r_content = None
                        if hasattr(message, "get"):
                            r_content = message.get("reasoning_content")
                        else:
                            try:
                                r_content = message.reasoning_content
                            except (AttributeError, KeyError):
                                r_content = None

                        if r_content:
                            full_reasoning += r_content

                        c_content = None
                        if hasattr(message, "get"):
                            c_content = message.get("content")
                        else:
                            try:
                                c_content = message.content
                            except (AttributeError, KeyError):
                                c_content = None

                        if c_content:
                            if isinstance(c_content, list):
                                for item in c_content:
                                    if isinstance(item, dict) and "text" in item:
                                        full_content += item["text"]
                            elif isinstance(c_content, str):
                                full_content += c_content

                    except Exception:
                        continue

                else:
                    if "AccessDenied" in str(chunk.code):
                        raise RuntimeError("AccessDenied")
                    return {
                        "success": False,
                        "slide_no": slide_no,
                        "error": f"Stream Error: {chunk.code}",
                    }

            if not full_content:
                if full_reasoning:
                    return {
                        "success": True,
                        "slide_no": slide_no,
                        "raw_text": (
                            "[Model only returned reasoning]\n\n"
                            f"Reasoning Trace:\n{full_reasoning[:500]}..."
                        ),
                    }
                return {
                    "success": False,
                    "slide_no": slide_no,
                    "error": "Empty response (Stream failed).",
                }

            return {"success": True, "slide_no": slide_no, "raw_text": full_content}

        except Exception as e:
            if "AccessDenied" in str(e):
                raise e
            if attempt == max_retries - 1:
                return {
                    "success": False,
                    "slide_no": slide_no,
                    "error": f"重试失败: {str(e)}",
                }
            time.sleep((attempt + 1) * 2)


def get_raw_content(raw_data_map, slide_no):
    """安全获取 Raw Data，并截断过长内容以节省 token。"""
    content = raw_data_map.get(slide_no, "(No Data / Out of Range)")
    if len(content) > 3000:
        return content[:3000] + "...(truncated)"
    return content


def run_stage_2_brain_parallel(slide_no, raw_data_map, config: AppConfig):
    """
    Step 2 Worker: 组装 5 页 Raw Data，并调用 Brain 模型。
    """
    filled_prompt = PROMPT_STAGE_2_BRAIN.format(
        prev_2_raw=get_raw_content(raw_data_map, slide_no - 2),
        prev_1_raw=get_raw_content(raw_data_map, slide_no - 1),
        target_raw=get_raw_content(raw_data_map, slide_no),
        next_1_raw=get_raw_content(raw_data_map, slide_no + 1),
        next_2_raw=get_raw_content(raw_data_map, slide_no + 2),
        slide_no=slide_no,
    )

    if config.brain_provider == "deepseek":
        return _run_deepseek_brain(filled_prompt, config)

    return _run_dashscope_brain(filled_prompt, config)


def _run_dashscope_brain(filled_prompt, config: AppConfig):
    try:
        responses = Generation.call(
            model=config.model_brain,
            messages=[{"role": "user", "content": filled_prompt}],
            result_format="message",
            enable_thinking=True,
            thinking_budget=config.thinking_budget_brain,
            stream=True,
            incremental_output=True,
        )

        full_reasoning = ""
        full_content = ""

        for chunk in responses:
            if chunk.status_code == 200:
                choice = chunk.output.choices[0]

                if hasattr(choice.message, "reasoning_content") and choice.message.reasoning_content:
                    full_reasoning += choice.message.reasoning_content

                if hasattr(choice.message, "content") and choice.message.content:
                    full_content += choice.message.content
            else:
                return f"Brain Error: {chunk.code} - {chunk.message}"

        if not full_content:
            return f"Error: Model generated thinking but no content. Trace: {full_reasoning[:100]}..."

        return full_content

    except Exception as e:
        return f"Brain Exception: {str(e)}"


def _run_deepseek_brain(filled_prompt, config: AppConfig):
    api_key = get_deepseek_api_key()
    if not api_key:
        return "DeepSeek Error: missing DEEPSEEK_API_KEY."

    payload = {
        "model": config.model_brain,
        "messages": [{"role": "user", "content": filled_prompt}],
        "thinking": {"type": "enabled"},
        "reasoning_effort": "high",
        "stream": True,
    }
    request = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        full_reasoning = ""
        full_content = ""
        with urllib.request.urlopen(request, timeout=900) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or line.startswith(":"):
                    continue
                if not line.startswith("data:"):
                    continue

                data = line[5:].strip()
                if data == "[DONE]":
                    break

                try:
                    event = json.loads(data)
                except json.JSONDecodeError:
                    continue

                choices = event.get("choices") or []
                if not choices:
                    continue

                delta = choices[0].get("delta") or {}
                full_reasoning += delta.get("reasoning_content") or ""
                full_content += delta.get("content") or ""

        if not full_content:
            return f"DeepSeek Error: model generated no content. Trace: {full_reasoning[:100]}..."
        return full_content

    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return f"DeepSeek HTTP Error: {e.code} {e.reason} {body[:500]}"
    except Exception as e:
        return f"DeepSeek Exception: {str(e)}"


def set_dashscope_api_key(task_key=None):
    if task_key:
        dashscope.api_key = task_key
    else:
        dashscope.api_key = get_dashscope_api_key()
