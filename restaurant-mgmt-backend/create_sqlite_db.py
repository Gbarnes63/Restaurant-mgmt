import sqlite3
from datetime import datetime

def create_database(db_name='restaurant.db'):
   
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        role VARCHAR(30) NOT NULL,
        email VARCHAR(100) UNIQUE,
        phone VARCHAR(20),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurant_tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number VARCHAR(10),
        capacity INTEGER NOT NULL,
        location VARCHAR(50),
        status VARCHAR(20),
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description TEXT,
        category VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        cost DECIMAL(10,2) NOT NULL,
        is_available BOOLEAN,
        preparation_time INTEGER,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)
    
    cursor.execute("""
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
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        staff_id INTEGER NOT NULL,
        order_time TIMESTAMP,
        status VARCHAR(20),
        total_amount DECIMAL(10,2),
        payment_method VARCHAR(30),
        payment_status VARCHAR(20),
        notes TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        FOREIGN KEY (table_id) REFERENCES restaurant_tables(id),
        FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        menu_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        special_instructions TEXT,
        status VARCHAR(20),
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff_schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id INTEGER NOT NULL,
        shift_date DATE NOT NULL,
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        status VARCHAR(20),
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_id INTEGER NOT NULL,
        customer_name VARCHAR(100) NOT NULL,
        customer_phone VARCHAR(20) NOT NULL,
        customer_email VARCHAR(100),
        reservation_time TIMESTAMP NOT NULL,
        party_size INTEGER NOT NULL,
        status VARCHAR(20),
        special_requests TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inventory_id INTEGER NOT NULL,
        menu_item_id INTEGER,
        quantity_used DECIMAL(10,3) NOT NULL,
        usage_date DATE NOT NULL,
        staff_id INTEGER NOT NULL,
        notes TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (inventory_id) REFERENCES inventory(id),
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id),
        FOREIGN KEY (staff_id) REFERENCES staff(id)
    )
    """)
    
    # Insert some sample data
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Staff
    cursor.executemany("""
    INSERT INTO staff (first_name, last_name, role, email, phone, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        ('John', 'Smith', 'manager', 'john.smith@restaurant.com', '555-0101', current_time, current_time),
        ('Sarah', 'Johnson', 'waiter', 'sarah.j@restaurant.com', '555-0102', current_time, current_time),
        ('Michael', 'Brown', 'chef', 'michael.b@restaurant.com', '555-0103', current_time, current_time)
    ])
    
    # Tables
    cursor.executemany("""
    INSERT INTO restaurant_tables (table_number, capacity, location, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('T1', 4, 'Main Dining', 'available', current_time, current_time),
        ('T2', 6, 'Main Dining', 'available', current_time, current_time),
        ('B1', 2, 'Bar Area', 'available', current_time, current_time)
    ])
    
    # Menu items
    cursor.executemany("""
    INSERT INTO menu_items (name, description, category, price, cost, is_available, preparation_time, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ('Margherita Pizza', 'Classic pizza with tomato sauce and mozzarella', 'Main Course', 12.99, 4.50, 1, 15, current_time, current_time),
        ('Caesar Salad', 'Romaine lettuce with Caesar dressing and croutons', 'Appetizer', 8.99, 2.80, 1, 10, current_time, current_time),
        ('Chocolate Cake', 'Rich chocolate cake with ganache', 'Dessert', 6.99, 1.75, 1, 5, current_time, current_time)
    ])
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print(f"Database '{db_name}' created successfully with sample data!")

if __name__ == "__main__":
    create_database()