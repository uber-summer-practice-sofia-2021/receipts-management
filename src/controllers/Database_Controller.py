import sqlite3
import json
from flask import g


class Database_Controller:
  def __init__(self, path):
    with open(path) as file:  
      db_directory = json.load(file)
      self.__database = db_directory['path']

  def get_db(self):
    db = getattr(g, '_database', None)
    if db is None:
      db = g._database = sqlite3.connect(self.__database)
    return db

  def close_db_connection(self):
    db = getattr(g, '_database', None)
    if db is not None:
      db.close()

  def make_dicts(cursor, row):
      return dict((cursor.description[idx][0], value)
                  for idx, value in enumerate(row))
                  
  def query_db(self, query, args=(), one=False):
    cur = self.get_db().execute(query, args)
    rv = cur.fetchall()
    self.close_db_connection()
    return (rv[0] if rv else None) if one else rv

  
