from models import *
import pytest
c = Customer('mike')
ct = Cart()
ui1 = UnitItem('Milk',2.99,2)
ui2 = UnitItem('Bread',2.89,1)
wi1 = WeightItem('Beef',19.99)
wi2 = WeightItem('Potato',2.79)

# model item test
def test_item_init():
    assert ui1.name =='Milk'
    assert ui2.unitPrice ==2.89
    assert ui2.quantity ==1
    assert wi1.unitPrice ==19.99
    assert wi2.name =='Potato'
    assert isinstance(wi1.weight,float) == True
def test_getItemPrice():
    assert ui1.getItemPrice() == 5.98
    assert ui2.getItemPrice() == 2.89
def test_itemDetail():
    assert ui1.itemDetail()=='Product: Milk, $2.99, 2, $5.98'

# model cart test
def test_addItem():
    assert ct.addItem(ui1) == 'Product: Milk, $2.99, 2, $5.98'

def test_checkOut():
    ct.checkout()
    assert ct.clubPoint == 0.6
def test_detailTitle():
    assert ct.detailTitle() == f'{ct.purchaseTime} Consumption: $5.98 Clubpoint:0.6\n'

# model customer test

def test_cust_init():
    assert c.name == 'mike'
    assert c.cardID ==10001
    assert c.clubPoints ==0
    assert c.currentCart == None
    assert c.historyCarts == []
    assert c.totalValue ==0

def test_startShopping():
    c.startShopping()
    c.currentCart.addItem(ui1)
    with pytest.raises(CustError) as e:
        c.startShopping()
        assert e.msg == ''

def test_getCustTitle():
    assert c.getCustTitle() == "Customer name: mike, Club ID: 10001, Club points: 0, Total consumption: $0\n"

def test_getAverageBefore():
    assert c.getAverage() == 0

def test_checkout():
    assert c.checkout().cartValue == 5.98

def test_getAverageAfter():
    assert c.getAverage() == 5.98

def test_calCarts():
    assert c.calCarts() == 1