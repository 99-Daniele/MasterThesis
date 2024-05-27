# this file handles events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.utilities.Utilities as utilities

# update types based on current dataframe.
def updateTypesBySelection(df, startDate, endDate, sections, subjects, judges):
    judgeTag = utilities.getTagName('judgeTag')
    processDateTag = utilities.getTagName('processDateTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, processDateTag, startDate, endDate)
    df_temp_1 = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp_1 = frame.getTypesDataFrame(df_temp_1, judgeTag, judges)
    df_temp_2 = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp_2 = frame.getTypesDataFrame(df_temp_2, judgeTag, judges)
    df_temp_3 = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp_3 = frame.getTypesDataFrame(df_temp_3, sectionTag, sections)
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    judges = frame.getGroupBy(df_temp_3, judgeTag)
    return [sections, subjects, judges]

# update types based on user selections.
def updateTypes(df, startDate, endDate, sections, subjects, judges):
    judgeTag = utilities.getTagName('judgeTag')
    processDateTag = utilities.getTagName('processDateTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
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
    dateTag = utilities.getTagName('dateTag')
    phaseTag = utilities.getTagName('phaseTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    df_temp = updateTypes(df_temp, startDate, endDate, sections, subjects, judges)
    [sections, subjects, judges] = updateTypesBySelection(df, startDate, endDate, sections, subjects, judges)
    df_phase = df_temp.groupby(type, as_index = False)[phaseTag].max()
    df_phase = df_phase.sort_values(by = [phaseTag, type])
    order_dict = df_phase.set_index(type).to_dict()[phaseTag]
    df_temp['sort_column'] = df_temp[type].map(order_dict)
    df_temp = df_temp.sort_values(['sort_column'], ascending = [False]).drop(columns = 'sort_column').reset_index(drop = True)
    fig = px.scatter(df_temp, x = dateTag, y = numProcessTag, color = type, color_discrete_sequence = utilities.phaseColorList(df_phase, type), labels = {numProcessTag:'Codice Processo', dateTag:'Data inizio processo'}, width = utilities.getWidth(1))
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
