from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .files import read_json


@dataclass(frozen=True)
class MinerUArtifacts:
    root: Path
    full_md: Path | None
    layout_json: Path | None
    block_list_json: Path | None
    content_list_json: Path | None
    content_list_v2_json: Path | None
    model_json: Path | None
    images_dir: Path | None

    def to_manifest(self) -> dict[str, str | None]:
        return {
            "root": str(self.root),
            "full_md": _path_str(self.full_md),
            "layout_json": _path_str(self.layout_json),
            "block_list_json": _path_str(self.block_list_json),
            "content_list_json": _path_str(self.content_list_json),
            "content_list_v2_json": _path_str(self.content_list_v2_json),
            "model_json": _path_str(self.model_json),
            "images_dir": _path_str(self.images_dir),
        }


def discover_mineru_artifacts(root: str | Path) -> MinerUArtifacts:
    artifact_root = Path(root)
    if not artifact_root.exists() or not artifact_root.is_dir():
        raise FileNotFoundError(f"MinerU artifact directory not found: {artifact_root}")

    json_files = list(artifact_root.glob("*.json"))
    content_v2 = _first_sorted(json_files, "*content_list_v2.json")
    content = _first_sorted(json_files, "*content_list.json", exclude="*content_list_v2.json")
    model = _first_sorted(json_files, "*_model.json")
    return MinerUArtifacts(
        root=artifact_root,
        full_md=_existing(artifact_root / "full.md"),
        layout_json=_existing(artifact_root / "layout.json") or _first_sorted(json_files, "*layout*.json"),
        block_list_json=_existing(artifact_root / "block_list.json"),
        content_list_json=content,
        content_list_v2_json=content_v2,
        model_json=model,
        images_dir=_existing_dir(artifact_root / "images"),
    )


def load_artifact_json(path: Path | None) -> Any:
    if path is None:
        return None
    return read_json(path)


def resolve_artifact_image(artifacts: MinerUArtifacts, img_path: str | None) -> Path | None:
    raw = str(img_path or "").strip()
    if not raw:
        return None
    candidates = []
    path = Path(raw)
    if path.is_absolute() and path.exists():
        return path
    normalized = raw.lstrip("/\\")
    candidates.append(artifacts.root / normalized)
    if artifacts.images_dir is not None:
        candidates.append(artifacts.images_dir / Path(normalized).name)
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _existing(path: Path) -> Path | None:
    return path if path.exists() and path.is_file() else None


def _existing_dir(path: Path) -> Path | None:
    return path if path.exists() and path.is_dir() else None


def _first_sorted(paths: list[Path], pattern: str, *, exclude: str | None = None) -> Path | None:
    matches = [path for path in paths if path.match(pattern)]
    if exclude:
        matches = [path for path in matches if not path.match(exclude)]
    matches.sort(key=lambda p: p.name)
    return matches[0] if matches else None


def _path_str(path: Path | None) -> str | None:
    return str(path) if path is not None else None
