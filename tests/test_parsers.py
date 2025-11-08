from receipt_ocr import parsers


def test_parse_date_variants():
    assert parsers.parse_date("2023-09-02") == "2023-09-02"
    assert parsers.parse_date("09/05/2023") == "2023-09-05"
    assert parsers.parse_date("5-9-23") == "2023-05-09"


def test_parse_total_and_items():
    assert parsers.parse_total("Total: $45.67") == 45.67
    items_text = "Item A      1  $10.00\nItem B      2  $20.10\nInvalid line"
    items = parsers.parse_items(items_text)
    assert len(items) == 2
    assert items[0].name == "Item A"
    assert items[0].qty == 1
    assert items[0].price == 10.0


def test_parse_fields_round_trip():
    fields = {
        "vendor": "Sample Vendor\n",
        "date": "2023-09-01",
        "total": "Total: $45.67",
        "items": "Coffee      2  $10.00\nSandwich    1  $12.10",
    }
    receipt = parsers.parse_fields(fields)
    assert receipt.vendor == "Sample Vendor"
    assert receipt.date == "2023-09-01"
    assert receipt.total == 45.67
    assert len(receipt.items) == 2
