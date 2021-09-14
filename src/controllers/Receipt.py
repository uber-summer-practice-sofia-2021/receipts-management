#from flask import json
import json
import uuid
import re

u_id_validator = re.compile('[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}', flags=re.IGNORECASE)
phone_validator = re.compile('(\+?359)?[- ]?(((\(0[7-8]00\)|0[7-8]00)[- ]?\d{5})|((\(02\)|02)[- ]?\d{3}[- ]?\d{4})|((\(02\d\)|02\d)[- ]?[- ]?(\d{2}[- ]?\d{4}|\d{3}[- ]?\d{3}))|((\(0?8[4-9]\)|0?8[7-9])[- ]?(\d{5}[- ]?\d{2}|\d{4}[- ]?\d{3}|\d{3}[- ]?\d{4}|\d{2}[- ]?\d{5}|\d[- ]?\d{6}|\d{2}[- ]?\d{3}[- ]?\d{2})))')

#gotta ask about this email validator
email_validator = re.compile("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")

class Receipt:
    template_data = None
    template_path = None

    def set_template_data(path):
        Receipt.template_path = path
        with open (Receipt.template_path) as file: 
            Receipt.template_data = json.load(file)

    def __checkUUID(self, u_id):
        u_id_match = u_id_validator.match(u_id)
        if u_id_match is None:
            raise Exception('Invalid UUID')

    def __checkPhoneNumber(self, phoneNumber):
        # (02) xxx xxxx (Sofia)
        # (0xx) xx xxxx
        # (0xxx) xxxxx
        # (0xxxx) xxxx
        # 08z xxxx xxx (mobiles)
        # 0800 xxxxx
        # +359-(089)-44-877-03 --------- biggest possible number
        phone_match = phone_validator.match(phoneNumber)
        if phone_match is None or len(phoneNumber)>20:
            raise Exception('Invalid Phone Number')

    def __checkNumberData(self, decimalNum):
        try:
            float(decimalNum)
        except:
            raise Exception(decimalNum + ' is not a valid float/int type.')

    def __checkString(self, data):
        if not isinstance(data, str):
            raise Exception(data + "is not a string")

    def __validateCourier(self, courierResponse):
        self.__checkUUID(courierResponse['courierId'])

    def __validateOrder(self, orderResponse):
        pass

    def __init__(self, courierResponse, orderResponse, tripId=None):
        #constructor 1 for creating objects from database
        #courierResponse in this case is the receiptId
        #the data is the deserialized input
        if tripId is None:
            self.receiptId = courierResponse
            self.data = orderResponse
        #constructor 2 for creating new receipts from real responses
        else:
            self.__validateCourier(courierResponse)
            self.__validateOrder(orderResponse)
            self.data = Receipt.template_data
            self.receiptId = str(uuid.uuid4())
            self.data['tripId'] = tripId
            for key in courierResponse:
                self.data[key] = courierResponse[key]
            for key in orderResponse:
                self.data[key] = orderResponse[key]