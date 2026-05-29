# HW-to-LINE Notifier (Node.js)

ระบบแจ้งเตือนการบ้านผ่าน Dashboard และส่งข้อความเข้า LINE Group โดยใช้ Node.js/Express

## Project Structure

```
.
|-- package.json
|-- .env.example
`-- src/
    |-- app.js
    |-- server.js
    |-- config/
    |   `-- env.js
    |-- routes/
    |   `-- notifyRoutes.js
    |-- services/
    |   |-- lineClient.js
    |   |-- messageBuilder.js
    |   `-- sheetService.js
    `-- views/
        |-- index.html
        |-- setup.html
        |-- docs.html
        |-- status.html
        `-- assets/
            |-- styles.css
            |-- dashboard.js
            `-- status.js
```

## Setup

1. Install dependencies

```bash
npm install
```

2. Configure environment variables (PowerShell)

```powershell
$env:LINE_ACCESS_TOKEN="YOUR_TOKEN_HERE"
$env:LINE_GROUP_ID="YOUR_GROUP_ID_HERE"
$env:PORT="8080"
$env:LINE_REQUEST_TIMEOUT_SEC="10"
$env:GOOGLE_SHEET_CSV_URL="https://docs.google.com/spreadsheets/d/<SHEET_ID>/export?format=csv&gid=0"
```

Alternatively, create a `.env` file using values from `.env.example`.

## Run

```bash
npm start
```

For development mode (auto reload):

```bash
npm run dev
```

Open http://localhost:8080 in your browser.

Pages:

- `/` Dashboard
- `/setup` Setup guide
- `/docs` API documentation
- `/status` System status

## Google Sheet Dashboard

ใส่ URL แบบ CSV export ลงใน `GOOGLE_SHEET_CSV_URL` แล้วหน้า Dashboard จะโหลดรายการจากชีตให้เอง พร้อมปุ่ม `ส่งแถวนี้` รายการละ 1 ปุ่ม

รองรับชื่อคอลัมน์แบบยืดหยุ่น เช่น:

- `subject` หรือ `subject_name` หรือ `วิชา`
- `title` หรือ `topic` หรือ `หัวข้อ`
- `detail` หรือ `description` หรือ `รายละเอียด`
- `due` หรือ `date` หรือ `deadline` หรือ `กำหนดส่ง`

ตัวอย่างข้อมูลจาก CSV ที่รองรับ:

```csv
subject,detail,date
subject_name,detail,22/04/2569
```

ระบบจะแปลงปี พ.ศ. (เช่น `2569`) เป็น ค.ศ. อัตโนมัติเมื่อสร้างข้อความแจ้งเตือน

## Endpoints

- `GET /` web form
- `GET /setup` setup guide
- `GET /docs` API docs
- `GET /status` system status
- `GET /api/config` dashboard config
- `GET /api/sheet-rows` load rows from Google Sheet CSV
- `POST /notify` send message to LINE Group
- `POST /notify-row` send selected sheet row
- `GET /health` health check
