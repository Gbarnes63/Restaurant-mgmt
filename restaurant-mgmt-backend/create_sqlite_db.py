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
    """Create the OrdersDB database and initialize the tables, including menu_items."""
    db = DatabaseHandler(db_name="./DB/OrdersDB.db")

    # Create Restaurant Tables table with table_number as the primary key
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS restaurant_tables (
        table_number INTEGER PRIMARY KEY,
        description TEXT,
        location TEXT,
        capacity INTEGER NOT NULL
    )
    """)

    # Insert mock restaurant tables data
    restaurant_tables_mock_data = [
        (1, "Window-side table", "Near entrance", 4),
        (2, "Cozy corner booth", "Back section", 6),
        (3, "Patio seating", "Outdoor area", 2),
        (4, "Large family table", "Center area", 8),
        (5, "Bar counter seat", "Near bar", 1)
    ]

    for table in restaurant_tables_mock_data:
        db.perform_query("""
        INSERT INTO restaurant_tables (table_number, description, location, capacity)
        VALUES (?, ?, ?, ?)
        """, table)

    # Create Staff table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        contact_info TEXT,
        hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert mock staff data
    staff_mock_data = [
        ("Alice Johnson", "Manager", "alice@example.com"),
        ("Bob Smith", "Chef", "bob@example.com"),
        ("Charlie Davis", "Waiter", "charlie@example.com"),
        ("Diana Lee", "Bartender", "diana@example.com"),
        ("Edward Wilson", "Host", "edward@example.com")
    ]

    for staff_member in staff_mock_data:
        db.perform_query("""
        INSERT INTO staff (name, role, contact_info)
        VALUES (?, ?, ?)
        """, staff_member)

    # Create Menu Items table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        price DECIMAL(10, 2) NOT NULL,
        category TEXT
    )
    """)

    # Insert mock menu items data
    menu_items_mock_data = [
        ("Margherita Pizza", "Classic pizza with tomato, mozzarella, and basil", 12.99, "Pizza"),
        ("Pepperoni Pizza", "Pizza with tomato sauce, mozzarella, and pepperoni", 14.99, "Pizza"),
        ("Caesar Salad", "Romaine lettuce, croutons, parmesan cheese, and Caesar dressing", 8.99, "Salads"),
        ("Greek Salad", "Tomatoes, cucumbers, onions, olives, and feta cheese", 9.50, "Salads"),
        ("Burger", "Beef patty with lettuce, tomato, onion, and cheese on a bun", 10.50, "Burgers"),
        ("Fries", "Crispy golden french fries", 4.50, "Sides"),
        ("Coke", "Coca-Cola soft drink", 2.50, "Drinks"),
        ("Water", "Bottled still water", 1.50, "Drinks"),
        ("Pasta Carbonara", "Spaghetti with eggs, cheese, pancetta, and black pepper", 13.75, "Pasta"),
        ("Garlic Bread", "Toasted bread with garlic and butter", 5.25, "Sides")
    ]

    for item in menu_items_mock_data:
        db.perform_query("""
        INSERT INTO menu_items (name, description, price, category)
        VALUES (?, ?, ?, ?)
        """, item)

    # Create Orders table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number INTEGER NOT NULL,
        staff_id INTEGER NOT NULL,
        order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(20),
        total_amount DECIMAL(10,2),
        payment_method VARCHAR(30),
        payment_status VARCHAR(20),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (table_number) REFERENCES restaurant_tables(table_number),
        FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
    """)

    # Create Order Items table
    db.perform_query("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        menu_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        special_instructions TEXT,
        status VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    )
    """)

    # Insert mock orders data
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    orders_mock_data = [
        (3, 2, current_time, "Completed", 45.99, "Credit Card", "Paid", "No special requests"),
        (4, 4, current_time, "Pending", 32.50, "Cash", "Unpaid", "Extra sauce"),
        (1, 1, current_time, "Preparing", 27.40, "Credit Card", "Paid", "Vegetarian option"),
        (2, 3, current_time, "Completed", 19.99, "Cash", "Paid", "Spicy level high"),
        (5, 5, current_time, "Pending", 60.75, "Credit Card", "Unpaid", "Gluten-free request")
    ]

    for order in orders_mock_data:
        db.perform_query("""
        INSERT INTO orders (table_number, staff_id, order_time, status, total_amount, payment_method, payment_status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, order)

    # Insert mock order items data (linking orders to menu items)
    order_items_mock_data = [
        (1, 1, 2, None, "Completed"),  # Order 1: 2 x Margherita Pizza
        (1, 6, 1, None, "Completed"),  # Order 1: 1 x Fries
        (2, 3, 1, "No croutons", "Pending"), # Order 2: 1 x Caesar Salad
        (2, 7, 2, None, "Pending"),  # Order 2: 2 x Coke
        (3, 5, 1, "Well-done", "Preparing"), # Order 3: 1 x Burger
        (3, 10, 1, None, "Preparing"), # Order 3: 1 x Garlic Bread
        (4, 9, 1, "Extra parmesan", "Completed"), # Order 4: 1 x Pasta Carbonara
        (5, 2, 1, None, "Pending"),  # Order 5: 1 x Pepperoni Pizza
        (5, 4, 2, None, "Pending")   # Order 5: 2 x Greek Salad
    ]

    for item in order_items_mock_data:
        db.perform_query("""
        INSERT INTO order_items (order_id, menu_item_id, quantity, special_instructions, status)
        VALUES (?, ?, ?, ?, ?)
        """, item)

    db.close_connection()
    print("OrdersDB setup complete with menu_items and mock data!")


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
