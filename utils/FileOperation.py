from bson import json_util
import json
import os
 
def removeFile(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def getDataFromJsonFile(filename):
    return json.load(open(filename, 'r'))

def getDataFromJsonFileWithTranslation(filename):
    try:
        jsonCache = json.load(open(filename, 'r'))
        return json.loads(jsonCache, object_hook = json_util.object_hook)
    except (IOError, ValueError):
        return {}
        
def writeOnJsonFile(filename, data):
    json.dump(data, open(filename, 'w'))
        
def writeOnJsonFileWithTranslation(filename, data):
    jsonData = json.dumps(data, default = json_util.default)
    json.dump(jsonData, open(filename, 'w'))
   