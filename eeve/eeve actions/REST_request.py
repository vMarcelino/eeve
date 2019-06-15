import requests
import time
import travel_backpack


def run(method: str, url: str, retry_count: int = -1, wait_time: float = 5, asynchronous: bool = True, **kwargs):
    """Makes a web request using the given method to the given url.

    It's possible to set how many times to retry with 'retry_count' parameter. The request can be made
    asynchronous too

    keyword arguments are passed directly to python's requests.request function
    
    Arguments:
        method {str} -- The method to use in the request (GET, POST ...)
        url {str} -- The url to make the request
    
    Keyword Arguments:
        retry_count {int} -- number of times to retry connection in case it was not successful (default: {-1})
        wait_time {float} -- time to wait between retry attempts (default: {5})
        asynchronous {bool} -- whether to start the request in a different thread (default: {True})
    """
    if asynchronous:
        travel_backpack.thread_encapsulation(run)(method,
                                                  url,
                                                  retry_count=retry_count,
                                                  wait_time=wait_time,
                                                  asynchronous=False,
                                                  **kwargs)
        return
    else:
        retry = True
        print('REST request:', method, url, kwargs)
        while retry:
            try:
                requests.request(method, url)
                retry = False
            except requests.exceptions.ConnectionError as e:
                #print(e)
                print('.')
                if retry_count == 0:
                    retry = False
                else:
                    retry_count -= 1
                    time.sleep(wait_time)
                    retry = True


actions = {'rest request': run}

if __name__ == '__main__':
    import sys
    a = sys.argv
    run(a[1], a[2], *a[2:])