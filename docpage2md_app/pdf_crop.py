from __future__ import annotations

import hashlib
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter  # type: ignore

from .input_inspection import compact_pages_to_ranges, estimate_pdf_pages, parse_page_selection


@dataclass(frozen=True)
class PreparedPdfUpload:
    original_path: Path
    upload_path: Path
    api_page_ranges: str | None
    physical_pdf_crop: dict | None = None
    cleanup_dir: Path | None = None

    @property
    def was_cropped(self) -> bool:
        return self.physical_pdf_crop is not None


def prepare_pdf_upload_for_page_ranges(
    source: str | Path,
    page_ranges: str | None,
    *,
    temp_root: str | Path | None = None,
) -> PreparedPdfUpload:
    """Return the local file that should be uploaded for a requested PDF page range.

    API page-range parameters still work, but for local PDFs they force the provider
    to receive the whole PDF. When a real subset is requested, this helper writes a
    temporary PDF containing only those pages and clears the API page range.
    """

    source_path = Path(source).resolve()
    requested_ranges = (page_ranges or "").strip()
    if source_path.suffix.lower() != ".pdf" or not requested_ranges:
        return PreparedPdfUpload(source_path, source_path, requested_ranges or None)

    total_pages = estimate_pdf_pages(source_path)
    if not total_pages:
        return PreparedPdfUpload(source_path, source_path, requested_ranges)
    selected_pages = parse_page_selection(requested_ranges, total_pages=total_pages)
    if selected_pages is None:
        raise ValueError("页码范围格式应类似 1-10 或 2,4-6。")
    if not selected_pages:
        raise ValueError(f"页码范围 {requested_ranges} 没有选中任何页面。")
    if selected_pages == list(range(1, total_pages + 1)):
        return PreparedPdfUpload(source_path, source_path, requested_ranges)

    reader = PdfReader(str(source_path))
    writer = PdfWriter()
    for page_no in selected_pages:
        writer.add_page(reader.pages[page_no - 1])

    temp_parent = Path(temp_root) if temp_root is not None else Path(tempfile.gettempdir())
    temp_dir = Path(tempfile.mkdtemp(prefix="docpage2md_pdf_crop_", dir=str(temp_parent)))
    digest = hashlib.sha256(f"{source_path}|{requested_ranges}|{selected_pages}".encode("utf-8")).hexdigest()[:10]
    upload_path = temp_dir / f"{_safe_stem(source_path.stem)}__pages_{digest}.pdf"
    with upload_path.open("wb") as handle:
        writer.write(handle)

    original_size = source_path.stat().st_size
    cropped_size = upload_path.stat().st_size
    audit = {
        "enabled": True,
        "strategy": "local_pdf_physical_page_crop",
        "original_path": str(source_path),
        "upload_path": str(upload_path),
        "requested_page_ranges": requested_ranges,
        "total_pages": total_pages,
        "selected_page_count": len(selected_pages),
        "selected_pages": selected_pages,
        "selected_ranges": compact_pages_to_ranges(selected_pages),
        "page_map": [
            {"uploaded_page": index, "original_page": page_no}
            for index, page_no in enumerate(selected_pages, start=1)
        ],
        "original_size_bytes": original_size,
        "cropped_size_bytes": cropped_size,
        "bytes_saved": max(0, original_size - cropped_size),
    }
    return PreparedPdfUpload(source_path, upload_path, None, audit, temp_dir)


def cleanup_prepared_pdf_upload(prepared: PreparedPdfUpload) -> None:
    if prepared.cleanup_dir:
        shutil.rmtree(prepared.cleanup_dir, ignore_errors=True)


def _safe_stem(stem: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in stem).strip("_")
    return (cleaned or "document")[:60]
