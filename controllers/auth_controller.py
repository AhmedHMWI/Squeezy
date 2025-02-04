from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from database import get_db_connection
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # ✅ التأكد من إدخال البيانات
        if not email or not password:
            flash("❌ Please enter both email and password!", "error")
            return render_template('login.html')

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        except Exception as e:
            flash(f"❌ Database error: {str(e)}", "error")
            return render_template('login.html')

        finally:
            conn.close()

        # ✅ التحقق من صحة البيانات
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session.clear()  # تنظيف الجلسة قبل بدء جلسة جديدة
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            session.permanent = True  # جعل الجلسة دائمة حتى لا يتم تسجيل الخروج تلقائيًا

            flash("✅ Login successful!", "success")

            if user['role'] == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('user.user_dashboard'))

        flash("❌ Invalid email or password!", "error")
        return render_template('login.html')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash("✅ You have been logged out!", "info")
    return redirect(url_for('auth.login'))
