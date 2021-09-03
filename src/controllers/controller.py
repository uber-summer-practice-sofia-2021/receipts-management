from clients.http import HTTPClient

class Controller:
    def __init__(self, pathToConfig):
        self.get_trip_info = HTTPClient(pathToConfig, 'get_trip_info')
        self.get_courier_info = HTTPClient(pathToConfig, 'get_courier_info')