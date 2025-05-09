from DbHandler import DatabaseHandler



class InventorySystem:
    def __init__(self, inventoryID, items):
        self.inventoryID = inventoryID
        self.items = items
        self.databasehandler = DatabaseHandler('./DB/InventoryDB.db')

    def checkItemAvailability(self):
        pass

    def updateInventory(self, order):
        """Reduce inventory stock based on the ordered items."""
        try:
            for item in order.items:
                self.databasehandler.perform_query("""
                    UPDATE inventory 
                    SET quantity = quantity - ? 
                    WHERE id = ?
                """, (item["quantity"], item["id"]))

            return {"success": True, "message": "Inventory updated successfully"}
        
        except Exception as e:
            return {"success": False, "error": str(e)}

    def getMenuItems(self):
      
        return self.databasehandler.fetch_all("SELECT * FROM menu_items")

