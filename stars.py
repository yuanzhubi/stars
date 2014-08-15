import os
import requests
import urlparse
from threading import Thread
from Queue import Queue


USER = os.environ['GH_USER']
PASSWORD = os.environ['GH_PASS']
BASE_URL = 'https://api.github.com'

def get_last_pagenum():
    return urlparse.parse_qs(requests.head('https://api.github.com/user/starred?per_page=100&page=1', auth=(USER, PASSWORD)).links['last']['url'])['page'][0]


def get_page_url(pagenum):
    return BASE_URL + '/user/starred?per_page=100&page=' + str(pagenum)


def get_page_json(q, url):
    q.put(requests.get(url, auth=(USER, PASSWORD)).json())


def main():
    q = Queue()
    lp = get_last_pagenum()

    for url in [get_page_url(page) for page in range(1,int(lp)+1)]:
        t = Thread(target=get_page_json, args=(q, url))
        t.daemon = True
        t.start()

    s = q.get()
    print s


if __name__ == '__main__':
    main()