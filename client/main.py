#!/usr/bin/env python3
import threading, queue

from app import GameHandler
from Network import NetworkManager


def main():
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    network = NetworkManager(input_queue, output_queue)
    game_handler = GameHandler(input_queue, output_queue)
    network_thread = network.run()
    game_handler.launch()


if __name__ == '__main__':
    main()
