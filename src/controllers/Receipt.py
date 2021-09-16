#from flask import json
import json
import uuid
import re
import dateutil.parser
from controllers.Validation_Exception import Validation_Exception

u_id_validator = re.compile('[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}', flags=re.IGNORECASE)
phone_validator = re.compile('(\+?359[- ]?)?(((\(0?8[4-9]\)|0?8[7-9])[- ]?(\d{5}[- ]?\d{2}|\d{4}[- ]?\d{3}|\d{3}[- ]?\d{4}|\d{2}[- ]?\d{5}|\d[- ]?\d{6}|\d{2}[- ]?\d{3}[- ]?\d{2}))|((\(0[7-8]00\)|0[7-8]00)[- ]?\d{5})|((\(02\)|02)[- ]?\d{3}[- ]?\d{4})|((\(0\d{2}\)|0\d{2})[- ]?[- ]?(\d{2}[- ]?\d{4}|\d{3}[- ]?\d{3}))|((\(0\d{3}\)|0\d{3})[- ]?\d{5})|((\(0\d{4}\)|0\d{4})[- ]?\d{4}))')
email_validator = re.compile("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")

class Receipt:
    template_data = None
    template_path = None

    def set_template_data(path):
        Receipt.template_path = path
        with open (Receipt.template_path) as file: 
            Receipt.template_data = json.load(file)

    def __check_UUID(self, u_id):
        u_id_match = u_id_validator.match(u_id)
        if u_id_match is None or len(u_id)>36:
            raise Validation_Exception('Invalid UUID')

    def __check_phone_number(self, phoneNumber):        
        # (02) xxx xxxx (Sofia)
        # (0xx) xx xxxx
        # (0xxx) xxxxx
        # (0xxxx) xxxx
        # 08z xxxx xxx (mobiles)
        # 0800 xxxxx
        # +359-(089)-44-877-03 --------- biggest possible number
        try:
            phone_match = phone_validator.search(phoneNumber).group()
            return phone_match
        except Exception as e:
            raise Validation_Exception('Invalid Phone Number.') from e

    def __check_email(self, userMail):
        try:
            email = email_validator.search(userMail).group()
            return email
        except Exception as e:
            raise Validation_Exception('Invalid E-mail.') from e

    def __check_number_data(self, decimalNum):
        try:
            float(decimalNum)
        except ValueError as e:
            raise Validation_Exception('Data is not a valid float/int type.') from e

    def __check_string(self, data):
        try:
            float(data)
            raise Validation_Exception('Data is of type float/int. Should be a string.')
        except ValueError:
            pass

    def __check_date_time(self, data):
        try:
            dateutil.parser.isoparse(data)
        except Exception as e:
            raise Validation_Exception("DateTime is invalid RFC 3339 format.") from e

    def __validate_courier(self, courier_response):
        self.__check_UUID(courier_response['courierId'])
        self.__check_UUID(courier_response['orderId'])
        self.__check_number_data(courier_response['distance'])
        self.__check_string(courier_response['courierName'])
        self.__check_date_time(courier_response['deliveredAt'])
        self.__check_number_data(courier_response['distance'])


    def __validate_order(self, order_response):
        self.__check_string(order_response['clientName'])
        self.__check_string(order_response['deliveryType'])
        self.__check_date_time(order_response['createdAt'])
        order_response['clientEmail'] = self.__check_email(order_response['clientEmail'])
        order_response['phoneNumber'] = self.__check_phone_number(order_response['phoneNumber'])
        for subkey in order_response['dimensions']:
            self.__check_number_data(order_response['dimensions'].get(subkey))

    def __assign_data(self, courier_response, order_response, logger):
        for key in Receipt.template_data:
            #logger.debug(self.data[key])
            if key in courier_response:
                self.data[key] = courier_response[key]
            elif key in order_response:
                self.data[key] = order_response[key]
            
            #logger.debug(self.data[key])
            if isinstance(Receipt.template_data[key],dict):
                for subkey in Receipt.template_data[key]:
                    if subkey not in self.data[key] or self.data[key][subkey]=='tagged':
                        raise Validation_Exception("Subkey is empty or doesn't contain all fields.")
            else:
                if self.data[key]=="tagged":
                    raise Validation_Exception("Key is empty.")


    def __init__(self, courier_response, order_response, logger, trip_id=None, alt=False):
        # constructor 1 for creating objects from database
        # courier_response in this case is the receiptId
        # the data is the deserialized input
        if alt==True:
            logger.debug("Getting receipt id.")
            self.receiptId = courier_response
            logger.debug("Getting whole deserialized data.")
            self.data = order_response
        # constructor 2 for creating new receipts from real responses
        else:
            self.__check_UUID(trip_id)
            self.__validate_courier(courier_response)
            self.__validate_order(order_response)
            self.data = Receipt.template_data
            self.receiptId = trip_id
            self.__assign_data(courier_response, order_response, logger)