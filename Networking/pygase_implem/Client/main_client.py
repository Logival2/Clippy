#!/usr/bin/env python3
import time
import logging
from pygase import Client
from pygase.utils import logger
from pygase.connection import ConnectionStatus
logging.basicConfig()
logging.root.setLevel(logging.INFO)


class Clippy_Client(object):
    """docstring for Clippy_Client."""

    def __init__(self):
        super(Clippy_Client, self).__init__()
        self.client = Client()
        self.running = True
        self.connection_thread = None

    def run(self):
        retries = 5
        while retries > 0:
            print(f"try {retries}")
            self.connection_thread = self.client.connect_in_thread(port=8080)
            time.sleep(1)
            if(self.client.connection.status != ConnectionStatus.get("Connected")):
                print("connection to the server failed, retrying...")
                self.connection_thread.join()
            else:
                break
        if self.client.connection.status != ConnectionStatus.get("Connected"):
            print("failed to connect to server")
            return

        while self.running:
            with self.client.access_game_state() as game_state:
                try:
                    print(game_state.position)
                    print(game_state.hp)
                except Exception as e:
                    print(e)
                time.sleep(0.5)


def main():
    game = Clippy_Client()
    game.run()


if __name__ == '__main__':
    main()
