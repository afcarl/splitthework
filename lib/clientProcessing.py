from lib.compress import *
from lib.downloadPages import *

def processWork(data):
    results = downloadPages(data)
    print(sys.getsizeof(json.dumps(results)))
    dataCompressed = compress(results)
    print(sys.getsizeof(dataCompressed))
    return dataCompressed
