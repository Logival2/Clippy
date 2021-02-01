import json

from NetworkManager import NetworkManager
from utils import Packet
from CONFIG import *

class Manager(object):
    def __init__(self):
        self.clients = {}
        self.network_manager = NetworkManager(self.clients)
        print("Init done, server started")

    def start(self):
        while 42:
            self.network_manager.do_turn()
            for client_id, client_object in self.clients.items():
                if not client_object.todo:
                    continue
                result = self.handle_msg(client_object.todo)  # Returns a Response object
                client_object.result = result
                client_object.todo = None

    def handle_msg(self, msg):
        print(msg)
        return Packet(2, msg)


if __name__ == '__main__':
    try:
        manager = Manager()
    except OSError:
        print("{}Init failed, TCP address already in use, change TCP port{}".format(RED, RESET))
    else:
        manager.start()
