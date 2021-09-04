import sqlite3

database = sqlite3.connect("receipts.db")

cs = database.cursor()

cs.execute("""CREATE TABLE receipts (
        receiptID TEXT PRIMARY KEY UNIQUE NOT NULL,
        name TEXT NOT NULL,
        phone TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        orderID TEXt UNIQUE NOT NULL,
        address_from TEXT NOT NULL,
        longitude_from REAL NOT NULL,
        latitude_from REAL NOT NULL,
        address_to TEXT NOT NULL,
        logitutude_to REAL NOT NULL,
        latitude_to REAL NOT NULL,
        dimensions TEXT,
        courierID TEXT UNIQUE NOT NULL,
        courier_phone TEXT,
        courier_email TEXT  NOT NULL,
        base_fare REAL NOT NULL
    )""")