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


@user_bp.route('/dashboard')
def user_dashboard():
    if 'user_id' not in session:
        flash("You must log in first!", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM fruits")
    fruits = cursor.fetchall()

    cursor.execute("""
        SELECT juices.id, juices.name, juices.price, juices.image_url,
               GROUP_CONCAT(fruits.name SEPARATOR ', ') AS fruit_names
        FROM juices
        LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
        LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
        WHERE juices.user_id = %s
        GROUP BY juices.id;
    """, (session['user_id'],))
    juices = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('user_dashboard.html', user=user['name'], fruits=fruits, juices=juices)


@user_bp.route('/create_juice', methods=['POST'])
def create_juice():
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    juice_name = request.form.get('juice_name')
    fruit_ids = request.form.getlist('selected_fruits[]')
    image_url = None

    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f"uploads/{filename}"


    if not juice_name or not fruit_ids:
        flash("Please select at least one fruit and enter a juice name.", "danger")
        return redirect(url_for('user.user_dashboard'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            flash("User does not exist!", "danger")
            return redirect(url_for('user.user_dashboard'))

        cursor.execute("INSERT INTO juices (name, image_url, user_id) VALUES (%s, %s, %s)", 
                    (juice_name, image_url, session['user_id']))
        juice_id = cursor.lastrowid

        if not juice_id:
            raise ValueError("Failed to retrieve `lastrowid` after inserting juice!")

        total_price = 0
        for fruit_id in fruit_ids:
            cursor.execute("SELECT price FROM fruits WHERE id = %s", (fruit_id,))
            fruit_price = cursor.fetchone()

            if not fruit_price or fruit_price['price'] is None:
                continue

            total_price += fruit_price['price']
            cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id, quantity) VALUES (%s, %s, %s)", (juice_id, fruit_id, 1))

        cursor.execute("UPDATE juices SET price = %s WHERE id = %s", (total_price, juice_id))
        conn.commit()

        flash("Your juice has been created successfully!", "success")

    except Exception as e:
        flash(f"Error creating juice: {str(e)}", "error")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for('user.user_dashboard'))


@user_bp.route('/edit_juice/<int:juice_id>', methods=['GET', 'POST'])
def edit_juice(juice_id):
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM juices WHERE id = %s AND user_id = %s", (juice_id, session['user_id']))
    juice = cursor.fetchone()

    if not juice:
        flash("Juice not found or unauthorized!", "error")
        return redirect(url_for('user.user_dashboard'))

    cursor.execute("SELECT * FROM fruits")
    all_fruits = cursor.fetchall()

    cursor.execute("""
        SELECT fruit_id FROM juice_fruits WHERE juice_id = %s
    """, (juice_id,))
    selected_fruit_ids = [fruit['fruit_id'] for fruit in cursor.fetchall()]

    user_name = session.get('user_name', 'Guest')

    if request.method == 'POST':
        juice_name = request.form.get('juice_name')
        selected_fruits = request.form.getlist('selected_fruits')

        image_url = juice['image_url']
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                image_url = f"uploads/{filename}"

        try:
            cursor.execute("""
                UPDATE juices 
                SET name = %s, image_url = %s 
                WHERE id = %s AND user_id = %s
            """, (juice_name, image_url, juice_id, session['user_id']))

            cursor.execute("DELETE FROM juice_fruits WHERE juice_id = %s", (juice_id,))
            for fruit_id in selected_fruits:
                cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id) VALUES (%s, %s)", (juice_id, fruit_id))

            conn.commit()
            flash("Juice updated successfully!", "success")
            return redirect(url_for('user.user_dashboard'))
        except Exception as e:
            flash(f"Error updating juice: {str(e)}", "error")

    return render_template('edit_juice.html', juice=juice, all_fruits=all_fruits, selected_fruit_ids=selected_fruit_ids, user_name=user_name)


@user_bp.route('/juice/delete/<int:juice_id>', methods=['POST'])
def delete_juice(juice_id):
    if 'user_id' not in session:
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM juices WHERE id = %s AND user_id = %s", (juice_id, user_id))
    juice = cursor.fetchone()

    if not juice:
        flash("Juice not found or unauthorized!", "error")
        conn.close()
        return redirect(url_for('user.user_dashboard'))

    try:
        cursor.execute("DELETE FROM juice_fruits WHERE juice_id = %s", (juice_id,))
        cursor.execute("DELETE FROM juices WHERE id = %s", (juice_id,))
        conn.commit()

        flash("Juice deleted successfully!", "danger")
    except Exception as e:
        flash(f"Error deleting juice: {str(e)}", "error")
    finally:
        conn.close()

    return redirect(url_for('user.user_dashboard'))


def get_user_juices(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
    SELECT juices.id, juices.name, juices.price, 
           IFNULL(juices.image_url, '') AS image_url, 
           IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
    FROM juices
    LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
    LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
    WHERE juices.user_id = %s
    GROUP BY juices.id
    ORDER BY juices.created_at DESC
"""
        cursor.execute(query, (user_id,))
        juices = cursor.fetchall()

        return juices
    except Exception as e:
        return []
    finally:
        conn.close()
