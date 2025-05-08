from DbHandler import DatabaseHandler
from Classes.InventorySystem import InventorySystem

class OrderInputService:
    def __init__(self, order=None):
        self.order = order
        self.db = DatabaseHandler('./DB/OrdersDB.db')
        self.inventory_system = InventorySystem(inventoryID=None, items=order.items if order else [])

    def process_order(self):
      
      
        print(list(self.order.items))
        try:
            # Insert order into orders table
            self.db.perform_query("""
                INSERT INTO orders (table_number,staff_id, order_time, status, total_amount)
                VALUES (?, ?,CURRENT_TIMESTAMP, ?, ?)
            """, (self.order.tableID, self.order.staffID, self.order.status, sum(item["price"] * item["quantity"] for item in self.order.items)))

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


    def get_order(self, order_id):
        try:
            
            if not order_id:
                orders_data = self.db.fetch_all("""
                    SELECT
                        o.id AS order_id,
                        o.order_time,
                        o.table_number,
                        o.staff_id,
                        o.status,
                        o.total_amount,
                        GROUP_CONCAT(mi.name || ' (' || oi.quantity || ')') AS items
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                    GROUP BY o.id
                    ORDER BY o.order_time DESC
                """)
              
                if orders_data is not None:
                    orders_list = []
                    columns = ["order_id", "order_time", "table_number", "staff_id", "status", "total_amount", "items"]
                    for row in orders_data:
                        orders_list.append(dict(zip(columns, row)))
                    return {"success": True, "orders": orders_list}
                else:
                    return {"success": False, "error": "No orders found"}
            else:
                order_data = self.db.fetch_one("""
                    SELECT
                        o.id AS order_id,
                        o.order_time,
                        o.table_number,
                        o.staff_id,
                        o.status,
                        o.total_amount,
                        o.payment_method,
                        o.payment_status,
                        o.notes,
                        GROUP_CONCAT(mi.name || ' (' || oi.quantity || ')') AS items
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
                    WHERE o.id = ?
                    GROUP BY o.id
                """, (order_id,))
           
                if order_data:
                    columns = ["order_id", "order_time", "table_number", "staff_id", "status", "total_amount", "payment_method", "payment_status", "notes", "items"]
                    order_dict = dict(zip(columns, order_data))
                    return {"success": True, "order": order_dict}
                else:
                    return {"success": False, "error": f"Order with ID {order_id} not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}