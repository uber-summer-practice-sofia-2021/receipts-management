#from flask import json
import json
import uuid
import numbers

class Receipt:
    template_data = None
    template_path = None

    def set_template_data(path):
        Receipt.template_path = path
        with open (Receipt.template_path) as file: 
            Receipt.template_data = json.load(file)

    def __checkNumber(self, data):
        return isinstance(data, numbers.Number)

    def __checkString(self, data):
        return isinstance(data, str)

    def __validateCourier(self, courierResponse):
        pass

    def __validateOrder(self, orderResponse):
        pass

    def __init__(self, courierResponse, orderResponse, tripId=None):
        if tripId is None:
            self.receiptId = uuid.UUID(courierResponse)
            self.data = orderResponse
        else:
            self.data = Receipt.template_data
            self.receiptId = str(uuid.uuid4())
            self.data['tripId'] = tripId
            for key in courierResponse:
                self.data[key] = courierResponse[key]
            for key in orderResponse:
                self.data[key] = orderResponse[key]