import pickle
import socket
import concurrent.futures as futures
import time

from mywork import MyWork

pool = futures.ThreadPoolExecutor(4)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
work_handler = MyWork(client_socket)


def analyze_data(bytes):
    obj = pickle.loads(bytes)
    print('protocol type:{}, data:{}'.format(type(obj), obj))
    if obj['type'] == 1:
        work_handler.start_work()


def receive():
    def do():
        client_socket.connect(('localhost', 10014))
        while True:
            try:
                data = client_socket.recv(1024)
                analyze_data(data)
            except Exception as e:
                print("client: received error : ", e)
                break
        print('client received end !!!')

    return pool.submit(do)


if __name__ == '__main__':
    futrue = receive()
    futures.wait([futrue])
    print('client end !!!')
