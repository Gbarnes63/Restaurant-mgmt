from DbHandler import DatabaseHandler



class InventorySystem:
    def __init__(self, inventoryID, items):
        self.inventoryID = inventoryID
        self.items = items
        self.databasehandler = DatabaseHandler('./DB/InventoryDB.db')

    def checkItemAvailability(self):
        pass

    def updateInventory(self):
        pass

    def getMenuItems(self):
        print('i was called')
        return self.databasehandler.fetch_all("SELECT * FROM menu_items")

