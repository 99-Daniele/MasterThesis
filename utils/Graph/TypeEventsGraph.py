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
    df_temp = df.copy()
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, codeJudgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    return df_temp

# update types based on user choices on different parameters.
def updateTypeDataBySelection(df, df_data, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    df_temp = df.copy()
    if sections != None and len(sections) > 0:
        df_temp_1 = updateTypeData(df_temp, None, subjects, judges, finished)
    else:
        df_temp_1 = df_data
    if subjects != None and len(subjects) > 0:
        df_temp_2 = updateTypeData(df_temp, sections, None, judges, finished)
    else:
        df_temp_2 = df_data
    if judges != None and len(judges) > 0:
        df_temp_3 = updateTypeData(df_temp, sections, subjects, None, finished)
    else:
        df_temp_3 = df_data
    if finished != None and len(finished) > 0:
        df_temp_4 = updateTypeData(df_temp, sections, subjects, judges, None)
    else:
        df_temp_4 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    judges = frame.getGroupBy(df_temp_3, codeJudgeTag)
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    return [sections, subjects, judges, finished]

# update type events based on user choice.
def typeEventUpdate(df, type, typeChoices, tagChoice, first, avg, text, sections, subjects, judges, finished):
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    firstTag = utilities.getPlaceholderName("first")
    lastTag = utilities.getPlaceholderName("last")
    numProcessTag = utilities.getTagName('numProcessTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    statesInfo = getter.getStatesInfo()
    df_temp = df.copy()
    if first == firstTag:
        df_temp = df_temp.groupby([type, numProcessTag]).first().reset_index()
    elif first == lastTag:
        df_temp = df_temp.groupby([type, numProcessTag]).last().reset_index()
    df_temp = frame.getTypesDataFrame(df_temp, type, typeChoices)
    df_data = updateTypeData(df_temp, sections, subjects, judges, finished)
    [sections, subjects, judges, finished] = updateTypeDataBySelection(df_temp, df_data, sections, subjects, judges, finished)
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoiceOrderByPhase(df_data, tagChoice, avg)   
    xticks = frame.getUniques(allData, tagChoice)
    if tagChoice == eventTag:
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 12)).data
            )         
    else:
        colorMap = frame.phaseColorMap(tagChoice, statesInfo)
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 12)).data
            )
    fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False, legend = dict(font = dict(size = 16)))
    fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
    return [fig, sections, subjects, judges, finished]

# update type events based on user choice.
def typeSequenceUpdate(df, typeChoices, tagChoice, avg, text, sections, subjects, judges, finished):
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    statesInfo = getter.getStatesInfo()
    df_temp = df.copy()
    df_temp = frame.selectFollowingRows(df_temp, tagChoice, typeChoices)
    df_data = updateTypeData(df_temp, sections, subjects, judges, finished) 
    [sections, subjects, judges, finished] = updateTypeDataBySelection(df_temp, df_data, sections, subjects, judges, finished)
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoiceOrderByPhase(df_data, tagChoice, avg)
    xticks = frame.getUniques(allData, tagChoice)
    if tagChoice == eventTag:
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 12)).data
            )         
    else:
        colorMap = frame.phaseColorMap(tagChoice, statesInfo)
        if text == [textTag]:
            fig = px.histogram(allData, x = tagChoice, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Count', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
        else:
            fig = px.box(allData, x = tagChoice, y = durationTag, color = tagChoice, color_discrete_map = colorMap, labels = {durationTag:'Duration', tagChoice:'ID'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            fig.add_traces(
                px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 12)).data
            )
    fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False, legend = dict(font = dict(size = 16)))
    fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
    return [fig, sections, subjects, judges, finished]
        