import sqlite3
import os


database = sqlite3.connect(os.path.dirname(__file__) + "/resources/database/receipts.db")

cs = database.cursor()

cs.execute("""CREATE TABLE receipts (
        receiptId TEXT PRIMARY KEY UNIQUE NOT NULL,
        clientName TEXT NOT NULL,
        clientEmail TEXT NOT NULL,
        phoneNumber TEXT NOT NULL,
        orderId TEXT UNIQUE NOT NULL,
        from TEXT NOT NULL,
        to TEXT NOT NULL,
        dimensions TEXT,
        deliveryType TEXT NOT NULL,
        tripId TEXT NOT NULL,
        courierId TEXT NOT NULL,
        courierName TEXT NOT NULL,
        courier_phone TEXT,
        courier_email TEXT  NOT NULL,
        total_cost REAL NOT NULL
    )""")

cs.close()