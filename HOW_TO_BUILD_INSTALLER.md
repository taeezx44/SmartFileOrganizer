# 🛠️ วิธีสร้าง Windows Setup Installer

## ขั้นตอนทั้งหมด (3 ขั้น)

---

## ✅ ขั้นที่ 1 — ติดตั้ง Python

1. ไปที่ https://python.org/downloads
2. ดาวน์โหลด Python 3.11 หรือ 3.12
3. ติดตั้ง **ต้องติ๊ก ✅ "Add Python to PATH"**

---

## ✅ ขั้นที่ 2 — รัน install.bat

1. แตก zip โปรเจคออกมา
2. ดับเบิลคลิก **`install.bat`**
3. รอติดตั้ง dependencies (PyQt6)
4. โปรแกรมจะเปิดขึ้นมาอัตโนมัติ ✅

> ครั้งต่อไปใช้ `run.bat` เปิดได้เลย

---

## ✅ ขั้นที่ 3 — Build เป็น Setup.exe

### 3.1 Build EXE ด้วย PyInstaller

```
ดับเบิลคลิก build_exe.bat
```

รอ 2-5 นาที จะได้โฟลเดอร์ `dist\SmartFileOrganizer\`

### 3.2 ติดตั้ง Inno Setup

ดาวน์โหลดฟรีที่: https://jrsoftware.org/issetup.php

### 3.3 สร้าง Setup.exe

1. เปิด **Inno Setup Compiler**
2. File → Open → เลือก **`installer.iss`**
3. กด **Build → Compile** (หรือ **F9**)
4. รอสักครู่...
5. Setup.exe จะอยู่ที่ **`dist\installer\SmartFileOrganizer_Setup_v1.0.0.exe`** 🎉

---

## 📦 ผลลัพธ์ที่ได้

```
dist\
└── installer\
    └── SmartFileOrganizer_Setup_v1.0.0.exe   ← แจกจ่ายได้เลย!
```

Setup นี้จะ:
- ✅ ติดตั้งโปรแกรมไปที่ `C:\Program Files\Smart File Organizer Pro\`
- ✅ สร้าง Start Menu shortcut
- ✅ สร้าง Desktop shortcut (ถ้าเลือก)
- ✅ มี Uninstall ใน Windows Settings
- ✅ รันโปรแกรมหลังติดตั้งเสร็จ

---

## 🔁 ขั้นตอนสรุป

```
install.bat  →  build_exe.bat  →  Inno Setup (F9)  →  Setup.exe ✅
```
