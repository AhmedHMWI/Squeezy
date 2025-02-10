import os
import mysql.connector
import bcrypt
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

def get_db_connection():
    """ ✅ Create and return a database connection """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "juice_store"),
        )
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None  # ✅ Return None instead of breaking the app

def create_tables():
    """ ✅ Create necessary tables in the database """
    conn = get_db_connection()
    if not conn:
        print("❌ Unable to connect to database. Tables were not created.")
        return
    
    cursor = conn.cursor()
    tables = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'user') DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS fruits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(100) NOT NULL UNIQUE,  -- Ensure fruit name is unique
            price DECIMAL(10,2) NOT NULL,
            quantity INT NOT NULL,
            image_url VARCHAR(255) UNIQUE,  -- Ensure image_url is unique for fruits
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS juices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(100) NOT NULL UNIQUE,  -- Ensure juice name is unique
            price DECIMAL(10,2) NOT NULL,
            image_url VARCHAR(255) UNIQUE,  -- Ensure image_url is unique for juices
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS juice_fruits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            juice_id INT NOT NULL,
            fruit_id INT NOT NULL,
            quantity INT NOT NULL,
            FOREIGN KEY (juice_id) REFERENCES juices(id) ON DELETE CASCADE,
            FOREIGN KEY (fruit_id) REFERENCES fruits(id) ON DELETE CASCADE
        )
        """
    ]
    
    try:
        for table in tables:
            cursor.execute(table)
        conn.commit()
        print("✅ Tables created successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()

def seed_data():
    """ ✅ Insert initial test data into the database """
    conn = get_db_connection()
    if not conn:
        print("❌ Unable to connect to database. Seeding data failed.")
        return
    
    cursor = conn.cursor()

    try:
        # ✅ Delete existing data (to prevent foreign key issues)
        cursor.execute("DELETE FROM juice_fruits")
        cursor.execute("DELETE FROM order_items")
        cursor.execute("DELETE FROM orders")
        cursor.execute("DELETE FROM juices")
        cursor.execute("DELETE FROM fruits")
        cursor.execute("DELETE FROM users")
        conn.commit()

        # ✅ Hash passwords securely
        def hash_password(password):
            return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # ✅ Insert users
        users = [
            ("Ahmed", "ahmed@example.com", hash_password("admin123"), "admin"),
            ("Amr", "amr@example.com", hash_password("amr123"), "user"),
            ("Hashem", "hashem@example.com", hash_password("hashem123"), "user")
        ]
        cursor.executemany("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", users)
        conn.commit()

        # ✅ Get user IDs
        cursor.execute("SELECT id, email FROM users")
        user_data = {email: user_id for user_id, email in cursor.fetchall()}

        admin_id = user_data.get("ahmed@example.com")
        user1_id = user_data.get("amr@example.com")
        user2_id = user_data.get("hashem@example.com")

        if not all([admin_id, user1_id, user2_id]):
            print("❌ Error: User insertion failed!")
            return

        print(f"✅ Users inserted successfully! (Admin: {admin_id}, User1: {user1_id}, User2: {user2_id})")

        # ✅ Insert fruits
        fruits = [
            (admin_id, "Apple", 1.5, 50),
            (admin_id, "Banana", 0.8, 100),
            (user1_id, "Strawberry", 2.0, 30),
            (user1_id, "Mango", 2.5, 25)
        ]
        cursor.executemany("INSERT INTO fruits (user_id, name, price, quantity) VALUES (%s, %s, %s, %s)", fruits)
        conn.commit()

        print("✅ Fruits inserted successfully!")

        # ✅ Insert juices
        juices = [
            (admin_id, "Mango Juice", 5.0),
            (user1_id, "Strawberry Banana Mix", 6.0)
        ]
        cursor.executemany("INSERT INTO juices (user_id, name, price) VALUES (%s, %s, %s)", juices)
        conn.commit()

        print("✅ Juices inserted successfully!")

        # Get all juice and fruit IDs for creating juice_fruits
        cursor.execute("SELECT id FROM juices WHERE user_id IN (%s, %s, %s)", (admin_id, user1_id, user2_id))
        juice_ids = [juice[0] for juice in cursor.fetchall()]  # Use index 0 since fetchall returns tuples

        cursor.execute("SELECT id FROM fruits WHERE user_id IN (%s, %s, %s)", (admin_id, user1_id, user2_id))
        fruit_ids = [fruit[0] for fruit in cursor.fetchall()]  # Use index 0 since fetchall returns tuples

        # ✅ Insert juice_fruits (using valid juice_id and fruit_id)
        juice_fruits = []
        for juice_id in juice_ids:
            for fruit_id in fruit_ids:
                juice_fruits.append((juice_id, fruit_id, 1))

        cursor.executemany("INSERT INTO juice_fruits (juice_id, fruit_id, quantity) VALUES (%s, %s, %s)", juice_fruits)
        conn.commit()

        print("✅ Juice fruits inserted successfully!")

    except mysql.connector.Error as e:
        print(f"❌ Database Error while seeding: {e}")
    finally:
        cursor.close()
        conn.close()




if __name__ == "__main__":
    create_tables() 
    seed_data() 
