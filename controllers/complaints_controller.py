from flask import render_template, Blueprint, session, request, flash, redirect, url_for
from models.complaints import Complaint

complaints_bp = Blueprint('complaints', __name__, url_prefix='/complaints', template_folder='../templates')

@complaints_bp.route('/submit_complaint', methods=['GET', 'POST'])
def submit_complaint():
    user_name = session.get('user_name', 'Guest')

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not name or not email or not message:
            flash("All fields are required. Please fill in all fields.", "error")
            return redirect(url_for('complaints.submit_complaint'))

        complaint = Complaint(name, email, message)
        complaint.save_complaint()

        flash("Thank you for your complaint or suggestion! We will review it shortly.", "info")
        return redirect(url_for('home.home'))

    return render_template('complaint.html', user_name=user_name)

@complaints_bp.route('/view_complaints', methods=['GET'])
def view_complaints():
    if session.get('role') != 'admin':
        flash("You don't have permission to view this page.", "error")
        return redirect(url_for('home.home'))

    user_name = session.get('user_name', 'Guest')
    complaints = Complaint.get_complaints()
    return render_template('view_complaints.html', complaints=complaints, user_name=user_name)
