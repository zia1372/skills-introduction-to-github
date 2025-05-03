from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime

add_driver_bp = Blueprint('add_driver', __name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def get_db():
    conn = sqlite3.connect('bmtaxi.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_driver_bp.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    conn = get_db()

    if request.method == 'POST':
        name = request.form['name']
        family = request.form['family']
        national_code = request.form['national_code']
        phone = request.form['phone']
        car_model = request.form['car_model']
        license_plate = request.form['license_plate']
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(f"{national_code}_{datetime.now().timestamp()}.{image.filename.rsplit('.', 1)[1]}")
            image.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash("لطفاً یک تصویر معتبر انتخاب کنید", "danger")
            return redirect(url_for('add_driver.add_driver'))

        # جلوگیری از تکرار کد ملی
        existing = conn.execute("SELECT id FROM drivers WHERE national_code = ?", (national_code,)).fetchone()
        if existing:
            flash("راننده‌ای با این کد ملی قبلاً ثبت شده است", "warning")
            conn.close()
            return redirect(url_for('add_driver.add_driver'))

        conn.execute('''
            INSERT INTO drivers (name, family, national_code, phone, car_model, license_plate, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, family, national_code, phone, car_model, license_plate, filename))
        conn.commit()
        flash("راننده با موفقیت ثبت شد", "success")

    drivers = conn.execute("SELECT * FROM drivers ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('add_driver.html', drivers=drivers)
