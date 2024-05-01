# encoding='utr-8'
import pickle
import socket
import threading
import concurrent.futures as futures
from http_protocol import run_flask

pool = futures.ThreadPoolExecutor(max_workers=4)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('0.0.0.0', 10014))


class ClientSocket:
    def __init__(self, client_socket, address):
        self.client_socket = client_socket
        self.address = address

    def receive(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
            except Exception:
                break
            if not data:
                break
            obj = pickle.loads(data)
            print('server: protocol_data:', obj)
        print('server: client ', self.address, ' close')
        self.client_socket.colse()


def listen_client():
    # 参数: 指定最多允许多少个客户连接到服务器。它的值至少为1。收到连接请求后，这些请求需要排队，如果队列满，就拒绝请求。
    server_socket.listen(20)

    while True:
        print('server: accept connection')
        client_socket, addr = server_socket.accept()
        print('server: connected:', addr)
        client = ClientSocket(client_socket, addr)
        pool.submit(client.receive)
        client_socket.send(pickle.dumps({'type': 1, 'data': 'welcome'.encode('utf-8')}))


if __name__ == '__main__':
    f1 = pool.submit(listen_client)
    run_flask()
    futures.wait([f1])
