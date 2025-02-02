from flask import Flask, render_template, redirect, url_for, session
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp

app = Flask(__name__)
app.secret_key = "super_secret_key"

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

@app.route('/dashboard/admin')
def admin_dashboard():
    if 'user_id' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html', user=session['user_name'])
    return redirect(url_for('auth.login'))

@app.route('/dashboard/user')
def user_dashboard():
    if 'user_id' in session and session['role'] == 'user':
        return render_template('user_dashboard.html', user=session['user_name'])
    return redirect(url_for('auth.login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
