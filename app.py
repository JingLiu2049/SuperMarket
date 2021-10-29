from flask import Flask,jsonify,render_template,request
from models.MyResponse import MyResponse
from utils import *
from functools import wraps

app = Flask(__name__)
sm = getSuperMarket()

# decorator to deal with uncatched errors
def commonError(func):
    @wraps(func)
    def inner(*args,**kwargs):
        try:
            response = func(*args,**kwargs)
        except Exception as e:
            print(e)
            error = MyResponse(0,'Your connection is unstable, please try later.')
            response = jsonify(error.__dict__)
        return response
    return inner

# method to return the main page
@app.route('/')
def home():
    return render_template('home.html',custs = sm.customers)

# method to start shopping for a customer
@app.route('/api/start/<int:custID>/')
@commonError 
def start(custID):
    response = sm.startShoping(custID)
    return jsonify(response.__dict__)

# method to add an item
@app.route('/api/item/<int:custID>/',methods=['POST'])
@commonError 
def item(custID):
    data = request.form
    name = data['itemName']
    if not name:
        return jsonify(MyResponse(0,'Please input product name.').__dict__)
    try:
        print(name)
        if data['itemType'] == 'unitItem':
            uprice = float(data['unitPrice'])
            quantity = int(data['quantity'])
            response = sm.addUnitItem(custID,name,uprice,quantity)
        else:
            wprice = float(data['weightPrice'])
            response = sm.addWeightItem(custID,name,wprice)
    except ValueError as ve:
        response = MyResponse(0,'Item information incorrect, pelase check your input.')
    except KeyError as ke:
        response = MyResponse(0,'Item type has to be selected.')
    return jsonify(response.__dict__)

# method to chenge a customer 
@app.route('/api/next/<int:custID>/')
@commonError 
def next(custID):
    isCheckout = sm.isCheckout(custID)
    return jsonify(MyResponse(1,data=isCheckout).__dict__)

# method to checkout for a customer 
@app.route('/api/checkout/<int:custID>/')
@commonError 
def checkout(custID):
    response = sm.checkout(custID)
    return jsonify(response.__dict__)

# method to return detailed info for a customer 
@app.route('/api/custDetail/<int:custID>/')
@commonError 
def custDetail(custID):
    response = sm.getCustomerInfo(custID)
    return jsonify(response.__dict__)

# method to return sale summary for cutomers
@app.route('/api/saleByCust/')
@commonError 
def saleByCust():
    return jsonify(sm.getSaleSum().__dict__)

# method to return total sale info 
@app.route('/api/totalSale/')
@commonError 
def totalSale():
    return jsonify(sm.getTotalSales().__dict__)

# method to return top customer info
@app.route('/api/topCust/')
@commonError 
def topCust():
    try:
        response = sm.getStarCust()
    except AttributeError as ae:
        response = MyResponse(0,"You don't have any sales yet.")
    return jsonify(response.__dict__)

# method to return average info
@app.route('/api/avgCart/')
@commonError 
def avgCart():
    response =sm.getAvgExpense()
    return jsonify(response.__dict__)

# method to return sale info for one selected month
@app.route('/api/monthlySale/<int:year>/<int:month>/')
@commonError 
def monthlySale(year,month):
    return jsonify(sm.getMonthlySale(year,month).__dict__)

if __name__ == '__main__':
    Flask.run(app,debug=True)