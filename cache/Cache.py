# this file handles getting and updating cache.

import pandas as pd

import utils.FileOperation as file

# convert input data into json data and then write on file.
def cacheUpdate(filename, data):
    filename = "cache/" + filename
    jsonData = data.to_json(orient = 'split')
    file.writeOnJsonFile(filename, jsonData)

# compare current cache data with data in the database and if there are differences update cache.
def updateCache(filename, databaseData):
    cacheUpdate(filename, databaseData)
    print(filename[:-5] + " updated!")

# return cached data from chosen file.
def getData(filename):
    filename = "cache/" + filename
    data = file.getDataFromJsonFile(filename)
    return data

# return cached dataframe from chosen file.
def getDataframe(filename):
    filename = "cache/" + filename
    data = file.getDataframeFromJsonFile(filename)
    return data
