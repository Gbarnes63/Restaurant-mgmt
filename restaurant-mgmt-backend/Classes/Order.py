
class Order:
    def __init__(self, orderID, tableID, items, status,staffID):
        self.orderID = orderID
        self.tableID = tableID
        self.staffID = staffID
        self.items = items
        self.status = status