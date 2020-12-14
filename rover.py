import json


class InventoryItem():
    def __init__(self, type, qty, priority):
        self.type = type
        self.qty = qty
        self.priority = priority


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

    def toDict(self):
        mylist = []
        for item in self.inventory:
            mylist.append(item.__dict__)
        return {
            "location": self.location.__dict__,
            "battery": self.battery,
            "inventory": mylist
        }
