#!/usr/bin/env python3
import trio
import threading


class NetworkManager(object):

    def __init__(self, incomingQueue, outgoingQueue, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.incomingQueue = incomingQueue
        self.outgoingQueue = outgoingQueue
        self.stream = None
        self.isRunning = False
        self.thread = None

    async def sender(self):
        print("network -- sender started")
        while self.isRunning:
            data = await trio.to_thread.run_sync(self.outgoingQueue.get)
            print(f"network -- sending '{data}'")
            await self.stream.send_all(data)

    async def receiver(self):
        print("network -- receiver started")
        async for data in self.stream:
            if not self.isRunning:
                return
            await trio.to_thread.run_sync(self.incomingQueue.put, data)
        print("network -- receiver: connection closed")
        return

    async def connect(self):
        print(f"network -- connecting to {self.host}:{self.port}.")
        self.stream = await trio.open_tcp_stream(self.host, self.port)
        async with self.stream:
            async with trio.open_nursery() as nursery:
                print("network -- spawning sender...")
                nursery.start_soon(self.sender)
                print("network -- spawning receiver...")
                nursery.start_soon(self.receiver)
            print("network -- receiver and sender exited, nursery closed, closing stream...")
        print("network -- stream closed")

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        self.thread = threading.Thread(target=trio.run, args=[self.connect])
        self.thread.start()
        return self.thread
