from Staff import Staff

class Waitstaff(Staff):
    def __init__(self, staffID, name, isLoggedIn):
        super().__init__(staffID, name, isLoggedIn)
