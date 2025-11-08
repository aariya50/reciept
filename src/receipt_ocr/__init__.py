"""Receipt OCR package exposing the end-to-end extraction pipeline."""

from .pipeline import ReceiptExtractor, extract_receipt

__all__ = ["ReceiptExtractor", "extract_receipt"]
