import requests
import time


class Request:
    def __init__(self, method, url, *args, retry_count=-1, wait_time=5, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.method = method
        self.url = url
        self.retry_count = retry_count
        self.wait_time = wait_time

    def run(self):
        retry = True
        while retry:
            try:
                print('REST request:', self.method, self.url, self.args, self.kwargs)
                requests.request(self.method, self.url)
                retry = False
            except requests.exceptions.ConnectionError as e:
                print(e)
                if self.retry_count == 0:
                    retry = False
                else:
                    self.retry_count -= 1
                    time.sleep(self.wait_time)
                    retry = True


actions = {'rest request': Request}