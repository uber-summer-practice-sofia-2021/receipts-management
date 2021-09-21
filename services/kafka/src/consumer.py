"""
Mock kafka consumer.

By defualt use at least once processing.
See 'https://faust.readthedocs.io/en/latest/userguide/settings.html#processing-guarantee'.

"""

import faust
import aiohttp
import os

# all ENVs

# freya_url = "http://localhost:5000/receive_trip_id"
# broker="kafka://kafka:29092",
# test

#    "kafka_consumer",
# broker="kafka://kafka:29092",
# test
# freya_url = "http://localhost:5000/receive_trip_id"

APP_ID = os.environ["APP_ID"]
BROKERS = os.environ["BROKERS"]
TOPIC = os.environ["TOPIC"]
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


trips_topic = app.topic(TOPIC, key_type=None, value_type=Trip)


@app.agent(trips_topic)
async def read_trip_IDs(trips):
    async with aiohttp.ClientSession() as session:
        async for trip in trips:
            ## json ala freya url style -- see receipts-management/src/server.py
            my_json = {"tripId": trip.tripID}

            async with session.post(FREYA_URL, json=my_json) as resp:
                helper = await resp.text()
                print(f"send message with trip id {trip.tripID}")


if __name__ == "__main__":
    app.main()
