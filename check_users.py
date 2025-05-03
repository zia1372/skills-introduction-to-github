import sqlite3

# اتصال به دیتابیس
conn = sqlite3.connect('bmtaxi.db')
cursor = conn.cursor()

# نمایش کاربران موجود
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# چاپ اطلاعات کاربران
for user in users:
    print(user)

conn.close()