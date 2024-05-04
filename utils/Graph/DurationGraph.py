# this file handles duration graph management.

import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities.Utilities as utilities

# update dataframe based on user choice.
def updateDuration(df, finished, years, sequences, phases, changes):
    df_temp = df.copy()
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    if not (phases == None or len(phases) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phases)
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    if not (years == None or len(years) == 0):
        df_temp = frame.getYearDataFrame(df_temp, years)
    if not (changes == None or len(changes) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'cambio', changes)
    return df_temp

# update types based on user choice. This method is for processes duration graph.
def updateTypesProcess(df_temp, finished, years, sequences, phases, changes):
    df_temp_1 = updateDuration(df_temp, None, years, sequences, phases, changes)
    new_finished = frame.getGroupBy(df_temp_1, 'finito')
    df_temp_2 = updateDuration(df_temp, finished, None, sequences, phases, changes)
    new_years = frame.getAllYears(df_temp_2)
    df_temp_3 = updateDuration(df_temp, finished, years, None, phases, changes)
    new_sequences = frame.getGroupBy(df_temp_3, 'sequenza')
    df_temp_4 = updateDuration(df_temp, finished, years, sequences, None, changes)
    new_phases = frame.getGroupBy(df_temp_4, 'fasi')
    df_temp_5 = updateDuration(df_temp, finished, years, sequences, phases, None)
    new_changes = frame.getGroupBy(df_temp_5, 'cambio')
    df_temp = updateDuration(df_temp, finished, years, sequences, phases, changes)
    return [df_temp, new_finished, new_years, new_sequences, new_phases, new_changes]

# update types based on user choice. This method is for court hearings duration graph.
def updateTypesCourtHearings(df_temp, finished, years, changes):
    df_temp_1 = updateDuration(df_temp, None, years, None, None, changes)
    new_finished = frame.getGroupBy(df_temp_1, 'finito')
    df_temp_2 = updateDuration(df_temp, finished, None, None, None, changes)
    new_years = frame.getAllYears(df_temp_2)
    df_temp_3 = updateDuration(df_temp, finished, years, None, None, None)
    new_changes = frame.getGroupBy(df_temp_3, 'cambio')
    df_temp = updateDuration(df_temp, finished, years, None, None, changes)
    return [df_temp, new_finished, new_years, new_changes]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process duration graph.
def durationProcessUpdate(df, dateType, date, finished, years, sequences, phases, changes):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    [df_temp, finished, years, sequences, phases, changes] = updateTypesProcess(df_temp, finished, years, sequences, phases, changes)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date, finished, years, sequences, phases, changes

# return all needed parameters in order to change graph after any user choice.
# this method is only for court hearings duration graph.
def durationCourtHearingsUpdate(df, dateType, date, finished, years, changes):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    [df_temp, finished, years, changes] = updateTypesCourtHearings(df_temp, finished, years, changes)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':"Durata dell' udienza [giorni]", 'data':'Data inizio udienza'}, width = 1400, height = 600, points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date, finished, years, changes
