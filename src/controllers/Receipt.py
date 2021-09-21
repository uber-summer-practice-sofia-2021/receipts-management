import re
import dateutil.parser
from requests.api import request
from controllers.ValidationException import ValidationException
import jsonschema
import googlemaps
import traceback
import requests
from PIL import Image
import io, base64, os
import datetime

API_KEY = os.environ['MAPS_KEY']
map_client = googlemaps.Client(API_KEY)


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
            "required": ["clientName","clientEmail","phoneNumber","orderId","from","to","deliveryType","courierId","courierName","createdAt","deliveredAt"]
        }

    def __init__(self, courier_response, order_response, logger, trip_id=None, alt=False):
        # constructor 1 for creating objects from database
        # courier_response in this case is the receiptId
        # the data is the deserialized input
        if alt==True:
            logger.info("Getting receipt id.")
            self.receiptId = courier_response
            logger.info("Getting whole deserialized data.")
            self.data = order_response
        # constructor 2 for creating new receipts from real responses
        else:
            try:
                self.__check_UUID(trip_id)
                self.data = dict()
                self.receiptId = trip_id
                self.__assign_data(courier_response, order_response)
                jsonschema.validate(self.data, Receipt.template_data)
                logger.info("Validated Data")
                self.__check_date_time()
                self.get_map(logger)
                self.calculate_price()
            except Exception as e:
                raise ValidationException("Invalid information") from e

    def __check_UUID(self, u_id):
        u_id_match = re.match(Receipt.u_id_expr,u_id)
        if u_id_match is None or len(u_id)>36:
            raise ValidationException('Invalid UUID')

    def __assign_data(self, courier_response, order_response):
        for key in Receipt.template_data['properties']:
            if key in courier_response:
                self.data[key] = courier_response[key]
            elif key in order_response:
                self.data[key] = order_response[key]
            
    def __check_date_time(self):
        try:
            dateutil.parser.isoparse(self.data['createdAt'])
            dateutil.parser.isoparse(self.data['deliveredAt'])
            self.data['createdAt'] = datetime.datetime.strptime(self.data['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
            self.data['deliveredAt'] = datetime.datetime.strptime(self.data['deliveredAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
        except Exception as e:
            raise ValidationException("DateTime is invalid RFC 3339 format.") from e

    def get_map(self, logger):
        start = (self.data['from']['latitude'],self.data['from']['longitude'])
        end = (self.data['to']['latitude'], self.data['to']['longitude'])
        try:
            new_distance = map_client.distance_matrix(origins = start, destinations = end, mode = "driving")
            new_direction = map_client.directions(origin = start, destination = end, mode = "driving")
            self.data['distance'] = new_distance['rows'][0]['elements'][0]['distance']['value']
            map_url= "https://maps.googleapis.com/maps/api/staticmap?size=600x400"
            map_url+="&markers=color:purple%7C{0},{1}".format(start[0], start[1])
            map_url+="&markers=color:black%7C{0},{1}".format(end[0], end[1])
            encoded_polyline = str(new_direction[0]['overview_polyline']['points']).replace("\\\\", "\\")
            map_url+="&path=enc:"+encoded_polyline
            map_url+="&key="+API_KEY
            self.data['img_url'] = map_url
            response = requests.get(map_url, stream=True)
            img_response = Image.open(io.BytesIO(response.content))
            img_data = io.BytesIO()
            img_response.save(img_data, "PNG")
            encoded_image = base64.b64encode(img_data.getvalue())
            self.data['img'] =  encoded_image.decode('utf-8')
        except Exception as e:
            logger.warn(traceback.format_exc())
            raise ValidationException("Invalid coordinates and/or distance") from e

    def calculate_price(self):
        try:
            base_fare = 5 #this is for the delivery to the town itself
            VAT = 0.2
            tax_per_meter = 0.0004
            base_price = self.data['distance']
            base_price*= tax_per_meter
            base_price = round(base_price, 2)

            #calculate days
            time = self.data['deliveredAt']-self.data['createdAt']

            total_price = base_price+base_fare
            if(time.days>3):
                if(time.days>6):
                    if(time.days>29):
                        discount = 0.75*total_price
                        discount = round(discount, 2)
                        self.data['discount']=discount
                        total_price-=discount
                    else:
                        discount = 0.5*total_price
                        discount = round(discount, 2)
                        self.data['discount']=discount
                        total_price-=discount
                else:
                    discount = 0.2*total_price
                    discount = round(discount, 2)
                    self.data['discount']=discount
                    total_price-=discount
            else:
                self.data['discount']=0

            total_price = round(total_price + total_price*VAT, 2)
            self.data['totalPrice'] = total_price
            self.data['VAT'] = '20%'
            self.data['baseFare']=base_fare
            self.data['basePrice']=base_price
        except Exception as e:
            raise ValidationException("Something went wrong during the price calculations") from e