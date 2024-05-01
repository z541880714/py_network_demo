import os.path
import pickle

import requests
from concurrent.futures import ThreadPoolExecutor, wait

pool = ThreadPoolExecutor(max_workers=1)

dir = os.path.dirname(__file__)


class MyWork:
    def __init__(self, client_socket, key):
        self.client_socket = client_socket
        self.key = key

    def start_work(self):
        def do():
            assert self.send_file()

        pool.submit(do)

    def send_file(self):
        print("client start work")
        self.client_socket.send(pickle.dumps({'type': 3, 'data': "start upload file!!!"}))
        print('path:', os.path.abspath('res'))
        result = requests.post('http://127.0.0.1:10013/upload',
                               files={'file': open(f'{dir}/res/微信图片_20240427002225.jpg', 'rb')}
                               )

        return result.text == '1'
