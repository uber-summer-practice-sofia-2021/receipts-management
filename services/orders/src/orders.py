import os
import json
from flask import Flask, request, Response,  jsonify
import requests

server = Flask(__name__)

@server.route("/")
def hello():
  return "Hello World!"

#Simulates courier API interacting with us
@server.route("/get_order_info", methods=["POST"])
def getTripInfo():
  server.logger.debug(request.json)

  json_path = os.path.join(server.root_path, "fixtures", "order.json")
  order_info = json.load(open(json_path))

  #return Response(json.dumps(trip_info), mimetype='application/json')
  return order_info

if __name__ == "__main__":
   server.run(host='0.0.0.0')