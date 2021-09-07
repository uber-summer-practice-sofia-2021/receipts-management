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
<<<<<<< HEAD
  server.logger.debug(request.json)

  json_path = os.path.join(server.root_path, "fixtures", "order.json")
  order_info = json.load(open(json_path))

  #return Response(json.dumps(trip_info), mimetype='application/json')
  return order_info
=======
  orderId = request.json
  file = json.load(open("fixtures/" + orderId + ".json"))
  return file
>>>>>>> 22d6e5cd48adc89b4a6ee20074958bd98c1fc1a6

if __name__ == "__main__":
   server.run(host='0.0.0.0')