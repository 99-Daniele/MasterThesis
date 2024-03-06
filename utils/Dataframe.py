import pandas as pd

import utils.Legenda as legenda

def createEventsDataFrame(events):
    pIds = []
    dates = []
    phases = []
    tags = []
    eIds = []
    finishedEventProcesses = []
    for e in events:
            if e[2] != '5' or e[0] not in finishedEventProcesses:
                pIds.append(e[0])
                dates.append(e[1])
                phases.append(e[2])
                tags.append(e[3])
                eIds.append(e[4])
                if e[2] == '5':
                    finishedEventProcesses.append(e[0])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases, "evento": tags, "numEvento": eIds})

def createProcessesDurationDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    sequences = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(p[5])
        changes.append(p[6])
        sequences.append(p[8])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "sequenza": sequences})

def createStatesDurationsDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    tags = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(p[5])
        changes.append(p[6])
        tags.append(p[8])
        phases.append(p[10])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "etichetta": tags, "fase": phases})

def createPhasesDurationsDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(p[5])
        changes.append(p[6])
        phases.append(p[8])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "fase": phases})

def createEventsDurationsDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    events = []
    phases = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(p[5])
        changes.append(p[6])
        events.append(p[9])
        phases.append(p[11])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes, "evento": events, "fase": phases})

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
            df1['data'] = df1['data'].map(lambda x: legenda.getWeekNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).median()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: legenda.weeks[x - 1])
            df2['data'] = df2['data'].map(lambda x: legenda.weeks[x - 1])
            return [df1, df2]
        case "M":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: x.month)
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).median()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: legenda.months[x - 1])
            df2['data'] = df2['data'].map(lambda x: legenda.months[x - 1])
            return [df1, df2]
        case "MY":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].dt.to_period("M")
            df1['data'] = df1['data'].map(lambda x: legenda.getMonthYearDate(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).median()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            return [df1, df2]
        
def getAvgStdDataFrameByState(df):
    df1 = df[['etichetta', 'durata', 'fase']].copy()
    df2 = df1.groupby(['etichetta', 'fase'], as_index = False).median()
    df2['conteggio'] = df1.groupby(['etichetta', 'fase']).size().tolist()
    df2['quantile'] = df1.groupby(['etichetta', 'fase'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['fase', 'etichetta']).reset_index(drop = True)
    df2 = df2.sort_values(['fase', 'etichetta']).reset_index(drop = True)
    return [df1, df2]

def getAvgStdDataFrameByPhase(df):
    df1 = df[['fase', 'durata']].copy()
    df2 = df1.groupby(['fase'], as_index = False).median()
    df2['conteggio'] = df1.groupby(['fase']).size().tolist()
    df2['quantile'] = df1.groupby(['fase'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['fase']).reset_index(drop = True)
    df2 = df2.sort_values(['fase']).reset_index(drop = True)
    return [df1, df2]

def getAvgStdDataFrameByEvent(df):
    df1 = df[['evento', 'durata']].copy()
    df2 = df1.groupby(['evento'], as_index = False).median()
    df2['conteggio'] = df1.groupby(['evento']).size().tolist()
    df2['quantile'] = df1.groupby(['evento'], as_index = False).quantile(0.75)['durata']
    df1 = df1.sort_values(['evento']).reset_index(drop = True)
    df2 = df2.sort_values(['evento']).reset_index(drop = True)
    return [df1, df2]

def getAvgDataFrameByType(df, datetype, type):
    df3 = df.groupby([type], as_index = False).size()
    df3 = df3.sort_values(['size'], ascending = False).reset_index(drop = True)
    df3.drop(df3[df3[type] == 'null'].index, inplace = True)
    df3 = df3.head(50)
    order_dict = df3.set_index(type)['size'].to_dict()
    order_list = df3[type].tolist()
    df_temp = df[['data', 'durata', type]].copy()
    df_temp = df_temp[df_temp[type].isin(order_list)]
    match datetype:
        case "W":
            df_temp['data'] = df_temp['data'].map(lambda x: legenda.getWeekNumber(x))
            df1 = df_temp.groupby(['data', type], as_index = False).mean()
            df1['sort_column'] = df1[type].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: legenda.weeks[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: legenda.weeks[x - 1])
            return [df1, df2, df3]
        case "M":
            df_temp['data'] = df_temp['data'].map(lambda x: x.month)
            df1 = df_temp.groupby(['data', type], as_index = False).mean()
            df1['sort_column'] = df1[type].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: legenda.months[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: legenda.months[x - 1])
            return [df1, df2, df3]
        case "MY":
            df_temp['data'] = df_temp['data'].map(lambda x: legenda.getMonthYearDate(x))
            df1 = df_temp.groupby(['data', type], as_index = False).mean()
            df1['sort_column'] = df1[type].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            return [df1, df2, df3]
        
def getAvgDataFrameBySubject(df, type):
    df3 = df.groupby(['materia'], as_index = False).size()
    df3 = df3.sort_values(['size'], ascending = False).reset_index(drop = True)
    df3 = df3.head(15)
    order_dict = df3.set_index('materia')['size'].to_dict()
    order_list = df3['materia'].tolist()
    df_temp = df[['data', 'durata', 'materia']].copy()
    df_temp = df_temp[df_temp['materia'].isin(order_list)]
    match type:
        case "W":
            df_temp['data'] = df_temp['data'].map(lambda x: legenda.getWeekNumber(x))
            df1 = df_temp.groupby(['data', 'materia'], as_index = False).mean()
            df1['sort_column'] = df1['materia'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: legenda.weeks[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: legenda.weeks[x - 1])
            return [df1, df2, df3]
        case "M":
            df_temp['data'] = df_temp['data'].map(lambda x: x.month)
            df1 = df_temp.groupby(['data', 'materia'], as_index = False).mean()
            df1['sort_column'] = df1['materia'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df1['data'] = df1['data'].map(lambda x: legenda.months[x - 1])
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            df2['data'] = df2['data'].map(lambda x: legenda.months[x - 1])
            return [df1, df2, df3]
        case "MY":
            df_temp['data'] = df_temp['data'].map(lambda x: legenda.getMonthYearDate(x))
            df1 = df_temp.groupby(['data', 'materia'], as_index = False).mean()
            df1['sort_column'] = df1['materia'].map(order_dict)
            df1 = df1.sort_values(['sort_column', 'data'], ascending = [False, True]).drop(columns = 'sort_column').reset_index(drop = True)
            df2 = df_temp.groupby(['data'], as_index = False)['durata'].mean()
            df2 = df2.sort_values(['data']).reset_index(drop = True)
            return [df1, df2, df3]

def getFinishedDataFrame(df, finished):
    if finished == None or len(finished) == 0:
        return df
    finished = [(lambda x: legenda.finishedNumber(x))(x) for x in finished]
    return df[df['finito'].isin(finished)]

def getYearDataFrame(df, years):
    if years == None or len(years) == 0:
        return df
    return df[df['data'].dt.year.isin(years)]

def getSequenceDataFrame(df, sequence):
    df_temp = df
    if sequence == None:
        return df
    return df_temp[df_temp['sequenza'] == sequence]

def getChangeJudgeDataFrame(df, change):
    if change == None:
        return df
    if change == "SI":
        change = 1
    else:
        change = 0
    return df[df['cambio'] == change]

def getStateDataFrame(df, state):
    if state == None:
        return df
    return df[df['etichetta'] == state]

def getPhaseDataFrame(df, phase):
    if phase == None:
        return df
    return df[df['fase'] == phase]

def getEventDataFrame(df, event):
    if event == None:
        return df
    return df[df['evento'] == event]

def getEventsDataFrame(df, events):
    if (events == None or len(events) == 0):
        return df
    return df[df['evento'].isin(events)]

def getDateDataFrame(df, startDate, endDate):
    if startDate == None or endDate == None:
        return df
    d = df[df['data'] >= startDate]
    d = d[d['data'] <= endDate]
    return d

def getAllYears(df):
    df_temp = df['data']
    df_temp = df_temp.map(lambda x: x.year).sort_values()
    years = df_temp.unique()
    return years

def getAllStates(df):
    df_temp = df['etichetta']
    states = df_temp.unique()
    return states

def getAllSequences(df):
    df_temp = df
    sequences = df_temp.groupby(['sequenza'])['sequenza'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)['sequenza']
    return sequences

def getAllPhases(df):
    df_temp = df['fase']
    phases = df_temp.unique()
    return phases

def getAllEvents(df):
    df_temp = df['evento']
    events = df_temp.unique()
    return events

def getTop10Judges(df):
    df_temp = df
    judges = df_temp.groupby(['giudice'])['giudice'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return judges

def getTop10Subjects(df):
    df_temp = df
    subjects = df_temp.groupby(['materia'])['materia'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return subjects
