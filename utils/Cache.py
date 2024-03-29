import utils.DatabaseConnection as connect
import utils.FileOperation as file
import utils.Getters as getter

def getCacheData(func):
    cache = file.getDataFromJsonFileWithTranslation('utils/cache.json')

    def wrapper(*args):
        id = args[0]
        if id in cache.keys():
            return cache.get(id)
        else:
            result = func(*args)
            cache.update({id: result})
            file.writeOnJsonFileWithTranslation('utils/cache.json', cache)
            return result
    return wrapper

@getCacheData
def getData(id, query):
    connection = connect.getDatabaseConnection()
    data = connect.getDataFromDatabase(connection, query)
    return data
