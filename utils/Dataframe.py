import pandas as pd
import utils.Legenda as lg

def createEventsDataFrame(events):
    pIds = []
    dates = []
    phases = []
    tags = []
    for e in events:
            pIds.append(e[0])
            dates.append(e[1])
            phases.append(e[2])
            tags.append(e[3])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases, "etichetta": tags})

def createProcessesDurationDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    finished = []
    changes = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        subjects.append(p[3])
        sections.append(p[4])
        finished.append(p[5])
        changes.append(p[6])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges,  "materia": subjects, "sezione": sections, "finito": finished, "cambio": changes})

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

def getAvgStdDataFrameByDate(df, type):
    match type:
        case "W":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: lg.getWeekNumber(x))
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).median()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: lg.weeks[x - 1])
            df2['data'] = df2['data'].map(lambda x: lg.weeks[x - 1])
            return [df1, df2]
        case "M":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].map(lambda x: x.month)
            df1 = df1.sort_values(['data'])
            df2 = df1.groupby(['data'], as_index = False).median()
            df2['conteggio'] = df1.groupby(['data']).size().tolist()
            df2['quantile'] = df1.groupby(['data'], as_index = False).quantile(0.75)['durata']
            df1['data'] = df1['data'].map(lambda x: lg.months[x - 1])
            df2['data'] = df2['data'].map(lambda x: lg.months[x - 1])
            return [df1, df2]
        case "MY":
            df1 = df[['data', 'durata']].copy()
            df1['data'] = df1['data'].dt.to_period("M")
            df1['data'] = df1['data'].map(lambda x: lg.getMonthYearDate(x))
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

def getFinishedDataFrame(df, finished):
    df_temp = df.copy()
    if finished == None or len(finished) == 0:
        return df
    finished = [(lambda x: lg.finishedNumber(x))(x) for x in finished]
    return df_temp[df_temp['finito'].isin(finished)]

def getStatesDataFrame(df, states):
    df_temp = df.copy()
    if states == None or len(states) == 0:
        return df
    return df_temp[df_temp['etichetta'].isin(states)]

def getYearDataFrame(df, years):
    df_temp = df.copy()
    if years == None or len(years) == 0:
        return df
    return df_temp[df_temp['data'].dt.year.isin(years)]

def getChangeJudgeDataFrame(df, change):
    df_temp = df.copy()
    if change == None:
        return df
    if change == "SI":
        change = 1
    else:
        change = 0
    return df_temp[df_temp['cambio'] == change]

def updateDataFrame(df, judges, subjects, sections):
    df_temp = df.copy()
    if judges is None:
        if subjects is None:
            if sections is None:
                return df
            else:
                return df_temp[df_temp['sezione'] == sections]
        else:
            if sections is None:
                return df_temp[df_temp['materia'] == subjects]
            else:
                return df_temp[(df_temp['materia'] == subjects) & (df_temp['sezione'] == sections)]
    else:
        if subjects is None:
            if sections is None:
                return df_temp[df_temp['giudice'] == judges]
            else:
                return df_temp[(df_temp['giudice'] == judges) & (df_temp['sezione'] == sections)]
        else:
            if sections is None:
                return df_temp[(df_temp['giudice'] == judges) & (df_temp['materia'] == subjects)]
            else:
                return df_temp[(df_temp['giudice'] == judges) & (df_temp['materia'] == subjects) & (df['sezione'] == sections)]
            
def getAllYears(df):
    df_temp = df['data'].copy()
    df_temp = df_temp.map(lambda x: x.year).sort_values()
    years = df_temp.unique()
    return years

def getAllStates(df):
    df_temp = df['etichetta'].copy()
    states = df_temp.unique()
    return states

def getTop10Judges(df):
    df_temp = df.copy()
    judges = df_temp.groupby(['giudice'])['giudice'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return judges

def getTop10Subjects(df):
    df_temp = df.copy()
    subjects = df_temp.groupby(['materia'])['materia'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return subjects
