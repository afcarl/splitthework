import os

from lib.compress import *


def processData(dataCompressed):
    data = decompress(dataCompressed)
    for d in data:
        folder = 'data/' + str(int(int(d) / 1000))
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(folder + '/' + str(d) + '.html','w') as f:
            f.write(data[d])
        os.system('lzma ' + folder + '/' + str(d) + '.html')
