# 🗂️ Smart File Organizer Pro

โปรแกรมจัดระเบียบไฟล์อัตโนมัติ พร้อม GUI สวยงาม Dark/Light Mode และ Windows Installer

**สร้างโดย: กรวิชญ์ ชูเลื่อน (Korawit Chuluean)**

---

## ✨ Features

| Feature | รายละเอียด |
|---|---|
| 📁 Auto-Sort | จัดไฟล์ตามประเภท (รูป, วิดีโอ, เอกสาร ฯลฯ) อัตโนมัติ |
| 👁️ Live Preview | Scan และดูตัวอย่างก่อน organize จริง |
| ⚙️ Custom Rules | เพิ่ม/ลบ/แก้ไข rule ได้เอง |
| ↩️ Undo | ย้อนกลับ organize ครั้งล่าสุดได้ทันที |
| 📊 Dashboard | ดูสถิติไฟล์ทั้งหมดที่ organize แล้ว |
| 🌙 Dark/Light Mode | สลับธีมได้ |
| 💾 Session History | เก็บประวัติการ organize ใน SQLite |

---

## 🚀 การติดตั้งและรัน (Development)

### 1. Clone / Download โปรเจค

```bash
git clone https://github.com/yourname/SmartFileOrganizer
cd SmartFileOrganizer
```

### 2. สร้าง Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. รันโปรแกรม

```bash
python main.py
```

---

## 📦 Build เป็น .exe (Windows)

### Step 1: Build ด้วย PyInstaller

```bash
pip install pyinstaller
pyinstaller build.spec
```

ผลลัพธ์จะอยู่ใน `dist/SmartFileOrganizer/`

### Step 2: สร้าง Installer ด้วย Inno Setup

1. ดาวน์โหลด [Inno Setup](https://jrsoftware.org/issetup.php)
2. เปิดไฟล์ `installer.iss` ใน Inno Setup Compiler
3. กด **Build → Compile** (หรือกด F9)
4. Installer จะอยู่ใน `dist/installer/SmartFileOrganizer_Setup_v1.0.0.exe`

---

## 📁 โครงสร้างโปรเจค

```
SmartFileOrganizer/
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
├── build.spec               # PyInstaller config
├── installer.iss            # Inno Setup installer script
├── README.md
├── ui/
│   ├── __init__.py
│   ├── main_window.py       # Main window + sidebar + nav
│   ├── organizer_page.py    # Scan, preview, organize, undo
│   ├── dashboard.py         # Stats dashboard
│   ├── rules_editor.py      # Custom rules editor
│   └── styles.py            # Dark & Light QSS themes
├── core/
│   ├── __init__.py
│   ├── scanner.py           # Scan folder → list of FileInfo
│   ├── sorter.py            # Move files (background thread)
│   └── undo_manager.py      # Undo last session
├── data/
│   ├── __init__.py
│   └── database.py          # SQLite: sessions + stats
└── assets/
    └── (icon.ico)           # App icon — add your own
```

---

## 🔧 Default File Rules

| Extension | Destination |
|---|---|
| .jpg .jpeg .png .gif | `Images/` |
| .mp4 .mov .avi .mkv | `Videos/` |
| .mp3 .wav .flac | `Music/` |
| .pdf .doc .docx .xlsx .pptx | `Documents/` |
| .zip .rar .7z | `Archives/` |
| .py .js .html .css | `Code/` |
| .exe .msi | `Programs/` |
| อื่นๆ | `Others/` |

---

## 📅 Development Roadmap

- [x] สัปดาห์ 1-2: GUI skeleton (PyQt6) + Dark/Light theme
- [x] สัปดาห์ 3-4: Core logic (Scanner, Sorter, Rule Engine)
- [x] สัปดาห์ 5-6: Dashboard + Undo system + SQLite
- [x] สัปดาห์ 7: Packaging (PyInstaller + Inno Setup)
- [ ] สัปดาห์ 8: Test, polish, release

---

## 📄 License

MIT License — free to use and modify.

---

## 👨‍💻 Developer

**กรวิชญ์ ชูเลื่อน (Korawit Chuluean)**
- GitHub: https://github.com/taeezx44
- Project Repository: https://github.com/taeezx44/SmartFileOrganizer
