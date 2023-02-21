import requests
import concurrent.futures

def get_status(url):

    resp = requests.get(url=url)
    return resp.status_code

urls = ['http://webcode.me', 'https://httpbin.org/get',
    'https://google.com', 'https://stackoverflow.com',
    'https://github.com', 'https://clojure.org',
    'https://fsharp.org']


def checkStatus(urls):
    with concurrent.futures.ThreadPoolExecutor() as executor:

        futures = []
        statusList = []
        for url in urls:
            futures.append(executor.submit(get_status, url=url))

        for future in concurrent.futures.as_completed(futures):
            statusList.append(future.result())
    return statusList

status = checkStatus(urls)
res = {urls[i]: status[i] for i in range(len(status))}





res = {'http://webcode.me': 200, 'https://httpbin.org/get': 200, 'https://google.com': 200, 'https://stackoverflow.com': 200, 'https://github.com': 200, 'https://clojure.org': 200, 'https://fsharp.org': 200}

urls = [key for key, val in res.items() if val == 200]

print(urls)