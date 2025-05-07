from DbHandler import DatabaseHandler
from Classes.InventorySystem import InventorySystem

class OrderInputService:
    def __init__(self, order):
        self.order = order
        self.db = DatabaseHandler('./DB/OrdersDB.db')
        self.inventory_system = InventorySystem(inventoryID=None, items=order.items)

    def process_order(self):
      
      
        print(list(self.order.items))
        try:
            # Insert order into orders table
            self.db.perform_query("""
                INSERT INTO orders (table_number,staff_id, order_time, status, total_amount) 
                VALUES (?, ?,CURRENT_TIMESTAMP, ?, ?)
            """, (self.order.tableID,self.order.staffID, self.order.status, sum(item["price"] * item["quantity"] for item in self.order.items)))

            # Last OrderID
            order_id = self.db.fetch_one("SELECT last_insert_rowid()")[0]

            # Insert each menu item to order_items
           
            for item in self.order.items:
                self.db.perform_query("""
                    INSERT INTO order_items (order_id, menu_item_id, quantity, status, created_at, updated_at) 
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                """, (order_id, item["itemid"], item["quantity"], "Pending"))

            # Update stock
            self.inventory_system.updateInventory(self.order)

            self.db.close_connection()
            return {"success": True, "message": "Order processed successfully", "order_id": order_id}

        except Exception as e:
            return {"success": False, "error": str(e)}

