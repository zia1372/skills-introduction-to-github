from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3, os
from werkzeug.utils import secure_filename
from datetime import datetime

add_user_bp = Blueprint('add_user', __name__)

UPLOAD_FOLDER = 'static/uploads'

@add_user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']
        role = request.form['role']

        # ذخیره عکس
        photo_file = request.files['photo']
        photo_filename = secure_filename(photo_file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        final_photo_name = f"{timestamp}_{photo_filename}"
        photo_path = os.path.join(UPLOAD_FOLDER, final_photo_name)
        photo_file.save(photo_path)

        # درج در دیتابیس
        conn = sqlite3.connect('taxi.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (first_name, last_name, username, password, phone, role, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, username, password, phone, role, final_photo_name))
        conn.commit()
        conn.close()

        flash("کاربر با موفقیت ثبت شد.")
        return redirect(url_for('add_user.add_user'))

    return render_template('add_user.html')
