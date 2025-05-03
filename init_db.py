import sqlite3
import os

# مسیر دیتابیس
DB_PATH = "bmtaxi.db"

# حذف فایل دیتابیس قبلی (اختیاری: اگر می‌خواهی همیشه از صفر ساخته شود)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# اتصال به دیتابیس
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ساخت جدول رانندگان
cursor.execute("""
CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    national_code TEXT UNIQUE NOT NULL,
    phone TEXT,
    car_type TEXT,
    license_plate TEXT,
    photo_path TEXT
)
""")

# ساخت جدول کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    photo_path TEXT
)
""")

# ساخت جدول سفرها
cursor.execute("""
CREATE TABLE IF NOT EXISTS trip (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_name TEXT,
    destination TEXT,
    fare INTEGER,
    start_time TEXT
)
""")

# ساخت جدول صف رانندگان
cursor.execute("""
CREATE TABLE IF NOT EXISTS driver_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER,
    entry_time TEXT,
    FOREIGN KEY(driver_id) REFERENCES drivers(id)
)
""")

# درج مدیر پیش‌فرض
cursor.execute("""
INSERT INTO users (username, password, role, full_name)
VALUES (?, ?, ?, ?)
""", ("admin", "1234", "مدیر", "مدیر سیستم"))

# درج کاربر فروش پیش‌فرض
cursor.execute("""
INSERT INTO users (username, password, role, full_name)
VALUES (?, ?, ?, ?)
""", ("user", "1234", "کاربر فروش", "کاربر فروش پیش‌فرض"))

conn.commit()
conn.close()

print("✅ دیتابیس و کاربران پیش‌فرض با موفقیت ساخته شدند.")
