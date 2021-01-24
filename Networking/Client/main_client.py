#!/usr/bin/env python3
import queue
import time

# from app import GameHandler
from Network import NetworkManager


def main():
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    network = NetworkManager(input_queue, output_queue)
    # game_handler = GameHandler(input_queue, output_queue)
    network_thread = network.run()
    # game_handler.launch()

    #  Fake render loop
    ping_pong = True
    while True:
        while not input_queue.empty():
            rec = input_queue.get()
            print(f"server says: {rec!r}")
            input_queue.task_done()
        if not output_queue.full():
            data = b"ping" if ping_pong else b"pong"
            output_queue.put(data)
        time.sleep(2)
        ping_pong = not ping_pong


if __name__ == '__main__':
    main()
