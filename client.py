import uuid
import json
import os
import time
import sys
import random

import requests

from lib.clientProcessing import *

def doWork(server, apikey):
    # GET WORK
    r = requests.get(server, {'apikey': apikey})
    data = json.loads(r.text)
    print(data)

    if not data['success']:
        return False

    payload = {'apikey': apikey, 'work': data[
        'work'], 'rate': 0, 'data': 'None'}

    # RUN PROGRAM
    t0 = time.time()
    payload['data'] = processWork(data['work'])
    payload['rate'] = (time.time() - t0) / float(len(data['work']))

    # POST WORK
    try:
        r = requests.post(server, data=json.dumps(payload))
        data = json.loads(r.text)
    except:
        return False
    return True


if __name__ == '__main__':
    apikey = str(uuid.uuid4()).replace('-', '')
    server = sys.argv[1]
    print(server)
    stillWorkToDo = True
    while stillWorkToDo:
        stillWorkToDo = doWork('http://' + server + "/work", apikey)
