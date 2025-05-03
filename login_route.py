from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3

login_bp = Blueprint('login', __name__)

DATABASE = "database.db"  # مسیر دیتابیست رو در صورت نیاز تغییر بده

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ? AND role = ?",
            (username, password, role)
        ).fetchone()
        conn.close()

        if user:
            session['username'] = username
            session['role'] = role
            if role == 'admin':
                return redirect(url_for('dashboard.admin_dashboard'))
            elif role == 'sales':
                return redirect(url_for('dashboard.sales_dashboard'))
        else:
            error = "نام کاربری یا رمز عبور نادرست است."

    return render_template('login.html', error=error)
