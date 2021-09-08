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
  order = request.json
  with open (os.path.join(server.root_path, "fixtures", order + ".json")) as file:
    order_info = json.load(file)
  return order_info

if __name__ == "__main__":
   server.run(host='0.0.0.0')