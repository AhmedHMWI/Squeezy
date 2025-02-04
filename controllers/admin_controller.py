import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from database import get_db_connection

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True) 

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')

def allowed_file(filename):
    """ التحقق من امتداد الملف """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_all_fruits():
    """ جلب جميع الفواكه من قاعدة البيانات """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fruits")
        fruits = cursor.fetchall()
        return fruits
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    finally:
        conn.close()

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'user_name' not in session:
        flash("❌ Please log in first!", "error")
        return redirect(url_for('auth.login'))

    fruits = get_all_fruits()
    return render_template('admin_dashboard.html', fruits=fruits, user=session.get('user_name', 'Admin'))

@admin_bp.route('/add_fruit', methods=['POST'])
def add_fruit():
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']  # ✅ احصل على user_id من الجلسة
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    image_url = None  

    # ✅ معالجة رفع الصورة
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f"uploads/{filename}"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO fruits (user_id, name, price, quantity, image_url) VALUES (%s, %s, %s, %s, %s)", 
                    (user_id, name, price, quantity, image_url))
        conn.commit()
        flash("Fruit added successfully!", "success")
    except Exception as e:
        flash(f"Error adding fruit: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/edit_fruit/<int:fruit_id>', methods=['GET', 'POST'])
def edit_fruit(fruit_id):
    if 'user_name' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # ✅ جلب بيانات الفاكهة
        cursor.execute("SELECT * FROM fruits WHERE id = %s", (fruit_id,))
        fruit = cursor.fetchone()

        if not fruit:
            flash("❌ Fruit not found!", "error")
            return redirect(url_for('admin.admin_dashboard'))

        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            image_url = fruit['image_url']  

            # ✅ معالجة رفع صورة جديدة
            if 'image' in request.files:
                file = request.files['image']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)
                    image_url = f"uploads/{filename}" 

            # ✅ تحديث بيانات الفاكهة
            cursor.execute("UPDATE fruits SET name = %s, price = %s, quantity = %s, image_url = %s WHERE id = %s",
                           (name, price, quantity, image_url, fruit_id))
            conn.commit()

            flash("✅ Fruit updated successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))

        return render_template('edit_fruit.html', fruit=fruit, user=session.get('user_name', 'Admin'))

    except Exception as e:
        flash(f"❌ Error editing fruit: {str(e)}", "error")
        return redirect(url_for('admin.admin_dashboard'))
    finally:
        conn.close()

@admin_bp.route('/delete_fruit/<int:fruit_id>', methods=['POST'])
def delete_fruit(fruit_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM fruits WHERE id=%s", (fruit_id,))
        conn.commit()
        flash("❌ Fruit deleted successfully!", "danger")
    except Exception as e:
        flash(f"❌ Error deleting fruit: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('admin.admin_dashboard'))
