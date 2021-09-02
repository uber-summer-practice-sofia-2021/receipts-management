import os
import requests
from flask import Flask, request, render_template, url_for, json, Response

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")

@server.route("/message-queue")
def hello():
  return "Hello World!"

@server.route("/test")
def user():
  return render_template("index.html")

@server.route("/<string:trip>", methods = ['GET'])
def receipt_request(trip):
  username = request.args.get('name')
  return f'Hello {username}!'

#Simulates courier API interacting with us
@server.route("/get_trip_info", methods=["POST"])
def getTripInfo():
  #server.logger.debug(request.json)

  json_url = os.path.join(server.root_path, "fixtures", "tripInfo.json")
  trip_info = json.load(open(json_url))

  return Response(json.dumps(trip_info), mimetype='application/json')

#Simulates order API interacting with us
@server.route("/get_order_info", methods=["POST"])
def getOrderInfo():
  #server.logger.debug(request.json)

  json_url = os.path.join(server.root_path, "fixtures", "order.json")
  order_info = json.load(open(json_url))

  return Response(json.dumps(order_info), mimetype='application/json')

urls = ["localhost:5000/get_trip_info", "localhost:5000/get_order_info"]

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  order = request.json
  server.logger.debug(order)

  #response = requests.post(urls[0], data=order)

  #server.logger.debug(response)

  #response.raise_for_status()
  
  return "Successfully Received"
  

if __name__ == "__main__":
   server.run(host='0.0.0.0')