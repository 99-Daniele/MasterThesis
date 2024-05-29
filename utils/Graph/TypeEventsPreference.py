# this file handles updating type events preferences.

import dash as ds
import pandas as pd

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

def updateFile(data, df, dropColumnTag, filename):
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        dbData = df.to_dict('records')
        pairs = zip(data, dbData)
        if any(x != y for x, y in pairs):
            newDataDf = pd.DataFrame(data)
            newDataDf = newDataDf.drop(dropColumnTag, axis = 1)
            strData = utilities.fromListToString(list(newDataDf.itertuples(index = False, name = None)))
            file.writeOnTextFile(filename, strData)
            return data, True
    return data, False

def updateDatabase(data, df, dropColumnTag, filename):
    data = [{k: v for k, v in d.items() if k not in dropColumnTag} for d in data]
    strData = utilities.fromListToString(data)
    file.writeOnTextFile(filename, strData)
    print(data)
    exit()
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        dbData = df.to_dict('records')
        pairs = zip(data, dbData)
        if any(x != y for x, y in pairs):
            newDataDf = pd.DataFrame(data)
            newDataDf = newDataDf.drop(dropColumnTag, axis = 1)
            strData = utilities.fromListToString(list(newDataDf.itertuples(index = False, name = None)))
            file.writeOnTextFile(filename, strData)
            update.refreshData()
            return data, True
    return data, False
    