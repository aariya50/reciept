"""Text parsers that clean OCR output into structured receipt data."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import dateutil.parser


VENDOR_RE = re.compile(r"[^A-Z0-9 &'-]+", re.IGNORECASE)
DATE_RE = re.compile(r"(\d{1,2})[\-/](\d{1,2})[\-/](\d{2,4})")
TOTAL_RE = re.compile(r"([\d,.]+)")
ITEM_LINE_RE = re.compile(
    r"^(?P<name>.*?)\s+(?P<qty>\d+(?:\.\d+)?)\s+(?P<price>\$?\d+[\.,]\d{2})$"
)


@dataclass
class Item:
    name: str
    qty: float
    price: float


@dataclass
class ParsedReceipt:
    vendor: str
    date: str
    total: float
    items: List[Item]


def clean_vendor(text: str) -> str:
    text = text.strip()
    text = VENDOR_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(text: str) -> Optional[str]:
    text = text.strip()
    if not text:
        return None

    try:
        dt = dateutil.parser.parse(text, dayfirst=False, fuzzy=True)
        return dt.date().isoformat()
    except (ValueError, OverflowError, TypeError):
        pass

    match = DATE_RE.search(text)
    if not match:
        return None

    first, second, year = match.groups()
    month = int(first)
    day = int(second)
    if month > 12 and day <= 12:
        month, day = day, month
    if len(year) == 2:
        year = f"20{year}" if int(year) < 50 else f"19{year}"
    dt = datetime(int(year), month, day)
    return dt.date().isoformat()


def parse_total(text: str) -> Optional[float]:
    match = TOTAL_RE.search(text)
    if not match:
        return None
    cleaned = match.group(1).replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_items(text: str) -> List[Item]:
    items: List[Item] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = ITEM_LINE_RE.match(line)
        if not match:
            continue
        price = float(match.group("price").replace("$", "").replace(",", ""))
        qty = float(match.group("qty"))
        name = match.group("name").strip()
        items.append(Item(name=name, qty=qty, price=price))
    return items


def parse_fields(fields: Dict[str, str]) -> ParsedReceipt:
    vendor = clean_vendor(fields.get("vendor", ""))
    date = parse_date(fields.get("date", "")) or ""
    total = parse_total(fields.get("total", "")) or 0.0
    items = parse_items(fields.get("items", ""))
    return ParsedReceipt(vendor=vendor, date=date, total=total, items=items)


def asdict(receipt: ParsedReceipt) -> Dict[str, object]:
    return {
        "vendor": receipt.vendor,
        "date": receipt.date,
        "total": receipt.total,
        "items": [item.__dict__ for item in receipt.items],
    }


__all__ = [
    "Item",
    "ParsedReceipt",
    "clean_vendor",
    "parse_date",
    "parse_total",
    "parse_items",
    "parse_fields",
    "asdict",
]
