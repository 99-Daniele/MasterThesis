# this file handles dataframe managements.

import datetime as dt
import pandas as pd
import textwrap

import utils.FileOperation as file
import utils.Utilities as utilities

# importantProcessStates, importantSections and importantSubjects are taken from text file. This are type of events that are the most important.
importantProcessStates = file.getDataFromTextFile('utils/preferences/importantProcessStates.txt')
importantSections = file.getDataFromTextFile('utils/preferences/importantSections.txt')
importantSubjects = file.getDataFromTextFile('utils/preferences/importantSubjects.txt')


# from events list create basic events dataframe. Later he will be integrated with subject, state, phase chosen by user.
def createBasicEventsDataFrame(events, dateTag, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, eventTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag):
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag])
    df = df.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return df

# create events dataframe with only one end phase event for each process.
def createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag):
    # divide df into dfEnd which have only end phase events and dfNotEnd which are the other events.
    dfNotEnd = df[df[phaseTag] != endPhase].reset_index(drop = True)
    dfEnd = df[df[phaseTag] == endPhase].reset_index(drop = True)
    # dfEnd takes only the first event of each process.
    dfEnd = dfEnd.groupby(numProcessTag, as_index = False).first().reset_index(drop = True)
    # then concant dfNotEnd and calculated dfEnd.
    df = pd.concat([dfNotEnd, dfEnd])
    df = df.dropna()
    df = df.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return df

# from events info list create events info dataframe.
def createEventsInfoDataFrame(eventsInfo, codeEventTag, eventTag):
    df = pd.DataFrame(eventsInfo, columns = [codeEventTag, eventTag])
    return df

# from states info list create states info dataframe.
def createStatesInfoDataFrame(statesInfo, codeStateTag, phaseTag, phaseDBTag, stateTag):
    df = pd.DataFrame(statesInfo, columns = [codeStateTag, stateTag, phaseDBTag, phaseTag])
    df[phaseTag] = df[phaseTag].fillna(0)
    return df

# from events info list create events info dataframe.
def createSubjectsInfoDataFrame(subjectsInfo, codeSubjectTag, ritualTag, subjectTag):
    df = pd.DataFrame(subjectsInfo, columns = [codeSubjectTag, subjectTag, ritualTag])
    return df

# from processes list create process duration dataframe.
def createProcessDurationsDataFrame(process, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag, codeSubjectTag):
    df = pd.DataFrame(process, columns = [numProcessTag, durationTag, dateTag, numEventTag, codeJudgeTag, codeSubjectTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, eventPhaseSequenceTag, nextDateTag, nextIdTag])
    df[codeSubjectTag] = df[codeSubjectTag].astype(str)
    # filteredDf is df filtered by only important process states, important sections and important subjects.
    filteredDf = df.copy()
    if importantProcessStates != None and len(importantProcessStates) > 0:
        filteredDf = filteredDf[filteredDf[finishedTag].isin(importantProcessStates)]
    if importantSections != None and len(importantSections) > 0:
        filteredDf = filteredDf[filteredDf[sectionTag].isin(importantSections)]
    if importantSubjects != None and len(importantSubjects) > 0:
        filteredDf = filteredDf[filteredDf[codeSubjectTag].isin(importantSubjects)]
    df = df.sort_values(by = [dateTag, numProcessTag]).reset_index(drop = True)
    df = df.dropna()
    filteredDf = filteredDf.sort_values(by = [dateTag, numProcessTag]).reset_index(drop = True)
    filteredDf = filteredDf.dropna()
    return [df, filteredDf]

# from events list create type duration dataframe.
def createTypeDurationsDataFrame(events, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag):
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, codeEventTag, eventTag, durationTag, dateTag, codeJudgeTag, codeStateTag, stateTag, phaseTag, codeSubjectTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag])
    df[codeSubjectTag] = df[codeSubjectTag].astype(str)
    # filteredDf is df filtered by only important sections and important subjects.
    filteredDf = df.copy()
    if importantSections != None and len(importantSections) > 0:
        filteredDf = filteredDf[filteredDf[sectionTag].isin(importantSections)]
    if importantSubjects != None and len(importantSubjects) > 0:
        filteredDf = filteredDf[filteredDf[codeSubjectTag].isin(importantSubjects)]
    df = df.dropna()
    filteredDf = filteredDf.dropna()
    return [df, filteredDf]

# from states duration and state names list create state names dataframe with info.
def createStateNameDataframeWithInfo(statesDuration, stateNames):
    codeStateTag = utilities.getTagName('codeStateTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    # from statesDuration calculates mean duration and size of each state.
    statesDuration = statesDuration.groupby([codeStateTag]) \
        .agg({statesDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {statesDuration.columns[2]:countTag}) \
        .reset_index()
    statesDuration[durationTag] = statesDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    statesDuration[codeStateTag] = statesDuration[codeStateTag].astype(str)
    result = joinDataframe(stateNames, statesDuration, codeStateTag, None, None)
    result = result.fillna(0)
    result = result.sort_values([codeStateTag]).reset_index(drop = True)
    return result

# from events duration and event names list create event names dataframe with info.
def createEventNameDataframeWithInfo(eventsDuration, eventNames):
    codeEventTag = utilities.getTagName('codeEventTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    # from eventDuration calculates mean duration and size of each event.
    eventsDuration = eventsDuration.groupby([codeEventTag]) \
        .agg({eventsDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {eventsDuration.columns[2]:countTag}) \
        .reset_index()
    eventsDuration[durationTag] = eventsDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    eventsDuration[codeEventTag] = eventsDuration[codeEventTag].astype(str)
    result = joinDataframe(eventNames, eventsDuration, codeEventTag, None, None)
    result = result.fillna(0)
    result = result.sort_values([codeEventTag]).reset_index(drop = True)
    return result

# from process duration and subject names list create subject names dataframe with info.
def createSubjectNameDataframeWithInfo(processDuration, subjectNames):
    codeSubjectTag = utilities.getTagName('codeSubjectTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    # from subjectsDuration calculates mean duration and size of each process subject.
    processDuration = processDuration.groupby([codeSubjectTag]) \
        .agg({processDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {processDuration.columns[2]:countTag}) \
        .reset_index()
    processDuration[durationTag] = processDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    result = joinDataframe(subjectNames, processDuration, codeSubjectTag, None, None)
    result = result.fillna(0)
    result = result.sort_values([codeSubjectTag]).reset_index(drop = True)
    return result

# from process duration create process types dataframe with info.
def creatFinishedDataframeWithInfo(processDuration):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    finishedTag = utilities.getTagName('finishedTag')
    # from subjectsDuration calculates mean duration and size of each process subject.
    processDuration = processDuration.groupby([finishedTag]) \
        .agg({processDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {processDuration.columns[2]:countTag}) \
        .reset_index()
    processDuration[durationTag] = processDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    return processDuration

# from process duration create section dataframe with info.
def creatSectionDataframeWithInfo(processDuration):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    sectionTag = utilities.getTagName('sectionTag')
    # from subjectsDuration calculates mean duration and size of each process subject.
    processDuration = processDuration.groupby([sectionTag]) \
        .agg({processDuration.columns[2]: 'size', durationTag: 'mean'}) \
        .rename(columns = {processDuration.columns[2]:countTag}) \
        .reset_index()
    processDuration[durationTag] = processDuration[durationTag].astype(float).apply('{:,.2f}'.format)
    return processDuration

# from input df return another dataframe with size and mean/median duration group by date.
def getAvgTotDataframeByDate(df, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag')
    df = df.sort_values([dateTag]).reset_index(drop = True)
    if avgChoice == avgTag:
        df2 = df.groupby([dateTag], as_index = False).mean()
    else:
        df2 = df.groupby([dateTag], as_index = False).median()
    df2[countTag] = df.groupby([dateTag]).size().tolist()
    df2[quantileTag] = df.groupby([dateTag], as_index = False).quantile(0.75)[durationTag]
    return [df, df2]

# return dataframe grouped by chosen data type.
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

# from input df return another dataframe with size and mean/median duration group by date and filter.
def getAvgTotDataframeByDataAndFilter(df, order_dict, avgChoice):
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
        df2 = df.groupby([dateTag]) \
            .agg({filterTag: 'size', durationTag:'mean'}) \
            .rename(columns = {filterTag: countTag}) \
            .reset_index()
    else:
        df2 = df.groupby([dateTag]) \
            .agg({filterTag: 'size', durationTag:'median'}) \
            .rename(columns = {filterTag: countTag}) \
            .reset_index()
    df2 = df2.sort_values([dateTag]).reset_index(drop = True)
    return [df1, df2]

# return data group by user type and datetype choices.
def getAvgDataFrameByTypeChoices(df, avgChoice, datetype, typesChoice, order, eventChoice, stateChoice, phaseChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    filterTag = utilities.getTagName('filterTag')
    month = utilities.getPlaceholderName("month")
    monthYear = utilities.getPlaceholderName("monthYear")
    phaseTag = utilities.getTagName('phaseTag')
    stateTag = utilities.getTagName('stateTag')
    trimester = utilities.getPlaceholderName("trimester")
    trimesterYear = utilities.getPlaceholderName("trimesterYear")
    week = utilities.getPlaceholderName("week")
    year = utilities.getPlaceholderName("year")
    if typesChoice == None or len(typesChoice) == 0:
        return None
    df5 = df.copy()
    types = typesChoice.copy()
    # if user select event choice getEventDataframe() is called.
    if eventChoice != None and eventChoice in types:
        df5 = getEventDataFrame(df5, eventChoice)
        index = types.index(eventChoice)
        types[index] = eventTag
    # if user select state choice getStateDataframe() is called.
    if stateChoice != None and stateChoice in types:
        df5 = getStateDataFrame(df5, stateChoice)
        index = types.index(stateChoice)
        types[index] = stateTag
    # if user select phase choice getPhaseDataframe() is called.
    if phaseChoice != None and phaseChoice in types:
        df5 = getPhaseDataFrame(df5, phaseChoice)
        index = types.index(phaseChoice)
        types[index] = phaseTag
    # group dataframe by chosen types.
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
    # df3 concatenates all chosen types into one column named filterTag.
    df3 = df3.rename(columns = {types[0]: filterTag})
    i = 1
    while i < len(types):
        df3[filterTag] = df3[filterTag].astype(str) + " - " + df4[types[i]].astype(str)
        i = i + 1
    # df3 is filtered by only important data.
    df3 = keepOnlyImportant(df3, 0.75, 18)
    df3 = df3.sort_values([order], ascending = False).reset_index(drop = True)
    # order_dict and order_list frame the selected order of filter tag based on order user choice.
    order_dict = df3.set_index(filterTag)[order].to_dict()
    order_list = df3[filterTag].tolist()
    # newDF concatenates all chosen types into one column named filterTag and order it.
    newDF = df5[[dateTag, durationTag, types[0]]].copy()
    newDF = newDF.rename(columns = {types[0]:filterTag})
    i = 1
    while i < len(types):
        newDF[filterTag] = newDF[filterTag].astype(str) + " - " + df5[types[i]].astype(str)
        i = i + 1
    newDF = newDF[newDF[filterTag].isin(order_list)]
    # based on user date choices aggregate newDF.
    if datetype == week:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getWeekNumber(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getWeek(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getWeek(x))
        return [df1, df2, df3]
    elif datetype == month:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getMonthNumber(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonth(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonth(x))
        return [df1, df2, df3]
    elif datetype == monthYear:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getMonthYearDate(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getMonthYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getMonthYear(x))
        return [df1, df2, df3]
    elif datetype == trimester:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getTrimesterDate(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimester(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimester(x))
        return [df1, df2, df3]
    elif datetype == trimesterYear:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getTrimesterYearDate(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        df1[dateTag] = df1[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        df2[dateTag] = df2[dateTag].map(lambda x: utilities.getTrimesterYear(x))
        return [df1, df2, df3]
    elif datetype == year:
        newDF[dateTag] = newDF[dateTag].map(lambda x: utilities.getYearNumber(x))
        [df1, df2] = getAvgTotDataframeByDataAndFilter(newDF, order_dict, avgChoice)
        return [df1, df2, df3]
        
# return data group by chosen type.
def getAvgStdDataFrameByType(df, typeChoice, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag')
    phaseTag = utilities.getTagName('phaseTag')
    df = df.sort_values(by = phaseTag).reset_index(drop = True) 
    types = getUniques(df, typeChoice)
    typeDuration = [typeChoice, durationTag]
    df1 = df[typeDuration].copy()
    if avgChoice == avgTag:
        df2 = df1.groupby(typeChoice, as_index = False).mean()
    else:
        df2 = df1.groupby(typeChoice, as_index = False).median()
    df2[countTag] = df1.groupby(typeChoice).size().tolist()
    df2[quantileTag] = df1.groupby(typeChoice, as_index = False).quantile(0.75)[durationTag]
    df1[typeChoice] = df1[typeChoice].astype("category")
    df1[typeChoice] = df1[typeChoice].cat.set_categories(types)
    df1 = df1.sort_values([typeChoice]).reset_index(drop = True)
    df1[typeChoice] = df1[typeChoice].astype(str)
    df2[typeChoice] = df2[typeChoice].astype("category")
    df2[typeChoice] = df2[typeChoice].cat.set_categories(types)
    df2 = df2.sort_values([typeChoice]).reset_index(drop = True)
    df2[typeChoice] = df2[typeChoice].astype(str)
    return [df1, df2]

# return data group by chosen type ordered by phase.
def getAvgStdDataFrameByTypeChoiceOrderedByPhase(df, typeChoice, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag') 
    phaseTag = utilities.getTagName('phaseTag')
    df = df.sort_values(by = phaseTag).reset_index(drop = True) 
    types = getUniques(df, typeChoice)   
    typeDuration = [typeChoice, durationTag]
    df1 = df[typeDuration].copy()
    df1[durationTag] = df1[durationTag].astype(int)
    df1 = keepOnlyRelevant(df1, 0.005, typeChoice).reset_index(drop = True)
    if avgChoice == avgTag:
        df2 = df1.groupby(typeChoice, as_index = False).mean()
    else:
        df2 = df1.groupby(typeChoice, as_index = False).median()
    df2[countTag] = df1.groupby(typeChoice).size().tolist()
    df2[quantileTag] = df1.groupby(typeChoice, as_index = False).quantile(0.75)[durationTag]
    df1[typeChoice] = df1[typeChoice].astype("category")
    df1[typeChoice] = df1[typeChoice].cat.set_categories(types)
    df1 = df1.sort_values([typeChoice]).reset_index(drop = True)
    df1[typeChoice] = df1[typeChoice].astype(str)
    df2[typeChoice] = df2[typeChoice].astype("category")
    df2[typeChoice] = df2[typeChoice].cat.set_categories(types)
    df2 = df2.sort_values([typeChoice]).reset_index(drop = True)
    df2[typeChoice] = df2[typeChoice].astype(str)
    return [df1, df2]

# return data group by chosen type filtered by quantile. Remove all outlier value.
def getAvgStdDataFrameByTypeQuantileFilter(df, typeChoice, avgChoice):
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    quantileTag = utilities.getTagName('quantileTag') 
    typeDuration = [typeChoice, durationTag]
    types = getUniques(df, typeChoice)   
    df1 = df[typeDuration].copy()
    df1[durationTag] = df1[durationTag].astype(int)
    df1 = keepOnlyRelevant(df1, 0.005, typeChoice).reset_index(drop = True)
    df_q = df1.groupby(typeChoice, as_index = False).quantile(0.75)
    df3 = df1.iloc[:0,:].copy()
    for i, row in df_q.iterrows():
        newDF = df1[df1[typeChoice] == row[typeChoice]]
        newDF = newDF[newDF[durationTag] <= row[durationTag]]        
        df3 = pd.concat([df3, newDF], ignore_index = True)
    if avgChoice == avgTag:
        df2 = df3.groupby(typeChoice, as_index = False).mean()
    else:
        df2 = df3.groupby(typeChoice, as_index = False).median()
        df3 = pd.concat([df3, newDF], ignore_index = True)
    df2[countTag] = df3.groupby(typeChoice).size().tolist()
    df2[quantileTag] = df3.groupby(typeChoice, as_index = False).quantile(0.75)[durationTag]
    df3[typeChoice] = df3[typeChoice].astype("category")
    df3[typeChoice] = df3[typeChoice].cat.set_categories(types)
    df3 = df3.sort_values([typeChoice]).reset_index(drop = True)
    df3[typeChoice] = df3[typeChoice].astype(str)
    df2[typeChoice] = df2[typeChoice].astype("category")
    df2[typeChoice] = df2[typeChoice].cat.set_categories(types)
    df2 = df2.sort_values([typeChoice]).reset_index(drop = True)
    df2[typeChoice] = df2[typeChoice].astype(str)
    return [df3, df2]

# return dataframe with rows which type is present a relevant number of times.
def keepOnlyRelevant(df, perc, tag):
    countTag = utilities.getTagName('countTag')
    newDF = df.copy()
    newDF = newDF.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = countTag)
    totCount = newDF[countTag].sum()
    threshold = totCount * perc
    relevant = newDF[newDF[countTag] >= threshold][tag].tolist()
    return df[df[tag].isin(relevant)]

# reduce dataframe to a number of rows such that they cover at least given percentage.
def keepOnlyImportant(df, perc, minNumber):
    countTag = utilities.getTagName('countTag')
    newDF = df.copy()
    totCount = newDF[countTag].sum()
    threshold = totCount * perc
    newDF = newDF.sort_values([countTag], ascending = False).reset_index(drop = True)
    sum = 0
    newDf = newDF.iloc[:0,:].copy()
    for i, row in newDF.iterrows():
        sum = sum + row[countTag]
        newDf = newDf._append(row, ignore_index = True)
        if sum > threshold and i > minNumber:
            break
    return newDf

# return dataframe rows where given tag is contained in given types.
def getTypesDataFrame(df, tag, types):
    if types == None or len(types) == 0:
        return df
    newDF = df.copy()
    return newDF[newDF[tag].isin(types)]

# return dataframe rows where given tag is contained in given types from string.
def getTypesDataFrameFromString(df, tag, type):
    if type == None:
        return df
    newDF = df.copy()
    return newDF[newDF[tag].str.contains(type)]

# return dataframe rows where date month is contained given months.
def getMonthDataFrame(df, months):
    if months == None or len(months) == 0:
        return df
    dateTag = utilities.getTagName('dateTag')
    newDF = df.copy()
    newDF[dateTag] = newDF[dateTag].map(lambda x: str(dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month))
    return newDF[newDF[dateTag].isin(months)]

# return dataframe rows where date year is contained given years.
def getYearDataFrame(df, years):
    if years == None or len(years) == 0:
        return df
    dateTag = utilities.getTagName('dateTag')
    newDF = df.copy()
    newDF[dateTag] = newDF[dateTag].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
    return newDF[newDF[dateTag].isin(years)]

# return dataframe rows where date is between given startDate and endDate.
def getDateDataFrame(df, type, startDate, endDate):
    if startDate == None or endDate == None:
        return df
    newDF = df.copy()
    d = newDF[newDF[type] >= startDate]
    d = d[d[type] <= endDate]
    return d

# return dataframe where event sequence contains or not a particular event.
def getEventDataFrame(df, event):
    if event == None:
        return df
    eventTag = utilities.getTagName('eventTag')
    eventSequenceTag = utilities.getTagName('eventSequenceTag')
    eventPhaseSequenceTag = utilities.getTagName("eventPhaseSequenceTag")
    phaseTag = utilities.getPlaceholderName("phase")
    withOut = utilities.getPlaceholderName("without")
    newDF = df.copy()
    newDF[eventTag] = newDF[eventSequenceTag]
    for i, row in newDF.iterrows():
        eventSequence = utilities.fromStringToList(row[eventSequenceTag])
        eventPhaseSequence = utilities.fromStringToList(row[eventPhaseSequenceTag])
        try:
            eventIndex = eventSequence.index(event)
            phase = eventPhaseSequence[eventIndex]
            eventString = event + " " + phaseTag.upper() + " " + str(phase)
        except:
            eventString = withOut + " " + event
        newDF.at[i, eventTag] = eventString
    return newDF

# return dataframe where state sequence contains or not a particular state.
def getStateDataFrame(df, state):
    if state == None:
        return df
    stateTag = utilities.getTagName('stateTag')
    stateSequenceTag = utilities.getTagName('stateSequenceTag')
    withTag = utilities.getPlaceholderName("with")
    withOut = utilities.getPlaceholderName("without")
    newDF = df.copy()
    newDF[stateTag] = newDF[stateSequenceTag]
    for i, row in newDF.iterrows():
        stateSequence = utilities.fromStringToList(row[stateSequenceTag])
        try:
            stateSequence.index(state)
            stateString = withTag + " " + state
        except:
            stateString = withOut + " " + state
        newDF.at[i, stateTag] = stateString
    return newDF

# return dataframe where phase sequence contains or not a particular phase.
def getPhaseDataFrame(df, phase):
    if phase == None:
        return df
    phaseTag = utilities.getTagName('phaseTag')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    withTag = utilities.getPlaceholderName("with")
    withOut = utilities.getPlaceholderName("without")
    newDF = df.copy()
    newDF[phaseTag] = newDF[phaseSequenceTag]
    for i, row in newDF.iterrows():
        phaseSequence = utilities.fromStringToList(row[phaseSequenceTag])
        try:
            phaseSequence.index(phase)
            phaseString = withTag + " " + phaseTag + " " + phase
        except:
            phaseString = withOut + " " + phaseTag + " " + phase
        newDF.at[i, phaseTag] = phaseString
    return newDF

# return unique years in given dataframe dates.
def getAllYears(df):
    dateTag = utilities.getTagName('dateTag')
    newDF = df[dateTag].copy()
    newDF = newDF.map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year).sort_values().reset_index(drop = True)
    years = newDF.unique()
    return years

# return group by types with corrispondent counts.
def getGroupBy(df, tag):
    countTag = utilities.getTagName('countTag')
    newDF = df.copy()
    types = newDF.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = countTag)[tag].tolist()
    return types

# return group by types with corrispondent counts from string.
def getGroupByFromString(df, tag):
    newDF = df.copy()
    types = {}
    for d in newDF[tag]:
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
    newDF = df[tag].copy()
    uniques = newDF.unique()
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

# return joins of dataframe
def joinDataframe(df1, df2, tagJoin, dropJoin1, dropJoin2):
    newDF_1 = df1.copy()
    newDF_2 = df2.copy()
    if dropJoin1 != None:
        newDF_1 = newDF_1.drop(dropJoin1, axis = 1)
    if dropJoin2 != None:
        newDF_2 = newDF_2.drop(dropJoin2, axis = 1)
    newDf = newDF_1.join(newDF_2.set_index(tagJoin), on = tagJoin)
    return newDf

# return following rows of chosen event/state/phase.
def selectFollowingRows(df, tag, tagChoices):
    nextIdTag = utilities.getTagName("nextIdTag")
    numEventTag = utilities.getTagName('numEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    df = df.sort_values(by = [numProcessTag, numEventTag]).reset_index(drop = True)
    df_tag = df[df[tag].isin(tagChoices)].copy()
    df_tag = df_tag[df_tag[numEventTag] != df_tag[nextIdTag]]
    df_tag = df_tag[[nextIdTag]].reset_index(drop = True)
    df_tag = df_tag.rename(columns = {nextIdTag:numEventTag})
    newDf = joinDataframe(df_tag, df, numEventTag, None, None)
    newDf = newDf.dropna()
    return newDf

# get phase of state from dataframe.
def getPhaseOfState(statesName, state, phaseTag):
    phase = statesName.get(state)[phaseTag]
    return phase

# create map to decide color based on state phase.
def phaseColorMap(type, statesInfoDataframe):
    statesInfo = statesInfoDataframe.to_dict('records')
    colors = file.getDataFromJsonFile('utils/utilities/phaseColors.json')
    phaseTag = utilities.getTagName("phaseTag")
    map = {}
    for s in statesInfo:
        key = str(s[type])
        phase = str(s[phaseTag])
        map.update({key: colors.get(phase)})
    return map
