import os

from lib.compress import *


def processData(dataCompressed):
    data = decompress(dataCompressed)
    for d in data:
        with open('data/' + str(d) + '.html','w') as f:
            f.write(data[d])
        os.system('lzma data/' + str(d) + '.html')
