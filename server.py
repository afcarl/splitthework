import logging
import copy
from itertools import groupby
import json
import time

from flask import Flask, jsonify, request

from lib.serverProcessing import *

app = Flask(__name__)
app.debug = False
state = {}

# set up logging to file - see previous section for more details
logging.basicConfig(filename='server.log',level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')

CHUNK_SIZE = 8

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

@app.route('/work', methods=['GET', 'POST'])
def work():
    global state
    logger = logging.getLogger('/work')
    payload = {'success': True, 'message': ''}
    if request.method == 'POST':  # client posts work to server
        payload['message'] = 'Recieved content!'
        content = request.get_json(force=True)
        apikey = content['apikey']
        rate = content['rate']
        data = content['data']
        processData(data)
        logger.info('Recieved content from ' + apikey)
        state['finished'] += content['work']
        state['doing'] = list(set(state['doing']) - set(content['work']))
        state['todo'] = list(set(state['todo']) - set(content['work']))
        state['connected'][apikey]['lastSeen'] = time.time()
        state['connected'][apikey]['lastDoing'] = "POSTed work."
        state['connected'][apikey]['rate'].append(rate)
        if len(state['connected'][apikey]['rate']) > 10:
            state['connected'][apikey]['rate'].pop(0)
    else:  # client gets work from server
        apikey = request.args.get('apikey', '')
        if apikey in state['connected'] and state['connected'][apikey]['lastDoing'] == "GETed work.":
            payload['message'] = "Please POST work before GETing more."
            payload['success'] = False
        else:
            possible = list(set(state['todo']) - set(state['finished']) - set(state['doing']))
            if len(possible) == 0:
                logger.info('No more work.')
                payload['message'] = 'No more work.'
                payload['success'] = False
            else:
                logger.info('Recieved work requests, ' +
                            str(len(possible)) + ' more.')
                payload['message'] = 'New work.'
                payload['apikey'] = apikey
                if apikey not in state['connected']:
                    state['connected'][apikey] = {}
                    state['connected'][apikey]['rate'] = []
                state['connected'][apikey]['lastSeen'] = time.time()
                state['connected'][apikey]['lastDoing'] = "GETed work."
                for chunk in chunks(possible, CHUNK_SIZE):
                    state['connected'][apikey]['work'] = list(chunk)
                    break
                state['doing'] += state['connected'][apikey]['work']
                payload['work'] = state['connected'][apikey]['work']
                logger.info(payload)

    with open('state.json', 'w') as f:
        f.write(json.dumps(state))
    return jsonify(**payload)

def init():
    global state
    try:
        state = json.load(open('state.json', 'r'))
    except:
        state = {}
        state['finished'] = []
    state['todo'] = list(range(1,100))
    state['doing'] = []
    state['connected'] = {}

init()

if __name__ == '__main__':
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8119)
    IOLoop.instance().start()
