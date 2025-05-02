import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="default.db"):
   
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def perform_query(self, query, params=()):
        
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def fetch_all(self, query, params=()):
      
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=()):
      
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
