import main
import utils.DatabaseConnection as connect

from bson import json_util
import json

def getCacheData(func):
    try:
        jsonCache = json.load(open('cache.json', 'r'))
        cache = json.loads(jsonCache, object_hook = json_util.object_hook)
    except (IOError, ValueError):
        cache = {}

    def wrapper(*args):
        id = args[0]
        if id in cache.keys():
            return cache.get(id)
        else:
            result = func(*args)
            cache.update({id: result})
            jsonCache = json.dumps(cache, default = json_util.default) 
            json.dump(jsonCache, open('cache.json', 'w'))
            return result
    return wrapper


@getCacheData
def getData(id, query):
    connection = main.getConnection()
    data = connect.getDataFromDatabase(connection, query)
    return data