import sys
import zlib
import hashlib
import pickle

from CONFIG import *


class ClientObject(object):
    def __init__(self, client_id):
        self.client_id = client_id
        self.todo = None
        self.result = None

    def get_done_task(self):
        if not self.result:
            return
        res = self.result
        self.result = None
        return res


class Packet(object):
    def __init__(self, code, data):
        self.code = code
        self.data = data
        self.id = hash(self)

    def serialize(self):
        byte_data = pickle.dumps(self)
        compressed_data = zlib.compress(byte_data)
        # Split message if needed
        if sys.getsizeof(compressed_data) > MAX_TCP_PACKET_SIZE:
            res = list(chunk_map(compressed_data, MAX_TCP_PACKET_SIZE))
        else:
            res = [compressed_data]
        return res


def chunk_map(bs, n):
    for i in range(0, len(bs), n):
        yield bs[i:i+n]
