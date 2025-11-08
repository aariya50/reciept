from pathlib import Path

import numpy as np

from receipt_ocr import pipeline


def test_receipt_extractor_uses_alignment_and_parsers(monkeypatch):
    roi_cfg = {
        "canvas": {"width": 10, "height": 10},
        "rois": {"vendor": {"x": 0, "y": 0, "w": 5, "h": 5}},
    }
    extractor = pipeline.ReceiptExtractor(template_path=Path("data/template.jpg"), roi_config=roi_cfg)

    def fake_align(image_path, template_path, output_size, max_features=2000, min_matches=10):
        class Result:
            warped = np.zeros((10, 10), dtype=np.uint8)
        return Result()

    def fake_read_fields(image, cfg):
        return {"vendor": "Mock Vendor", "date": "", "total": "", "items": ""}

    def fake_parse_fields(fields):
        class Dummy:
            vendor = fields["vendor"]
            date = ""
            total = 0.0
            items = []
        return Dummy()

    monkeypatch.setattr(pipeline.alignment, "align_image", fake_align)
    monkeypatch.setattr(pipeline.ocr, "read_fields", fake_read_fields)
    monkeypatch.setattr(pipeline.parsers, "parse_fields", fake_parse_fields)

    receipt = extractor.extract("dummy.jpg")
    assert receipt.vendor == "Mock Vendor"
