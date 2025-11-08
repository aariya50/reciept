"""Download a public sample receipt and matching template image.

This helper keeps binary assets out of version control while still making it
easy to run smoke tests locally. The download targets a sample receipt from the
Azure Form Recognizer SDK test corpus, which is openly published on GitHub.

Usage:

    python tools/fetch_sample_receipt.py \
        --template data/sample_template.jpg \
        --receipt examples/sample_receipt.jpg

Both files default to the paths above; pass ``--force`` to overwrite existing
files. The script stores the assets exactly as published (1688×3000 JPEG).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.request import urlretrieve


TEMPLATE_URL = (
    "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/"
    "main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/"
    "receipt/contoso-allinone.jpg"
)


def download(url: str, destination: Path, force: bool = False) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"Skipping existing file: {destination}")
        return

    print(f"Downloading {url}\n  -> {destination}")
    urlretrieve(url, destination)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path("data/sample_template.jpg"),
        help="Where to save the canonical template image.",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        default=Path("examples/sample_receipt.jpg"),
        help="Where to save the matching sample receipt image.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite files even if they already exist.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    download(TEMPLATE_URL, args.template, force=args.force)
    download(TEMPLATE_URL, args.receipt, force=args.force)
    print("Done.")
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main(sys.argv[1:]))
