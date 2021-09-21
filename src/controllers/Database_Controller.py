import sqlite3
import json
import os
import pickle
import sqlalchemy
from controllers.ValidationException import ValidationException


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
    logger.info("Inserting into the database")
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor() 
      data_tuple = (receiptObj.receiptId, self.__serialize_data(receiptObj.data))
      command= """ INSERT INTO receipts (receiptId, information) VALUES (?, ?)"""
      db_cursor.execute(command, data_tuple)
      connection.commit()
    except sqlite3.IntegrityError as e:
      raise ValidationException("Already in the database") from e
    except sqlite3.Error as e:
      raise e
    finally:
      logger.info("CLOSING DATABASE CONNECTION")
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
        raise ValidationException("This receipt is already in the database")
    except ValidationException:
      raise
    except IndexError:
      pass
    except Exception as e:
      raise sqlite3.Error("Something went wrong with the database") from e
    finally:
      connection.close()

  def get_from_db(self, u_id, logger, Receipt):
    logger.info("Selecting from db")
    try:
      connection = self.my_pool.connect()
      db_cursor = connection.cursor()
      command = """SELECT * 
              FROM receipts 
              WHERE receiptId = ? """
      db_cursor.execute(command, (u_id,))
      data = db_cursor.fetchall()
      logger.info("CREATING RECEIPT FROM DB")
      newReceipt = Receipt(data[0][0], self.__deserialize_data(data[0][1]),logger, alt=True)
      return newReceipt
    except IndexError as e:
      raise ValidationException("No such receipt in database.") from e
    except Exception as e:
      raise sqlite3.Error("Something went wrong with the database.") from e
    finally:
      logger.info("CLOSING DATABASE CONNECTION")
      connection.close()

  
