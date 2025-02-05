from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from database import get_db_connection

juice_bp = Blueprint('juice', __name__, url_prefix='/juice')

def get_all_fruits():
    """ Fetch all available fruits from the database """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM fruits")
        fruits = cursor.fetchall()
        # print("✅ Fruits fetched successfully!")  
        return fruits
    except Exception as e:
        print(f"❌ Database Error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

@juice_bp.route('/create_juice', methods=['POST'])
def create_juice():
    """ Create a new juice with selected fruits """
    if 'user_id' not in session:
        flash("❌ Please log in first!", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    name = request.form.get('juice_name')
    fruit_ids = request.form.getlist('selected_fruits[]')


    if not name or not fruit_ids:
        flash("❌ Please select at least one fruit and enter a juice name.", "danger")
        return redirect(url_for('user.user_dashboard'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if the user exists before inserting the juice
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            # print("❌ Invalid user_id:", user_id)
            # flash("❌ User does not exist!", "danger")
            return redirect(url_for('user.user_dashboard'))

        # Insert juice into the database
        cursor.execute("INSERT INTO juices (user_id, name, price) VALUES (%s, %s, 0)", (user_id, name))
        juice_id = cursor.lastrowid

        if not juice_id:
            raise ValueError("❌ Failed to retrieve `lastrowid` after inserting juice!")

        total_price = 0
        for fruit_id in fruit_ids:
            cursor.execute("SELECT price FROM fruits WHERE id = %s", (fruit_id,))
            fruit_price = cursor.fetchone()

            if not fruit_price or fruit_price['price'] is None:
                print(f"⚠️ Skipping fruit_id {fruit_id}, price not found")
                continue  # Skip if price is not found

            total_price += fruit_price['price']
            cursor.execute("INSERT INTO juice_fruits (juice_id, fruit_id, quantity) VALUES (%s, %s, %s)", (juice_id, fruit_id, 1))

        cursor.execute("UPDATE juices SET price = %s WHERE id = %s", (total_price, juice_id))
        conn.commit()

        print(f"✅ Juice Created: {name}, Total Price: {total_price}")  # Debugging
        flash("✅ Your juice has been created successfully!", "success")

    except Exception as e:
        print(f"❌ Error creating juice: {str(e)}")  # Debugging error
        flash(f"❌ Error creating juice: {str(e)}", "error")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return redirect(url_for('user.user_dashboard'))
