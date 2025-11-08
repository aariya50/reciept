"""Evaluate OCR extraction accuracy against labeled examples."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

from receipt_ocr.pipeline import ReceiptExtractor


def load_ground_truth(path: Path) -> Dict[str, object]:
    gt_path = path.with_suffix(".json")
    if gt_path.exists():
        return json.loads(gt_path.read_text(encoding="utf-8"))
    return {}


def evaluate_dataset(dataset: Path, extractor: ReceiptExtractor) -> Dict[str, object]:
    results: List[Dict[str, object]] = []
    totals = {"vendor": 0, "date": 0, "total": 0, "items": 0}
    correct = {key: 0 for key in totals}

    for image_path in sorted(dataset.glob("*.jpg")):
        prediction = extractor.extract_dict(image_path)
        truth = load_ground_truth(image_path)
        comparison = {"image": image_path.name, "prediction": prediction, "truth": truth}
        for key in totals:
            totals[key] += 1
            if truth.get(key) == prediction.get(key):
                correct[key] += 1
        results.append(comparison)

    accuracy = {key: (correct[key] / totals[key] if totals[key] else 0.0) for key in totals}
    return {"accuracy": accuracy, "details": results}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate receipt OCR accuracy")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    extractor = ReceiptExtractor.from_files(args.template, args.config)
    report = evaluate_dataset(args.dataset, extractor)

    payload = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":  # pragma: no cover
    main()
