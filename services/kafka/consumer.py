import faust

# from datetime import datetime

app = faust.App(
    "kafka_consumer",
    broker="kafka://localhost:9092",
    topic_partitions=1,
)

# datetime: https://faust.readthedocs.io/en/latest/userguide/models.html?highlight=datetime
class TripID(faust.Record):
    id: str


# 'test' is the name of the topic, set in ./docker-compose.yml
trip_IDs_topic = app.topic("test", key_type=None, value_type=TripID)


@app.agent(trip_IDs_topic)
async def read_trip_IDs(trips):
    async for trip in trips:
        print(f"trip {trip.id} happened")


if __name__ == "__main__":
    app.main()
