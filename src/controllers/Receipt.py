#from flask import json
import json
import uuid
import numbers
import os


#temporary (left only for tests)
rootpath = os.path.dirname(os.path.dirname(__file__))
with open(rootpath + '/fixtures/trip.json') as file:
    courier  = json.load(file)
with open(rootpath + '/fixtures/4d32a9dc-122d-4dc5-922a-4aa595434a7e.json') as file:
    order  = json.load(file)

class Receipt:

    def __init__(self, path_to_config):
        with open(path_to_config) as file:
            self.__data = json.load(file)

    def __checkNumber(self, data):
        return isinstance(data, numbers.Number)

    def __checkString(self, data):
        return isinstance(data, str)

    def __validateCourier(self, courierResponse):
        return "Error"

    def __validateOrder(self, orderResponse):
        return "Error"

    def get_data(self):
        return self.__data


    def transform(self, courierResponse, orderResponse, tripId):
        self.__validateCourier(courierResponse)
        self.__validateOrder(orderResponse)
        self.__data['receiptId'] = uuid.uuid4()
        self.__data['tripId'] = tripId
        for key in courierResponse:
            self.__data[key] = courierResponse[key]
        for key in orderResponse:
            self.__data[key] = orderResponse[key]
        print(self.get_data())

    
ip = Receipt(rootpath)