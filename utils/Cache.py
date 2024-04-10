import utils.DatabaseConnection as connect
import utils.FileOperation as file

def updateCache(id, cache, query):
    cacheData = getData(id, query)
    cacheData = [tuple(x) for x in cacheData]
    connection = connect.getDatabaseConnection()
    databaseData = connect.getDataFromDatabase(connection, query)
    if set(cacheData) != set(databaseData):
        cache.update({id: databaseData})
        file.writeOnJsonFileWithTranslation('utils/cache.json', cache)

def getData(id, query):
    cache = file.getDataFromJsonFileWithTranslation('utils/cache.json')
    if id in cache.keys():
        return cache.get(id)
    else:
        connection = connect.getDatabaseConnection()
        data = connect.getDataFromDatabase(connection, query)
        updateCache(id, data, cache)
        return data