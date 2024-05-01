import pickle
import socket
import threading

import concurrent.futures as futures

pool = futures.ThreadPoolExecutor(4)


class ProtocolData:
    def __init__(self, type, data):
        self.type = type
        self.data = data

    @staticmethod
    def loads(bytes):
        return pickle.loads(bytes)

    def dumps(self):
        return pickle.dumps(self)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def analyze_data(bytes):
    data = ProtocolData.loads(bytes)
    print('protocol data:', data.type, 'data:', data.data)


def receive():
    def do():
        socket.connect(('localhost', 10014))
        while True:
            try:
                data = socket.recv(1024)
                analyze_data(data)
            except Exception as e:
                print("client: received error : ", e)
                break
        print('client received end !!!')

    return pool.submit(do)


def send(protocol_data):
    pool.submit(lambda: protocol_data.dumps(protocol_data))


if __name__ == '__main__':
    futrue = receive()
    futures.wait([futrue])
    print('client end !!!')
