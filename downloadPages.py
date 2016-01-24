import socks
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
import socket
socket.socket = socks.socksocket
import json
import os
import sys
import multiprocessing

import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

import logging
# set up logging to file - see previous section for more details
logging.basicConfig(filename='downloadPages.log',level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

CHUNK_SIZE = 4

def getURL(num):
    lineNum = 0
    with open("sitemap/URLS.txt",'r') as f:
        for line in f:
            lineNum += 1
            if lineNum == num:
                return line.strip()
    raise

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def downloadPage(num):
    logger = logging.getLogger('downloadPage')
    try:
        r = requests.get(getURL(num), headers=headers)
        #r = requests.get('http://whatsmyip.net/', headers=headers, timeout=10)
        html_text = r.text
        if r.status_code != 200:
            raise
        return True, num, html_text
    except:
        return False, num, ""


def downloadPages(nums):
    logger = logging.getLogger('downloadPages')
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    data = {}
    for numsToDo in chunks(nums,CHUNK_SIZE):
        finished = False
        numsToDo = list(numsToDo)
        while not finished:
            logger.info(numsToDo)
            results = pool.map(downloadPage, list(numsToDo))
            finished = True
            for result in results:
                if result[0] == True:
                    data[result[1]] = result[2]
                    numsToDo = list(set(numsToDo) - set([result[1]]))
                else:
                    finished = False
            if not finished:
                os.system('/etc/init.d/tor restart')
                logger.debug("Restarting tor")
    return data

if __name__ == '__main__':
    nums = []
    for arg in sys.argv[1:]:
        nums.append(int(arg))
    data = downloadPages(nums)
    with open('downloadedPages.json','w') as f:
        f.write(json.dumps(data))
