import hashlib
from dataclasses import dataclass
from typing import Any


OCR_CONFUSION_SCHEMA_VERSION = 1
MAX_CONFUSION_REPLACEMENTS = 20
MAX_CONFUSION_REPLACEMENT_RATIO = 0.02

OCR_CONFUSION_REPLACEMENTS = {
    "０": "0",
    "１": "1",
    "２": "2",
    "３": "3",
    "４": "4",
    "５": "5",
    "６": "6",
    "７": "7",
    "８": "8",
    "９": "9",
    "＋": "+",
    "－": "-",
    "−": "-",
    "＝": "=",
    "＜": "<",
    "＞": ">",
    "≤": r"\le",
    "≥": r"\ge",
    "𝛼": "α",
    "𝜶": "α",
    "𝝰": "α",
    "𝞪": "α",
    "𝛽": "β",
    "𝜷": "β",
    "𝝱": "β",
    "𝞫": "β",
    "𝛾": "γ",
    "𝜸": "γ",
    "𝝲": "γ",
    "𝞬": "γ",
}


@dataclass(frozen=True)
class ConfusionAudit:
    enabled: bool
    status: str
    applied: bool
    replacement_count: int
    replacement_ratio: float
    replacements: list[dict[str, Any]]
    text_before_sha256: str | None = None
    text_after_sha256: str | None = None
    reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": OCR_CONFUSION_SCHEMA_VERSION,
            "enabled": self.enabled,
            "status": self.status,
            "applied": self.applied,
            "replacement_count": self.replacement_count,
            "replacement_ratio": self.replacement_ratio,
            "replacements": self.replacements,
            "text_before_sha256": self.text_before_sha256,
            "text_after_sha256": self.text_after_sha256,
            "reason": self.reason,
        }


def apply_ocr_confusion_fixes(
    text: str,
    *,
    enabled: bool = False,
    max_replacements: int = MAX_CONFUSION_REPLACEMENTS,
    max_ratio: float = MAX_CONFUSION_REPLACEMENT_RATIO,
) -> tuple[str, dict[str, Any]]:
    """Apply a small, reversible whitelist of OCR confusion fixes."""
    original = text or ""
    if not enabled:
        return original, ConfusionAudit(
            enabled=False,
            status="disabled",
            applied=False,
            replacement_count=0,
            replacement_ratio=0.0,
            replacements=[],
            text_before_sha256=_sha256_text(original),
            text_after_sha256=_sha256_text(original),
        ).to_dict()

    candidate = original
    replacements = []
    replacement_count = 0
    for before, after in OCR_CONFUSION_REPLACEMENTS.items():
        count = candidate.count(before)
        if not count:
            continue
        candidate = candidate.replace(before, after)
        replacement_count += count
        replacements.append(
            {
                "before": before,
                "after": after,
                "count": count,
                "before_sha256": _sha256_text(before),
                "after_sha256": _sha256_text(after),
            }
        )

    ratio = _replacement_ratio(original, replacement_count)
    if replacement_count == 0:
        return original, ConfusionAudit(
            enabled=True,
            status="no_op",
            applied=False,
            replacement_count=0,
            replacement_ratio=0.0,
            replacements=[],
            text_before_sha256=_sha256_text(original),
            text_after_sha256=_sha256_text(original),
        ).to_dict()

    if replacement_count > max_replacements or ratio > max_ratio:
        return original, ConfusionAudit(
            enabled=True,
            status="rejected_high_density",
            applied=False,
            replacement_count=replacement_count,
            replacement_ratio=ratio,
            replacements=replacements,
            text_before_sha256=_sha256_text(original),
            text_after_sha256=_sha256_text(original),
            reason="replacement_density_exceeded",
        ).to_dict()

    return candidate, ConfusionAudit(
        enabled=True,
        status="applied",
        applied=True,
        replacement_count=replacement_count,
        replacement_ratio=ratio,
        replacements=replacements,
        text_before_sha256=_sha256_text(original),
        text_after_sha256=_sha256_text(candidate),
    ).to_dict()


def _replacement_ratio(text: str, replacement_count: int) -> float:
    meaningful = [ch for ch in text if not ch.isspace()]
    if not meaningful:
        return 0.0
    return round(replacement_count / max(len(meaningful), 200), 6)


def _sha256_text(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()
