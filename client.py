import uuid
import json
import os
import time
import sys

import requests

from lib.clientProcessing import *

def doWork(server, apikey):
    # GET WORK
    r = requests.get(server, {'apikey': apikey})
    data = json.loads(r.text)

    if not data['success']:
        return False

    payload = {'apikey': apikey, 'work': data[
        'work'], 'rate': 0, 'data': 'None'}

    # RUN PROGRAM
    t0 = time.time()
    payload['data'] = processWork(data['work'])
    payload['rate'] = (time.time() - t0) / float(len(data['work']))

    # POST WORK
    postSuccess = False
    counter = 0
    while postSuccess == False:
        try:
            r = requests.post(server, data=json.dumps(payload))
            data = json.loads(r.text)
            postSuccess = data['success']
        except:
            time.sleep(3)
            counter += 1
            if counter > 3:
                return False # if server not responding, then exit

    return True


if __name__ == '__main__':
    apikey = str(uuid.uuid4()).replace('-', '')
    server = sys.argv[1]
    stillWorkToDo = True
    while stillWorkToDo:
        stillWorkToDo = doWork('http://' + server + "/work", apikey)
