import os
import sys
from flask import Flask, send_from_directory
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.user_controller import user_bp
from controllers.home_controller import home_bp
from controllers.complaints_controller import complaints_bp

from dotenv import load_dotenv

# Ensure UTF-8 Encoding for Console Output
sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Using a secure secret key
app.secret_key = os.getenv("SECRET_KEY", "super_secret_key")

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(home_bp, url_prefix='/')
app.register_blueprint(complaints_bp, url_prefix='/complaints')

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """ Securely Serve Uploaded Files """
    uploads_dir = os.path.abspath(os.path.join('static', 'uploads'))
    return send_from_directory(uploads_dir, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
