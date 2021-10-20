from abc import ABC, abstractmethod
import random
class Item(ABC):
    def __init__(self, name:str,unitPrice:float):
        self.__name = name
        self.__unitPrice = unitPrice
        self.__itemPrice = None

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,value):
        self.__name = value
    @property
    def unitPrice(self):
        return self.__unitPrice
    @unitPrice.setter
    def unitPrice(self,value):
        self.__unitPrice = value
    @property
    def itemPrice(self):
        return self.__itemPrice
    @unitPrice.setter
    def itemPrice(self,value):
        self.__itemPrice = value

    # method used to ge item details
    @abstractmethod
    def itemDetail(self):
        pass
    # abstract method to calculate item price 
    @abstractmethod
    def getItemPrice(self):
        pass

class UnitItem(Item):
    def __init__(self, name: str, unitPrice: float,quantity:int):
        self.__quantity = quantity
        super().__init__(name, unitPrice)
    
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self,value):
        self.__quantity = value
    # overwrite method to calculate unititems cost
    def getItemPrice(self)->float:
        return round(self.quantity * self.unitPrice,2)
    def itemDetail(self)->str:
        price = self.getItemPrice()
        return f'Product: {self.name}, ${self.unitPrice}, {self.quantity}, ${price}'

class WeightItem(Item):
    def __init__(self, name: str, unitPrice: float):
        self.__weight = self.__scale()
        super().__init__(name, unitPrice)
    
    @property
    def weight(self):
        return self.__weight
    @weight.setter
    def weight(self,value):
        self.__weight = value

    # rewrite method to calculate weightitems cost
    def getItemPrice(self)->float:
        return round(self.weight * self.unitPrice,2) 
    
    def __scale(self):
        return round(random.uniform(0,4),2) 

    def itemDetail(self)->str:
        price = self.getItemPrice()
        return f'Product: {self.name}, ${self.unitPrice}/kilo, {self.weight} kilo, ${price}'

if __name__ == "__main__":
    a = round(0.66,5)
    print(a)
