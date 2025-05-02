from DbHandler import DatabaseHandler
from datetime import datetime

def create_logins_db():
    """Create the LoginsDB database and initialize the staff_login table."""
    db = DatabaseHandler(db_name="./DB/LoginsDB.db")

    # Create Staff Login table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS staff_login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER NOT NULL,
        username VARCHAR(50) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert mock login data
    login_mock_data = [
        (1, "john_doe", "hashed_password_1"),
        (2, "alice_smith", "hashed_password_2"),
        (3, "robert_jones", "hashed_password_3"),
        (4, "emma_wilson", "hashed_password_4"),
        (5, "mark_taylor", "hashed_password_5")
    ]

    for login in login_mock_data:
        db.perform_query("""
        INSERT INTO staff_login (staff_id, username, password_hash) 
        VALUES (?, ?, ?)
        """, login)

    # Fetch and display mock login data
    print("Staff Logins:", db.fetch_all("SELECT * FROM staff_login"))

    db.close_connection()
    print("LoginsDB setup complete with mock data!")

def create_orders_db():
    """Create the OrdersDB database and initialize the orders table."""
    db = DatabaseHandler(db_name="./DB/OrdersDB.db")

    # Create Orders table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        staff_id INTEGER NOT NULL,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20) NOT NULL,
        total_amount DECIMAL(10,2),
        payment_method VARCHAR(30),
        payment_status VARCHAR(20),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert mock order data
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    orders_mock_data = [
        (1, 2, current_time, "Completed", 45.99, "Credit Card", "Paid", "No special requests"),
        (2, 4, current_time, "Pending", 32.50, "Cash", "Unpaid", "Extra sauce"),
        (3, 1, current_time, "Preparing", 27.40, "Credit Card", "Paid", "Vegetarian option"),
        (4, 3, current_time, "Completed", 19.99, "Cash", "Paid", "Spicy level high"),
        (5, 5, current_time, "Pending", 60.75, "Credit Card", "Unpaid", "Gluten-free request")
    ]

    for order in orders_mock_data:
        db.perform_query("""
        INSERT INTO orders (table_id, staff_id, order_time, status, total_amount, payment_method, payment_status, notes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, order)

    # Fetch and display mock orders
    print("Orders:", db.fetch_all("SELECT * FROM orders"))

    db.close_connection()
    print("OrdersDB setup complete with mock data!")

if __name__ == "__main__":
    create_logins_db()
    create_orders_db()
