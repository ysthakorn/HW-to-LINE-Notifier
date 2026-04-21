# HW-to-LINE Notifier (Node.js)

ระบบแจ้งเตือนการบ้านผ่านเว็บฟอร์ม และส่งข้อความเข้า LINE Group โดยใช้ Node.js/Express

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
    |   `-- messageBuilder.js
    `-- views/
        `-- index.html
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

## Endpoints

- `GET /` web form
- `POST /notify` send message to LINE Group
- `GET /health` health check
