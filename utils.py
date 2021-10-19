from SuperMarket import SuperMarket


def getFileData(filename):
    args = []
    with open(filename) as custs:
        data = custs.read().splitlines()
        for i in data:
            args.append(i)
    return args

# a function to create Supermarket object with data from a file
def getSuperMarket():
    sm = SuperMarket()
    try:
        custData = getFileData('Customers.txt')
        for i in custData:
            sm.createCustomer(i)
    except Exception as e:
        print(e.__class__,e)
    return sm

