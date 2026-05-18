import csv
from io import StringIO
import requests

from .config import ENV

HEADER_ALIASES = {
    "subject": ["subject", "subject_name", "วิชา"],
    "title": ["title", "topic", "หัวข้อ", "งาน"],
    "detail": ["detail", "description", "รายละเอียด"],
    "due": ["due", "date", "deadline", "กำหนดส่ง", "วันที่"],
}


def normalize_header(value: str | None) -> str:
    return str(value or "").strip().lower()


def pick_field(row: dict[str, str], aliases: list[str]) -> str:
    for key in aliases:
        value = row.get(normalize_header(key), "").strip()
        if value:
            return value
    return ""


def map_to_homework_row(row: dict[str, str], index: int) -> dict[str, str | int]:
    return {
        "rowId": index + 1,
        "subject": pick_field(row, HEADER_ALIASES["subject"]),
        "title": pick_field(row, HEADER_ALIASES["title"]),
        "detail": pick_field(row, HEADER_ALIASES["detail"]),
        "due": pick_field(row, HEADER_ALIASES["due"]),
    }


def parse_csv_text(csv_text: str) -> list[dict[str, str]]:
    if not csv_text or not csv_text.strip():
        return []

    reader = csv.DictReader(StringIO(csv_text))
    rows: list[dict[str, str]] = []
    for row in reader:
        normalized: dict[str, str] = {}
        for key, value in row.items():
            normalized[normalize_header(key)] = (value or "").strip()
        rows.append(normalized)
    return rows


def has_any_content(row: dict[str, str | int]) -> bool:
    return bool(row["subject"] or row["title"] or row["detail"] or row["due"])


def fetch_homework_rows() -> list[dict[str, str | int]]:
    if not ENV.google_sheet_csv_url:
        raise ValueError("GOOGLE_SHEET_CSV_URL is not configured")

    response = requests.get(ENV.google_sheet_csv_url, timeout=ENV.request_timeout_sec)
    response.raise_for_status()

    raw_rows = parse_csv_text(response.text)
    mapped_rows = [map_to_homework_row(row, index) for index, row in enumerate(raw_rows)]
    return [row for row in mapped_rows if has_any_content(row)]
