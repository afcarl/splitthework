from lib.compress import *

def processData(dataCompressed):
    data = decompress(dataCompressed)
    print("Processing data")
    for d in data:
        print(d, data[d])
