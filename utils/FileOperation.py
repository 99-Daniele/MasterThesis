# this file handles operations on text and json files.

from io import StringIO
import numpy as np
import os
import pandas as pd
import shutil
import ujson

# create folder.
def createFolder(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)

# remove folder.
def removeFolder(directory):
    if os.path.isdir(directory):
        shutil.rmtree(directory)

# get data from text file.
# in case file not existing, return empty list.
def getDataFromTextFile(filename):
    try:
        file = open(filename, 'r')
        data = (file.read()).split(",")
        return data
    except (FileNotFoundError):
        return []

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
        df = pd.read_json(StringIO(data), orient = 'split') 
        columns = df.columns
        for c in columns:
            if np.issubdtype(df[c].dtype, np.datetime64):
                df[c] = df[c].dt.strftime("%Y-%m-%d %H:%M:%S")
        return df
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

# write on json file.
# in case file not existing, raise an exception.
def writeOnJsonFile(filename, data):
    try:
        ujson.dump(data, open(filename, 'w'))
    except (FileNotFoundError):
        raise Exception("\n" + filename + " does not exists!")
