from DbHandler import DatabaseHandler
from datetime import datetime

def create_logins_db():
    """Create the LoginsDB database and initialize the staff_login table."""
    db = DatabaseHandler(db_name="./DB/LoginsDB.db")

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

    print("Staff Logins:", db.fetch_all("SELECT * FROM staff_login"))
    db.close_connection()
    print("LoginsDB setup complete with mock data!")

def create_orders_db():
    """Create the OrdersDB database and initialize the orders table."""
    db = DatabaseHandler(db_name="./DB/OrdersDB.db")

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

    print("Orders:", db.fetch_all("SELECT * FROM orders"))
    db.close_connection()
    print("OrdersDB setup complete with mock data!")

def create_inventory_db():
    """Create the InventoryDB database and initialize inventory tables."""
    db = DatabaseHandler(db_name="./DB/InventoryDB.db")

    db.perform_query("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL,
        quantity DECIMAL(10,3) NOT NULL,
        unit VARCHAR(20) NOT NULL,
        supplier VARCHAR(100),
        last_restock_date DATE,
        next_restock_date DATE,
        min_quantity DECIMAL(10,3) NOT NULL,
        status VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    db.perform_query("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        cost DECIMAL(10,2) NOT NULL,
        is_available BOOLEAN,
        preparation_time INTEGER,
        inventory_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (inventory_id) REFERENCES inventory(id)
    )
    """)

    db.perform_query("""
    CREATE TABLE IF NOT EXISTS inventory_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inventory_id INTEGER NOT NULL,
        menu_item_id INTEGER,
        quantity_used DECIMAL(10,3) NOT NULL,
        usage_date DATE NOT NULL,
        staff_id INTEGER NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (inventory_id) REFERENCES inventory(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    )
    """)

    current_time = datetime.now().strftime('%Y-%m-%d')
    inventory_mock_data = [
        ("Flour", "Baking", 50, "kg", "BestSupplier Ltd.", current_time, "2025-06-01", 10, "Available"),
        ("Tomatoes", "Vegetables", 100, "kg", "Green Farms", current_time, "2025-05-15", 20, "Available"),
        ("Chicken Breast", "Meat", 80, "kg", "MeatCo", current_time, "2025-05-10", 15, "Available"),
        ("Cheese", "Dairy", 30, "kg", "DairyDelight", current_time, "2025-05-20", 5, "Low Stock"),
        ("Olive Oil", "Condiments", 25, "liters", "OilMasters", current_time, "2025-07-01", 5, "Available")
    ]

    menu_mock_data = [
        ("Margherita Pizza", "Classic tomato sauce & mozzarella", "Main Course", 12.99, 4.50, 1, 15, 1),
        ("Caesar Salad", "Romaine lettuce & croutons", "Appetizer", 8.99, 2.80, 1, 10, 2),
        ("Chocolate Cake", "Rich chocolate ganache", "Dessert", 6.99, 1.75, 1, 5, 3),
        ("Grilled Salmon", "Served with lemon butter sauce", "Main Course", 18.99, 7.00, 1, 20, 4),
        ("Iced Tea", "Fresh brewed iced tea", "Drinks", 3.99, 0.75, 1, 2, 5)
    ]

    for inventory in inventory_mock_data:
        db.perform_query("""
        INSERT INTO inventory (item_name, category, quantity, unit, supplier, last_restock_date, next_restock_date, min_quantity, status) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, inventory)

    for menu_item in menu_mock_data:
        db.perform_query("""
        INSERT INTO menu_items (name, description, category, price, cost, is_available, preparation_time, inventory_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, menu_item)

    print("Inventory Items:", db.fetch_all("SELECT * FROM inventory"))
    print("Menu Items:", db.fetch_all("SELECT * FROM menu_items"))

    db.close_connection()
    print("InventoryDB setup complete with mock data!")

if __name__ == "__main__":
    create_logins_db()
    create_orders_db()
    create_inventory_db()
