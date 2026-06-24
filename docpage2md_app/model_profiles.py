from dataclasses import dataclass, replace
from typing import Dict

from .config import AppConfig


ROLE_LAYOUT_ENGINE = "layout_engine"
ROLE_PAGE_VISION = "page_vision"
ROLE_CROP_VISION = "crop_vision"
ROLE_OCR_HELPER = "ocr_helper"
ROLE_BRAIN = "brain"
ROLE_REFINER = "refiner"
ROLE_REVIEWER = "reviewer"

MODEL_PROFILE_CHEAP = "cheap"
MODEL_PROFILE_BALANCED = "balanced"
MODEL_PROFILE_ACCURATE = "accurate"
MODEL_PROFILE_MANUAL = "manual"


@dataclass(frozen=True)
class RoleBinding:
    role: str
    provider: str
    model: str
    base_url: str
    api_key_env: str
    thinking_enabled: bool = False
    json_mode: bool = False
    supports_vision: bool = False
    note: str = ""

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "api_key_env": self.api_key_env,
            "thinking_enabled": self.thinking_enabled,
            "json_mode": self.json_mode,
            "supports_vision": self.supports_vision,
            "note": self.note,
        }


@dataclass(frozen=True)
class ModelProfile:
    name: str
    roles: Dict[str, RoleBinding]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "roles": {role: binding.to_dict() for role, binding in self.roles.items()},
        }


def default_model_profiles(config: AppConfig | None = None) -> Dict[str, ModelProfile]:
    config = config or AppConfig()
    dashscope_base = config.openai_base_url
    deepseek_base = "https://api.deepseek.com"
    mineru_base = config.mineru_base_url

    def mineru_binding():
        return RoleBinding(
            role=ROLE_LAYOUT_ENGINE,
            provider="mineru",
            model="vlm",
            base_url=mineru_base,
            api_key_env=config.mineru_api_token_env,
            note="MinerU precise API, model_version=vlm.",
        )

    def vision(model: str, *, provider: str = "dashscope"):
        return RoleBinding(
            role=ROLE_PAGE_VISION,
            provider=provider,
            model=model,
            base_url=dashscope_base,
            api_key_env=config.vision_api_key_env,
            thinking_enabled=True,
            supports_vision=True,
        )

    def crop(model: str, *, provider: str = "dashscope"):
        return RoleBinding(
            role=ROLE_CROP_VISION,
            provider=provider,
            model=model,
            base_url=dashscope_base,
            api_key_env=config.vision_api_key_env,
            thinking_enabled=True,
            supports_vision=True,
        )

    def deepseek(role: str, model: str):
        return RoleBinding(
            role=role,
            provider="deepseek",
            model=model,
            base_url=deepseek_base,
            api_key_env=config.brain_api_key_env,
            thinking_enabled=True,
            json_mode=True,
        )

    def ocr():
        return RoleBinding(
            role=ROLE_OCR_HELPER,
            provider="dashscope",
            model="qwen-vl-ocr-latest",
            base_url=dashscope_base,
            api_key_env=config.vision_api_key_env,
            supports_vision=True,
            note="Optional OCR helper; not used by the default pipeline.",
        )

    return {
        MODEL_PROFILE_CHEAP: ModelProfile(
            MODEL_PROFILE_CHEAP,
            {
                ROLE_LAYOUT_ENGINE: mineru_binding(),
                ROLE_PAGE_VISION: vision("qwen3-vl-flash"),
                ROLE_CROP_VISION: crop("qwen3-vl-flash"),
                ROLE_OCR_HELPER: ocr(),
                ROLE_BRAIN: deepseek(ROLE_BRAIN, "deepseek-v4-flash"),
                ROLE_REFINER: deepseek(ROLE_REFINER, "deepseek-v4-flash"),
            },
        ),
        MODEL_PROFILE_BALANCED: ModelProfile(
            MODEL_PROFILE_BALANCED,
            {
                ROLE_LAYOUT_ENGINE: mineru_binding(),
                ROLE_PAGE_VISION: vision("qwen3-vl-plus"),
                ROLE_CROP_VISION: crop("qwen3-vl-plus"),
                ROLE_OCR_HELPER: ocr(),
                ROLE_BRAIN: deepseek(ROLE_BRAIN, "deepseek-v4-flash"),
                ROLE_REFINER: deepseek(ROLE_REFINER, "deepseek-v4-flash"),
            },
        ),
        MODEL_PROFILE_ACCURATE: ModelProfile(
            MODEL_PROFILE_ACCURATE,
            {
                ROLE_LAYOUT_ENGINE: mineru_binding(),
                ROLE_PAGE_VISION: vision("qwen3.7-plus", provider="dashscope_openai"),
                ROLE_CROP_VISION: crop("qwen3.7-plus", provider="dashscope_openai"),
                ROLE_OCR_HELPER: ocr(),
                ROLE_BRAIN: deepseek(ROLE_BRAIN, "deepseek-v4-pro"),
                ROLE_REFINER: deepseek(ROLE_REFINER, "deepseek-v4-pro"),
            },
        ),
    }


def get_model_profile(name: str, config: AppConfig | None = None) -> ModelProfile:
    profiles = default_model_profiles(config)
    return profiles.get(name) or profiles[MODEL_PROFILE_BALANCED]


def apply_model_profile(config: AppConfig, profile_name: str) -> AppConfig:
    if profile_name == MODEL_PROFILE_MANUAL:
        return replace(config, model_profile=MODEL_PROFILE_MANUAL)
    profile = get_model_profile(profile_name, config)
    page_vision = profile.roles[ROLE_PAGE_VISION]
    brain = profile.roles[ROLE_BRAIN]
    return replace(
        config,
        model_profile=profile.name,
        vision_provider=page_vision.provider,
        model_vision=page_vision.model,
        vision_base_url=page_vision.base_url,
        vision_api_key_env=page_vision.api_key_env,
        brain_provider=brain.provider,
        model_brain=brain.model,
        brain_base_url=brain.base_url,
        brain_api_key_env=brain.api_key_env,
    )
