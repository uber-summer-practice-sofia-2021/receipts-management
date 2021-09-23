"""
Mock kafka consumer.

By defualt use at least once processing.
See 'https://faust.readthedocs.io/en/latest/userguide/settings.html#processing-guarantee'.

"""

import faust
import aiohttp
import os
import time

# all ENVs

# freya_url = "http://localhost:5000/receive_trip_id"
# broker="kafka://kafka:29092",
# test

#    "kafka_consumer",
# broker="kafka://kafka:29092",
# test
# freya_url = "http://localhost:5000/receive_trip_id"

TOPIC0000 = os.environ["TOPIC0000"]
# TOPIC0001 = os.environ["TOPIC0001"]
# TOPIC0002 = os.environ["TOPIC0002"]
# TOPIC0006 = os.environ["TOPIC0006"]
# TOPIC0024 = os.environ["TOPIC0024"]
# TOPIC0120 = os.environ["TOPIC0120"]
# TOPIC0720 = os.environ["TOPIC0720"]
# TOPIC5040 = os.environ["TOPIC5040"]
TOPIC_DLQ = os.environ["TOPIC_DLQ"]

APP_ID = os.environ["APP_ID"]
BROKERS = os.environ["BROKERS"]
FREYA_URL = os.environ["FREYA_URL"]

# faust App
app = faust.App(
    APP_ID,
    broker=BROKERS,
)


## no schema, but the couriers' fixture's key's name is "tripID"
# {
#     "tripID": "f570aa5e-5836-43ed-89e3-910be85bed12"
# }
#
class Trip(faust.Record):
    tripID: str


trips_topic_0000 = app.topic(TOPIC0000, key_type=None, value_type=Trip)
# trips_topic_0001 = app.topic(TOPIC0001, key_type=None, value_type=Trip)
# trips_topic_0002 = app.topic(TOPIC0002, key_type=None, value_type=Trip)
# trips_topic_0006 = app.topic(TOPIC0006, key_type=None, value_type=Trip)
# trips_topic_0024 = app.topic(TOPIC0024, key_type=None, value_type=Trip)
# trips_topic_0120 = app.topic(TOPIC0120, key_type=None, value_type=Trip)
# trips_topic_0720 = app.topic(TOPIC0720, key_type=None, value_type=Trip)
# trips_topic_5040 = app.topic(TOPIC5040, key_type=None, value_type=Trip)
trips_topic__dlq = app.topic(TOPIC_DLQ, key_type=None, value_type=Trip)


@app.agent(trips_topic_0000)
async def read_trips_IDs_0000(trips):
    async with aiohttp.ClientSession() as session:
        async for trip in trips:
            ## json ala freya url style -- see receipts-management/src/server.py
            my_json = {"tripId": trip.tripID}

            ## stdout is my log
            print(f"{TOPIC0000}: {trip.tripID}")  # <<<--------

            async with session.post(FREYA_URL, json=my_json) as resp:
                response = await resp.text()
                if response == 200:
                    pass
                elif response == 503:  # <<<--------
                    # await trips_topic_0001.send(value=Trip(tripID=trip.tripID))
                    await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))
                else:
                    await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


if __name__ == "__main__":
    ## docker race condition hack - see readme
    time.sleep(5)

    app.main()


# @app.agent(trips_topic_0000)
# async def read_trips_IDs_0000(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0000}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0001.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0001)
# async def read_trip_IDs_0001(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0001}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0002.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0002)
# async def read_trip_IDs_0002(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0002}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0006.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0006)
# async def read_trip_IDs_0006(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0006}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0024.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0024)
# async def read_trip_IDs_0024(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0024}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0120.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0120)
# async def read_trip_IDs_0120(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0120}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_0720.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_0720)
# async def read_trip_IDs_0720(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC0720}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic_5040.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))


# @app.agent(trips_topic_5040)
# async def read_trip_IDs_5040(trips):
#     async with aiohttp.ClientSession() as session:
#         async for trip in trips:
#             ## json ala freya url style -- see receipts-management/src/server.py
#             my_json = {"tripId": trip.tripID}

#             ## stdout is my log
#             print(f"{TOPIC5040}: {trip.tripID}")  # <<<--------

#             async with session.post(FREYA_URL, json=my_json) as resp:
#                 response = await resp.text()
#                 if response == 200:
#                     pass
#                 elif response == 503:  # <<<--------
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))
#                 else:
#                     await trips_topic__dlq.send(value=Trip(tripID=trip.tripID))
