# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_db_connection():
#     connection = mysql.connector.connect(
#         host=os.getenv("DB_HOST", "localhost"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASSWORD", ""),
#         database=os.getenv("DB_NAME", "juice_store")
#     )
#     return connection



import mysql.connector
import os
import bcrypt
from dotenv import load_dotenv

# ✅ تحميل بيانات الاتصال من .env
load_dotenv()

def get_db_connection():
    """ إنشاء اتصال بقاعدة البيانات """
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "juice_store")
    )
    return connection

def create_tables():
    """ إنشاء الجداول في قاعدة البيانات """
    conn = get_db_connection()
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
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            quantity INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS juices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
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
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            juice_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (juice_id) REFERENCES juices(id) ON DELETE CASCADE
        )
        """
    ]

    for table in tables:
        cursor.execute(table)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables created successfully!")

def seed_data():
    """ إدخال بيانات تجريبية في الجداول """
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ حذف البيانات القديمة لمنع أخطاء المفتاح الأجنبي
    cursor.execute("DELETE FROM juice_fruits")
    cursor.execute("DELETE FROM order_items")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM juices")
    cursor.execute("DELETE FROM fruits")
    cursor.execute("DELETE FROM users")
    conn.commit()  # ✅ تأكيد الحذف قبل الإدخال الجديد

    # ✅ تشفير كلمات المرور قبل إدخالها في قاعدة البيانات
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # ✅ إدخال بيانات المستخدمين أولًا
    users = [
        ("Ahmed", "ahmed@example.com", hash_password("admin123"), "admin"),
        ("Amr", "amr@example.com", hash_password("amr123"), "user"),
        ("Hashem", "hashem@example.com", hash_password("hashem123"), "user")
    ]
    cursor.executemany("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", users)
    conn.commit()  # ✅ تأكيد الإدخال

    # ✅ جلب معرفات المستخدمين بعد إدخالهم
    cursor.execute("SELECT id FROM users WHERE email = 'ahmed@example.com'")
    admin_result = cursor.fetchone()
    admin_id = admin_result[0] if admin_result else None

    cursor.execute("SELECT id FROM users WHERE email = 'amr@example.com'")
    user1_result = cursor.fetchone()
    user1_id = user1_result[0] if user1_result else None

    cursor.execute("SELECT id FROM users WHERE email = 'hashem@example.com'")
    user2_result = cursor.fetchone()
    user2_id = user2_result[0] if user2_result else None

    if not all([admin_id, user1_id, user2_id]):
        print("❌ Error: One or more users were not inserted correctly!")
        return

    print(f"✅ Users inserted successfully! (Admin ID: {admin_id}, User1 ID: {user1_id}, User2 ID: {user2_id})")

    # ✅ إدخال بيانات الفواكه بعد التأكد من وجود المستخدمين
    fruits = [
        (admin_id, "Apple", 1.5, 50),
        (admin_id, "Banana", 0.8, 100),
        (user1_id, "Strawberry", 2.0, 30),
        (user1_id, "Mango", 2.5, 25)
    ]
    cursor.executemany("INSERT INTO fruits (user_id, name, price, quantity) VALUES (%s, %s, %s, %s)", fruits)

    print("✅ Fruits inserted successfully!")

    # ✅ إدخال بيانات العصائر
    juices = [
        (admin_id, "Mango Juice", 5.0),
        (user1_id, "Strawberry Banana Mix", 6.0)
    ]
    cursor.executemany("INSERT INTO juices (user_id, name, price) VALUES (%s, %s, %s)", juices)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    create_tables() 
    seed_data() 
