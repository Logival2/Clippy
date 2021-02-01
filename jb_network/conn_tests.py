#!/usr/bin/env python3
import socket

from CONFIG import *


class Client(object):
    def __init__(self, id):
        self.data = "{} - Hello World\0".format(id)
        self.id = id
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.send(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.s.shutdown(socket.SHUT_RDWR)
        self.s.close()

    def connect(self):
        try:
            self.s.connect(SERVER_ADDRESS)
        except ConnectionRefusedError:
            print("{} cannot connect".format(self.id))

    def send(self, receive=False):
        self.s.sendall(self.data.encode())
        print("{} - Bytes Sent: {}".format(self.id, self.data))
        if receive:
            received = self.s.recv(BUFFER_SIZE)
            print("{} - Bytes Received: {}".format(self.id, received))


if __name__ == '__main__':
    clients = [Client(a) for a in range(2000)]
    # clients2 = [Client(a) for a in range(1020)]
    for client in clients:
        client.send(True)
