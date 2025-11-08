# Receipt OCR

This project provides an end-to-end pipeline that aligns scanned receipts to a canonical template, extracts text from predefined regions of interest (ROIs) using Tesseract OCR, and parses the text into structured JSON.

## Project layout

```
.
├── config/roi_config.json   # Canvas size and ROI definitions
├── data/                    # Place the canonical template used for alignment
├── examples/                # Ground-truth JSON and (locally supplied) sample receipts
├── notebooks/               # Analysis notebooks (e.g., evaluation)
├── src/receipt_ocr/         # Python package implementation
├── tests/                   # Unit and integration tests
└── tools/                   # Utility scripts such as evaluation
```

## Getting started

1. Install system dependencies (required for OpenCV and the Tesseract CLI):

   ```bash
   sudo apt-get update
   sudo apt-get install -y libgl1 tesseract-ocr
   ```

2. Install Python dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. Capture a high-resolution template image (e.g., `data/template.jpg`) by placing a blank sample receipt on a flat surface, ensuring even lighting. Store the file in the `data/` directory—this repository does not ship binary assets by default. Align all subsequent receipts in a similar orientation when scanning or photographing.

   Similarly, supply your own receipt scans for evaluation in `examples/`; only lightweight JSON annotations are tracked in Git to
   avoid binary file handling issues when opening pull requests.

4. Tune ROIs in `config/roi_config.json` by opening the template in an image editor and measuring the pixel coordinates for each field. Update the JSON file with the `x`, `y`, `w`, and `h` values as well as field-specific Tesseract page segmentation modes (`psm`).

5. Run the pipeline on a receipt:

   ```bash
   python -m receipt_ocr.cli --image path/to/scan.jpg --config config/roi_config.json --template data/template.jpg --output receipt.json
   ```

   The CLI prints or saves the extracted JSON containing `vendor`, `date`, `total`, and an array of `items` with `name`, `qty`, and `price` fields.

### Quick smoke test (downloads required)

A helper script downloads an openly published sample receipt from the [Azure Form Recognizer SDK test corpus](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt). This keeps the Git history binary-free while still offering a reproducible demo.

```bash
python tools/fetch_sample_receipt.py \
  --template data/sample_template.jpg \
  --receipt examples/sample_receipt.jpg

python -m receipt_ocr.cli \
  --image examples/sample_receipt.jpg \
  --config config/roi_config.json \
  --template data/sample_template.jpg \
  --output sample_receipt.json
```

The helper downloads the same image for both template and receipt inputs so the default ORB-based alignment succeeds out of the box. Replace these files with your own scans when calibrating ROIs for production usage.

> **Note:** The default `config/roi_config.json` is calibrated for the downloaded Contoso Cafe sample (native resolution 1688×3000). If you swap in a differently sized template, update the canvas dimensions and ROI coordinates accordingly.

## Evaluation

Use the evaluation script to score OCR accuracy on a held-out dataset (after placing your template image in `data/` and local
receipt scans in `examples/`):

```bash
python tools/evaluate.py --dataset examples/ --config config/roi_config.json --template data/template.jpg
```

The script aggregates field-wise accuracy, highlights misreads, and outputs a summary report. For exploratory analysis or visualization, create notebooks in `notebooks/` such as `notebooks/evaluate.ipynb` to inspect failure cases and tune ROIs.

## Testing

Tests mock OCR calls to keep results deterministic. Run them with:

```bash
pytest
```

## Contributing

Contributions are welcome! Please include updates to documentation, configuration, and tests when introducing new ROIs or changing parsing logic.
