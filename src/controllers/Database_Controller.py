import sqlite3
import json
import os
import pickle
import sqlalchemy
from controllers.Validation_Exception import Validation_Exception


class Database_Controller:
  def __init__(self, path):
    with open(path) as file:  
      self.db_directory = json.load(file)
      self.db_directory = os.path.dirname(os.path.dirname(__file__)) + self.db_directory['path']
      self.my_pool = sqlalchemy.pool.QueuePool(self.get_connection, max_overflow=10, pool_size=6)

  def get_connection(self):
    connection = sqlite3.connect(self.db_directory)
    return connection

  def __serialize_data(self, data):
    serialized = pickle.dumps(data)
    return serialized

  def __deserialize_data(self, data):
    deserialized = pickle.loads(data)
    return deserialized

  def insert_into_db(self, receiptObj, logger):
    logger.debug('Inserting into db')
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor() 
      data_tuple = (receiptObj.receiptId, self.__serialize_data(receiptObj.data))
      command= """ INSERT INTO receipts (receiptId, information) VALUES (?, ?)"""
      db_cursor.execute(command, data_tuple)
      connection.commit()
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.DBAPIError) as db_error:
      logger.debug(db_error.detail)
    except (sqlite3.Error) as db_error:
      logger.debug(db_error)
    finally:
      logger.debug("CLOSING CONNECTION")
      connection.close()

  def check_existing_id(self, u_id):
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor()
      command = """SELECT * 
              FROM receipts 
              WHERE receiptId = ? """
      db_cursor.execute(command, (u_id,))
      row = db_cursor.fetchone()
      if row is not None:
        raise Validation_Exception("This receipt is already in the database")
    finally:
      connection.close()

  def get_from_db(self, u_id, logger, Receipt):
    logger.debug("Selecting from db")
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor()
      logger.debug("Just before command")
      command = """SELECT * 
              FROM receipts 
              WHERE receiptId = ? """
      db_cursor.execute(command, (u_id,))
      data = db_cursor.fetchall()

      if data is None:
        raise Validation_Exception("No such receipt in database")

      logger.debug("CREATING RECEIPT FROM DB")
      newReceipt = Receipt(data[0][0], self.__deserialize_data(data[0][1]),logger, alt=True)
      return newReceipt
    finally:
      logger.debug("CLOSING CONNECTION")
      connection.close()

  
