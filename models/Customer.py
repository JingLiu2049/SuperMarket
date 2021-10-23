from typing import List
from models.Cart import Cart
from models.Error import CustError
class Customer:
    CARDNO = 10000
    def __init__(self,name:str):
        Customer.CARDNO +=1
        self.__cardID = Customer.CARDNO
        self.__name = name
        self.__totalClubPoints = 0
        self.__totalValue = 0
        self.__currentCart = None
        self.__historyCarts:List[Cart] = []
    
    

    
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name

    # following properties are not suposed to be changed from outside, 
    # will provide methods to deal with them
    @property
    def cardID(self):
        return self.__cardID
    
    @property
    def clubPoints(self):
        return self.__totalClubPoints
    
    @property
    def totalValue(self):
        return self.__totalValue


    @property
    def currentCart(self):
        return self.__currentCart

    @property
    def historyCarts(self):
        return self.__historyCarts

    # method used to get customer information
    def customerDetail(self) ->str: 
        info = self.getCustTitle()
        for cart in self.historyCarts:
            info += f'{cart.cartDetails()}' 
        return info
    
    def getCustTitle(self)->str:
        info = f"Customer name: {self.name}, Club ID: {self.cardID}, Club points: {self.clubPoints}, Total consumption: ${self.__totalValue}\n"
        return  info

    def getAverage(self) ->float:
        try:
            avg = round(self.totalValue/self.calCarts(),2)
        except ZeroDivisionError:
            avg = 0
        return avg
    def calCarts(self) ->int:
        return len(self.historyCarts)
    # method used to add a cart instance to a customer as the property currentCart
    # a customer would always have only one cart before they pay
    def startShopping(self):
        if not self.currentCart:
            cart = Cart()
            self.__currentCart = cart
        elif self.currentCart.items:
            raise CustError()
        
    # method used to move the current cart to history cart list after customers paid 
    # total purchase and total club points update would also be executed here
    def checkout(self) -> Cart:
        self.currentCart.checkout()
        cart = self.currentCart
        if len(cart.items)!=0:
            self.__totalValue = round(self.__totalValue+ cart.cartValue,2) 
            self.__totalClubPoints = round(self.__totalClubPoints+cart.clubPoint, 2) 
            self.__historyCarts.append(cart)
            self.__currentCart = None
        return cart


