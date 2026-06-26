from pathlib import Path

from pypdf import PdfWriter

from docpage2md_app.input_inspection import estimate_path_pages, estimate_pdf_pages


def test_estimate_pdf_pages_uses_real_pdf_reader(tmp_path: Path):
    pdf = tmp_path / "real.pdf"
    writer = PdfWriter()
    for _ in range(3):
        writer.add_blank_page(width=72, height=72)
    with pdf.open("wb") as handle:
        writer.write(handle)

    assert estimate_pdf_pages(pdf) == 3
    assert estimate_path_pages(pdf) == 3
    assert estimate_path_pages(pdf, "2-3") == 2
