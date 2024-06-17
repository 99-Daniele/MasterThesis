# this file handles events graph management.

import dash as ds
import numpy as np
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Utilities as utilities

# update dataframe based on user selections.
def updateDataframe(df, startDate, endDate, sections, subjects, judges):
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    processDateTag = utilities.getTagName('processDateTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, processDateTag, startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, codeJudgeTag, judges)
    return df_temp

# update types based on current dataframe.
def updateTypesBySelection(df, df_data, startDate, endDate, sections, subjects, judges):
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    df_temp = df.copy()
    if sections != None and len(sections) > 0:
        df_temp_1 = updateDataframe(df_temp, startDate, endDate, None, subjects, judges)
    else:
        df_temp_1 = df_data
    if subjects != None and len(subjects) > 0:
        df_temp_2 = updateDataframe(df_temp, startDate, endDate, sections, None, judges)
    else:
        df_temp_2 = df_data
    if judges != None and len(judges) > 0:
        df_temp_3 = updateDataframe(df_temp, startDate, endDate, sections, subjects, None)
    else:
        df_temp_3 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    judges = frame.getGroupBy(df_temp_3, codeJudgeTag)
    return [sections, subjects, judges]

# return all needed parameters in order to change graph after any user choice.
def eventUpdate(df, startDate, endDate, symbol, type, minDate, maxDate, sections, subjects, judges):
    df_temp = df.copy()
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    dateTag = utilities.getTagName('dateTag')
    codeEventTag = utilities.getTagName('codeEventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseTag = utilities.getTagName('phaseTag') 
    statesInfo = getter.getStatesInfo()
    df_temp = updateDataframe(df_temp, startDate, endDate, sections, subjects, judges)
    df_temp = df_temp.sort_values(by = phaseTag).reset_index(drop = True)
    [sections, subjects, judges] = updateTypesBySelection(df, df_temp, startDate, endDate, sections, subjects, judges)
    colorMap = frame.phaseColorMap(type, statesInfo)
    if symbol:
        symbols = list(frame.getUniques(df_temp, codeEventTag))
        fig = px.scatter(df_temp, x = dateTag, y = numProcessTag, color = type, symbol = codeEventTag, color_discrete_map = colorMap, labels = {numProcessTag:'Process ID', dateTag:'Process Start Date'}, width = utilities.getWidth(1))   
        for i, trace in enumerate(fig.data):
            name = trace.name.split(', ')
            trace['name'] = name[1]
            trace['legendgroup'] = symbols.index(name[1])
        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend=False)
                if (trace.name in names) else names.add(trace.name))
    else:
        fig = px.scatter(df_temp, x = dateTag, y = numProcessTag, color = type, color_discrete_map = colorMap, labels = {numProcessTag:'Process ID', dateTag:'Process Start Date'}, width = utilities.getWidth(1))   
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99,
            font = dict(size = 16)
        ),
        yaxis = dict(
            showticklabels = False
        )
    )
    fig.update_xaxes(
        dtick = "M1",
        tickformat = "%b\n%Y",
        ticklabelmode = "period"
    ) 
    return fig, startDate, endDate, sections, subjects, judges
