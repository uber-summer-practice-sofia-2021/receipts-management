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
  file = {"tripID":"trip"}
  server.logger.debug(file)
  requests.post("http://receipts:5000/receive_trip_id", json = file)
  return jsonify(file)

@server.route("/get_trip_info", methods = ["POST"])
def sendAllInfo():
  tripID = request.json
  server.logger.debug(tripID)
  file = json.load(open("fixtures/" + tripID+ ".json"))
  server.logger.debug(file)
  requests.post("http://receipts:5000/get_trip_info", json = file)
  return "Successfully Sent"

if __name__ == "__main__":
   server.run(host='0.0.0.0')