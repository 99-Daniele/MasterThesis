# this file handles operations on text and json files.

from io import StringIO
import os
import pandas as pd
import ujson

# remove file.
def removeFile(filename):
    if os.path.isfile(filename):
        os.remove(filename)

# get data from text file.
# in case file not existing, raise an exception.
def getDataFromTextFile(filename):
    try:
        file = open(filename, 'r')
        data = []
        for line in file.read().splitlines():
            if line[-1] == ',':
                line = line[0:-1]
            d = eval(line)
            data.append(d)
        return data
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")

# get dataframe from text file.
# in case file not existing, return None.
def getDataframeFromTextFile(filename, tags):
    try:
        data = getDataFromTextFile(filename)
        data = list(data[0])
        dataframe = pd.DataFrame(data, columns = tags)
        return dataframe, True
    except:
        return None, False

# get data from json file.
# in case file not existing, return empty dictionary.
def getDataFromJsonFile(filename):
    try:
        return ujson.load(open(filename, 'r'))
    except (FileNotFoundError):
        return {}
    
# get dataframe from json file.
# in case file not existing, return None.
def getDataframeFromJsonFile(filename):
    try:
        jsonCache = ujson.load(open(filename, 'r'))
        jsonData = ujson.dumps(jsonCache)
        data = ujson.loads(jsonData)
        return pd.read_json(StringIO(data), orient = 'split') 
    except (FileNotFoundError):
        return None

# write on text file.
# in case file not existing, raise an exception.
def writeOnTextFile(filename, data):
    try:
        f = open(filename, 'w')
        f.write(data)
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")

# append on text file.
# in case file not existing, raise an exception.
def appendOnTextFile(filename, data):
    try:
        f = open(filename, 'a')
        f.write(data)
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")

# write on json file.
# in case file not existing, raise an exception.
def writeOnJsonFile(filename, data):
    try:
        ujson.dump(data, open(filename, 'w'))
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")

# write dataframe on json file.
# in case file not existing, raise an exception.
def writeDataframeOnJsonFile(filename, data):
    try:
        jsonData = data.to_json()
        ujson.dump(jsonData, open(filename, 'w'))
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")
