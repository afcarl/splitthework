import uuid
import json
import lzma
import base64
import sys

def compress(dictionary):
    return base64.b64encode(lzma.compress(str.encode(json.dumps(dictionary)))).decode('utf-8')

def decompress(dictionary):
    return json.loads(lzma.decompress(base64.b64decode(dictionary)).decode('utf-8'))
