import os

from lib.compress import *

def processWork(data):
    strData = []
    for a in data:
        strData.append(str(a))
    os.system("sudo python3 downloadPages.py " + " ".join(strData))
    results = json.load(open('downloadedPages.json','r'))
    # print(sys.getsizeof(json.dumps(results)))
    dataCompressed = compress(results)
    # print(sys.getsizeof(dataCompressed))
    return dataCompressed
