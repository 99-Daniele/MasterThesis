# this file handles type events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.utilities.Utilities as utilities

# update data base on user choices on different parameters.
def updateTypeData(df, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("codeSubjectTag")
    df_temp = df.copy()
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, judgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    return df_temp

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
    df_temp = updateTypeData(df_temp, sections, subjects, judges, finished)
    if first == firstTag:
        df_temp = df_temp.groupby([type, numProcessTag]).first().reset_index()
    df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoice(df_temp, tagChoice, avg)      
    xticks = frame.getUniques(allData, tagChoice)
    fig = px.box(allData, x = tagChoice, y = durationTag, color = phaseTag, color_discrete_sequence = utilities.phaseColorList(df_temp, phaseTag), labels = {durationTag:'Durata evento', tagChoice:'Codice'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
    fig.add_traces(
        px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = 'red').data
    )
    if text == [textTag]:
        fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    else:fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    fig.update_traces(showlegend = False)
    fig.update_layout(xaxis_tickvals = xticks)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return [fig]

# update type events based on user choice.
def typeSequenceUpdate(df, type, typeChoice, tagChoice, avg, text, sections, subjects, judges, finished):
    countTag = utilities.getTagName('countTag')
    durationTag = utilities.getTagName('durationTag')
    numProcessTag = utilities.getTagName('numProcessTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    df_temp = updateTypeData(df_temp, sections, subjects, judges, finished)
    df_temp = frame.selectFollowingRows(df_temp, tagChoice, typeChoice)   
    print(df_temp)
    exit()
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoice(df_temp, [tagChoice], avg)      
    xticks = frame.getUniques(allData, tagChoice)
    fig = px.box(allData, x = tagChoice, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata evento', tagChoice:'Codice'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
    fig.add_traces(
        px.line(avgData, x = tagChoice, y = durationTag, markers = True).update_traces(line_color = 'red').data
    )
    if text == [textTag]:
        fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    else:fig.add_traces(
            px.line(avgData, x = tagChoice, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
    fig.update_layout(xaxis_tickvals = xticks)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return [fig]
        