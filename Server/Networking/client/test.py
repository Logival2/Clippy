#!/usr/bin/env python3
import threading
import queue
import GameHandler from app
import NetworkManager from Network


def main():
    input_queue = queue.Queue()
    output_queue = queue.Queue()

    network = NetworkManager(input_queue, output_queue)
    game_handler = GameHandler(input_queue, output_queue)
    network_thread = network.run()
    game_handler.launch()


if __name__ == '__main__':
    main()
