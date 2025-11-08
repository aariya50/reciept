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

1. Install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

2. Capture a high-resolution template image (e.g., `data/template.jpg`) by placing a blank sample receipt on a flat surface, ensuring even lighting. Store the file in the `data/` directory—this repository does not ship binary assets by default. Align all subsequent receipts in a similar orientation when scanning or photographing.

   Similarly, supply your own receipt scans for evaluation in `examples/`; only lightweight JSON annotations are tracked in Git to
   avoid binary file handling issues when opening pull requests.

3. Tune ROIs in `config/roi_config.json` by opening the template in an image editor and measuring the pixel coordinates for each field. Update the JSON file with the `x`, `y`, `w`, and `h` values as well as field-specific Tesseract page segmentation modes (`psm`).

4. Run the pipeline on a receipt:

   ```bash
   python -m receipt_ocr.cli --image path/to/scan.jpg --config config/roi_config.json --template data/template.jpg --output receipt.json
   ```

   The CLI prints or saves the extracted JSON containing `vendor`, `date`, `total`, and an array of `items` with `name`, `qty`, and `price` fields.

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
