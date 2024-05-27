# this file handles dataframe managements.

import datetime as dt
import pandas as pd
import textwrap

import utils.FileOperation as file
import utils.utilities.Utilities as utilities

# importantProcessStates, importantSections and importantSubjects are taken from text file. This are type of events that are the most important. Thay can be changed or removed.
try:
    importantProcessStates = list(file.getDataFromTextFile('preferences/importantProcessStates.txt'))
except:
    importantProcessStates = None
try:
    importantSections = list(file.getDataFromTextFile('preferences/importantSections.txt'))
except:
    importantSections = None
try:
    importantSubjects = list(file.getDataFromTextFile('preferences/importantSubjects.txt'))
except:
    importantSubjects = None

# from events list create events dataframe.
def createEventsDataFrame(events, endPhase):
    dateTag = utilities.getTagName('dateTag')
    eventTag = utilities.getTagName('eventTag')
    eventCodeTag = utilities.getTagName('codeEventTag')
    judgeTag = utilities.getTagName('judgeTag')
    judgeCodeTag = utilities.getTagName('codeJudgeTag')
    numEventTag = utilities.getTagName('numEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseTag = utilities.getTagName('phaseTag')
    processDateTag = utilities.getTagName('processDateTag')
    sectionTag = utilities.getTagName('sectionTag')
    stateTag = utilities.getTagName('stateTag')
    stateCodeTag = utilities.getTagName('codeStateTag')
    subjectTag = utilities.getTagName('subjectTag')
    subjectCodeTag = utilities.getTagName('codeSubjectTag')
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, eventCodeTag, eventTag, judgeCodeTag, judgeTag, dateTag, processDateTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag])
    dfNotEnd = df[df[phaseTag] != endPhase].reset_index(drop = True)
    dfEnd = df[df[phaseTag] == endPhase].reset_index(drop = True)
    dfEnd = dfEnd.groupby(numProcessTag, as_index = False).first().reset_index(drop = True)
    df = pd.concat([dfNotEnd, dfEnd])
    df = df.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return df

# from processes list create process duration dataframe.
def createProcessDurationsDataFrame(process):
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventSequenceTag = utilities.getTagName('eventSequenceTag')
    endDateTag = utilities.getTagName('endDateTag')
    endIdTag = utilities.getTagName('endIdTag')
    finishedTag = utilities.getTagName('finishedTag')
    judgeTag = utilities.getTagName('judgeTag')
    numEventTag = utilities.getTagName('numEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    sectionTag = utilities.getTagName('sectionTag')
    stateSequenceTag = utilities.getTagName('sequenceTag')
    subjectCodeTag = utilities.getTagName('codeSubjectTag')
    df = pd.DataFrame(process, columns = [numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectCodeTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag])
    filteredDf = df.copy()
    if importantProcessStates != None:
        filteredDf = filteredDf[filteredDf[finishedTag].isin(importantProcessStates)]
    if importantSections != None:
        filteredDf = filteredDf[filteredDf[sectionTag].isin(importantSections)]
    if importantSubjects != None:
        filteredDf = filteredDf[filteredDf[subjectCodeTag].isin(importantSubjects)]
    df = df.sort_values(by = [dateTag, numProcessTag]).reset_index(drop = True)
    filteredDf = filteredDf.sort_values(by = [dateTag, numProcessTag]).reset_index(drop = True)
    return [df, filteredDf]

# from events list create type duration dataframe.
def createTypeDurationsDataFrame(events):
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    eventCodeTag = utilities.getTagName('codeEventTag')
    finishedTag = utilities.getTagName('finishedTag')
    judgeTag = utilities.getTagName('judgeTag')
    judgeCodeTag = utilities.getTagName('codeJudgeTag')
    nextDateTag = utilities.getTagName('endDateTag')
    nextIdTag = utilities.getTagName('endIdTag')
    numEventTag = utilities.getTagName('numEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseTag = utilities.getTagName('phaseTag')
    sectionTag = utilities.getTagName('sectionTag')
    stateTag = utilities.getTagName('stateTag')
    stateCodeTag = utilities.getTagName('codeStateTag')
    subjectTag = utilities.getTagName('subjectTag')
    subjectCodeTag = utilities.getTagName('codeSubjectTag')    
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, eventCodeTag, eventTag, durationTag, dateTag, judgeCodeTag, judgeTag, stateCodeTag, stateTag, phaseTag, subjectCodeTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag])
    filteredDf = df.copy()
    if importantSections != None:
        filteredDf = filteredDf[filteredDf[sectionTag].isin(importantSections)]
    if importantSubjects != None:
        filteredDf = filteredDf[filteredDf[subjectCodeTag].isin(importantSubjects)]
    return [df, filteredDf]

# from state names list create state names dataframe.
def createStateNameDataframe(stateNames):
    dbPhaseTag = utilities.getTagName('phaseDBTag')
    descrTag = utilities.getTagName('descriptionTag')
    phaseTag = utilities.getTagName('phaseTag')
    stateCodeTag = utilities.getTagName('codeStateTag')
    tagTag = utilities.getTagName('tagTag')
    df = pd.DataFrame(stateNames, columns = [stateCodeTag, descrTag, tagTag, dbPhaseTag, phaseTag])
    df[stateCodeTag] = df[stateCodeTag].astype(str)
    return df

# from state names list create state names dataframe with info.
def createStateNameDataframeWithInfo(statesDuration, stateNames):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    codeStateTag = utilities.getTagName('codeStateTag')
    statesDuration = statesDuration.groupby([codeStateTag]) \
        .agg({statesDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {statesDuration.columns[2]:countTag}) \
        .reset_index()
    statesDuration[durationTag] = statesDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    statesDuration[codeStateTag] = statesDuration[codeStateTag].astype(str)
    result = stateNames.join(statesDuration.set_index(codeStateTag), on = codeStateTag)
    result = result.fillna(0)
    result = result.sort_values([codeStateTag])
    return result

# from event names list create event names dataframe.
def createEventNameDataframe(eventNames):
    codeEventTag = utilities.getTagName('codeEventTag')
    descrTag = utilities.getTagName('descriptionTag')
    phaseTag = utilities.getTagName('phaseTag')
    tagTag = utilities.getTagName('tagTag')
    df = pd.DataFrame(eventNames, columns = [codeEventTag, descrTag, tagTag, phaseTag])
    df[codeEventTag] = df[codeEventTag].astype(str)
    return df

# from event names list create event names dataframe with info.
def createEventNameDataframeWithInfo(eventsDuration, eventNames):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    codeEventTag = utilities.getTagName('codeEventTag')
    eventsDuration = eventsDuration.groupby([codeEventTag]) \
        .agg({eventsDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {eventsDuration.columns[2]:countTag}) \
        .reset_index()
    eventsDuration[durationTag] = eventsDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    eventsDuration[codeEventTag] = eventsDuration[codeEventTag].astype(str)
    result = eventNames.join(eventsDuration.set_index(codeEventTag), on = codeEventTag)
    result = result.fillna(0)
    result = result.sort_values([codeEventTag])
    return result

# from judge names list create judge names dataframe.
def createJudgeNameDataframe(judgeNames):
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    judgeTag = utilities.getTagName('judgeTag')
    df = pd.DataFrame(judgeNames, columns = [codeJudgeTag, judgeTag])
    df[codeJudgeTag] = df[codeJudgeTag].astype(str)
    return df

# from judge names list create judges names dataframe with info.
def createJudgeNameDataframeWithInfo(processDuration, judgeNames):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    judgeTag = utilities.getTagName('judgeTag')
    processDuration = processDuration.groupby([judgeTag]) \
        .agg({processDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {processDuration.columns[2]:countTag}) \
        .reset_index()
    processDuration[durationTag] = processDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    processDuration[judgeTag] = processDuration[judgeTag].astype(str)
    result = judgeNames.join(processDuration.set_index(judgeTag), on = judgeTag)
    result = result.fillna(0)
    result = result.sort_values([judgeTag])
    return result

# from subject names list create subjects names dataframe.
def createSubjectNameDataframe(judgeNames):
    codeSubjectTag = utilities.getTagName('codeSubjectTag')
    descriptionTag = utilities.getTagName('descriptionTag')
    ritualTag = utilities.getTagName('ritualTag')
    subjectTag = utilities.getTagName('subjectTag')
    df = pd.DataFrame(judgeNames, columns = [codeSubjectTag, descriptionTag, ritualTag, subjectTag])
    df[codeSubjectTag] = df[codeSubjectTag].astype(str)
    return df

# from subject names list create subjects names dataframe with info.
def createSubjectNameDataframeWithInfo(processDuration, subjectNames):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    codeSubjectTag = utilities.getTagName('codeSubjectTag')
    processDuration = processDuration.groupby([codeSubjectTag]) \
        .agg({processDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {processDuration.columns[2]:countTag}) \
        .reset_index()
    processDuration[durationTag] = processDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    processDuration[codeSubjectTag] = processDuration[codeSubjectTag].astype(int)
    processDuration[codeSubjectTag] = processDuration[codeSubjectTag].astype(str)
    result = subjectNames.join(processDuration.set_index(codeSubjectTag), on = codeSubjectTag)
    result = result.sort_values([codeSubjectTag])
    return result

# return avg and tot dataframe.
def getAvgTotDataframeByDate(df1, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag')
    df1 = df1.sort_values([dateTag])
    df_q = df1.groupby([dateTag], as_index = False).quantile(0.75)
    df3 = df1.iloc[:0,:].copy()
    for i, row in df_q.iterrows():
        df_temp = df1[df1[dateTag] == row[dateTag]]
        df_temp = df_temp[df_temp[durationTag] <= row[durationTag]]
        df3 = pd.concat([df3, df_temp], ignore_index = True)
    if avgChoice == avgTag:
        df2 = df3.groupby([dateTag], as_index = False).mean()
    else:
        df2 = df3.groupby([dateTag], as_index = False).median()
    df2[countTag] = df3.groupby([dateTag]).size().tolist()
    df2[quantileTag] = df3.groupby([dateTag], as_index = False).quantile(0.75)[durationTag]
    return [df3, df2]

# return data group by chosen data type.
def getAvgStdDataFrameByDate(df, dataType, avgChoice):
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    month = utilities.getPlaceholderName("month")
    monthYear = utilities.getPlaceholderName("monthYear")
    trimester = utilities.getPlaceholderName("trimester")
    trimesterYear = utilities.getPlaceholderName("trimesterYear")
    week = utilities.getPlaceholderName("week")
    year = utilities.getPlaceholderName("year")
    df1 = df[[dateTag, durationTag]].copy()
    if dataType == week:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeekNumber(x))
        [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeek(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getWeek(x))
        return [df1, df2]
    elif dataType == month:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthNumber(x))
        [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonth(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonth(x))
        return [df1, df2]
    elif dataType == monthYear:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYearDate(x))
        [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonthYear(x))
        return [df1, df2]
    elif dataType == trimester:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterDate(x))
        [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimester(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimester(x))
        return [df1, df2]
    elif dataType == trimesterYear:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYearDate(x))
        [df1, df2] = getAvgTotDataframeByDate(df1, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        return [df1, df2]
    elif dataType == year:
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getYearNumber(x))
        return getAvgTotDataframeByDate(df1, avgChoice)

# return avg and tot dataframe.
def getAvgTotDataframe(df, order_dict, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    filterTag = utilities.getTagName('filterTag')
    if avgChoice == avgTag:
        df1 = df.groupby([dateTag, filterTag], as_index = False).mean()
    else:
        df1 = df.groupby([dateTag, filterTag], as_index = False).median()
    df1[countTag] = df.groupby([dateTag, filterTag]).size().tolist()
    df1['sort_column'] = df1[filterTag].map(order_dict)
    df1 = df1.sort_values(['sort_column', dateTag], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
    if avgChoice == avgTag:
        df2 = df1.groupby([dateTag]) \
            .agg({countTag: 'sum', durationTag:'mean'}) \
            .reset_index()
    else:
        df2 = df1.groupby([dateTag]) \
            .agg({countTag: 'sum', durationTag:'median'}) \
            .reset_index()
    df2 = df2.sort_values([dateTag]).reset_index(drop = True)
    return [df1, df2]

# return data group by chosen data type and types.
def getAvgDataFrameByType(df, avgChoice, datetype, typesChoice, order, eventChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    eventsTag = utilities.getTagName('eventSequenceTag')
    filterTag = utilities.getTagName('filterTag')
    if typesChoice == None or len(typesChoice) == 0:
        return None
    df5 = df.copy()
    types = typesChoice.copy()
    if eventChoice != None and eventChoice in types:
        df5 = getEventDataFrame(df5, eventChoice)
        index = types.index(eventChoice)
        types[index] = eventTag
    if avgChoice == avgTag:
        df4 = df5.groupby(types) \
            .agg({df5.columns[2]:'size', durationTag: 'mean'}) \
            .rename(columns = {df5.columns[2]:countTag, durationTag:avgTag}) \
            .reset_index()
    else:
        df4 = df5.groupby(types) \
            .agg({df5.columns[2]:'size', durationTag: 'median'}) \
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
    df3 = keepOnlyImportant(df3, 0.25)
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
    month = utilities.getPlaceholderName("month")
    monthYear = utilities.getPlaceholderName("monthYear")
    trimester = utilities.getPlaceholderName("trimester")
    trimesterYear = utilities.getPlaceholderName("trimesterYear")
    week = utilities.getPlaceholderName("week")
    year = utilities.getPlaceholderName("year")
    if datetype == week:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getWeekNumber(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeek(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getWeek(x))
        return [df1, df2, df3]
    elif datetype == month:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getMonthNumber(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonth(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonth(x))
        return [df1, df2, df3]
    elif datetype == monthYear:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getMonthYearDate(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonthYear(x))
        return [df1, df2, df3]
    elif datetype == trimester:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getTrimesterDate(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimester(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimester(x))
        return [df1, df2, df3]
    elif datetype == trimesterYear:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getTrimesterYearDate(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        return [df1, df2, df3]
    elif datetype == year:
        df_temp[dateTag] = df_temp[dateTag].map(lambda x: utilities.getYearNumber(x))
        [df1, df2] = getAvgTotDataframe(df_temp, order_dict, avgChoice)
        return [df1, df2, df3]
        
# return data group by chosen type.
def getAvgStdDataFrameByType(df, type, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag')
    typeDuration = type.copy()
    typeDuration.append(durationTag)
    df1 = df[typeDuration].copy()
    if avgChoice == avgTag:
        df2 = df1.groupby(type, as_index = False).mean()
    else:
        df2 = df1.groupby(type, as_index = False).median()
    df2[countTag] = df1.groupby(type).size().tolist()
    df2[quantileTag] = df1.groupby(type, as_index = False).quantile(0.75)[durationTag]
    df1 = df1.sort_values(type).reset_index(drop = True)
    df2 = df2.sort_values(type).reset_index(drop = True)
    return [df1, df2]

# return data group by chosen type.
def getAvgStdDataFrameByTypeChoice(df, type, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag')
    typeDuration = type.copy()
    typeDuration.append(durationTag)
    df1 = df[typeDuration].copy()
    df1[durationTag] = df1[durationTag].astype(int)
    df1 = keepOnlyRelevant(df1, 0.001, type[0])
    if avgChoice == avgTag:
        df2 = df1.groupby(type, as_index = False).mean()
    else:
        df2 = df1.groupby(type, as_index = False).median()
    df2[countTag] = df1.groupby(type).size().tolist()
    df2[quantileTag] = df1.groupby(type, as_index = False).quantile(0.75)[durationTag]
    df1 = df1.sort_values(type).reset_index(drop = True)
    df2 = df2.sort_values(type).reset_index(drop = True)
    return [df1, df2]

# return dataframe with rows which type is present a relevant number of times.
def keepOnlyRelevant(df, perc, tag):
    countTag = utilities.getTagName('countTag')
    df_temp = df.copy()
    df_temp = df_temp.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = countTag)
    totCount = df_temp[countTag].sum()
    threshold = totCount * perc
    relevant = df_temp[df_temp[countTag] >= threshold][tag].tolist()
    return df[df[tag].isin(relevant)]

# reduce dataframe to a number of rows such that they cover at least given percentage.
def keepOnlyImportant(df, perc):
    countTag = utilities.getTagName('countTag')
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
def getMonthDataFrame(df, months):
    if months == None or len(months) == 0:
        return df
    dateTag = utilities.getTagName('dateTag')
    df_temp = df.copy()
    df_temp[dateTag] = df_temp[dateTag].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
    return df_temp[df_temp[dateTag].isin(months)]

# return dataframe rows where date year is contained given years.
def getYearDataFrame(df, years):
    if years == None or len(years) == 0:
        return df
    dateTag = utilities.getTagName('dateTag')
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
def getEventDataFrame(df, event):
    if event == None:
        return df
    eventTag = utilities.getTagName('eventTag')
    eventsTag = utilities.getTagName('eventSequenceTag')
    withTag = utilities.getPlaceholderName("with")
    withOut = utilities.getPlaceholderName("without")
    df_temp = df.copy()
    df_temp[eventTag] = df_temp[eventsTag]
    for i, row in df_temp.iterrows():
        if event in utilities.fromStringToList(row[eventsTag]):
            df_temp.at[i, eventTag] = withTag + " " + event
        else:
            df_temp.at[i, eventTag] = withOut + " " + event
    return df_temp

# return unique years in given dataframe dates.
def getAllYears(df):
    dateTag = utilities.getTagName('dateTag')
    df_temp = df[dateTag].copy()
    df_temp = df_temp.map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year).sort_values()
    years = df_temp.unique()
    return years

# return group by types with corrispondent counts.
def getGroupBy(df, tag):
    countTag = utilities.getTagName('countTag')
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
    all = utilities.getPlaceholderName('all')
    totCount = df[countTag].sum()
    newName = all + " (" + str(totCount) + ")"
    return newName

# return index of dataframe selected rows.
def getSelectedRows(df, selection, tag):
    df_temp = df.copy()
    df_temp = df_temp[df_temp[tag].isin(selection)]
    selectedRows = list(df_temp.index)
    return selectedRows

# return dataframe rows from given index.
def getRowsFromIndex(df, index):
    df_temp = df.copy()
    df_temp = df_temp.iloc[index]
    return df_temp

def selectFollowingRows(df, tag, tagChoice):
    numEventTag = utilities.getTagName('numEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    df_tag = df.copy()
    df_tag = df[df[tag] == tagChoice]
    df_final = df.iloc[:0,:].copy()
    for i, row in df_tag.iterrows():
        numEvent = row[numEventTag]
        numProcess = row[numProcessTag]
        df_temp = df.copy()
        df_temp = df[df[numEventTag] > numEvent]
        df_temp = df_temp[df_temp[numProcessTag] == numProcess]
        df_final = pd.concat([df_final, df_temp.head(1)], ignore_index = True)
        print(numEvent)
    print(df_final)
    exit()
