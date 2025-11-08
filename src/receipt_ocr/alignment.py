"""Image alignment utilities using ORB features and homography estimation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

try:
    import cv2
except ImportError as exc:  # pragma: no cover - exercised in environments without OpenCV libs
    cv2 = None  # type: ignore
    _cv2_import_error = exc
else:
    _cv2_import_error = None

import numpy as np


def _ensure_cv2() -> None:
    if cv2 is None:  # pragma: no cover - depends on system packages
        raise ImportError(
            "OpenCV is required for alignment but could not be imported"
        ) from _cv2_import_error


@dataclass
class AlignmentResult:
    """Container returned by :func:`align_image`."""

    homography: np.ndarray
    warped: np.ndarray
    matches: list


def load_grayscale_template(path: str) -> np.ndarray:
    _ensure_cv2()
    """Load a template image in grayscale."""

    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template image not found at {path}")
    return template


def _detect_features(image: np.ndarray, max_features: int) -> Tuple[list, np.ndarray]:
    _ensure_cv2()
    orb = cv2.ORB_create(nfeatures=max_features)
    keypoints, descriptors = orb.detectAndCompute(image, None)
    if descriptors is None or len(keypoints) == 0:
        raise ValueError("Unable to detect features in image for alignment")
    return keypoints, descriptors


def align_image(
    image_path: str,
    template_path: str,
    output_size: Tuple[int, int],
    max_features: int = 2000,
    min_matches: int = 10,
) -> AlignmentResult:
    """Align ``image_path`` with ``template_path`` returning the warped image."""

    template = load_grayscale_template(template_path)
    _ensure_cv2()
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Input image not found at {image_path}")

    tpl_kp, tpl_desc = _detect_features(template, max_features)
    img_kp, img_desc = _detect_features(image, max_features)

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    raw_matches = matcher.match(img_desc, tpl_desc)
    if not raw_matches:
        raise ValueError("No matches found between input image and template")

    matches = sorted(raw_matches, key=lambda m: m.distance)[: max(min_matches * 5, 50)]
    if len(matches) < min_matches:
        raise ValueError(
            f"Insufficient matches for homography: required {min_matches}, got {len(matches)}"
        )

    src_pts = np.float32([img_kp[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([tpl_kp[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if homography is None:
        raise ValueError("Homography estimation failed")

    width, height = output_size
    warped = cv2.warpPerspective(image, homography, (width, height))
    return AlignmentResult(homography=homography, warped=warped, matches=matches)


__all__ = ["AlignmentResult", "align_image", "load_grayscale_template"]
