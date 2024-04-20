import dash as ds
import plotly.express as px

import utils.Dataframe as frame

def updateDuration(df, sequences, phases, finished, year, change):
    df_temp = df
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    if not (phases == None or len(phases) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phases)
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    if not (year == None or len(year) == 0):
        df_temp = frame.getYearDataFrame(df_temp, year)
    if not (change == None or len(change) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    return df_temp

def durationProcessUpdate(df, dateType, date, finished, year, sequence, phase, change):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    df_temp = updateDuration(df_temp, sequence, phase, finished, year, change)
    sequences = frame.getGroupBy(df, 'sequenza')
    phases = frame.getGroupBy(df, 'fasi')
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600, points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date, sequences, phases

def durationCourtHearingsUpdate(df, dateType, date, finished, year, change):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    df_temp = updateDuration(df_temp, None, None, finished, year, change)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':"Durata dell' udienza [giorni]", 'data':'Data inizio udienza'}, width = 1400, height = 600, points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date
