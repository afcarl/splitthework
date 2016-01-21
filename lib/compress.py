import uuid
import json
import lzma
import base64
import sys

def compress(dictionary):
    return base64.b64encode(lzma.compress(str.encode(json.dumps(dictionary)))).decode('utf-8')

def decompress(dictionary):
    return json.loads(lzma.decompress(base64.b64decode(dictionary)).decode('utf-8'))

def processData(dataCompressed):
    data = decompress(dataCompressed)
    print("Processing data")
    for d in data:
        print(d, data[d])

def processWork(data):
    results = {}
    for d in data:
        results[d] = str(open('test.html','r').read())
    print(sys.getsizeof(json.dumps(results)))
    dataCompressed = compress(results)
    print(sys.getsizeof(dataCompressed))
    return dataCompressed
