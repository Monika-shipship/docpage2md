from docpage2md_app.ir import build_page_ir
from docpage2md_app.provenance import build_page_provenance, merge_provenance_summaries
from docpage2md_app.refiner import refine_page_ir


def test_build_page_provenance_tracks_origins_and_generated_descriptions():
    page_ir = build_page_ir("标题:\n\n### Figure Analysis\n左侧是 A。", 1)

    provenance = build_page_provenance(page_ir)

    assert provenance["schema_version"] == 3
    assert [entry["origin"] for entry in provenance["entries"]] == [
        "renderer_template",
        "vision_ocr",
        "vision_description",
    ]
    assert provenance["entries"][0]["type"] == "renderer_template"
    assert provenance["entries"][0]["markdown"] == "# Slide 1"
    assert provenance["entries"][2]["generated_description"] is True
    assert provenance["summary"]["generated_description_count"] == 1
    assert provenance["summary"]["renderer_template_count"] == 1
    assert provenance["summary"]["origin_counts"]["renderer_template"] == 1


def test_page_provenance_tracks_visual_evidence():
    page_ir = build_page_ir("### Figure Analysis\n左侧是 A。", 4)
    page_ir["page_image_ref"] = "assets/pages/page-4.png"
    page_ir["blocks"][0]["page_image_ref"] = "assets/pages/page-4.png"
    page_ir["blocks"][0]["crop_ref"] = "assets/pages/page-4.png"
    page_ir["blocks"][0]["crop_ref_is_page"] = True

    provenance = build_page_provenance(page_ir)

    entry = provenance["entries"][1]
    assert entry["page_image_ref"] == "assets/pages/page-4.png"
    assert entry["crop_ref"] == "assets/pages/page-4.png"
    assert entry["crop_ref_is_page"] is True
    assert provenance["summary"]["visual_evidence_count"] == 1


def test_merge_provenance_summaries_counts_refiner_ops():
    refined = refine_page_ir(build_page_ir("### Formula\n$$\nE = mc^2\n$$", 2), slide_no=2).page_ir
    provenance = build_page_provenance(refined)

    merged = merge_provenance_summaries([{"provenance": provenance}])

    assert merged["origin_counts"]["refiner_op"] == 1
    assert merged["origin_counts"]["renderer_template"] == 1
    assert merged["refiner_op_count"] == 1
    assert merged["type_counts"]["formula_block"] == 1
    assert merged["type_counts"]["renderer_template"] == 1


def test_formula_provenance_records_latex_warning_count():
    page_ir = build_page_ir("### Formula\n\\frac a}{b", 3)
    provenance = build_page_provenance(page_ir)

    entry = next(entry for entry in provenance["entries"] if entry["type"] == "formula_block")
    assert entry["type"] == "formula_block"
    assert entry["formula_warning_count"] == 1
    assert entry["latex_sha256"]
