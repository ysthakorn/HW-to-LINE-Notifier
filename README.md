# HW-to-LINE Notifier (FastAPI)

ระบบแจ้งเตือนการบ้านผ่าน Dashboard และส่งข้อความเข้า LINE Group โดยใช้ Python + FastAPI

## Project Structure

```
.
|-- requirements.txt
|-- .env.example
`-- src/
    |-- main.py
    |-- config.py
    |-- line_client.py
    |-- message_builder.py
    |-- sheet_service.py
    `-- views/
        `-- index.html
```

## Setup

1. Create virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
LINE_ACCESS_TOKEN=YOUR_TOKEN_HERE
LINE_GROUP_ID=YOUR_GROUP_ID_HERE
PORT=8080
LINE_REQUEST_TIMEOUT_SEC=10
GOOGLE_SHEET_CSV_URL=https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv&gid=0
```

## Run

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

Open http://localhost:8080 in your browser.

## Google Sheet Dashboard

ใส่ URL แบบ CSV export ลงใน `GOOGLE_SHEET_CSV_URL` แล้วหน้า Dashboard จะโหลดรายการจากชีตให้เอง พร้อมปุ่ม `ส่งแถวนี้` รายการละ 1 ปุ่ม

รองรับชื่อคอลัมน์แบบยืดหยุ่น เช่น:

- `subject` หรือ `subject_name` หรือ `วิชา`
- `title` หรือ `topic` หรือ `หัวข้อ`
- `detail` หรือ `description` หรือ `รายละเอียด`
- `due` หรือ `date` หรือ `deadline` หรือ `กำหนดส่ง`

ระบบรองรับการแปลงวันที่ปี พ.ศ. (เช่น `2569`) เป็น ค.ศ. อัตโนมัติเมื่อสร้างข้อความแจ้งเตือน

## Endpoints

- `GET /` web dashboard
- `GET /api/config` dashboard config
- `GET /api/sheet-rows` load rows from Google Sheet CSV
- `POST /notify` send message to LINE Group
- `POST /notify-row` send selected sheet row
- `GET /health` health check
