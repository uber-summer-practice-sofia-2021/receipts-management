import sqlite3
import json
import os
import pickle

class Database_Controller:
  def __init__(self, path):
    with open(path) as file:  
      self.db_directory = json.load(file)
      self.db_directory = os.path.dirname(os.path.dirname(__file__)) + self.db_directory['path']
      self.database = sqlite3.connect(self.db_directory)

  def close_db_connection(self):
    self.datbase.close()

  def __serialize_data(self, data):
    serialized = pickle.dumps(data)
    return serialized

  def __deserialize_data(self, data):
    deserialized = pickle.loads(data)
    return deserialized

  def insert_into_db(self, receiptObj):
    cur = self.database.cursor()
    data_tuple = (receiptObj.receiptId, self.__serialize_data(receiptObj.data))
    command= """ INSERT INTO receipts (receiptId, information) VALUES (?, ?)"""
    cur.execute(command, data_tuple)
    self.database.commit()

  def get_from_db(self, u_id, logger, Receipt):
    cur = self.database.cursor()
    logger.debug("Just before command")
    command = """SELECT * 
             FROM receipts 
             WHERE receiptId = ? """
    cur.execute(command, (u_id,))
    data = cur.fetchall()
    newReceipt = Receipt(data[0][0], self.__deserialize_data(data[0][1]))
    return newReceipt

  
