# Examples

This directory can house sample receipt images that align with your canonical template for demos and evaluation. Binary assets (such as `.jpg` or `.png` scans) are intentionally excluded from version control to keep pull requests lightweight. Place your own images here locally and pair them with the JSON ground truth files when running `tools/evaluate.py`.

Run `python tools/fetch_sample_receipt.py` to download `examples/sample_receipt.jpg`, a public sample that matches the default ROI layout. Swap it out for real scans when you are ready to validate against production data.
