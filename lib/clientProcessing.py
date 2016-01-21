improt time
from lib.compress import *

def processWork(data):
    time.sleep(random.randint(1,4))
    results = {}
    for d in data:
        results[d] = str(open('test.html','r').read())
    print(sys.getsizeof(json.dumps(results)))
    dataCompressed = compress(results)
    print(sys.getsizeof(dataCompressed))
    return dataCompressed
