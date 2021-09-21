"""
Mock kafka producer.

By defualt use at least once processing.
See 'https://faust.readthedocs.io/en/latest/userguide/settings.html#processing-guarantee'.

"""

import faust

app = faust.App(
    "kafka_producer",
    broker="kafka://localhost:9092",
    topic_partitions=1,
)


class TripID(faust.Record):
    id: str


# 'test' is the name of the topic, set in ./docker-compose.yml
trip_IDs_topic = app.topic("test", key_type=None, value_type=TripID)


## each 1.0 seconds send values
@app.timer(10000.0)
async def send_value():
    await trip_IDs_topic.send(value=TripID(TripID(id="----------------send id:")))
    for i in range(1, 2):
        await trip_IDs_topic.send(
            value=TripID(TripID(id=f"97df8470-1a84-49fa-9164-92dcf4135b99"))
        )


if __name__ == "__main__":
    app.main()
