import asyncio
from websockets.asyncio.client import connect
import time
import signal
from confluent_kafka import Producer


URL = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"
_TIME_TO_STOP_SECONDS = 10


async def connect_to_firehose():
    consumed_messages = 0
    async with connect(URL) as websocket:
        start = time.time()
        t1 = time.time()
        # Close the connection when receiving SIGTERM.
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, loop.create_task, websocket.close())
        async for message in websocket:
            consumed_messages += 1
            curr = time.time()
            producer.produce("atproto_firehose_repo", value=message.encode("utf-8"))
            producer.flush()
            if curr - t1 >= 1:
                events_per_seconds = consumed_messages / (curr - t1)
                print(f"Messages per second {events_per_seconds:.0f}")
                t1 = time.time()
                consumed_messages = 0


if __name__ == "__main__":
    producer = Producer({"bootstrap.servers": "kafka:9092"})
    asyncio.run(connect_to_firehose())
