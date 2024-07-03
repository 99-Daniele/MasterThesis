# this file handles type events graph management.

import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Utilities as utilities

# update data based on user choices on different parameters.
def updateTypeData(df, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    newDF = df.copy()
    newDF = frame.getTypesDataFrame(newDF, sectionTag, sections)
    newDF = frame.getTypesDataFrame(newDF, subjectTag, subjects)
    newDF = frame.getTypesDataFrame(newDF, codeJudgeTag, judges)
    newDF = frame.getTypesDataFrame(newDF, finishedTag, finished)
    return newDF

# update types based on user choices on different parameters. In order to do that is used 'updateTypeData' method with chosen parameter as None. 
# this is done because when user select a parameter, analysed dataframe is filtered to only processes where chosen parameters holds.
# by doing that other chooseable parameters would disappear since they are calculated from input datafram which contains only processes with selected ones.
# so it calculates paramers like if no one was chosen and it set them in dropdown.
def updateTypeDataBySelection(df, df_data, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    newDF = df.copy()
    if sections != None and len(sections) > 0:
        newDF_1 = updateTypeData(newDF, None, subjects, judges, finished)
    else:
        newDF_1 = df_data
    if subjects != None and len(subjects) > 0:
        newDF_2 = updateTypeData(newDF, sections, None, judges, finished)
    else:
        newDF_2 = df_data
    if judges != None and len(judges) > 0:
        newDF_3 = updateTypeData(newDF, sections, subjects, None, finished)
    else:
        newDF_3 = df_data
    if finished != None and len(finished) > 0:
        newDF_4 = updateTypeData(newDF, sections, subjects, judges, None)
    else:
        newDF_4 = df_data
    sections = frame.getGroupBy(newDF_1, sectionTag)
    subjects = frame.getGroupBy(newDF_2, subjectTag)
    judges = frame.getGroupBy(newDF_3, codeJudgeTag)
    finished = frame.getGroupBy(newDF_4, finishedTag)
    return [sections, subjects, judges, finished]

# update type events based on user choice.
#
# input data are: df is the dataframe, type refers to what type graph is shown (event, state or phase), typeChoices are the types chosen by user to be shown,
# tagChoice is the tag correlated to type, first refers to if user wnats to show first, last or all, avgChoice is the user choice on how aggregate data on median or mean,
# text is chosen by user to decide to show load of processes or not, sections are the sections chosen by user to filter data, subjects are the subjects chosen by user to filter data, 
# judges are the judges chosen by user to filter data, finished are the type of processes chosen by user to filter data.
#
# return data are: fig is the figure shown, sections are the new updated chooseable sections, subjects are the new updated chooseable subjects, 
# judges are the new updated chooseable judges, finished are the new updated chooseable process types.
def typeUpdate(df, type, typeChoices, tagChoice, first, avgChoice, text, sections, subjects, judges, finished):
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    firstTag = utilities.getPlaceholderName("first")
    lastTag = utilities.getPlaceholderName("last")
    numProcessTag = utilities.getTagName('numProcessTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    statesInfo = getter.getStatesInfo()
    newDF = df.copy()
    # if first is selected newDF is filtered by only first events/states.
    if first == firstTag:
        newDF = newDF.groupby([type, numProcessTag]).first().reset_index()
    # if last is selected newDF is filtered by only last events/states.
    elif first == lastTag:
        newDF = newDF.groupby([type, numProcessTag]).last().reset_index()
    newDF = frame.getTypesDataFrame(newDF, type, typeChoices)
    # df_data is calculated as newDF filtered based on user choices.
    df_data = updateTypeData(newDF, sections, subjects, judges, finished)
    # parameters remaining choices are calculated based on user choices.
    [sections, subjects, judges, finished] = updateTypeDataBySelection(newDF, df_data, sections, subjects, judges, finished)
    # allData contains all data with duration and type value.
    # avgData contains for each different type the calculated average duration.
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoiceOrderedByPhase(df_data, tagChoice, avgChoice)   
    xticks = frame.getUniques(allData, tagChoice)
    # if it's an event graph color is unique, otherwise color is decised based on colorMap which associate to each phase a different color.
    if tagChoice == eventTag:
        # if text is selected by user then an histogram graph is shown, otherwise boxplot.
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 12)).data
            )         
    else:
        colorMap = frame.phaseColorMap(tagChoice, statesInfo)
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
    fig.update_layout(xaxis_tickvals = xticks, showlegend = False, font = dict(size = 14))
    fig.update_xaxes(tickangle = 45)
    fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
    return fig, sections, subjects, judges, finished

# update type events based on user choice.
#
# input data are: df is the dataframe, typeChoices are the types chosen by user to be shown, tagChoice is the tag correlated to type, first refers to if user wnats to show first, last or all, 
# avgChoice is the user choice on how aggregate data on median or mean, text is chosen by user to decide to show load of processes or not, sections are the sections chosen by user to filter data, 
# subjects are the subjects chosen by user to filter data, judges are the judges chosen by user to filter data, finished are the type of processes chosen by user to filter data.
#
# return data are: fig is the figure shown, sections are the new updated chooseable sections, subjects are the new updated chooseable subjects, 
# judges are the new updated chooseable judges, finished are the new updated chooseable process types.
def typeSequenceUpdate(df, typeChoices, tagChoice, avgChoice, text, sections, subjects, judges, finished):
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    textTag = utilities.getPlaceholderName("text")
    statesInfo = getter.getStatesInfo()
    newDF = df.copy()
    newDF = frame.selectFollowingRows(newDF, tagChoice, typeChoices)
    df_data = updateTypeData(newDF, sections, subjects, judges, finished) 
    [sections, subjects, judges, finished] = updateTypeDataBySelection(newDF, df_data, sections, subjects, judges, finished)
    # allData contains all data with duration and type value.
    # avgData contains for each different type the calculated average duration.
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoiceOrderedByPhase(df_data, tagChoice, avgChoice)
    xticks = frame.getUniques(allData, tagChoice)
    if tagChoice == eventTag:
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )       
    else:
        colorMap = frame.phaseColorMap(tagChoice, statesInfo)
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
    fig.update_layout(xaxis_tickvals = xticks, showlegend = False, font = dict(size = 14))
    fig.update_xaxes(tickangle = 45)
    fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
    return fig, sections, subjects, judges, finished
        