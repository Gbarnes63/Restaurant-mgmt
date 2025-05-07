from Staff import Staff

class KitchenStaff(Staff):
    def __init__(self, staffID, name, isLoggedIn):
        super().__init__(staffID, name, isLoggedIn)

    def viewStock(self):
        pass

    def operation(self):
        pass
