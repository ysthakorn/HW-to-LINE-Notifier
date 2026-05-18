from pathlib import Path
import requests
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import ENV
from .line_client import push_text_message
from .message_builder import build_homework_message
from .sheet_service import fetch_homework_rows

app = FastAPI()
app.mount("/fonts", StaticFiles(directory=Path(__file__).resolve().parent.parent / "fonts"), name="fonts")


class ManualNotifyPayload(BaseModel):
    subject: str | None = None
    title: str | None = None
    detail: str | None = None
    due: str | None = None


class NotifyRowPayload(BaseModel):
    rowId: int | None = None
    subject: str | None = None
    title: str | None = None
    detail: str | None = None
    due: str | None = None
    date: str | None = None


def _line_error_response(error: requests.HTTPError) -> JSONResponse:
    status = error.response.status_code if error.response is not None else 502
    detail = error.response.text.strip() if error.response is not None and error.response.text else ""
    return JSONResponse(status_code=status, content={"error": detail or "line_request_failed"})


@app.get("/")
def root() -> FileResponse:
    return FileResponse(Path(__file__).parent / "views" / "index.html")


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}


@app.get("/api/config")
def api_config() -> dict[str, bool]:
    return {"hasGoogleSheet": bool(ENV.google_sheet_csv_url)}


@app.get("/api/sheet-rows")
def api_sheet_rows():
    try:
        rows = fetch_homework_rows()
        return {"ok": True, "rows": rows}
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "GOOGLE_SHEET_CSV_URL is not configured"})
    except requests.RequestException:
        return JSONResponse(status_code=400, content={"error": "failed_to_fetch_sheet_rows"})
    except Exception:  # noqa: BLE001
        return JSONResponse(status_code=400, content={"error": "failed_to_fetch_sheet_rows"})


@app.post("/notify")
def notify(payload: ManualNotifyPayload):
    message = build_homework_message(payload.subject, payload.title, payload.detail, payload.due)

    try:
        push_text_message(message)
        return {"ok": True}
    except requests.HTTPError as error:
        return _line_error_response(error)
    except requests.Timeout:
        return JSONResponse(status_code=504, content={"error": "line_request_timeout"})
    except requests.RequestException:
        return JSONResponse(status_code=502, content={"error": "line_request_failed"})
    except Exception:  # noqa: BLE001
        return JSONResponse(status_code=502, content={"error": "line_request_failed"})


@app.post("/notify-row")
def notify_row(payload: NotifyRowPayload):
    message = build_homework_message(payload.subject, payload.title, payload.detail, payload.due or payload.date)

    try:
        push_text_message(message)
        return {"ok": True}
    except requests.HTTPError as error:
        return _line_error_response(error)
    except requests.Timeout:
        return JSONResponse(status_code=504, content={"error": "line_request_timeout"})
    except requests.RequestException:
        return JSONResponse(status_code=502, content={"error": "line_request_failed"})
    except Exception:  # noqa: BLE001
        return JSONResponse(status_code=502, content={"error": "line_request_failed"})
