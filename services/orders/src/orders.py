import os
import json
from flask import Flask, request, Response,  jsonify
import requests

server = Flask(__name__)

@server.route("/")
def hello():
  return "Hello World!"

#Simulates courier API interacting with us
@server.route("/get_order_info", methods=["POST", "GET"])
def getTripInfo():
  if request.method == "POST":
    server.logger.debug(request.json)

  json_url = os.path.join(server.root_path, "fixtures", "order.json")
  trip_info = json.load(open(json_url))

  #return Response(json.dumps(trip_info), mimetype='application/json')
  return trip_info

if __name__ == "__main__":
   server.run(host='0.0.0.0')