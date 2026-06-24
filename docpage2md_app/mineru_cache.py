import hashlib
import zipfile
from pathlib import Path

from .files import write_json
from .mineru_artifacts import discover_mineru_artifacts


MINERU_CACHE_SCHEMA_VERSION = 1


def mineru_cache_root(output_folder: str | Path) -> Path:
    return Path(output_folder) / ".mineru_cache"


def cache_key_for_source(source: str | Path, *, page_ranges: str | None = None, model_version: str = "vlm") -> str:
    text = f"{Path(source).resolve() if Path(str(source)).exists() else source}|{page_ranges or ''}|{model_version}"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:24]


def task_cache_dir(output_folder: str | Path, cache_key: str) -> Path:
    return mineru_cache_root(output_folder) / cache_key


def unzip_mineru_result(zip_path: str | Path, dest_dir: str | Path) -> Path:
    target = Path(dest_dir)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            _safe_extract_member(archive, member, target)
    discover_mineru_artifacts(target)
    return target


def write_task_manifest(dest_dir: str | Path, **metadata):
    payload = {
        "schema_version": MINERU_CACHE_SCHEMA_VERSION,
        **metadata,
    }
    write_json(Path(dest_dir) / "mineru_task_manifest.json", payload)


def _safe_extract_member(archive: zipfile.ZipFile, member: zipfile.ZipInfo, target: Path):
    resolved = (target / member.filename).resolve()
    target_resolved = target.resolve()
    if target_resolved not in resolved.parents and resolved != target_resolved:
        raise ValueError(f"Unsafe zip member path: {member.filename}")
    archive.extract(member, target)
