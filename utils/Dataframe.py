import pandas as pd

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

def createProcessesDataFrame(processes):
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

def getAvgStdDataframe(df, type):
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

def getFinishedDataframe(df, finished):
    dft = df.copy()
    if finished == None or len(finished) == 0:
        return dft
    finished = [(lambda x: lg.finishedNumber(x))(x) for x in finished]
    return dft[dft['finito'].isin(finished)]

def getYearDataframe(df, years):
    dft = df.copy()
    if years == None or len(years) == 0:
        return dft
    return dft[dft['data'].dt.year.isin(years)]

def updateDataframe(df, ju_drop, su_drop, se_drop):
    if ju_drop is None:
        if su_drop is None:
            if se_drop is None:
                return df
            else:
                return df[df['sezione'] == se_drop]
        else:
            if se_drop is None:
                return df[df['materia'] == su_drop]
            else:
                return df[(df['materia'] == su_drop) & (df['sezione'] == se_drop)]
    else:
        if su_drop is None:
            if se_drop is None:
                return df[df['giudice'] == ju_drop]
            else:
                return df[(df['giudice'] == ju_drop) & (df['sezione'] == se_drop)]
        else:
            if se_drop is None:
                return df[(df['giudice'] == ju_drop) & (df['materia'] == su_drop)]
            else:
                return df[(df['giudice'] == ju_drop) & (df['materia'] == su_drop) & (df['sezione'] == se_drop)]