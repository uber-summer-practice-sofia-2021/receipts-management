from flask import config
import requests, json

class HTTPClient:
    def __init__(self, config_file_path, serviceIdentifier):
        self.config_file_path = config_file_path
        self.serviceIdentifier = serviceIdentifier

        config_file = json.load(open(self.config_file_path))
        for request in config_file:
            if serviceIdentifier != request['identifier']:
                continue
            self.request = request
            break

    def post(self, identifier, payload):
        for _ in range(self.request['retry_limit']):
            response = requests.post(self.request['endpoint'], json=payload, timeout=self.request['timeout'])
            if response.ok:
                return response
        
        #Fix later it proper bad request
        return None