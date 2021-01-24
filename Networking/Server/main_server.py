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

    #  Fake game loop
    while True:
        while not input_queue.empty():
            rec = input_queue.get()
            print(f"gameloop -- received : {rec!r}")
            if not output_queue.full():
                output_queue.put(b"I received " + rec)
            input_queue.task_done()
        time.sleep(0.5)


if __name__ == '__main__':
    main()
