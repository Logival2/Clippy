#!/usr/bin/env python3
import trio
import threading
from itertools import count

PORT = 8080
COUNTER = count()


class NetworkManager(object):

    def __init__(self, incomingQueue, outgoingQueue, port=8080):
        self.counter = count()
        self.port = port
        self.incomingQueue = incomingQueue
        self.outgoingQueue = outgoingQueue
        self.stream = None
        self.isRunning = False
        self.thread = None

    async def serve(self, stream):
        id = next(self.counter)
        try:
            async for data in stream:
                print(f"network -- connection n°{id} says: {data!r}")
                await trio.to_thread.run_sync(self.incomingQueue.put, data)
                if not self.outgoingQueue.empty():
                    data = await trio.to_thread.run_sync(self.outgoingQueue.get)
                    print(f"network -- conection n°{id} sending: {data!r}")
                    await stream.send_all(data)
            print(f"connection n°{id} closed")
        except Exception as e:
            print(f"connection n°{id} crashed: {e!r}")

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        self.thread = threading.Thread(target=trio.run, args=[trio.serve_tcp, self.serve, self.port])
        self.thread.start()
        return self.thread
