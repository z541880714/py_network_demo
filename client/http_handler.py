import requests
from concurrent.futures import ThreadPoolExecutor

pool = ThreadPoolExecutor(max_workers=4)


def send_file(file_path):
    file_path = file_path.replace('\\', '/')
    file_name = file_path.split('/')[-1]
    pool.submit(
        lambda: requests.post("http://127.0.0.1/update",
                              data={'file_name': file_name},
                              files={'file': open(file_path, 'rb')}))
