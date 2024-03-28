import utils.DatabaseConnection as connect
import utils.FileOperation as file
import utils.Utilities as utilities

def getCacheData(func):
    cache = file.getDataFromJsonFileWithTranslation('cache.json')

    def wrapper(*args):
        id = args[0]
        if id in cache.keys():
            return cache.get(id)
        else:
            result = func(*args)
            cache.update({id: result})
            file.writeOnJsonFile('cache.json', cache)
            return result
    return wrapper

@getCacheData
def getData(id, query):
    databaseInfo = utilities.dataBaseInfo
    connection = connect.connectToDatabase(databaseInfo[0], databaseInfo[1], databaseInfo[2], databaseInfo[3])
    data = connect.getDataFromDatabase(connection, query)
    return data