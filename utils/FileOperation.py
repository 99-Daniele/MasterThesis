from io import StringIO
import pandas as pd
import ujson
 
def removeFile(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def getDataFromTextFile(filename):
    file = open(filename, 'r')
    data = []
    for line in file.read().splitlines():
        if line[-1] == ',':
            line = line[0:-1]
        d = eval(line)
        data.append(d)
    return data

def getDataFromJsonFile(filename):
    try:
        return ujson.load(open(filename, 'r'))
    except (IOError, ValueError):
        return {}
    
def getDataframeFromJsonFile(filename):
    try:
        jsonCache = ujson.load(open(filename, 'r'))
        jsonData = ujson.dumps(jsonCache)
        data = ujson.loads(jsonData)
        return pd.read_json(StringIO(data), orient = 'split') 
    except (FileNotFoundError):
        return None

def writeOnTextFile(filename, data):
    f = open(filename, 'w')
    f.write(data)

def appendOnTextFile(filename, data):
    f = open(filename, 'a')
    f.write(data)

def writeOnJsonFile(filename, data):
    ujson.dump(data, open(filename, 'w'))

def dataTranslate(date):
    return date.strftime("%Y-%m-%d %H:%M:%S") 

def writeDataframeOnJsonFile(filename, data):
    jsonData = data.to_json()
    ujson.dump(jsonData, open(filename, 'w'))
   