import socket
import pickle
import queue
from threading import Thread


class NetworkManager(object):
    def __init__(s, client_id, ip, port, receive_q, send_q):
        s.client_id = client_id
        s.ip = ip
        s.port = port
        s.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.socket.connect((s.ip, s.port))
        s.receive_q = receive_q
        s.send_q = send_q
        s.receive_t = Thread(target=s.receive_f, args=(receive_q,))
        s.receive_t.setDaemon(True)
        s.receive_t.start()
        s.send_t = Thread(target=s.send_f, args=(send_q,))
        s.send_t.setDaemon(True)
        s.send_t.start()

    def send_f(s, send_q):
        while 42:
            if not send_q.empty():
                payload = send_q.get()
                s.socket.sendall(pickle.dumps(payload))

    def receive_f(s, receive_q):
        while 42:
            data = s.socket.recv(1024)
            receive_q.put(pickle.loads(data))
