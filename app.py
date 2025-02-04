import os
import sys
from flask import Flask, render_template, redirect, url_for, flash, session, send_from_directory
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.user_controller import user_bp
from controllers.juice_controller import juice_bp

from database import get_db_connection
from dotenv import load_dotenv
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
def home():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('user.user_dashboard'))  
    return redirect(url_for('auth.login'))

@app.route('/dashboard/user')
def user_dashboard():
    """ User dashboard """
    if 'user_id' in session and session['role'] == 'user':
        return render_template('user_dashboard.html', user=session.get('user_name', 'User'))
    
    flash("Please log in first!", "error")
    return redirect(url_for('auth.login'))

@app.route('/logout')
def logout():
    """ Logout and clear session """
    session.clear()
    flash("You have been logged out!", "info")
    return redirect(url_for('auth.login'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """ Serve uploaded files """
    uploads_dir = os.path.join('static', 'uploads')
    return send_from_directory(uploads_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
