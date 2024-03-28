from bson import json_util
import json
import os
 
def removeFile(filename):
    try:
        os.remove(filename)
    except:
        pass

def getDataFromJsonFile(filename):
    return json.load(open(filename, 'r'))

def getDataFromJsonFileWithTranslation(filename):
    try:
        jsonCache = json.load(open(filename, 'r'))
        return json.loads(jsonCache, object_hook = json_util.object_hook)
    except (IOError, ValueError):
        return {}
        
def writeOnJsonFile(filename, data):
    jsonData = json.dumps(data, default = json_util.default)
    json.dump(jsonData, open(filename, 'w'))
   