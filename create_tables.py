import sqlite3

# --- نام فایل دیتابیس ---
DATABASE = 'bmtaxi.db'

# --- تابع برای ساخت جداول ---
def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # جدول کاربران
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL, -- 'مدیر' یا 'کاربر فروش'
            photo_path TEXT
        )
    ''')
    
    # جدول رانندگان
    c.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone_number TEXT,
            vehicle_info TEXT
        )
    ''')

    # جدول صف رانندگان
    c.execute('''
        CREATE TABLE IF NOT EXISTS driver_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER NOT NULL,
            entry_time DATETIME NOT NULL,
            FOREIGN KEY (driver_id) REFERENCES drivers (id) ON DELETE CASCADE
        )
    ''')

    # جدول سفرها
    c.execute('''
        CREATE TABLE IF NOT EXISTS trip (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER NOT NULL,
            destination TEXT NOT NULL,
            fare REAL NOT NULL,
            date DATETIME NOT NULL,
            FOREIGN KEY (driver_id) REFERENCES drivers (id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

    print("Tables created successfully.")

# --- اجرای تابع ---
if __name__ == '__main__':
    create_tables()