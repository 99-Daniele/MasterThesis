from bson import json_util
import json
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
    return json.load(open(filename, 'r'))

def getDataFromJsonFileWithTranslation(filename):
    try:
        jsonCache = json.load(open(filename, 'r'))
        return json.loads(jsonCache, object_hook = json_util.object_hook)
    except (IOError, ValueError):
        return {}

def writeOnTextFile(filename, data):
    f = open(filename, 'w')
    f.write(data)

def appendOnTextFile(filename, data):
    f = open(filename, 'a')
    f.write(data)

def writeOnJsonFile(filename, data):
    json.dump(data, open(filename, 'w'))
        
def writeOnJsonFileWithTranslation(filename, data):
    jsonData = json.dumps(data, default = json_util.default)
    json.dump(jsonData, open(filename, 'w'))
   