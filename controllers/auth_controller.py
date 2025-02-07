from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from database import get_db_connection
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not name or not email or not password or not confirm_password:
            flash("❌ All fields are required!", "error")
            return render_template('register.html')

        if password != confirm_password:
            flash("❌ Passwords do not match!", "error")
            return render_template('register.html')

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # ✅ التحقق مما إذا كان البريد الإلكتروني مستخدمًا مسبقًا
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash("❌ Email already registered!", "error")
                return render_template('register.html')

            # ✅ تشفير كلمة المرور بشكل صحيح
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            except Exception as hash_error:
                flash("❌ Error while encrypting the password!", "error")
                return render_template('register.html')

            # ✅ إدراج المستخدم الجديد في قاعدة البيانات
            cursor.execute(
                "INSERT INTO users (name, email, password, role, created_at) VALUES (%s, %s, %s, %s, NOW())",
                (name, email, hashed_password, 'user')
            )
            conn.commit()

            # ✅ جلب بيانات المستخدم الذي تم إنشاؤه
            cursor.execute("SELECT id, name, role FROM users WHERE email = %s", (email,))
            new_user = cursor.fetchone()

            if not new_user:
                flash("❌ Registration failed, please try again.", "error")
                return render_template('register.html')

            # ✅ تسجيل الدخول مباشرة بعد التسجيل
            session.clear()
            session['user_id'] = new_user['id']
            session['user_name'] = new_user['name']
            session['role'] = new_user['role']
            session.permanent = True  # جعل الجلسة دائمة

            flash("✅ Registration successful! Welcome to your dashboard.", "success")
            return redirect(url_for('user.user_dashboard'))

        except Exception as e:
            flash(f"❌ Database error: {str(e)}", "error")
            return render_template('register.html')

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # ✅ التأكد من إدخال البيانات
        if not email or not password:
            flash("❌ Please enter both email and password!", "error")
            return render_template('login.html')

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

        except Exception as e:
            flash(f"❌ Database error: {str(e)}", "error")
            return render_template('login.html')

        finally:
            if cursor:
                cursor.close()
            if conn:
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
