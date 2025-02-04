from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from database import get_db_connection

user_bp = Blueprint('user', __name__, url_prefix='/user')

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

    if not selected_fruits:
        flash("Please select at least one fruit!", "error")
        return redirect(url_for('user.user_dashboard'))

    # Debugging
    print(f"Juice Name: {juice_name}")
    print(f"Selected Fruits: {selected_fruits}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert juice into the database
        cursor.execute("INSERT INTO juices (name) VALUES (%s)", (juice_name,))
        juice_id = cursor.lastrowid  # Get the created juice ID
        print(f"Created Juice ID: {juice_id}")  # Debugging

        # Link fruits to the juice in the database
        for fruit_id in selected_fruits:
            cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id) VALUES (%s, %s)", (juice_id, fruit_id))

        conn.commit()
        flash("Juice created successfully!", "success")
    except Exception as e:
        flash(f"Error creating juice: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('user.user_dashboard'))



def get_user_juices(user_id):
    """ Fetch all juices created by the logged-in user, including those without fruits """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT juices.id, juices.name, juices.price, 
            IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
        FROM juices
        LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
        LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
        WHERE juices.user_id = %s
        GROUP BY juices.id, juices.name, juices.price, juices.created_at
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

