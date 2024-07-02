# this file handles events graph management.

import dash as ds
import numpy as np
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Utilities as utilities

# update data based on user choices on different parameters.
def updateDataframe(df, startDate, endDate, sections, subjects, judges):
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    processDateTag = utilities.getTagName('processDateTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    # modify dataframe based on user chosen filters.
    newDF = df.copy()
    newDF = frame.getDateDataFrame(newDF, processDateTag, startDate, endDate)
    newDF = frame.getTypesDataFrame(newDF, sectionTag, sections)
    newDF = frame.getTypesDataFrame(newDF, subjectTag, subjects)
    newDF = frame.getTypesDataFrame(newDF, codeJudgeTag, judges)
    return newDF

# update types based on user choices on different parameters. In order to do that is used 'updateDataframe' method with chosen parameter as None. 
# this is done because when user select a parameter, analysed dataframe is filtered to only processes where chosen parameters holds.
# by doing that other chooseable parameters would disappear since they are calculated from input datafram which contains only processes with selected ones.
# so it calculates paramers like if no one was chosen and it set them in dropdown.
def updateTypesBySelection(df, df_data, startDate, endDate, sections, subjects, judges):
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    newDF = df.copy()
    # for each parameter evaluate if is not None, which is when user makes a selection,
    # and in case modify to a new df using updateProcessData() with correlated parameter as None.
    if sections != None and len(sections) > 0:
        newDF_1 = updateDataframe(newDF, startDate, endDate, None, subjects, judges)
    else:
        newDF_1 = df_data
    if subjects != None and len(subjects) > 0:
        newDF_2 = updateDataframe(newDF, startDate, endDate, sections, None, judges)
    else:
        newDF_2 = df_data
    if judges != None and len(judges) > 0:
        newDF_3 = updateDataframe(newDF, startDate, endDate, sections, subjects, None)
    else:
        newDF_3 = df_data
    sections = frame.getGroupBy(newDF_1, sectionTag)
    subjects = frame.getGroupBy(newDF_2, subjectTag)
    judges = frame.getGroupBy(newDF_3, codeJudgeTag)
    return [sections, subjects, judges]

# return all needed parameters in order to change graph after any user choice.
#
# input data are: df is the dataframe, startDate is the chosen start date of analyzed time interval, endDate is the chosen end date of analyzed time interval, 
# minDate is the minimum start date, maxDate is the maximum end date, symbol is True if scatter plot is both color and sybol, type refers to what type graph is shown (event, state or phase), 
# sections are the sections chosen by user to filter data, subjects are the subjects chosen by user to filter data, judges are the judges chosen by user to filter data.
#
# return data are: fig is the figure shown, startDate is the new startDate if reset was clicked, endDate is the new endDate is reset was clicked, sections are the new updated chooseable sections, 
# subjects are the new updated chooseable subjects, judges are the new updated chooseable judges.
def eventUpdate(df, startDate, endDate, symbol, type, minDate, maxDate, sections, subjects, judges):
    # if reset button is clicked time interval is set to default.
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    dateTag = utilities.getTagName('dateTag')
    eventTag = utilities.getTagName('eventTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseTag = utilities.getTagName('phaseTag') 
    statesInfo = getter.getStatesInfo()
    newDF = df.copy()
    # newDF is calculated as df filtered based on user choices.
    newDF = updateDataframe(newDF, startDate, endDate, sections, subjects, judges)
    newDF = newDF.sort_values(by = phaseTag).reset_index(drop = True)
    # parameters remaining choices are calculated based on user choices.
    [sections, subjects, judges] = updateTypesBySelection(df, newDF, startDate, endDate, sections, subjects, judges)
    # phaseColorMap maps to each phase the correlated color.
    colorMap = frame.phaseColorMap(type, statesInfo)
    # symbol = True when scatter plot needs both color and symbol. Is the case of allEvents graph.
    if symbol:
        symbols = list(frame.getUniques(newDF, eventTag))
        fig = px.scatter(newDF, x = dateTag, y = numProcessTag, color = type, symbol = eventTag, color_discrete_map = colorMap, labels = {numProcessTag:'Process ID', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95))   
        for i, trace in enumerate(fig.data):
            name = trace.name.split(', ')
            trace['name'] = name[1]
            trace['legendgroup'] = symbols.index(name[1])
        names = set()
        fig.for_each_trace(
            lambda trace:
                trace.update(showlegend = False)
                if (trace.name in names) else names.add(trace.name))
    else:
        fig = px.scatter(newDF, x = dateTag, y = numProcessTag, color = type, color_discrete_map = colorMap, labels = {numProcessTag:'Process ID', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95))   
    fig.update_layout(
        font = dict(size = 18),
        legend = dict(
            yanchor = "top",
            y = 0.99,
        ),
        xaxis = dict(
        ),
        yaxis = dict(
            showticklabels = False,
        )
    )
    fig.update_xaxes(
        dtick = "M1",
        tickformat = "%b\n%Y",
        ticklabelmode = "period"
    ) 
    return fig, startDate, endDate, sections, subjects, judges
