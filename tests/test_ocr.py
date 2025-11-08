import numpy as np

from receipt_ocr import ocr


def test_crop_roi_extracts_correct_region():
    image = np.arange(100, dtype=np.uint8).reshape(10, 10)
    roi = {"x": 2, "y": 3, "w": 4, "h": 5}
    cropped = ocr.crop_roi(image, roi)
    assert cropped.shape == (5, 4)
    assert int(cropped[0, 0]) == image[3, 2]


def test_read_fields_invokes_ocr(monkeypatch):
    image = np.zeros((10, 10), dtype=np.uint8)
    cfg = {"rois": {"vendor": {"x": 0, "y": 0, "w": 5, "h": 5, "psm": 7, "preprocess": "adaptive"}}}

    called = {}

    def fake_ocr(img, psm=6, config=None):
        called["psm"] = psm
        return "Sample"

    monkeypatch.setattr(ocr, "ocr_image", fake_ocr)
    results = ocr.read_fields(image, cfg)
    assert results["vendor"] == "Sample"
    assert called["psm"] == 7
