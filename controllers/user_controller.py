import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from database import get_db_connection

user_bp = Blueprint('user', __name__, url_prefix='/user', template_folder='../templates')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_fruits():
    """ Fetch all available fruits from the database """
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

@user_bp.route('/dashboard')
def user_dashboard():
    """ عرض لوحة تحكم المستخدم مع العصائر الخاصة به """
    if 'user_id' in session and session['role'] == 'user':
        user_id = session['user_id']
        fruits = get_all_fruits()
        juices = get_user_juices(user_id)  # ✅ جلب العصائر الخاصة بالمستخدم
        
        print("DEBUG: Juices sent to template:", juices)  # 🟢 طباعة البيانات لمعرفة هل يتم إرسالها إلى القالب

        return render_template('user_dashboard.html', user=session.get('user_name', 'User'), fruits=fruits, juices=juices)

    flash("Please log in first!", "error")
    return redirect(url_for('auth.login'))



@user_bp.route('/create_juice', methods=['POST'])
def create_juice():
    """ Create a new juice with selected fruits """
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    juice_name = request.form.get('juice_name')
    selected_fruits = request.form.getlist('selected_fruits')
    image_url = None

    # ✅ معالجة رفع الصورة
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f"uploads/{filename}"

    if not selected_fruits:
        flash("Please select at least one fruit!", "error")
        return redirect(url_for('user.user_dashboard'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # إدخال العصير مع رابط الصورة في قاعدة البيانات
        cursor.execute("INSERT INTO juices (name, image_url) VALUES (%s, %s)", (juice_name, image_url))
        juice_id = cursor.lastrowid  # الحصول على ID العصير الذي تم إنشاؤه

        # ربط الفواكه بالعصير في قاعدة البيانات
        for fruit_id in selected_fruits:
            cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id) VALUES (%s, %s)", (juice_id, fruit_id))

        conn.commit()
        flash("Juice created successfully!", "success")
    except Exception as e:
        flash(f"Error creating juice: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('user.user_dashboard'))





@user_bp.route('/juice/edit/<int:juice_id>', methods=['GET', 'POST'])
def edit_juice(juice_id):
    """ تعديل اسم العصير والفواكه المختارة """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # جلب بيانات العصير الحالي
        cursor.execute("SELECT * FROM juices WHERE id = %s", (juice_id,))
        juice = cursor.fetchone()
        if not juice:
            flash("Juice not found!", "error")
            return redirect(url_for('user.user_dashboard'))

        # جلب الفواكه المتاحة
        cursor.execute("SELECT * FROM fruits")
        all_fruits = cursor.fetchall()

        # جلب الفواكه المرتبطة بالعصير الحالي
        cursor.execute("SELECT fruit_id FROM juice_fruits WHERE juice_id = %s", (juice_id,))
        selected_fruit_ids = [row['fruit_id'] for row in cursor.fetchall()]

        if request.method == 'POST':
            new_name = request.form['juice_name']
            new_selected_fruits = request.form.getlist('selected_fruits')
            new_image_url = request.form.get('image_url')  # إضافة رابط الصورة الجديد

            # تحديث اسم العصير
            cursor.execute("UPDATE juices SET name = %s, image_url = %s WHERE id = %s", (new_name, new_image_url, juice_id))

            # حذف الفواكه القديمة
            cursor.execute("DELETE FROM juice_fruits WHERE juice_id = %s", (juice_id,))

            # إدخال الفواكه الجديدة
            for fruit_id in new_selected_fruits:
                cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id) VALUES (%s, %s)", (juice_id, fruit_id))

            conn.commit()
            flash("Juice updated successfully!", "success")
            return redirect(url_for('user.user_dashboard'))

        return render_template('edit_juice.html', juice=juice, all_fruits=all_fruits, selected_fruit_ids=selected_fruit_ids)

    except Exception as e:
        flash(f"Database Error: {e}", "error")
        return redirect(url_for('user.user_dashboard'))

    finally:
        conn.close()




@user_bp.route('/juice/delete/<int:juice_id>', methods=['POST'])
def delete_juice(juice_id):
    """ حذف العصير """
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # تحقق من أن العصير يخص المستخدم
    cursor.execute("SELECT id FROM juices WHERE id = %s AND user_id = %s", (juice_id, user_id))
    juice = cursor.fetchone()

    if not juice:
        flash("Juice not found or unauthorized!", "error")
        conn.close()
        return redirect(url_for('user.user_dashboard'))

    try:
        cursor.execute("DELETE FROM juice_fruits WHERE juice_id = %s", (juice_id,))  # حذف الفواكه المرتبطة
        cursor.execute("DELETE FROM juices WHERE id = %s", (juice_id,))  # حذف العصير نفسه
        conn.commit()
        flash("Juice deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting juice: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('user.user_dashboard'))




def get_user_juices(user_id):
    """ Fetch all juices created by the logged-in user, including those without fruits """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
                SELECT juices.id, juices.name, juices.price, juices.image_url,
                    IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
                FROM juices
                LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
                LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
                WHERE juices.user_id = %s
                GROUP BY juices.id, juices.name, juices.price, juices.image_url, juices.created_at
                ORDER BY juices.created_at DESC
                """
        
        cursor.execute(query, (user_id,))
        juices = cursor.fetchall()

        print("DEBUG: User Juices from DB:", juices)  # Debugging output to see what is fetched

        return juices
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    finally:
        conn.close()
        
        


def get_all_juices():
    """ Fetch all juices created by all users """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT juices.id, juices.name, juices.price, juices.image_url,
            IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
        FROM juices
        LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
        LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
        GROUP BY juices.id, juices.name, juices.price, juices.image_url, juices.created_at
        ORDER BY juices.created_at DESC
        """

        cursor.execute(query)
        juices = cursor.fetchall()
        return juices
    except Exception as e:
        print(f"Database Error: {e}")
        return []
    finally:
        conn.close()

        
        

@user_bp.route('/')
def home():
    """ الصفحة الرئيسية - تعرض جميع العصائر """
    juices = get_all_juices()
    return render_template('home.html', juices=juices)
