#!/usr/bin/env python3
from GameServer import Server


def main():
    server = Server("127.0.0.1", 1337)
    server.run()


if __name__ == '__main__':
    main()
