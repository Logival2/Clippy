#!/usr/bin/env python3
import sys
import trio

PORT = 8080
RUNNING = True


async def sender(stream):
    print("sender: started")
    while RUNNING:
        data = b"hello from client !"
        print(f"sender: sending {data!r}")
        await stream.send_all(data)
        await trio.sleep(1)


async def receiver(stream):
    print("receiver: started")
    async for data in stream:
        print(f"receiver: received '{data!r}'")
    print("receiver: connection closed")
    sys.exit()


async def parent():
    print(f"parent connecting to 127.0.0.1:{PORT}")
    stream = await trio.open_tcp_stream("127.0.0.1", PORT)
    async with stream:
        async with trio.open_nursery() as nursery:
            print("parent: spawn sender")
            nursery.start_soon(sender, stream)
            print("parent: spawn receiver")
            nursery.start_soon(receiver, stream)


def main():
    trio.run(parent)


if __name__ == '__main__':
    main()
