from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


def get_all_fruits():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, price, quantity FROM fruits") 
    fruits = cursor.fetchall()
    conn.close()
    return fruits


@admin_bp.route('/dashboard')
def admin_dashboard():
    fruits = get_all_fruits() 
    return render_template('admin_dashboard.html', fruits=fruits)





@admin_bp.route('/add_fruit', methods=['POST'])
def add_fruit():
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO fruits (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
    conn.commit()

    conn.close()
    flash("Fruit added successfully!", "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/edit_fruit/<int:fruit_id>', methods=['GET', 'POST'])
def edit_fruit(fruit_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM fruits WHERE id = %s", (fruit_id,))
        fruit = cursor.fetchone()
        conn.close()
        if fruit:
            return render_template('edit_fruit.html', fruit=fruit)
        else:
            flash("Fruit not found!", "error")
            return redirect(url_for('admin.admin_dashboard'))

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = request.form.get('quantity')

            if not name or not price or not quantity:
                flash("⚠️ All fields are required!", "error")
                return redirect(url_for('admin.edit_fruit', fruit_id=fruit_id))

            cursor.execute("UPDATE fruits SET name = %s, price = %s, quantity = %s WHERE id = %s",
                           (name, price, quantity, fruit_id))
            conn.commit()
            conn.close()

            flash("Fruit updated successfully!", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f" Error updating fruit: {str(e)}", "error")
            return redirect(url_for('admin.edit_fruit', fruit_id=fruit_id))

@admin_bp.route('/delete_fruit/<int:fruit_id>', methods=['POST'])
def delete_fruit(fruit_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM fruits WHERE id=%s", (fruit_id,))
    conn.commit()

    conn.close()
    flash("Fruit deleted successfully!", "danger")
    return redirect(url_for('admin.admin_dashboard'))