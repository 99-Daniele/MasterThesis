# this file handles duration graph management.

import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities.Utilities as utilities

# update dataframe based on user choice.
def updateDuration(df, finished, years, sequences, phases):
    df_temp = df.copy()
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    if not (phases == None or len(phases) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phases)
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    if not (years == None or len(years) == 0):
        df_temp = frame.getYearDataFrame(df_temp, years)
    return df_temp

# update types based on user choice. This method is for processes duration graph.
def updateTypesProcess(df_temp, finished, years, sequences, phases):
    df_temp_1 = updateDuration(df_temp, None, years, sequences, phases)
    new_finished = frame.getGroupBy(df_temp_1, 'finito')
    df_temp_2 = updateDuration(df_temp, finished, None, sequences, phases)
    new_years = frame.getAllYears(df_temp_2)
    df_temp_3 = updateDuration(df_temp, finished, years, None, phases)
    new_sequences = frame.getGroupBy(df_temp_3, 'sequenza')
    df_temp_4 = updateDuration(df_temp, finished, years, sequences, None)
    new_phases = frame.getGroupBy(df_temp_4, 'fasi')
    df_temp = updateDuration(df_temp, finished, years, sequences, phases)
    return [df_temp, new_finished, new_years, new_sequences, new_phases]

# update types based on user choice. This method is for court hearings duration graph.
def updateTypesCourtHearings(df_temp, finished, years):
    df_temp_1 = updateDuration(df_temp, None, years, None, None)
    new_finished = frame.getGroupBy(df_temp_1, 'finito')
    df_temp_2 = updateDuration(df_temp, finished, None, None, None)
    new_years = frame.getAllYears(df_temp_2)
    df_temp = updateDuration(df_temp, finished, years, None, None)
    return [df_temp, new_finished, new_years]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process duration graph.
def durationProcessUpdate(df, dateType, date, finished, years, sequences, phases):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    [df_temp, finished, years, sequences, phases] = updateTypesProcess(df_temp, finished, years, sequences, phases)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    xticks = frame.getUniques(avgData, 'data')
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(xaxis_tickvals = xticks)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return fig, dateType, date, finished, years, sequences, phases

# return all needed parameters in order to change graph after any user choice.
# this method is only for court hearings duration graph.
def durationCourtHearingsUpdate(df, dateType, date, finished, years):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    [df_temp, finished, years] = updateTypesCourtHearings(df_temp, finished, years)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date)
    xticks = frame.getUniques(avgData, 'data')
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':"Durata dell' udienza [giorni]", 'data':'Data inizio udienza'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(xaxis_tickvals = xticks)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return fig, dateType, date, finished, years
