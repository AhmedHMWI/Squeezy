# import os
# from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from database import get_db_connection

home_bp = Blueprint('home', __name__, url_prefix='/', template_folder='../templates')


@home_bp.route('/')
def home():
    """ Fetch all juices and render home page """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query to fetch all juices with their image_url and fruit_names
        cursor.execute("""
            SELECT juices.id, juices.name, juices.image_url, 
                IFNULL(GROUP_CONCAT(DISTINCT fruits.name ORDER BY fruits.name SEPARATOR ', '), 'No fruits selected') AS fruit_names
            FROM juices
            LEFT JOIN juice_fruits ON juices.id = juice_fruits.juice_id
            LEFT JOIN fruits ON juice_fruits.fruit_id = fruits.id
            GROUP BY juices.id
            ORDER BY juices.created_at DESC
        """)
        juices = cursor.fetchall()
    except Exception as e:
        juices = []  # In case of error, ensure juices is an empty list
        print(f"Error fetching juices: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('home.html', juices=juices)
