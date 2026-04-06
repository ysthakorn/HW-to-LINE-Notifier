# 📚 HW-to-LINE Notifier

ระบบแจ้งเตือนการบ้านผ่านเว็บฟอร์ม ส่งตรงเข้า LINE Group ทันที

## 🛠 วิธีติดตั้ง
1. ติดตั้ง Library ที่จำเป็น:
   ```bash
   pip install flask requests waitress
   ```
2. แก้ไขไฟล์ `app.py`:
   - ใส่ **LINE_ACCESS_TOKEN**
   - ใส่ **LINE_GROUP_ID**

## 🚀 วิธีใช้งาน
1. รันเซิร์ฟเวอร์:
   python app.py
2. เข้าใช้งานผ่านเบราว์เซอร์:
   `http://localhost:8080`

## 📄 ข้อมูลโปรเจกต์
- **Port:** 8080
- **Engine:** Python Flask + Waitress
- **UI:** CSS Modern Responsive

### 💡 วิธีรัน (Step-by-Step)
1. ก๊อปปี้โค้ดในข้อ **1** ไปวางในไฟล์ชื่อ `app.py`
2. ก๊อปปี้โค้ดในข้อ **2** ไปวางในไฟล์ชื่อ `README.md`
3. เปิด Command Prompt หรือ Terminal ในโฟลเดอร์นั้น
4. รันคำสั่ง: `pip install flask requests waitress`
5. รันโปรแกรม: `python app.py`
6. เปิดเบราว์เซอร์พิมพ์: `localhost:8080` พร้อมใช้งานทันทีครับ!
