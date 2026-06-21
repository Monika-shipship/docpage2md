import re
from dataclasses import dataclass


FIGURE_TYPE_KEYWORDS = (
    ("coordinate_plot", ("坐标图", "坐标轴", "函数曲线", "曲线", "plot", "axis", "axes", "curve")),
    ("flowchart", ("流程图", "流程", "flowchart", "process")),
    ("structure_diagram", ("结构图", "分层结构", "网络结构", "structure")),
    ("apparatus", ("装置图", "实验装置", "apparatus", "setup")),
    ("geometry", ("几何图", "三角形", "圆", "矩形", "geometry")),
    ("schematic", ("示意图", "模型图", "物理模型", "diagram", "schematic")),
)


@dataclass(frozen=True)
class FigureAnalysis:
    figure_type: str
    description: str
    labels: list[str]
    relations: list[str]
    unrecognizable: bool

    def to_block_fields(self):
        return {
            "figure_type": self.figure_type,
            "description": self.description,
            "labels": self.labels,
            "relations": self.relations,
            "unrecognizable": self.unrecognizable,
        }


def analyze_figure_description(text: str) -> FigureAnalysis:
    description = (text or "").strip()
    return FigureAnalysis(
        figure_type=_infer_figure_type(description),
        description=description,
        labels=_extract_labels(description),
        relations=_extract_relations(description),
        unrecognizable=_is_unrecognizable(description),
    )


def _infer_figure_type(text: str) -> str:
    lower = text.lower()
    for figure_type, keywords in FIGURE_TYPE_KEYWORDS:
        if any(keyword.lower() in lower for keyword in keywords):
            return figure_type
    return "unknown"


def _extract_labels(text: str) -> list[str]:
    labels = []
    for pattern in (
        r"(?:节点|标签|文字|标注|包含的文字|坐标轴名称)[:：]\s*([^\n。；;]+)",
        r"\b([A-Z][A-Za-z0-9_]{0,8})\b",
    ):
        for match in re.finditer(pattern, text):
            labels.extend(_split_label_text(match.group(1)))
    return _dedupe(labels)[:24]


def _extract_relations(text: str) -> list[str]:
    relations = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if (
            "指向" in stripped
            or "连接" in stripped
            or "箭头" in stripped
            or "连线" in stripped
            or "->" in stripped
            or "→" in stripped
        ):
            relations.append(stripped)
    return _dedupe(relations)[:16]


def _is_unrecognizable(text: str) -> bool:
    lower = text.lower()
    markers = (
        "无法识别",
        "无法确定",
        "看不清",
        "模糊",
        "遮挡",
        "不确定",
        "[?]",
        "uncertain",
        "illegible",
        "unrecognizable",
    )
    return any(marker in lower for marker in markers)


def _split_label_text(text: str) -> list[str]:
    parts = re.split(r"[,，、/；;和\s]+", text.strip())
    labels = []
    for part in parts:
        label = part.strip("：:，,。.;；()（）[]【】")
        if 1 <= len(label) <= 24:
            labels.append(label)
    return labels


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped
