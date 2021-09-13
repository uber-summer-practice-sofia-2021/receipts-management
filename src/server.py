from flask import Flask, request, render_template
import os
import json
import threading

server = Flask(__name__,  template_folder="resources/templates", static_folder="resources/")
server.config['CONFIG_PATH'] = os.path.join(server.root_path, "config")

#import controllers
from controllers.Init_Controllers import get_controller
from controllers.Init_Controllers import get_db_controller
from controllers.Receipt import Receipt


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
  courierResponse = get_controller().PostRequestToCourierService(tripId)
  courierResponse = courierResponse.json()

  #Request to Order
  orderResponse = get_controller().PostReuqestToOrderService(courierResponse['orderId'])
  orderResponse = orderResponse.json()

  #Creating a Receipt
  currentReceipt = Receipt(courierResponse, orderResponse, tripId)

  #test inserting into database
  #hard-coded for error testing (currently handles errors fine(but might be updated))
  currentReceipt.receiptId="124325"
  get_db_controller().insert_into_db(currentReceipt, server.logger)

  #test loading obj from database
  newReceipt = get_db_controller().get_from_db("9140e029-a1f6-40fa-be68-3f57a5318495", server.logger, Receipt)
  server.logger.debug(newReceipt.data)
  server.logger.debug('RIGHT AFTER DB')
  #get_controller().send_email(currentReceipt)
  server.logger.debug("AFTER COMMAND")



#Main function  
@server.route("/receive_trip_id", methods = ['POST'])
def receiveTripId():
  trip = request.json
  trip = trip['tripId'] 
  
  #now everybody's happy
  get_all_info(trip)

  #Request to Courier
  courierResponse = get_controller().PostRequestToCourierService(trip)
  courierResponse = courierResponse.json()
  
  #Request to Order
  orderResponse = get_controller().PostReuqestToOrderService(courierResponse['orderId'])
  orderResponse = orderResponse.json()
  
  #Creating a Receipt 
  currentReceipt = Receipt(courierResponse, orderResponse, trip)

  return render_template("index.html", data = currentReceipt.data, receiptId = currentReceipt.receiptId)


if __name__ == "__main__":
  server.run(host='0.0.0.0')
