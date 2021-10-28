from _pytest.monkeypatch import resolve
from SuperMarket import SuperMarket
from models import *
import pytest
s = SuperMarket()
ui1 = UnitItem('Milk',2.99,2)
ui2 = UnitItem('Bread',2.89,1)
wi1 = WeightItem('Beef',19.99)
wi2 = WeightItem('Potato',2.79)

def test_createCustomer():
    with pytest.raises(TypeError) as e:
        s.createCustomer(1)
    assert e.value.args[0] =='parameters type error'
    s.createCustomer('Mike')
    assert s.customers.get(10001).name =='Mike'
def test_startShopping():
    result = s.startShoping(10001)
    assert result.status ==1
    s.customers.get(10001).currentCart.addItem(ui1)
    result = s.startShoping(10001)
    assert result.msg == "You have unpaid products in your shopping cart, please continue shopping."


def test_addUnitItem():
    result = s.addUnitItem(10002,'Mile',1.99,2)
    assert result.msg =='Incorrect Cunstomer Card ID.'
    result = s.addUnitItem('10002','Mile',1.99,2)
    assert result.status == 0
    result = s.addUnitItem(10001,'Mile',1.99,2)
    assert result.status ==1

def test_getCustomerInfo():
    result = s.getCustomerInfo(10001)
    assert result.status ==1

def test_checkout():
    result = s.checkout(10001)
    assert result.status ==1
    result = s.checkout(10001)
    assert result.msg == 'Your shopping cart is empty, please pick products first.'
    s.startShoping(10001)
    result = s.checkout(10001)
    assert result.msg == 'Your shopping cart is empty, please pick products first.'

def test_getTotalSales():
    result = s.getTotalSales()
    assert result.status == 1
    assert isinstance(result.data,str) == True





