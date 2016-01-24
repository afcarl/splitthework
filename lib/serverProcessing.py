import os
from multiprocessing import Pool

from lib.compress import *

def saveData(x):
    d = x[0]
    datad = x[1]
    folder = 'data/' + str(int(int(d) / 1000))
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(folder + '/' + str(d) + '.html.lzma'):
        with open(folder + '/' + str(d) + '.html','w') as f:
            f.write(datad)
        os.system('lzma ' + folder + '/' + str(d) + '.html')
    return True

def processData(dataCompressed):
    data = decompress(dataCompressed)
    datas = []
    for d in data:
        datas.append((d,data[d]))
    p = Pool(8)
    p.map(saveData,datas)
    p.terminate()
