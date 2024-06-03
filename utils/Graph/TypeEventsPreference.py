# this file handles updating type events preferences.

import dash as ds
import pandas as pd

import Cache as cache
import utils.Dataframe as frame
import utils.DataUpdate as update
import utils.FileOperation as file
import utils.utilities.Utilities as utilities

def updateTextFile(data, oldSelectedRows, newSelectedRows, tag, filename):
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        if len(oldSelectedRows) != len(newSelectedRows) or len(list(set(oldSelectedRows) & set(newSelectedRows)) != len(oldSelectedRows)):
            df = frame.getRowsFromIndex(pd.DataFrame(data), newSelectedRows)
            strData = utilities.fromListToString(list(df[tag]))
            file.writeOnTextFile(filename, strData)
            return data, True
    return data, False

def updateDatabase(data, dfDatabase, tag, filename):
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        countTag = utilities.getTagName("countTag")
        durationTag = utilities.getTagName("durationTag")
        df_temp = dfDatabase[dfDatabase[countTag] > 0]
        dfData = pd.DataFrame(data)
        diff = pd.concat([df_temp, dfData]).drop_duplicates(keep = False)
        if len(diff) > 0:
            newDf = dfDatabase[~dfDatabase[tag].isin(dfData[tag])]
            newDf = pd.concat([newDf, dfData])
            newDf = newDf.drop([countTag, durationTag], axis = 1).reset_index(drop = True)
            cache.updateCache(filename, newDf)
            update.refreshData()
            return data, True
    return data, False
    