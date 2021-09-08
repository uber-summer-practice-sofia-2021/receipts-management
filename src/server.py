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
Receipt.set_template_data(server.config['CONFIG_PATH'] + "/receipt_template.json") 


#controllers
controller = Controller(server.config['CONFIG_PATH'] + "/HTTPClients.json")
db_controller = Database_Controller(server.config['CONFIG_PATH'] + "/db_config.json")

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
 json_url = os.path.join(server.root_path, "fixtures" ,"receiptsContent.json")
 json_data = json.load(open(json_url))
 return render_template('index.html', data = json_data)

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
  
  #Creating a Receipt 
  currentReceipt = Receipt(courierResponse, orderResponse, tripId)

  server.logger.debug(currentReceipt.data)

  return render_template("index.html", data = currentReceipt.data, receiptId = currentReceipt.receiptId)
  

#Main function  
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  tripId = request.json
  server.logger.debug(tripId)  
  
  #Request to Courier
  courierResponse = controller.PostRequestToCourierService(tripId)
  courierResponse = courierResponse.json()
  
  #Request to Order
  orderResponse = controller.PostReuqestToOrderService(courierResponse['orderId'])
  orderResponse = orderResponse.json()
  
  #Creating a Receipt 
  currentReceipt = Receipt(courierResponse, orderResponse, tripId)

  #server.logger.debug(currentReceipt.data)

  return render_template("index.html", data = currentReceipt.data, receiptId = currentReceipt.receiptId)


if __name__ == "__main__":
  server.run(host='0.0.0.0')
