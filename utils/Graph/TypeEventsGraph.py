# this file handles type events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.utilities.Utilities as utilities

# update data based on user choices on different parameters.
def updateTypeData(df, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    df_temp = df.copy()
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, judgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    return df_temp

# update types based on user choices on different parameters.
def updateTypeDataBySelection(df, df_data, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
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
    judges = frame.getGroupBy(df_temp_3, judgeTag)
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    return [sections, subjects, judges, finished]

# update type events based on user choice.
def typeEventUpdate(df, type, typeChoice, tagChoice, first, avg, text, sections, subjects, judges, finished):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    firstTag = utilities.getPlaceholderName("first")
    numProcessTag = utilities.getTagName('numProcessTag')
    phaseTag = utilities.getTagName('phaseTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    if first == firstTag:
        df_temp = df_temp.groupby([type, numProcessTag]).first().reset_index()
    df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
    df_data = updateTypeData(df_temp, sections, subjects, judges, finished)
    [sections, subjects, judges, finished] = updateTypeDataBySelection(df_temp, df_data, sections, subjects, judges, finished)
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoice(df_data, tagChoice, avg)      
    xticks = frame.getUniques(allData, tagChoice)
    fig = px.box(allData, x = tagChoice, y = durationTag, color = phaseTag, color_discrete_sequence = utilities.phaseColorList(allData, phaseTag), labels = {durationTag:'Durata evento', tagChoice:'Codice'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
    fig.add_traces(
        px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = 'black').data
    )
    if text == [textTag]:
        fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    else:fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return [fig, sections, subjects, judges, finished]

# update type events based on user choice.
def typeSequenceUpdate(df, type, typeChoice, tagChoice, avg, text, sections, subjects, judges, finished):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    phaseTag = utilities.getTagName('phaseTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    df_temp = updateTypeData(df_temp, sections, subjects, judges, finished)
    df_temp = frame.selectFollowingRows(df_temp, tagChoice, typeChoice)
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoice(df_temp, tagChoice, avg)      
    xticks = frame.getUniques(allData, tagChoice)
    fig = px.box(allData, x = tagChoice, y = durationTag, color = 'fase', labels = {durationTag:'Durata evento', tagChoice:'Codice'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
    fig.add_traces(
        px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = 'black').data
    )
    if text == [textTag]:
        fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    else:fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return [fig]
        