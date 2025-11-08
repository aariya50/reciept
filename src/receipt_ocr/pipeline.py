"""End-to-end receipt OCR pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import numpy as np

from . import alignment, ocr, parsers


@dataclass
class ReceiptExtractor:
    template_path: Path
    roi_config: Dict[str, object]

    @classmethod
    def from_files(cls, template_path: str | Path, roi_config_path: str | Path) -> "ReceiptExtractor":
        roi_cfg = ocr.load_roi_config(roi_config_path)
        return cls(template_path=Path(template_path), roi_config=roi_cfg)

    def _align(self, image_path: str | Path) -> np.ndarray:
        size = ocr.canonical_size(self.roi_config)
        if not all(size):
            raise ValueError("ROI configuration must define canvas width and height")
        result = alignment.align_image(str(image_path), str(self.template_path), size)
        return result.warped

    def _ocr(self, warped: np.ndarray) -> Dict[str, str]:
        return ocr.read_fields(warped, self.roi_config)

    def extract(self, image_path: str | Path) -> parsers.ParsedReceipt:
        warped = self._align(image_path)
        raw_fields = self._ocr(warped)
        return parsers.parse_fields(raw_fields)

    def extract_dict(self, image_path: str | Path) -> Dict[str, object]:
        return parsers.asdict(self.extract(image_path))


def extract_receipt(
    image_path: str | Path,
    template_path: str | Path,
    roi_config_path: str | Path,
) -> Dict[str, object]:
    extractor = ReceiptExtractor.from_files(template_path, roi_config_path)
    return extractor.extract_dict(image_path)


__all__ = ["ReceiptExtractor", "extract_receipt"]
