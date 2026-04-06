import requests
from datetime import datetime
from flask import Flask, request, render_template_string, jsonify
from waitress import serve

app = Flask(__name__)

# --- CONFIGURATION ---
CONFIG = {
    "LINE_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
    "LINE_GROUP_ID": "YOUR_GROUP_ID_HERE",
    "PORT": 8080
}

# --- UI TEMPLATE ---
HTML_TEMPLATE = """
<!doctype html>
<html lang="th">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HW Notifier</title>
  <link href="https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root { --line-green: #06c755; --bg-gray: #f4f7f9; }
    * { box-sizing: border-box; font-family: 'Sarabun', sans-serif; }
    body { background: var(--bg-gray); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .card { background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 100%; max-width: 400px; margin: 20px; }
    h2 { text-align: center; color: #333; margin-bottom: 1.5rem; font-size: 1.5rem; }
    label { display: block; margin-bottom: 6px; font-weight: 600; color: #555; font-size: 0.9rem; }
    input, textarea { width: 100%; padding: 12px; border: 1.5px solid #eee; border-radius: 12px; margin-bottom: 15px; font-size: 1rem; transition: 0.2s; }
    input:focus, textarea:focus { border-color: var(--line-green); outline: none; background: #fff; }
    button { width: 100%; padding: 14px; border: none; border-radius: 12px; background: var(--line-green); color: white; font-size: 1rem; font-weight: 600; cursor: pointer; transition: 0.3s; }
    button:hover { background: #05b34c; transform: translateY(-1px); }
    button:disabled { background: #ccc; transform: none; }
    #status { margin-top: 15px; text-align: center; font-size: 0.9rem; font-weight: 600; min-height: 1.2rem; }
  </style>
</head>
<body>
  <div class="card">
    <h2>🟢 ส่งการบ้านเข้า LINE</h2>
    <form id="hwForm">
      <label>ชื่อวิชา</label>
      <input name="subject" required placeholder="ระบุวิชา">
      
      <label>หัวข้อ/งาน</label>
      <input name="title" required placeholder="ระบุชื่อหัวข้อ">
      
      <label>รายละเอียด</label>
      <textarea name="detail" rows="3" required placeholder="รายละเอียดเพิ่มเติม..."></textarea>
      
      <label>กำหนดส่ง</label>
      <input type="datetime-local" name="due" required>
      
      <button type="submit" id="btn">ส่งข้อมูลทันที</button>
      <div id="status"></div>
    </form>
  </div>

  <script>
    const form = document.getElementById('hwForm');
    const btn = document.getElementById('btn');
    const status = document.getElementById('status');

    form.onsubmit = async (e) => {
      e.preventDefault();
      btn.disabled = true;
      status.textContent = "กำลังส่ง...";
      status.style.color = "#666";

      try {
        const res = await fetch('/notify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(Object.fromEntries(new FormData(form)))
        });
        
        if (res.ok) {
          status.textContent = "สำเร็จ! ข้อมูลถูกส่งเข้ากลุ่มแล้ว ✅";
          status.style.color = "var(--line-green)";
          form.reset();
        } else {
          status.textContent = "เกิดข้อผิดพลาด ❌";
          status.style.color = "#ff4d4d";
        }
      } catch (err) {
        status.textContent = "เชื่อมต่อเซิร์ฟเวอร์ไม่ได้";
        status.style.color = "#ff4d4d";
      } finally {
        btn.disabled = false;
      }
    };
  </script>
</body>
</html>
"""

# --- BACKEND LOGIC ---
@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    subject = data.get("subject")
    title = data.get("title")
    detail = data.get("detail")
    due = data.get("due")

    # Format Date
    try:
        dt = datetime.fromisoformat(due)
        due_str = dt.strftime("%d/%m/%Y @ %H:%M")
    except:
        due_str = due

    # LINE Message Format
    msg = (
        f"📢 การบ้านใหม่มาแล้ว!\n"
        f"━━━━━━━━━━━━━━\n"
        f"📘 วิชา: {subject}\n"
        f"📌 หัวข้อ: {title}\n"
        f"📝 รายละเอียด: {detail}\n"
        f"⏳ ส่งวันที่: {due_str}\n"
        f"━━━━━━━━━━━━━━"
    )

    headers = {
        "Authorization": f"Bearer {CONFIG['LINE_ACCESS_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": CONFIG['LINE_GROUP_ID'],
        "messages": [{"type": "text", "text": msg}]
    }

    resp = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    
    return jsonify({"ok": True}) if resp.status_code == 200 else jsonify({"error": resp.text}), resp.status_code

if __name__ == "__main__":
    print(f"🚀 Server is running on port {CONFIG['PORT']}...")
    serve(app, host="0.0.0.0", port=CONFIG['PORT'])
