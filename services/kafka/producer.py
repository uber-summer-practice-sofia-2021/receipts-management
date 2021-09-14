import faust

# from datetime import datetime

app = faust.App(
    "kafka_producer",
    broker="kafka://localhost:9092",
    topic_partitions=1,
)

# datetime: https://faust.readthedocs.io/en/latest/userguide/models.html?highlight=datetime
class TripID(faust.Record):
    id: str


# 'test' is the name of the topic, set in ./docker-compose.yml
trip_IDs_topic = app.topic("test", key_type=None, value_type=TripID)


## each 1.0 seconds send values
@app.timer(1.0)
async def send_value():
    await trip_IDs_topic.send(value=TripID(TripID(id="----------------send id:")))
    for i in range(1, 10):
        await trip_IDs_topic.send(value=TripID(TripID(id=f"send id: {i}")))


if __name__ == "__main__":
    app.main()
