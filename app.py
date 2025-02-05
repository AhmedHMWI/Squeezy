import os
import sys
from flask import Flask, render_template, redirect, url_for, flash, session, send_from_directory
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.user_controller import user_bp
from controllers.juice_controller import juice_bp

from database import get_db_connection
from dotenv import load_dotenv

# Ensure UTF-8 Encoding for Console Output
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super_secret_key")  # Using a secure secret key

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(juice_bp, url_prefix='/juice')


@app.route('/')
def index():
    """Redirect to user home or login if not logged in."""
    if 'user_id' in session:
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('auth.login'))


@app.route('/dashboard/user')
def user_dashboard():
    """User dashboard"""
    if 'user_id' not in session or session.get('role') != 'user':
        flash("Please log in first!", "error")
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch juices created by the user
        cursor.execute("SELECT * FROM juices WHERE user_id = %s", (session['user_id'],))
        juices = cursor.fetchall()

        # Fetch available fruits for juice creation
        cursor.execute("SELECT * FROM fruits")
        fruits = cursor.fetchall()

    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
        return redirect(url_for('auth.login'))

    finally:
        cursor.close()
        conn.close()

    return render_template('user_dashboard.html', user=session.get('user_name', 'User'), juices=juices, fruits=fruits)


@app.route('/logout')
def logout():
    """ Logout and clear session """
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for('auth.login'))


@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """ Securely Serve Uploaded Files """
    uploads_dir = os.path.abspath(os.path.join('static', 'uploads'))
    return send_from_directory(uploads_dir, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
