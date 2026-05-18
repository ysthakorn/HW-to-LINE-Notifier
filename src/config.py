from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Env:
    line_access_token: str
    line_group_id: str
    port: int
    request_timeout_sec: int
    google_sheet_csv_url: str


ENV = Env(
    line_access_token=os.getenv("LINE_ACCESS_TOKEN", "YOUR_TOKEN_HERE"),
    line_group_id=os.getenv("LINE_GROUP_ID", "YOUR_GROUP_ID_HERE"),
    port=int(os.getenv("PORT", "8080")),
    request_timeout_sec=int(os.getenv("LINE_REQUEST_TIMEOUT_SEC", "10")),
    google_sheet_csv_url=os.getenv("GOOGLE_SHEET_CSV_URL", ""),
)
