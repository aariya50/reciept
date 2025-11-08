"""OCR utilities for extracting receipt fields from aligned images."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

try:
    import cv2
except ImportError as exc:  # pragma: no cover - depends on system packages
    cv2 = None  # type: ignore
    _cv2_import_error = exc
else:
    _cv2_import_error = None

import numpy as np
import pytesseract


def load_roi_config(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def crop_roi(image: np.ndarray, roi: Dict[str, Any]) -> np.ndarray:
    x, y = int(roi["x"]), int(roi["y"])
    w, h = int(roi["w"]), int(roi["h"])
    return image[y : y + h, x : x + w]


def preprocess_roi(image: np.ndarray, method: str | None = None) -> np.ndarray:
    if image.ndim == 3:
        if cv2 is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.mean(axis=2).astype(np.uint8)
    else:
        gray = image

    if cv2 is None:
        threshold = gray.mean()
        binary = (gray > threshold).astype(np.uint8) * 255
        return binary

    if method == "adaptive":
        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            5,
        )
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def ocr_image(image: np.ndarray, psm: int = 6, config: Iterable[str] | None = None) -> str:
    cfg_parts = [f"--psm {psm}"]
    if config:
        cfg_parts.extend(config)
    text = pytesseract.image_to_string(image, config=" ".join(cfg_parts))
    return text.strip()


def read_fields(warped_img: np.ndarray, roi_cfg: Dict[str, Any]) -> Dict[str, str]:
    rois = roi_cfg.get("rois", {})
    results: Dict[str, str] = {}
    for field, roi in rois.items():
        cropped = crop_roi(warped_img, roi)
        processed = preprocess_roi(cropped, roi.get("preprocess"))
        psm = int(roi.get("psm", 6))
        text = ocr_image(processed, psm=psm)
        results[field] = text
    return results


def canonical_size(roi_cfg: Dict[str, Any]) -> Tuple[int, int]:
    canvas = roi_cfg.get("canvas", {})
    return int(canvas.get("width", 0)), int(canvas.get("height", 0))


__all__ = [
    "load_roi_config",
    "crop_roi",
    "preprocess_roi",
    "ocr_image",
    "read_fields",
    "canonical_size",
]
