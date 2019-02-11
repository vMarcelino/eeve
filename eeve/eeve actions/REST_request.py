import requests
import time


class Request:
    def run(self, method, url, *args, retry_count=-1, wait_time=5, **kwargs):
        retry = True
        while retry:
            try:
                print('REST request:', method, url, args, kwargs)
                requests.request(method, url)
                retry = False
            except requests.exceptions.ConnectionError as e:
                print(e)
                if retry_count == 0:
                    retry = False
                else:
                    retry_count -= 1
                    time.sleep(wait_time)
                    retry = True


actions = {'rest request': Request}