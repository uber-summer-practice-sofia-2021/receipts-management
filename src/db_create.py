from posixpath import relpath
import sqlite3
import os


database = sqlite3.connect(os.path.dirname(__file__) + "/resources/database/receipts.db")

cs = database.cursor()

cs.execute("""CREATE TABLE receipts (
        receiptID TEXT PRIMARY KEY UNIQUE NOT NULL,
        clientName TEXT NOT NULL,
        clientEmail TEXT NOT NULL,
        phone TEXT NOT NULL,
        orderID TEXt UNIQUE NOT NULL,
        address_from TEXT NOT NULL,
        longitude_from REAL NOT NULL,
        latitude_from REAL NOT NULL,
        address_to TEXT NOT NULL,
        longitude_to REAL NOT NULL,
        latitude_to REAL NOT NULL,
        length REAL,
        depth REAL,
        height REAL,
        weight REAL,
        deliveryType TEXT NOT NULL,
        courierID TEXT NOT NULL,
        courierName TEXT NOT NULL,
        courier_phone TEXT,
        courier_email TEXT  NOT NULL,
        total_cost REAL NOT NULL
    )""")

cs.close()