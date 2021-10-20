from datetime import datetime as dt
from models.Item import Item,WeightItem,UnitItem
from typing import List
class Cart:
    def __init__(self):
        # purchase time should be the time that the customer pay for this cart
        # update later togther with payment process 
        self.__purchaseTime = None
        self.__itmes:List[Item] = []
        self.__clubPoint = 0.00
        self.__cartValue = 0.00
    
    # all the properties are not suposed to be changed directly from outside
    # methods to deal with them will be provided 
    @property
    def purchaseTime(self):
        return self.__purchaseTime
    @property
    def items(self):
        return self.__itmes
    @property
    def clubPoint(self):
        return self.__clubPoint
    @property
    def cartValue(self):
        return self.__cartValue
    
    # method used to add an item instance to items list
    # value and club point created by the item will also be calculated and then be added to the properties
    def addItem(self,item:Item) -> str:
        self.__itmes.append(item)
        self.__cartValue = round(self.__cartValue+item.getItemPrice(),2) 

        return item.itemDetail()

    def checkout(self)->None:
        self.__purchaseTime = dt.now().strftime("%d/%m/%Y %H:%M:%S")
        self.__clubPoint = round(self.cartValue/10,2) 

    # method used to get cart detail information
    def cartDetails(self)->str:
        info = f'{self.purchaseTime} Consumption: ${self.cartValue} Clubpoint:{self.__clubPoint}\n'
        for i in self.items:
            info += f'----{i.itemDetail()}\n'
        return info