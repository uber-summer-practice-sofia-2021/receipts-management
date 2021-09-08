#from flask import json
import json
import uuid
import numbers

class Receipt:
    def __init__(self, path_to_config):
        self.__current_path = path_to_config
        with open(path_to_config) as file:
            self.__data = json.load(file)

    def __checkNumber(self, data):
        return isinstance(data, numbers.Number)

    def __checkString(self, data):
        #return isinstance(data, str)
        return "error"

    def __validateCourier(self, courierResponse):
        return "Error"

    def __validateOrder(self, orderResponse):
        return "Error"

    def get_data(self):
        return self.__data

    def get_path(self):
        return self.__current_path


    def create_receipt(self, courierResponse, orderResponse, tripId):
        self.__validateCourier(courierResponse)
        self.__validateOrder(orderResponse)
        data = self.__data
        data['receiptId'] = uuid.uuid4()
        data['tripId'] = tripId
        for key in courierResponse:
            data[key] = courierResponse[key]
        for key in orderResponse:
            data[key] = orderResponse[key]
        return data

