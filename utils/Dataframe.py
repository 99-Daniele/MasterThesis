# this file handles dataframe managements.

import datetime as dt
import pandas as pd
import textwrap

import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# importantProcessStates and importantSections are taken from text file. This are type of events that are the most important. Thay can be changed or removed.
try:
    importantProcessStates = list(file.getDataFromTextFile('preferences/importantProcessStates.txt'))
except:
    importantProcessStates = None
try:
    importantSections = list(file.getDataFromTextFile('preferences/importantSections.txt'))
except:
    importantSections = None

# from events list create events dataframe.
def createEventsDataFrame(events, numEventTag, numProcessTag, eventCodeTag, eventTag, judgeCodeTag, judgeTag, dateTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag, endPhase):
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, eventCodeTag, eventTag, judgeCodeTag, judgeTag, dateTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag])
    dfNotEnd = df[df[phaseTag] != endPhase].reset_index(drop = True)
    dfEnd = df[df[phaseTag] == endPhase].reset_index(drop = True)
    dfEnd = dfEnd.groupby(numProcessTag, as_index = False).first().reset_index(drop = True)
    df = pd.concat([dfNotEnd, dfEnd])
    df = df.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return df

# from processes list create processes duration dataframe.
def createProcessesDurationDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    pIds = []
    sequences = []
    phases = []
    events = []
    for p in processes:
        if (importantSections == None or p[4] in importantSections) and (importantProcessStates == None or utilities.getProcessState(p[5]) in importantProcessStates):
            dates.append(p[0])
            durations.append(p[1])
            judges.append(p[2])
            subjects.append(p[3])
            sections.append(p[4])
            finished.append(utilities.getProcessState(p[5]))
            pIds.append(p[6])
            sequences.append(p[7])
            phases.append(p[8])
            events.append(p[9])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "sequenza": sequences, "fasi": phases, "eventi": events})

# from process list create process duration dataframe.
def createProcessDurationsDataFrame(process, numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag):
    df = pd.DataFrame(process, columns = [numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag])
    if importantProcessStates != None:
        df = df[df[finishedTag].isin(importantProcessStates)]
    if importantSections != None:
        df = df[df[sectionTag].isin(importantSections)]
    df = df.sort_values(by = [dateTag, numProcessTag]).reset_index(drop = True)
    return df

# from events list create type duration dataframe.
def createTypeDurationsDataFrame(events, numEventTag, numProcessTag, eventCodeTag, eventTag, durationTag, dateTag, judgeCodeTag, judgeTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag):
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, eventCodeTag, eventTag, durationTag, dateTag, judgeCodeTag, judgeTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag])
    filteredDf = df.copy()
    if importantProcessStates != None:
        filteredDf = filteredDf[filteredDf[finishedTag].isin(importantProcessStates)]
    if importantSections != None:
        filteredDf = filteredDf[filteredDf[sectionTag].isin(importantSections)]
    filteredDf = filteredDf.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return [df, filteredDf]

def createStateNameDataframe(stateNames, stateCodeTag, descrTag, tagTag, dbPhaseTag, phaseTag):
    df = pd.DataFrame(stateNames, columns = [stateCodeTag, descrTag, tagTag, dbPhaseTag, phaseTag])
    df[stateCodeTag] = df[stateCodeTag].astype(str)
    return df

def createStateNameDataframeWithInfo(statesDuration, stateNames, stateTag,  durationTag, countTag):
    statesDuration = statesDuration.groupby([stateTag]) \
        .agg({statesDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {statesDuration.columns[2]:countTag}) \
        .reset_index()
    statesDuration[durationTag] = statesDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    stateNames[stateTag] = stateNames[stateTag].astype(str)
    result = stateNames.join(statesDuration.set_index(stateTag), on = stateTag)
    result = result.fillna(0)
    result = result.sort_values([stateTag])
    return result

# return avg and tot dataframe.
def getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag):
    df1 = df1.sort_values([dateTag])
    df_q = df1.groupby([dateTag], as_index = False).quantile(0.75)
    df3 = df1.iloc[:0,:].copy()
    for i, row in df_q.iterrows():
        df_temp = df1[df1[dateTag] == row[dateTag]]
        df_temp = df_temp[df_temp[durationTag] <= row[durationTag]]
        df3 = pd.concat([df3, df_temp], ignore_index = True)
    if avgChoice == 'media':
        df2 = df3.groupby([dateTag], as_index = False).mean()
    else:
        df2 = df3.groupby([dateTag], as_index = False).median()
    df2[countTag] = df3.groupby([dateTag]).size().tolist()
    df2[quantileTag] = df3.groupby([dateTag], as_index = False).quantile(0.75)[durationTag]
    return [df3, df2]

# return data group by chosen data type.
def getAvgStdDataFrameByDate(df, dataType, avgChoice, dateTag, durationTag, countTag, quantileTag):
    df1 = df[[dateTag, durationTag]].copy()
    match dataType:
        case "SETTIMANA":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeekNumber(x))
            [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeek(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getWeek(x))
            return [df1, df2]
        case "MESE":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthNumber(x))
            [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonth(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonth(x))
            return [df1, df2]
        case "MESE DELL'ANNO":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYearDate(x))
            [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYear(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonthYear(x))
            return [df1, df2]
        case "TRIMESTRE":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterDate(x))
            [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimester(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimester(x))
            return [df1, df2]
        case "TRIMESTRE DELL'ANNO":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYearDate(x))
            [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYear(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimesterYear(x))
            return [df1, df2]
        case "ANNO":
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getYearNumber(x))
            return getAvgTotDataframeByDate(df1, avgChoice, dateTag, durationTag, countTag, quantileTag)

# return avg and tot dataframe.
def getAvgTotDataframe(df, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag):
    if avgChoice == 'mean':
        df1 = df.groupby([dateTag, filterTag], as_index = False).mean()
    else:
        df1 = df.groupby([dateTag, filterTag], as_index = False).median()
    df1[countTag] = df.groupby([dateTag, filterTag]).size().tolist()
    df1['sort_column'] = df1[filterTag].map(order_dict)
    df1 = df1.sort_values(['sort_column', dateTag], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
    df2 = df1.groupby([dateTag]) \
        .agg({countTag: 'sum', durationTag:avgChoice}) \
        .reset_index()
    df2 = df2.sort_values([dateTag]).reset_index(drop = True)
    return [df1, df2]

# return data group by chosen data type and types.
def getAvgDataFrameByType(df, avgChoice, datetype, typesChoice, order, eventChoice, dateTag, durationTag, eventsTag, eventTag, countTag, avgTag, filterTag):
    if typesChoice == None or len(typesChoice) == 0:
        return None
    if avgChoice == 'media':
        avgChoice = 'mean'
    else:
        avgChoice = 'median'
    df5 = df.copy()
    types = typesChoice.copy()
    if eventChoice != None and eventChoice in types:
        df5 = getEventDataFrame(df5, eventChoice, eventTag, eventsTag)
        index = types.index(eventChoice)
        types[index] = eventTag
    df4 = df5.groupby(types) \
        .agg({df5.columns[2]:'size', durationTag: avgChoice}) \
        .rename(columns = {df5.columns[2]:countTag, durationTag:avgTag}) \
        .reset_index()
    for t in types: 
        df4.drop(df4[df4[t] == 'null'].index, inplace = True)
    df3 = df4[[types[0], countTag, avgTag]].copy()
    df3 = df3.rename(columns = {types[0]: filterTag})
    i = 1
    while i < len(types):
        df3[filterTag] = df3[filterTag].astype(str) + " - " + df4[types[i]].astype(str)
        i = i + 1
    df3 = keepOnlyImportant(df3, 0.25, countTag)
    df3 = df3.sort_values([order], ascending = False).reset_index(drop = True)
    order_dict = df3.set_index(filterTag)[order].to_dict()
    order_list = df3[filterTag].tolist()
    df_temp = df5[[dateTag, durationTag, types[0]]].copy()
    df_temp = df_temp.rename(columns = {types[0]:filterTag})
    i = 1
    while i < len(types):
        df_temp[filterTag] = df_temp[filterTag].astype(str) + " - " + df5[types[i]].astype(str)
        i = i + 1
    df_temp = df_temp[df_temp[filterTag].isin(order_list)]
    match datetype:
        case "SETTIMANA":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getWeekNumber(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeek(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getWeek(x))
            return [df1, df2, df3]
        case "MESE":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getMonthNumber(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonth(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonth(x))
            return [df1, df2, df3]
        case "MESE DELL'ANNO":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getMonthYearDate(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYear(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonthYear(x))
            return [df1, df2, df3]
        case "TRIMESTRE":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getTrimesterDate(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimester(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimester(x))
            return [df1, df2, df3]
        case "TRIMESTRE DELL'ANNO":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getTrimesterYearDate(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYear(x))
            df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimesterYear(x))
            return [df1, df2, df3]
        case "ANNO":
            df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getYearNumber(x))
            [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice, dateTag, durationTag, countTag, filterTag)
            return [df1, df2, df3]
        
# return data group by chosen type.
def getAvgStdDataFrameByType(df, type, avgChoice, durationTag, countTag, quantileTag):
    typeDuration = type.copy()
    typeDuration.append(durationTag)
    df1 = df[typeDuration].copy()
    if avgChoice == 'media':
        df2 = df1.groupby(type, as_index = False).mean()
    else:
        df2 = df1.groupby(type, as_index = False).median()
    df2[countTag] = df1.groupby(type).size().tolist()
    df2[quantileTag] = df1.groupby(type, as_index = False).quantile(0.75)[durationTag]
    df1 = df1.sort_values(type).reset_index(drop = True)
    df2 = df2.sort_values(type).reset_index(drop = True)
    return [df1, df2]

# return data group by chosen type.
def getAvgStdDataFrameByTypeChoice(df, type, durationTag, countTag, quantileTag):
    typeDuration = type.copy()
    typeDuration.append(durationTag)
    df1 = df[typeDuration].copy()
    df1[durationTag] = df1[durationTag].astype(int)
    df1 = keepOnlyRelevant(df1, 0.05, type[0], countTag)
    df2 = df1.groupby(type, as_index = False).mean()
    df2[countTag] = df1.groupby(type).size().tolist()
    df2[quantileTag] = df1.groupby(type, as_index = False).quantile(0.75)[durationTag]
    df1 = df1.sort_values(type).reset_index(drop = True)
    df2 = df2.sort_values(type).reset_index(drop = True)
    return [df1, df2]

# return dataframe with rows which type is present a relevant number of times.
def keepOnlyRelevant(df, perc, tag, countTag):
    df_temp = df.copy()
    df_temp = df_temp.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = countTag)
    totCount = df_temp[countTag].sum()
    threshold = totCount * perc
    relevant = df_temp[df_temp[countTag] >= threshold][tag].tolist()
    return df[df[tag].isin(relevant)]

# reduce dataframe to a number of rows such that they cover at least given percentage.
def keepOnlyImportant(df, perc, countTag):
    df_temp = df.copy()
    totCount = df_temp[countTag].sum()
    threshold = totCount * perc
    df_temp = df_temp.sort_values([countTag], ascending = False)
    i = 0
    sum = 0
    if df_temp[countTag].items() == None:
        return df
    while (i < 15 or sum < threshold) and i < len(list(df_temp[countTag].items())):
        sum = sum + list(df_temp[countTag].items())[i][1]
        i = i + 1
    while i < len(list(df_temp[countTag].items())):
        index = list(df_temp[countTag].items())[i][0]
        df = df.drop(index)
        i = i + 1
    df.reset_index(drop = True)
    return df

# return dataframe rows where given tag is contained in given types.
def getTypesDataFrame(df, tag, types):
    if types == None or len(types) == 0:
        return df
    df_temp = df.copy()
    return df_temp[df_temp[tag].isin(types)]

# return dataframe rows where given tag is contained in given types from string.
def getTypesDataFrameFromString(df, tag, type):
    if type == None:
        return df
    df_temp = df.copy()
    return df_temp[df_temp[tag].str.contains(type)]

# return dataframe rows where date month is contained given months.
def getMonthDataFrame(df, months, dateTag):
    if months == None or len(months) == 0:
        return df
    df_temp = df.copy()
    df_temp[dateTag] = df_temp[dateTag].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
    return df_temp[df_temp[dateTag].isin(months)]

# return dataframe rows where date year is contained given years.
def getYearDataFrame(df, years, dateTag):
    if years == None or len(years) == 0:
        return df
    df_temp = df.copy()
    df_temp[dateTag] = df_temp[dateTag].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
    return df_temp[df_temp[dateTag].isin(years)]

# return dataframe rows where date is between given stratDate and endDate.
def getDateDataFrame(df, type, startDate, endDate):
    if startDate == None or endDate == None:
        return df
    df_temp = df.copy()
    d = df_temp[df_temp[type] >= startDate]
    d = d[d[type] <= endDate]
    return d

#return dataframe wos where event sequence contains or not a particular event
def getEventDataFrame(df, event, eventTag, eventsTag):
    if event == None:
        return df
    df_temp = df.copy()
    df_temp[eventTag] = df_temp[eventsTag]
    for i, row in df_temp.iterrows():
        if event in utilities.fromStringToList(row[eventsTag]):
            df_temp.at[i, eventTag] = "CON " + event
        else:
            df_temp.at[i, eventTag] = "SENZA " + event
    return df_temp

# return unique years in given dataframe dates.
def getAllYears(df, dateTag):
    df_temp = df[dateTag].copy()
    df_temp = df_temp.map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year).sort_values()
    years = df_temp.unique()
    return years

# return group by types with corrispondent counts.
def getGroupBy(df, tag, countTag):
    df_temp = df.copy()
    types = df_temp.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = countTag)[tag].tolist()
    return types

# return group by types with corrispondent counts from string.
def getGroupByFromString(df, tag):
    df_temp = df.copy()
    types = {}
    for d in df_temp[tag]:
        typeList = utilities.fromStringToList(d)
        for l in typeList:
            if l in types.keys():
                count = types.get(l) + 1
            else:
                count = 1
            types.update({l: count})
    types = list(dict(sorted(types.items(), key = lambda x: x[1], reverse = True)).keys())
    return types

# return uniques values of dataframe column.
def getUniques(df, tag):
    df_temp = df[tag].copy()
    uniques = df_temp.unique()
    return uniques

# returns a string with input name followed by how many times is present in the dataframe.
def addCountToName(df, name, filterTag, countTag):
    count = df[df[filterTag].astype(str) == name][countTag].item()
    newName = name + " (" + str(count) + ")"
    newName = '<br>'.join(textwrap.wrap(newName, width = 50))
    return newName

# returns a string with total sum of counts in dataframe.
def addTotCountToName(df, countTag):
    totCount = df[countTag].sum()
    newName = "TUTTI (" + str(totCount) + ")"
    return newName
