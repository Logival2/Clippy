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

    def serialize(self):
        return pickle.dumps(self)
