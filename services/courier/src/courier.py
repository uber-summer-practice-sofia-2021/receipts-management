import os
import json
from flask import Flask, request, Response,  jsonify
from flask.json import JSONDecoder
import requests

server = Flask(__name__)

@server.route("/")
def hello():
  return "Hello World!"

#Simulates courier API interacting with us
@server.route("/send", methods=["POST"])
def sendTripInfo():
  file = {"tripId":"trip"}
  requests.post("http://receipts:5000/receive_trip_id", json = file)
  return "Successfully Sent"

@server.route("/get_trip_info", methods = ["POST"])
def sendAllInfo():
  tripId = request.json
  with open(os.path.join(server.root_path, "fixtures", tripId + ".json")) as file:
    trip_info = json.load(file)
  server.logger.debug(trip_info)
  return trip_info

if __name__ == "__main__":
   server.run(host='0.0.0.0')
