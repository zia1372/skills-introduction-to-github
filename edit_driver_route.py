from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

edit_driver_bp = Blueprint('edit_driver', __name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def get_db():
    conn = sqlite3.connect('bmtaxi.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@edit_driver_bp.route('/edit_driver/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    conn = get_db()
    cur = conn.cursor()

    # دریافت اطلاعات فعلی راننده
    cur.execute("SELECT * FROM drivers WHERE id = ?", (driver_id,))
    driver = cur.fetchone()

    if not driver:
        flash("راننده مورد نظر یافت نشد", "danger")
        return redirect(url_for('dashboard.dashboard'))  # یا هر صفحه‌ی دیگر مناسب

    if request.method == 'POST':
        name = request.form['name']
        family = request.form['family']
        national_code = request.form['national_code']
        phone = request.form['phone']
        car_model = request.form['car_model']
        license_plate = request.form['license_plate']
        image = request.files['image']

        image_path = driver['image_path']

        # بررسی اگر تصویر جدید آپلود شده
        if image and allowed_file(image.filename):
            filename = secure_filename(f"{national_code}_{datetime.now().timestamp()}.{image.filename.rsplit('.', 1)[1]}")
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            image_path = filename  # عکس جدید جایگزین شود

        # بروزرسانی اطلاعات در دیتابیس
        cur.execute('''
            UPDATE drivers
            SET name = ?, family = ?, national_code = ?, phone = ?, car_model = ?, license_plate = ?, image_path = ?
            WHERE id = ?
        ''', (name, family, national_code, phone, car_model, license_plate, image_path, driver_id))

        conn.commit()
        conn.close()

        flash("اطلاعات راننده با موفقیت ویرایش شد", "success")
        return redirect(url_for('dashboard.dashboard'))  # یا مسیر مناسب برای بازگشت

    return render_template('edit_driver.html', driver=driver)
