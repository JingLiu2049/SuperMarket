from models import *
import pytest
c = Customer('mike')
ct = Cart()
def test_init():
    
    assert c.name == 'mike'
    assert c.cardID ==10001
    assert c.clubPoints ==0
    assert c.currentCart == None
    assert c.historyCarts == []
    assert c.totalValue ==0
def test_getCustTitle():
    assert c.getCustTitle() == "Customer name: mike, Club ID: 10001, Club points: 0, Total consumption: $0\n"


