import os
import requests
from controllers.controller import Controller
from flask import Flask, config, request, render_template, url_for, json, Response, jsonify
#Import the g object, sqlite3 and all functions for the database
from db_class import *


#server stuff
server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

#controllers
myController = Controller(server.config['CONFIG_PATH'] + "/HTTPClients.json")
dbController = DB(open(server.config['CONFIG_PATH'] + "/db_config.json"))

def saveTrip(tripId):
  try:
    with open ("/fixtures/trips/" + tripId + "json", 'x') as file : 
      server.logger.debug(file)
  except:
    server.logger.debug("File already exists")


@server.route("/message-queue")
def hello():
  return "cool?"


@server.route("/test")
def user():
  return render_template("index.html")

@server.route("/testdb", methods = ["GET"])
def testdb():
  with open (os.path.join(server.config['CONFIG_PATH'], 'HTTPClients.json')) as file:
    data = json.load(file)
    server.logger.debug(data)
  #open('HTTPClients.json')
  return "cool"

def getAllInfo(tripID):
  courierResponse = requests.post(myController.get_trip_info, json = tripID)
  courierResponse = courierResponse.json()
  orderResponse = requests.post(myController.get_order_info, json = courierResponse['orderId'])
  orderResponse = orderResponse.json()
  server.logger.debug(orderResponse)
  server.logger.debug(courierResponse)

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripID = request.json
  server.logger.debug(tripID)

  response_from_courier = myController.PostRequestToCourierService(tripID)

  server.logger.debug(response_from_courier.text)

  response_from_order = myController.PostReuqestToOrderService({"orderId": response_from_courier.json()['orderId']})

  server.logger.debug(response_from_order.text)

  return "Successfully received"


if __name__ == "__main__":
  server.run(host='0.0.0.0')