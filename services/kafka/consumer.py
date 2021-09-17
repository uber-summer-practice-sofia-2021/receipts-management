"""
Mock kafka consumer.

By defualt use at least once processing.
See 'https://faust.readthedocs.io/en/latest/userguide/settings.html#processing-guarantee'.

"""

import faust
import aiohttp

app = faust.App(
    "kafka_consumer",
    broker="kafka://localhost:9092",
    topic_partitions=1,
)


class TripID(faust.Record):
    id: str


# 'test' is the name of the topic, set in ./docker-compose.yml
trip_IDs_topic = app.topic("test", key_type=None, value_type=TripID)


@app.agent(trip_IDs_topic)
async def read_trip_IDs(trips):
    async with aiohttp.ClientSession() as session:
        async for trip in trips:
            freya_url = "http://localhost:5000/receive_trip_id"
            ## temporary fix until our main endpoint is properly configured
            my_json = {"tripId": "97df8470-1a84-49fa-9164-92dcf4135b99"}
            async with session.post(freya_url, json=my_json) as resp:
                helper = await resp.text()
                print(f"send message with trip id {trip.id}")


if __name__ == "__main__":
    app.main()
