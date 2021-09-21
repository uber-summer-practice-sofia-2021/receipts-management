"""
Mock kafka producer.

By defualt use at least once processing.
See 'https://faust.readthedocs.io/en/latest/userguide/settings.html#processing-guarantee'.

"""

import faust
import os

BROKERS = os.environ["BROKERS"]
TOPIC = os.environ["TOPIC"]
FREYA_URL = os.environ["FREYA_URL"]


## app TripID and the topic
app = faust.App(
    "kafka_producer",
    # broker="kafka://kafka:29092",
    broker=BROKERS,
)


class Trip(faust.Record):
    tripID: str


trips_topic = app.topic(TOPIC, key_type=None, value_type=Trip)


## each 1.0 seconds send values
@app.timer(1.0)
async def send_value():
    #    await trip_IDs_topic.send(value=TripID(TripID(id="----------------send id:")))
    for i in range(1, 10):
        await trips_topic.send(
            value=Trip(tripID=f"97df8470-1a84-49fa-9164-92dcf4135b99")
        )


if __name__ == "__main__":
    app.main()
