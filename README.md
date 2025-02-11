# Squeezy Project

## Description
This project is a web-based application for managing a juice store. Users can create, edit, and delete juices and fruit selections, while administrators can manage fruit and juice data. The project is built using Flask, MySQL, and supports user authentication.

## Features
- User login and registration
- Fruit creation, modification, and deletion by admin
- Juice creation, modification, and deletion by users and admin
- Admin role with the ability to manage fruits and juices
- Image upload for juices and fruits
- View and manage complaints

## Tech Stack
- **Backend**: Flask (Python web framework)
- **Database**: MySQL
- **Frontend**: HTML, CSS (Bootstrap for responsive layout)
- **Authentication**: Session-based with Flask sessions
- **Image Uploads**: Handled by Werkzeug for secure file handling

## Setup Instructions

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.x
- pip
- MySQL
- Virtualenv (optional but recommended)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AhmedHMWI/Squeezy.git
    cd squeezy
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the MySQL database:
    - Create a `.env` file at the root of the project.
    - Add your database configuration:
    ```bash
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=password
    DB_NAME=juice_store
    ```

5. Run the database schema setup:
    ```bash
    python init_db.py
    ```

6. Run the Flask application:
    ```bash
    flask run
    ```

7. Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

### File Structure
- `app.py`: The main entry point for the Flask application.
- `models/`: Contains the model files (e.g., `complaints.py`).
- `controllers/`: Contains the model files (e.g., `admin_controller.py`, `user_controller.py`, `auth_controller.py`).
- `templates/`: Contains HTML files for rendering views.
- `static/`: Contains static assets (CSS, images, JavaScript).
- `.env`: Environment variables for database configuration.
- `requirements.txt`: Python dependencies for the project.

## Usage

### Authentication
- Users can register and log in using their email and password.
- Admin users have extra privileges to manage fruit and juice data.

### Juice Management
- Users can create juices by selecting fruits and entering a name and image.
- Users can edit or delete their created juices.
- Admin users can manage all juices and fruits (add, edit, delete).

### Complaints
- Users can submit complaints or suggestions that are stored in the database.
- Admin users can view and manage all complaints.

## Contributions
If you'd like to contribute to the project, feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- Special thanks to Flask and MySQL for providing the tools needed to create this application.
