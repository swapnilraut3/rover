import json


class InventoryItem():
    def __init__(self, type, qty, priority):
        self.type = type
        self.qty = qty
        self.priority = priority

    # def __str__(self):
    #     return f'''Type: {self.type}
    #     qty: {self.qty}
    #     priority: {self.priority}'''


class Location():
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Rover():
    def __init__(self, location, battery, inventory):
        self.location = Location(row=location.get(
            'row'), column=location.get('column'))
        self.battery = battery
        self.inventory = []
        for item in inventory:
            singleInventoryItem = InventoryItem(
                item.get('type'), item.get('quantity'), item.get('priority'))
            self.inventory.append(singleInventoryItem)

    # def __str__(self):
    #     mystr = []
    #     for item in self.inventory:
    #         mystr.append(item.__str__())
    #     return f'''This is really good rover. 
    #     Current location is: {self.location}
    #     Battery Level is: {self.battery}
    #     Inventory is: {mystr}
    #     '''

    def toDict(self):
        mylist = []
        for item in self.inventory:
            mylist.append(item.__dict__)
        return {
            "location": self.location.__dict__,
            "battery": self.battery,
            "inventory": mylist
        }
