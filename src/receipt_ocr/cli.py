"""Command-line interface for the receipt OCR pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import extract_receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract structured data from receipt scans")
    parser.add_argument("--image", required=True, help="Path to the receipt image to process")
    parser.add_argument(
        "--config",
        default="config/roi_config.json",
        help="Path to the ROI configuration JSON file",
    )
    parser.add_argument(
        "--template",
        default="data/template.jpg",
        help="Path to the canonical template image",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to save the extracted JSON. Defaults to stdout",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = extract_receipt(args.image, args.template, args.config)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
