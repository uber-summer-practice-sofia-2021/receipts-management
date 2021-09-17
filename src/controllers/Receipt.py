#from flask import json
import json
import uuid
import re
import dateutil.parser
from controllers.Validation_Exception import Validation_Exception
import jsonschema

class Receipt:

    phone_expr = "(\+?359[- ]?)?(((\(0?8[4-9]\)|0?8[7-9])[- ]?(\d{5}[- ]?\d{2}|\d{4}[- ]?\d{3}|\d{3}[- ]?\d{4}|\d{2}[- ]?\d{5}|\d[- ]?\d{6}|\d{2}[- ]?\d{3}[- ]?\d{2}))|((\(0[7-8]00\)|0[7-8]00)[- ]?\d{5})|((\(02\)|02)[- ]?\d{3}[- ]?\d{4})|((\(0\d{2}\)|0\d{2})[- ]?[- ]?(\d{2}[- ]?\d{4}|\d{3}[- ]?\d{3}))|((\(0\d{3}\)|0\d{3})[- ]?\d{5})|((\(0\d{4}\)|0\d{4})[- ]?\d{4}))"
    u_id_expr = "[\da-f]{8}-[\da-f]{4}-4[\da-f]{3}-[89ab][\da-f]{3}-[\da-f]{12}"
    email_expr = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"


    template_data = {
        "type": "object",
            "properties": {
                "clientName": {"type": "string"},
                "clientEmail": {"type": "string","pattern": email_expr},
                "phoneNumber": {"type": "string","pattern":phone_expr},
                "orderId": {"type": "string","pattern":u_id_expr},
                "from": {
                    "type": "object","properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"},
                        "addressName": {"type": "string"}
                },
                    "required": ["latitude","longitude","addressName"]
                },
                "to": {
                    "type": "object",
                        "properties": {
                            "latitude": {"type": "number"},
                            "longitude": {"type": "number"},
                            "addressName": {"type": "string"}
                        },
                    "required": ["latitude","longitude","addressName"]
                },
                "dimensions": {
                    "type": "object",
                        "properties": {
                            "length": {"type": "number"},
                            "depth": {"type": "number"},
                            "height": { "type": "number"},
                            "weight": {"type": "number"}
                        }
                },
                "deliveryType": {"type": "string"},
                "courierId": {"type": "string", "pattern":u_id_expr},
                "courierName": {"type": "string"},
                "courier_phone": {"type": "string"},
                "courier_email": {"type": "string", "pattern":email_expr},
                "distance": {"type": "number"},
                "createdAt": {"type": "string"},
                "deliveredAt": {"type": "string"}
            },
            "required": ["clientName","clientEmail","phoneNumber","orderId","from","to","deliveryType","courierId","courierName","distance","createdAt","deliveredAt"]
        }

    def __check_UUID(self, u_id):
        u_id_match = re.match(Receipt.u_id_expr,u_id)
        if u_id_match is None or len(u_id)>36:
            raise Validation_Exception('Invalid UUID')

    def __assign_data(self, courier_response, order_response):
        for key in order_response:
            self.data[key] = order_response[key]
        for key in courier_response:
            self.data[key]=courier_response[key]


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
            self.data = dict()
            self.receiptId = trip_id
            self.__assign_data(courier_response, order_response)
            try:
                jsonschema.validate(self.data, Receipt.template_data)
            except Exception as e:
                logger.debug(e)
                raise Validation_Exception("Invalid information") from e
            