from flask import Flask, request, render_template, url_for
import os
import json

template_dir = os.path.relpath('/resources/templates/')
print(template_dir)

server = Flask(__name__)

@server.route("/message-queue")
def hello():
  return "Hello World!"

@server.route("/test")
def user():
  return render_template('user.html')

@server.route("/<string:trip>", methods = ['GET'])
def receipt_request(trip):
  username = request.args.get('name')
  return f'Hello {username}!'

@server.route("/orders", methods = ['POST'])
def orders():
  order = request.json
  server.logger.debug(order)
  
  return "Successfully Received"



  

if __name__ == "__main__":
   server.run(host='0.0.0.0')


