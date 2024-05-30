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

def updateDatabase(data, df, dropColumnTag, filename):
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        dbData = df.to_dict('records')
        pairs = zip(data, dbData)
        if any(x != y for x, y in pairs):
            newData = {}
            keys = list(data[0].keys())
            key = keys[0]
            others = list(set(keys) - set(dropColumnTag))
            others.remove(key)
            for d in data:
                element = {}
                id = d[key]
                for o in others:
                    value = str(d[o])
                    element.update({o: value})
                newData.update({id: element})
            file.writeOnJsonFile(filename, newData)
            update.refreshData()
            return data, True
    return data, False
    