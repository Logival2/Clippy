#!/usr/bin/env python3
import trio
import threading
from itertools import count


class NetworkManager(object):

    def __init__(self, incomingQueue, outgoingQueue, port=8080):
        self.port = port
        self.incomingQueue = incomingQueue
        self.outgoingQueue = outgoingQueue
        self.isRunning = False
        self.thread = None
        self.connectionCounter = count()

    async def handle_connection(self, connection):
        id = next(self.connectionCounter)
        print(f"received connection: connection number {id}")
        try:
            async for data in connection:
                print(f"connection n°{id}: received --> '{repr(data)}'")
                await connection.send_all(data)
            print(f"connection n°{id}: connection closed")
        except Exception as exc:
            print(f"connection n°{id} crashed: {repr(exc)}")

    async def serve(self):
        print(f"server listening on port {self.port}")
        await trio.serve_tcp(self.handle_connection, self.port)

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        self.thread = threading.Thread(target=trio.run, args=[self.serve])
        self.thread.start()
        return self.thread
