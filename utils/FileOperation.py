import ujson
import os
 
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
    
def getDataFromJsonFileWithTranslation(filename):
    try:
        jsonCache = ujson.load(open(filename, 'r'))
        return ujson.loads(jsonCache)
    except (IOError, ValueError):
        return {}

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

def writeOnJsonFileWithTranslation(filename, data):
    jsonData = ujson.dumps(data, default = dataTranslate)
    ujson.dump(jsonData, open(filename, 'w'))
   