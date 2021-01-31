import re
import os
import datetime

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


class Response(object):
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def serialize(self):
        return self.__str__()

    def __str__(self):
        data = [str(x) for x in self.data]
        return "{}{}{}{}".format(str(self.code), SEPARATOR, SEPARATOR.join(data), EOM)


class Logger(object):
    def __init__(self):
        if CREATE_LOG:
            if not os.path.isdir(LOGS_PATH):
                os.mkdir(LOGS_PATH)
            self.f = open(
                LOGS_PATH + datetime.datetime.now().strftime("%d_%m_%Y_%H:%M:%S") + '.log',
                "w",
                encoding='utf-8'
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if CREATE_LOG:
            self.f.close()

    def log(self, msg, color='', individual_msg=False):
        if not LOG_INDIVIDUAL_CONNECTIONS and individual_msg:
            return
        if CREATE_LOG:
            self.f.write(msg + '\n')
        print("{}[{}]: {}{}".format(color, datetime.datetime.now().strftime("%H:%M:%S"), msg, RESET))
