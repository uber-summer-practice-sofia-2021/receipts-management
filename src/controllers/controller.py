from clients.http import HTTPClient

class Controller:
    def __init__(self, pathToConfig):
        self.get_order_info = HTTPClient(pathToConfig, 'get_order_info')
        self.get_trip_info = HTTPClient(pathToConfig, 'get_trip_info')
    
    def PostRequestToCourierService(self, payload):
        return self.get_trip_info.post(payload)

    def PostReuqestToOrderService(self, payload):
        return self.get_order_info.post(payload)