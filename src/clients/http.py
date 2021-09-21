import requests, json, os

class HTTPClient:
    def __init__(self, config_file_path, serviceIdentifier):
        self.config_file_path = config_file_path # Path to the HTTPClients.json
        self.serviceIdentifier = serviceIdentifier

        config_file = json.load(open(self.config_file_path))
        for request in config_file:
            if serviceIdentifier != request['identifier']:
                continue
            self.request = request
            break

    def get(self, payload):
        response = 0
        for _ in range(self.request['retry_limit']):
            response = requests.get(os.environ[f"{self.request['identifier']}"] + payload, timeout=self.request['timeout'])

            # Assert that there were no errors
            response.raise_for_status()

            return response
        
        #Fix later it proper bad request
        return response