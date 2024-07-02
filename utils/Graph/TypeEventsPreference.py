# this file handles updating type events preferences.

import pandas as pd

import utils.Cache as cache
import utils.DataUpdate as update
import utils.FileOperation as file
import utils.Utilities as utilities

# update cache data if user has modified some parameters.
#
# input data are: data are the new data, olddata are the old data, 
# tag refers to which tag is the key of data, filename is the file where update cache.
#
# return data are: data as the new data, True if data is modified or False if not.
def updateData(data, oldData, tag, filename):
    countTag = utilities.getTagName("countTag")
    durationTag = utilities.getTagName("durationTag")
    df_old = oldData[oldData[countTag] > 0]
    dfData = pd.DataFrame(data)
    # diff concatenate oldData and newData removing duplicates. If diff is empty there is no difference,
    # otherwise there exists a difference and in that case update cache return True.
    diff = pd.concat([df_old, dfData]).drop_duplicates(keep = False)
    if len(diff) > 0:
        newDf = oldData[~oldData[tag].isin(dfData[tag])]
        newDf = pd.concat([newDf, dfData])
        newDf = newDf.drop([countTag, durationTag], axis = 1).reset_index(drop = True)
        cache.updateCacheDataframe(filename, newDf)
        update.refreshData()
        return data, True
    return data, False

# update important type files if user has made some changes.
#
# input data are: trigger to understand if user has selected something or not,
# data are the data, tag refers to which tag is the key of data, 
# newImportantIndex is the index of new important types, filename is the file where update cache.
#
# return data is newImportantIndex
def updateImportant(trigger, data, tag, newImportantIndex, filename):
    # oldImportant are the old important types taken from filename.
    # oldImporantIndex is the index of oldImporant based on data.
    oldImportant = file.getDataFromTextFile(filename)
    if oldImportant == None or oldImportant == ['']:
        oldImportantIndex = []
    else:
        oldImportantIndex = []
        for i in range(len(data)):
            d = data[i]
            if d.get(tag) in oldImportant:
                oldImportantIndex.extend([i])
    # if trigger is None newImportantIndex is equal to oldImportantIndex.                
    if trigger == None:
        newImportantIndex = oldImportantIndex
    # if omsething was trigered important is the list of important types based on newImportantIndex and data.
    else:
        if newImportantIndex == None or len(newImportantIndex) == 0:
            important = []
        else:
            important = [data[x].get(tag) for x in newImportantIndex]
        # if there is a difference between important and oldImporant filename is modified with new important types.
        if len(list(set(important) - set(oldImportant))) > 0 or len(list(set(oldImportant) - set(important))) > 0:
            file.writeOnTextFile(filename, utilities.fromListToString(important))
    return newImportantIndex
