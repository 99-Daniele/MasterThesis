import pandas as pd

import utils.Utilities as utilities

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
    changes = []
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
            finished.append(utilities.processState[e[11]])
            if e[12] == 1:
                changes.append("SI")
            else:
                changes.append("NO")
            startProcessDates.append(e[13])
            if e[2] == '5':
                finishedEventProcesses.append(e[0])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases, "evento": tagEvents, "numEvento": eIds, "dataInizioProcesso": startProcessDates})

def createProcessesDurationDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    pIds = []
    sequences = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(utilities.processState[p[5]])
        if p[6] == 1:
            changes.append("SI")
        else:
            changes.append("NO")
        pIds.append(p[7])
        sequences.append(p[8])
        phases.append(p[9])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "sequenza": sequences, "fasi": phases})

def createStatesDurationsDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    pIds = []
    tags = []
    states = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(utilities.processState[p[5]])
        if p[6] == 1:
            changes.append("SI")
        else:
            changes.append("NO")
        pIds.append(p[7])
        tags.append(p[8])
        states.append(p[9])
        phases.append(p[10])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "etichetta": tags, "fase": phases})

def createPhasesDurationsDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    pIds = []
    phases = []
    orders = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(utilities.processState[p[5]])
        if p[6] == 1:
            changes.append("SI")
        else:
            changes.append("NO")
        pIds.append(p[7])
        phases.append(p[8])
        orders.append(p [9])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "fase": phases})

def createEventsDurationsDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    eIds = []
    pIds = []
    tagEvents = []
    typeEvents = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(utilities.processState[p[5]])
        if p[6] == 1:
            changes.append("SI")
        else:
            changes.append("NO")
        eIds.append(p[7])
        pIds.append(p[8])
        tagEvents.append(p[9])
        typeEvents.append(p[10])
        phases.append(p[11])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "evento": tagEvents, "fase": phases})

def createCourtHearingsDurationDataFrame(processes):
    dates = []
    durations = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    pIds = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(utilities.processState[p[5]])
        if p[6] == 1:
            changes.append("SI")
        else:
            changes.append("NO")
        pIds.append(p[7])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes})

def getEventType(df, type, importantEventsType, courtHearingEventsType):
    match type:
        case "ALL":
            return df
        case "IMP":
            df = df[df['evento'].isin(importantEventsType)]
            return df
        case "CH":
            df = df[df['evento'].isin(courtHearingEventsType)]
            return df

def getAvgStdDataFrameByDate(df, type):
    match type:
        case "W":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: utilities.getWeekNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.weeks[x - 1])
            df2['data'] = df2['data'].map(lambda x: utilities.weeks[x - 1])
            return [df1, df2]
        case "M":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: x.month)
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: utilities.months[x - 1])
            df2['data'] = df2['data'].map(lambda x: utilities.months[x - 1])
            return [df1, df2]
        case "MY":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].dt.to_period("M")
            df1['data'] = df1['data'].map(lambda x: utilities.getMonthYearDate(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).mean()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            return [df1, df2]
        
def getAvgStdDataFrameByState(df):
    df1 = df[['etichetta', 'durata', 'fase']].copy()
    df2 = df1.groupby(['etichetta', 'fase'], as_index = False).mean()
    df2['conteggio'] = df1.groupby(['etichetta', 'fase']).size().tolist()
    df2['quantile'] = df1.groupby(['etichetta', 'fase'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['fase', 'etichetta']).reset_index(drop = True)
    df2 = df2.sort_values(['fase', 'etichetta']).reset_index(drop = True)
    return [df1, df2]

def getAvgStdDataFrameByPhase(df):
    df1 = df[['fase', 'durata']].copy()
    df2 = df1.groupby(['fase'], as_index = False).mean()
    df2['conteggio'] = df1.groupby(['fase']).size().tolist()
    df2['quantile'] = df1.groupby(['fase'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['fase']).reset_index(drop = True)
    df2 = df2.sort_values(['fase']).reset_index(drop = True)
    return [df1, df2]

def getAvgStdDataFrameByEvent(df):
    df1 = df[['evento', 'durata']].copy()
    df2 = df1.groupby(['evento'], as_index = False).mean()
    df2['conteggio'] = df1.groupby(['evento']).size().tolist()
    df2['quantile'] = df1.groupby(['evento'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['evento']).reset_index(drop = True)
    df2 = df2.sort_values(['evento']).reset_index(drop = True)
    return [df1, df2]

def keepOnlyImportant(df, perc):
    df_temp = df.copy()
    totCount = df_temp['conteggio'].sum()
    threshold = totCount * perc
    df_temp = df_temp.sort_values(['conteggio'], ascending = False)
    i = 0
    sum = 0
    while (i < 20 or sum < threshold) and i < len(list(df_temp['conteggio'].items())):
        sum = sum + list(df_temp['conteggio'].items())[i][1]
        i = i + 1
    while i < len(list(df_temp['conteggio'].items())):
        index = list(df_temp['conteggio'].items())[i][0]
        df = df.drop(index)
        i = i + 1
    df.reset_index(drop = True)
    return df

def getAvgDataFrameByType(df, datetype, types, order):
    df4 = df.groupby(types) \
       .agg({'giudice':'size', 'durata':'mean'}) \
       .rename(columns = {'giudice':'conteggio','durata':'media'}) \
       .reset_index()
    for t in types: 
        df4.drop(df4[df4[t] == 'null'].index, inplace = True)
    df3 = df4[[types[0], 'conteggio', 'media']].copy()
    df3 = df3.rename(columns = {types[0]:'filtro'})
    i = 1
    while i < len(types):
        df3['filtro'] = df3['filtro'] + " - " + df4[types[i]]
        i = i + 1
    df3 = keepOnlyImportant(df3, 0.85)
    df3 = df3.sort_values([order], ascending = False).reset_index(drop = True)
    order_dict = df3.set_index('filtro')[order].to_dict()
    order_list = df3['filtro'].tolist()
    df_temp = df[['data', 'durata', types[0]]].copy()
    df_temp = df_temp.rename(columns = {types[0]:'filtro'})
    i = 1
    while i < len(types):
        df_temp['filtro'] = df_temp['filtro'] + " - " + df[types[i]]
        i = i + 1
    df_temp = df_temp[df_temp['filtro'].isin(order_list)]
    match datetype:
        case "W":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getWeekNumber(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: utilities.weeks[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: utilities.weeks[x - 1])
            return [df1, df2, df3]
        case "M":
            df_temp['data'] = df_temp['data'].map(lambda x: x.month)
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: utilities.months[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: utilities.months[x - 1])
            return [df1, df2, df3]
        case "MY":
            df_temp['data'] = df_temp['data'].map(lambda x: utilities.getMonthYearDate(x))
            df1 = df_temp.groupby(['data', 'filtro'], as_index = False).mean()
            df1['sort_column'] = df1['filtro'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            return [df1, df2, df3]
        
def getTypesDataFrame(df, tag, types):
    if types == None or len(types) == 0:
        return df
    return df[df[tag].isin(types)]

def getTypeDataFrame(df, tag, type):
    if type == None:
        return df
    return df[df[tag] == type]

def getYearDataFrame(df, years):
    if years == None or len(years) == 0:
        return df
    return df[df['data'].dt.year.isin(years)]

def getDateDataFrame(df, startDate, endDate):
    if startDate == None or endDate == None:
        return df
    d = df[df['dataInizioProcesso'] >= startDate]
    d = d[d['dataInizioProcesso'] <= endDate]
    return d

def getAllYears(df):
    df_temp = df['data']
    df_temp = df_temp.map(lambda x: x.year).sort_values()
    years = df_temp.unique()
    return years

def getUniques(df, tag):
    df_temp = df[tag]
    types = df_temp.unique()
    return types

def getGroupBy(df, tag):
    df_temp = df
    types = df_temp.groupby([tag])[tag].size().sort_values(ascending = False).reset_index(name = 'count')[tag]
    return types
