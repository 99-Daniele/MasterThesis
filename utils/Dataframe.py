# this file handles dataframe managements.

import datetime as dt
import numpy as np
import pandas as pd

import utils.FileOperation as file
import utils.Utilities.Utilities as utilities

# importantProcessStates, importantSections, importantSUbjects are taken from text file. This are type of events that are the most important. Thay can be changed or removed.
try:
    importantProcessStates = file.getDataFromTextFile('preferences/importantProcessStates.txt')
except:
    importantProcessStates = None
try:
    importantSections = file.getDataFromTextFile('preferences/importantSections.txt')
except:
    importantSections = None

# from events list create events dataframe.
def createEventsDataFrame(events):
    pIds = []
    dates = []
    phases = []
    tagEvents = []
    eIds = []
    typeEvents = []
    tagStates = []
    typeStates = []
    judges = []
    subjects = []
    sections = []
    finished = []
    startProcessDates = []
    finishedEventProcesses = []
    for e in events:
        if e[2] != '5' or e[0] not in finishedEventProcesses:
            pIds.append(e[0])
            dates.append(e[1])
            phases.append(e[2])
            tagEvents.append(e[3])
            eIds.append(e[4])
            typeEvents.append(e[5])
            tagStates.append(e[6])
            typeStates.append(e[7])
            judges.append(e[8])
            subjects.append(e[9])
            sections.append(e[10])
            finished.append(utilities.getProcessState(e[11]))
            startProcessDates.append(e[12])
            if e[2] == '5':
                finishedEventProcesses.append(e[0])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases, "evento": tagEvents, "numEvento": eIds, "dataInizioProcesso": startProcessDates, "stato": tagStates, "giudice": judges, "sezione": sections, "materia": subjects})

# from processes list create processes duration dataframe.
def createProcessesDurationDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    months = []
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
            month = dt.datetime.strptime(p[0], '%Y-%m-%d %H:%M:%S').month
            months.append(utilities.getMonth(month))
            pIds.append(p[6])
            sequences.append(p[7])
            phases.append(p[8])
            events.append(p[9])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "mese": months, "sequenza": sequences, "fasi": phases, "eventi": events})

# from states list create states duration dataframe.
def createStatesDurationsDataFrame(stateEvents):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    pIds = []
    tags = []
    states = []
    phases = []
    for s in stateEvents:
        if (importantSections == None or s[4] in importantSections) and (importantProcessStates == None or utilities.getProcessState(s[5]) in importantProcessStates):
            dates.append(s[0])
            durations.append(s[1])
            judges.append(s[2])
            subjects.append(s[3])
            sections.append(s[4])
            finished.append(utilities.getProcessState(s[5]))
            pIds.append(s[6])
            tags.append(s[7])
            states.append(s[8])
            phases.append(s[9])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "stato": tags, "fase": phases})

# from phases list create phases duration dataframe.
def createPhasesDurationsDataFrame(phaseEvents):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    pIds = []
    phases = []
    orders = []
    for p in phaseEvents:
        if (importantSections == None or p[4] in importantSections) and (importantProcessStates == None or utilities.getProcessState(p[5]) in importantProcessStates):
            dates.append(p[0])
            durations.append(p[1])
            judges.append(p[2])
            subjects.append(p[3])
            sections.append(p[4])
            finished.append(utilities.getProcessState(p[5]))
            pIds.append(p[6])
            phases.append(p[7])
            orders.append(p [8])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "fase": phases})

# from events list create events duration dataframe.
def createEventsDurationsDataFrame(events):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    eIds = []
    pIds = []
    tagEvents = []
    typeEvents = []
    phases = []
    for e in events:
        if (importantSections == None or e[4] in importantSections) and (importantProcessStates == None or utilities.getProcessState(e[5]) in importantProcessStates):
            dates.append(e[0])
            durations.append(e[1])
            judges.append(e[2])
            subjects.append(e[3])
            sections.append(e[4])
            finished.append(utilities.getProcessState(e[5]))
            eIds.append(e[6])
            pIds.append(e[7])
            tagEvents.append(e[8])
            typeEvents.append(e[9])
            phases.append(e[10])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "evento": tagEvents, "fase": phases})

# from court hearings list create court hearings duration dataframe.
def createCourtHearingsDurationDataFrame(courtHearings):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    pIds = []
    for c in courtHearings:
        if (importantSections == None or c[4] in importantSections) and (importantProcessStates == None or utilities.getProcessState(c[5]) in importantProcessStates):
            dates.append(c[0])
            durations.append(c[1])
            judges.append(c[2])
            subjects.append(c[3])
            sections.append(c[4])
            finished.append(utilities.getProcessState(c[5]))
            pIds.append(c[6])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished})

# return data group by chosen data type.
def getAvgStdDataFrameByDate(df, dataType):
    match dataType:
        case "SETTIMANA":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getWeekNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.getWeek(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getWeek(x))
            return [df1, df2]
        case "MESE":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getMonthNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.getMonth(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getMonth(x))
            return [df1, df2]
        case "MESE DELL'ANNO":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getMonthYearDate(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.getMonthYear(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getMonthYear(x))
            return [df1, df2]
        case "TRIMESTRE":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimesterDate(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimester(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getTrimester(x))
            return [df1, df2]
        case "TRIMESTRE DELL'ANNO":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimesterYearDate(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimesterYear(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getTrimesterYear(x))
            return [df1, df2]
        case "ANNO":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getYearNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            return [df1, df2]

# return data group by chosen data type and types.
def getAvgDataFrameByType(df, datetype, types, order, eventsChoice):
    if types == None:
        return None
    df5 = df.copy()
    if eventsChoice != None and len(eventsChoice) > 0:
        for i, row in df5.iterrows():
            if set(eventsChoice).issubset(set(utilities.fromStringToList(row["eventi"]))):
                df5.at[i, "eventi"] = utilities.fromListToString(eventsChoice) + " SI"
            else:
                df5.at[i, "eventi"] = utilities.fromListToString(eventsChoice) + " NO"
    df4 = df5.groupby(types) \
    .agg({'giudice':'size', 'durata':'mean'}) \
    .rename(columns = {'giudice':'conteggio','durata':'media'}) \
    .reset_index()
    for t in types: 
        df4.drop(df4[df4[t] == 'null'].index, inplace = True)
    df3 = df4[[types[0], 'conteggio', 'media']].copy()
    df3 = df3.rename(columns = {types[0]:'filtro'})
    i = 1
    while i < len(types):
        df3['filtro'] = df3['filtro'].astype(str) + " - " + df4[types[i]].astype(str)
        i = i + 1
    df3 = keepOnlyImportant(df3, 0.25)
    df3 = df3.sort_values([order], ascending = False).reset_index(drop = True)
    order_dict = df3.set_index('filtro')[order].to_dict()
    order_list = df3['filtro'].tolist()
    df_temp = df5[['data', 'durata', types[0]]].copy()
    df_temp = df_temp.rename(columns = {types[0]:'filtro'})
    i = 1
    while i < len(types):
        df_temp['filtro'] = df_temp['filtro'].astype(str) + " - " + df5[types[i]].astype(str)
        i = i + 1
    df_temp = df_temp[df_temp['filtro'].isin(order_list)]
    match datetype:
        case "SETTIMANA":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getWeekNumber(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df1['data'] = df1['data'].map(lambda x: utilities.getWeek(x))
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: utilities.getWeek(x))
            return [df1, df2, df3]
        case "MESE":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getMonthNumber(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df1['data'] = df1['data'].map(lambda x: utilities.getMonth(x))
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: utilities.getMonth(x))
            return [df1, df2, df3]
        case "MESE DELL'ANNO":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getMonthYearDate(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df1['data'] = df1['data'].map(lambda x: utilities.getMonthYear(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getMonthYear(x))
            return [df1, df2, df3]
        case "TRIMESTRE":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getTrimesterDate(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimester(x))
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: utilities.getTrimester(x))
            return [df1, df2, df3]
        case "TRIMESTRE DELL'ANNO":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getTrimesterYearDate(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df1['data'] = df1['data'].map(lambda x: utilities.getTrimesterYear(x))
            df2['data'] = df2['data'].map(lambda x: utilities.getTrimesterYear(x))
            return [df1, df2, df3]
        case "ANNO":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getYearNumber(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['conteggio'] = df_temp.groupby(['data', 'filtro']).size().tolist()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2['conteggio'] = df_temp.groupby(['data']).size().tolist()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            return [df1, df2, df3]
        
# return data group by chosen type.
def getAvgStdDataFrameByType(df, type):
    typeDuration = type.copy()
    typeDuration.append('durata')
    df1 = df[typeDuration].copy()
    df2 = df1.groupby(type, as_index = False).mean()
    df2['conteggio'] = df1.groupby(type).size().tolist()
    df2['quantile'] = df1.groupby(type, as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(type).reset_index(drop = True)
    df2 = df2.sort_values(type).reset_index(drop = True)
    return [df1, df2]

# reduce dataframe to a number of rows such that they cover at least given percentage.
def keepOnlyImportant(df, perc):
    df_temp = df.copy()
    totCount = df_temp['conteggio'].sum()
    threshold = totCount * perc
    df_temp = df_temp.sort_values(['conteggio'], ascending = False)
    i = 0
    sum = 0
    if df_temp['conteggio'].items() == None:
        return df
    while (i < 15 or sum < threshold) and i < len(list(df_temp['conteggio'].items())):
        sum = sum + list(df_temp['conteggio'].items())[i][1]
        i = i + 1
    while i < len(list(df_temp['conteggio'].items())):
        index = list(df_temp['conteggio'].items())[i][0]
        df = df.drop(index)
        i = i + 1
    df.reset_index(drop = True)
    return df

# return dataframe rows where given tag is contained in given types.
def getTypesDataFrame(df, tag, types):
    if types == None or len(types) == 0:
        return df
    return df[df[tag].isin(types)]

# return dataframe rows where given tag is contained in given types from string.
def getTypesDataFrameFromString(df, tag, type):
    if type == None:
        return df
    return df[df[tag].str.contains(type)]

# return dataframe rows where date month is contained given months.
def getMonthDataFrame(df, months):
    if months == None or len(months) == 0:
        return df
    df_temp = df.copy()
    df_temp['data'] = df_temp['data'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').month)
    return df[df_temp['data'].isin(months)]

# return dataframe rows where date year is contained given years.
def getYearDataFrame(df, years):
    if years == None or len(years) == 0:
        return df
    df_temp = df.copy()
    df_temp['data'] = df_temp['data'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
    return df[df_temp['data'].isin(years)]

# return dataframe rows where date is between given stratDate and endDate.
def getDateDataFrame(df, type, startDate, endDate):
    if startDate == None or endDate == None:
        return df
    d = df[df[type] >= startDate]
    d = d[d[type] <= endDate]
    return d

# return unique years in given dataframe dates.
def getAllYears(df):
    df_temp = df['data'].copy()
    df_temp = df_temp.map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year).sort_values()
    years = df_temp.unique()
    return years

# return group by types with corrispondent counts.
def getGroupBy(df, tag):
    df_temp = df.copy()
    types = df_temp.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = 'count')[tag].tolist()
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

def getUniques(df, tag):
    df_temp = df[tag].copy()
    uniques = df_temp.unique()
    return uniques
