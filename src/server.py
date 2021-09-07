import os
import requests
from controllers.Controller import Controller
from flask import Flask, config, request, render_template, url_for, json, Response, jsonify
#Import the g object, sqlite3 and all functions for the database
from controllers.Database_Controller import *
from controllers.Receipt import Receipt


#server stuff
server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

#controllers
controller = Controller(server.config['CONFIG_PATH'] + "/HTTPClients.json")
db_controller = Database_Controller(server.config['CONFIG_PATH'] + "/db_config.json")
receipt_controller = Receipt(server.config['CONFIG_PATH'] + "/receipt_template.json")

def save_trip(tripId):
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
  return "cool"

def get_all_info(tripId):

  #Request to Courier
  courierResponse = controller.PostRequestToCourierService(tripId)
  courierResponse = courierResponse.json()
  
  #Request to Order
  orderResponse = controller.PostReuqestToOrderService(courierResponse['orderId'])
  orderResponse = orderResponse.json()
  
  server.logger.debug(courierResponse)
  server.logger.debug(orderResponse)
  #server.logger.debug(Receipt.get_path())
  #Creating a Receipt 
  #current_receipt = Receipt.get_receipt(courierResponse, orderResponse)
  

#Main function
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripId = request.json
  server.logger.debug(tripId)  
  get_all_info(tripId['tripId'])
  return "Successfully received"


if __name__ == "__main__":
  server.run(host='0.0.0.0')