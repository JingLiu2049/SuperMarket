from flask import Flask,jsonify,render_template,request
from models.MyResponse import MyResponse
from utils import *

app = Flask(__name__)
sm = getSuperMarket()

@app.route('/')
def home():
    return render_template('home.html',custs = sm.customers)

@app.route('/api/start/<int:custID>/')
def start(custID):
    response = sm.startShoping(custID)
    return jsonify(response.__dict__)

@app.route('/api/item/<int:custID>/',methods=['POST'])
def item(custID):
    data = request.form
    for i in data.values():
        print(i)
    try:
        name = data['itemName']
        if data['itemType'] == 'unitItem':
            uprice = float(data['unitPrice'])
            quantity = int(data['quantity'])
            response = sm.addUnitItem(custID,name,uprice,quantity)
        else:
            wprice = float(data['weightPrice'])
            response = sm.addWeightItem(custID,name,wprice)
    except ValueError as ve:
        response = MyResponse(0,'Item information missing, pelase check your input.')
    except KeyError as ke:
        response = MyResponse(0,'Item type has to be selected.')
    return jsonify(response.__dict__)

@app.route('/api/next/<int:custID>/')
def next(custID):
    isCheckout = sm.isCheckout(custID)
    return jsonify(MyResponse(1,data=isCheckout).__dict__)

@app.route('/api/checkout/<int:custID>/')
def checkout(custID):
    response = sm.checkout(custID)
    return jsonify(response.__dict__)

@app.route('/api/custDetail/<int:custID>/')
def custDetail(custID):
    response = sm.getCustomerInfo(custID)
    return jsonify(response.__dict__)
    
@app.route('/api/saleByCust/')
def saleByCust():
    return jsonify(sm.getSaleSum().__dict__)

@app.route('/api/totalSale/')
def totalSale():
    return jsonify(sm.getTotalSales().__dict__)

@app.route('/api/topCust/')
def topCust():
    try:
        response = sm.getStarCust()
    except AttributeError as ae:
        response = MyResponse(0,"You don't have any sales yet.")
    return jsonify(response.__dict__)

@app.route('/api/avgCart/')
def avgCart():
    response =sm.getAvgExpense()
    return jsonify(response.__dict__)

@app.route('/api/monthlySale/<int:year>/<int:month>/')
def monthlySale(year,month):
    return jsonify(sm.getMonthlySale(year,month).__dict__)

if __name__ == '__main__':
    Flask.run(app,debug=True)