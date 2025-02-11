from flask import Blueprint, render_template, session
from database import get_db_connection

home_bp = Blueprint('home', __name__, url_prefix='/', template_folder='../templates')

@home_bp.route('/')
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT juices.id, juices.name, juices.image_url, juices.price, 
                IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
            FROM juices
            LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
            LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
            GROUP BY juices.id
            ORDER BY juices.created_at DESC
        """)
        juices = cursor.fetchall()
    except Exception as e:
        juices = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('home.html', juices=juices, user=session.get('user_name', 'Guest'))
