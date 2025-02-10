from flask import render_template, Blueprint, session, request, flash, redirect, url_for
from models.complaints import Complaint

complaints_bp = Blueprint('complaints', __name__, url_prefix='/complaints', template_folder='../templates')

@complaints_bp.route('/submit_complaint', methods=['GET', 'POST'])
def submit_complaint():
    user_name = session.get('user_name', 'Guest')  # Get user name from session, or default to 'Guest' if not logged in

    if request.method == 'POST':
        # Get the values from the form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Check if all required fields are filled
        if not name or not email or not message:
            flash("❌ All fields are required. Please fill in all fields.", "error")
            return redirect(url_for('complaints.submit_complaint'))

        # Create a new complaint object and save it
        complaint = Complaint(name, email, message)
        complaint.save_complaint()

        flash("Thank you for your complaint or suggestion! We will review it shortly.", "info")
        return redirect(url_for('complaints.view_complaints'))

    # If it's a GET request, just render the complaint form
    return render_template('complaint.html', user_name=user_name)

@complaints_bp.route('/view_complaints', methods=['GET'])
def view_complaints():
    user_name = session.get('user_name', 'Guest')  # Get user name from session, or default to 'Guest'
    complaints = Complaint.get_complaints()
    return render_template('view_complaints.html', complaints=complaints, user_name=user_name)
