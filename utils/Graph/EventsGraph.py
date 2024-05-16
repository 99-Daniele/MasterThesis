# this file handles events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities.Utilities as utilities

# update types based on current dataframe.
def updateTypes(df, sectionTag, subjectTag, judgeTag, countTag):
    df_temp = df.copy()
    sections = frame.getGroupBy(df_temp, sectionTag, countTag)
    subjects = frame.getGroupBy(df_temp, subjectTag, countTag)
    judges = frame.getGroupBy(df_temp, judgeTag, countTag)
    return [sections, subjects, judges]

# update types based on user selections.
def updateTypesBySelection(df, processDateTag, sectionTag, subjectTag, judgeTag, startDate, endDate, sections, subjects, judges):
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, processDateTag, startDate, endDate)
    if sections != None and len(sections) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    if subjects != None and len(subjects) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    if judges != None and len(judges) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, judgeTag, judges)
    return df_temp

# return all needed parameters in order to change graph after any user choice.
def eventUpdate(df, startDate, endDate, type, mustEvents, minDate, maxDate, sections, subjects, judges):
    df_temp = df.copy()
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    dateTag = df.columns[0]
    numProcessTag = df.columns[1]
    processDateTag = df.columns[5]
    sectionTag = df.columns[8]
    subjectTag = df.columns[9]
    judgeTag = df.columns[7]
    countTag = 'conteggio'
    df_temp = updateTypesBySelection(df_temp, processDateTag, sectionTag, subjectTag, judgeTag, startDate, endDate, sections, subjects, judges)
    [sections, subjects, judges] = updateTypes(df_temp, sectionTag, subjectTag, judgeTag, countTag)
    fig = px.scatter(df_temp, x = dateTag, y = numProcessTag, color = type, color_discrete_sequence = utilities.phaseColorList(df_temp, type), labels = {numProcessTag:'Codice Processo', dateTag:'Data inizio processo'}, width = utilities.getWidth(1))
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99
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
    if mustEvents != None:
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name not in mustEvents else False))
    return fig, startDate, endDate, sections, subjects, judges
