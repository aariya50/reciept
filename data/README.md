# Template Image Placeholder

The canonical receipt template image is not tracked in the repository to avoid committing binary assets. Place your template image in this directory (for example as `template.jpg`) before running alignment or evaluation commands.

For quick smoke tests you can run `python tools/fetch_sample_receipt.py` to download a public sample template (`data/sample_template.jpg`) that matches the default ROI configuration.

Suggested workflow:

1. Capture or scan a clean copy of the receipt layout.
2. Save the image into this folder, keeping the filename referenced by your CLI invocations (e.g., `data/template.jpg`).
3. Update `config/roi_config.json` if your template resolution or ROI coordinates change.
