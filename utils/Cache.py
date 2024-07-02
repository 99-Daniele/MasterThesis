# this file handles getting and updating cache.

import utils.FileOperation as file

# convert input data into json data and then write on file.
def updateCache(filename, data):
    filename = "cache/" + filename
    jsonData = data.to_json(orient = 'split')
    file.writeOnJsonFile(filename, jsonData)
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
