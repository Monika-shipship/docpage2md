from pathlib import Path

from pypdf import PdfReader, PdfWriter

from docpage2md_app.pdf_crop import cleanup_prepared_pdf_upload, prepare_pdf_upload_for_page_ranges


def _write_pdf(path: Path, pages: int) -> None:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=72, height=72)
    with path.open("wb") as handle:
        writer.write(handle)


def test_prepare_pdf_upload_physically_crops_selected_pages(tmp_path):
    source = tmp_path / "notes.pdf"
    _write_pdf(source, 5)

    prepared = prepare_pdf_upload_for_page_ranges(source, "2,4-5", temp_root=tmp_path)
    try:
        assert prepared.was_cropped is True
        assert prepared.upload_path != source
        assert prepared.api_page_ranges is None
        assert len(PdfReader(str(prepared.upload_path)).pages) == 3
        assert prepared.physical_pdf_crop
        assert prepared.physical_pdf_crop["selected_pages"] == [2, 4, 5]
        assert prepared.physical_pdf_crop["page_map"] == [
            {"uploaded_page": 1, "original_page": 2},
            {"uploaded_page": 2, "original_page": 4},
            {"uploaded_page": 3, "original_page": 5},
        ]
    finally:
        cleanup_prepared_pdf_upload(prepared)

    assert not prepared.upload_path.exists()


def test_prepare_pdf_upload_keeps_original_when_range_is_all_pages(tmp_path):
    source = tmp_path / "notes.pdf"
    _write_pdf(source, 3)

    prepared = prepare_pdf_upload_for_page_ranges(source, "1-3", temp_root=tmp_path)

    assert prepared.was_cropped is False
    assert prepared.upload_path == source
    assert prepared.api_page_ranges == "1-3"
