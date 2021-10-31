import pytz
from models import *
from typing import Dict, List
from datetime import datetime as dt, timedelta
from pytz import timezone




TZ = timezone('Pacific/Auckland')
class SuperMarket:
    def __init__(self) -> None:
       self.customers:Dict[int,Customer] = {}
        
    # method to create a customer object 
    def createCustomer(self,name:str)->Customer:
        if isinstance(name,str):
            newCust = Customer(name)
            self.customers.setdefault(newCust.cardID, newCust)
            return newCust
        else:
            raise TypeError('parameters type error')
    # method to start shopping for a customer
    def startShoping(self,custID:int) ->MyResponse:
        cust = self.__getCust(custID)
        try:
            cust.startShopping()
            return MyResponse(1)
        except CustError as cse:
            items = cust.currentCart.cartDetails()
            msg= "You have unpaid products in your shopping cart, please continue shopping."
            return MyResponse(1,msg,items)
    # method to chekc if id is in eligable 
    def checkID(self,custID):
        cust = self.customers.get(custID)
        return bool(cust)
    # method to get customer by id
    def __getCust(self,custID) ->Customer or None:
        cust = self.customers.get(custID)
        return cust 
    # method to check if parameter types are eligable to create objects
    def __paraCheck(self, validation:dict) ->None:
        for key in validation.keys():
            if not isinstance(key,validation[key]):
                raise TypeError('parameters type error')
    # method to add an unit time to shopping cart for one customer 
    def addUnitItem(self,custID:int,itemName:str,price:float,quantity:int)->MyResponse:
        cust = self.__getCust(custID)
        if not cust:
            return MyResponse(0,'Incorrect Cunstomer Card ID.')
        if not cust.currentCart:
            self.startShoping(custID)
        try:
            paras = {itemName:str,price:float,quantity:int}
            self.__paraCheck(paras)
            item = UnitItem(itemName, price, quantity)
            cust.currentCart.addItem(item)
            info = cust.currentCart.cartItemsInfo()
            response = MyResponse(1,data = {'info':info})
        except TypeError as te:
            print(te)
            response = MyResponse(0,te.__str__())
        return response
    # method to add a weight time to shopping cart for one customer 
    def addWeightItem(self,custID:int,itemName:str,price:float)->MyResponse:
        cust = self.__getCust(custID)
        if not cust:
            return MyResponse(0,'Incorrect Cunstomer Card ID.')
        if not cust.currentCart:
            self.startShoping(custID)
        try:
            paras = {itemName:str,price:float}
            self.__paraCheck(paras)
            item = WeightItem(itemName,price)
            cust.currentCart.addItem(item)
            info = cust.currentCart.cartItemsInfo()
            response = MyResponse(1,data = {'info':info,'weight':item.weight})
        except TypeError as te:
            print(te)
            response = MyResponse(0,te.__str__())
        return response
    # method to check if the customer has checked out 
    def isCheckout(self,custID:int)->bool:
        cust = self.__getCust(custID)
        if cust.currentCart and cust.currentCart.items:
            result = True
        else:
            result = False
        return result
    # method to get detailed info of a customer 
    def getCustomerInfo(self,custID:int)->MyResponse:
        cust = self.__getCust(custID)
        if not cust:
            return MyResponse(0,'Incorrect Cunstomer Card ID.')

        info = cust.customerDetail()
        return MyResponse(1,data=info)
    # method to checkout for one customer 
    def checkout(self,custID:int)->MyResponse:
        cust = self.__getCust(custID)
        if not cust:
            return MyResponse(0,'Incorrect Cunstomer Card ID.')
        if not cust.currentCart:
            return MyResponse(0,'Your shopping cart is empty, please pick products first.')
        cart = cust.checkout()
        if cart.cartValue!=0:
            response = MyResponse(1,data={'cost':round(cart.cartValue,2) ,'info':cart.cartDetails()})
        else:
            response = MyResponse(0,'Your shopping cart is empty, please pick products first.')
        return response

    def __calTotalSale(self) ->float:
        totalSales = 0
        for cust in self.customers.values():
            for cart in cust.historyCarts:
                totalSales += cart.cartValue
        return totalSales
    # method to calculate total sales 
    def getTotalSales(self)->MyResponse:
        totalSales = self.__calTotalSale()
        utc_now = dt.now(timezone('UTC'))
        lt = utc_now.astimezone(TZ).strftime("%d/%m/%Y %H:%M:%S")

        info = f'As of {lt}, total revenues were {round(totalSales,2)}'
        return MyResponse(1,data= info )
    # method to get consumption summary for customers
    def getSaleSum(self)->MyResponse:
        info =''
        for cust in self.customers.values():
            info += f'{cust.name}  {cust.cardID} ${cust.totalValue}\n'
            for cart in cust.historyCarts:
                info += f'----{cart.purchaseTime} ${cart.cartValue}\n'
        return MyResponse(1,data=info)
    # method to calculate average expenses for each customer and total avaerage 
    def getAvgExpense(self)->MyResponse:
        
        info = ''
        totalCarts = 0
        for cust in self.customers.values():
            info += cust.getCustTitle()
            carts =cust.calCarts()
            totalCarts += carts
            info += f'Shopping {carts} times, Average: ${cust.getAverage()}\n'
        totalAvg = round(self.__calTotalSale()/totalCarts,2)
        info += f"Ttoal transaction: {totalCarts} times, Total average: ${totalAvg}"
        return MyResponse(1,data=info)
    # method to get the customer who spend most
    def getStarCust(self)->MyResponse:
        topExpense = 0
        startCust = None
        for cust in self.customers.values():
            if cust.totalValue > topExpense:
                topExpense = cust.totalValue
                startCust = cust
        info = startCust.getCustTitle()
        info += f'Shopping {startCust.calCarts()} times, Average: ${startCust.getAverage()}'
        return MyResponse(1,data=info)
        
    # method to get sale report for required month
    def getMonthlySale(self,year:int,month:int)->MyResponse:
        info = f'Sale for {year} - {month}: \n'
        monthTotal = 0
        for cust in self.customers.values():
            monthCsump = 0
            for cart in cust.historyCarts:
                time = cart.purchaseTime.astimezone(TZ)
                if time.year == year and time.month == month:
                    monthCsump += cart.cartValue
            if monthCsump != 0:
                info += f"{cust.name}, {cust.cardID}, ${round(monthCsump,2) }\n"
                monthTotal += monthCsump
        info+=f'\nTotal ${ round(monthTotal,2) }'
        return MyResponse(1,data=info)

if __name__ == '__main__':
    print(len(None))
    