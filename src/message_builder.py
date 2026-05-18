from datetime import datetime
import re


def parse_date_value(input_value: str | None) -> datetime | None:
    if not input_value:
        return None

    text = str(input_value).strip()
    for fmt in ("%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    match = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})(?:\s+(\d{1,2}):(\d{2}))?$", text)
    if not match:
        return None

    day = int(match.group(1))
    month = int(match.group(2))
    year = int(match.group(3))
    hour = int(match.group(4) or 0)
    minute = int(match.group(5) or 0)

    if year > 2400:
        year -= 543

    try:
        return datetime(year, month, day, hour, minute)
    except ValueError:
        return None


def format_due_date(date_string: str | None) -> str:
    parsed = parse_date_value(date_string)
    if parsed is None:
        return date_string or "-"

    return parsed.strftime("%d/%m/%Y @ %H:%M")


def build_homework_message(subject: str | None, title: str | None, detail: str | None, due: str | None) -> str:
    return "\n".join(
        [
            "📢 การบ้านใหม่มาแล้ว!",
            "━━━━━━━━━━━━━━",
            f"📘 วิชา: {subject or '-'}",
            f"📌 หัวข้อ: {title or '-'}",
            f"📝 รายละเอียด: {detail or '-'}",
            f"⏳ ส่งวันที่: {format_due_date(due)}",
            "━━━━━━━━━━━━━━",
        ]
    )
