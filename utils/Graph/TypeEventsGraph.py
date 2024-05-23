# this file handles type events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# update type events based on user choice.
def typeEventUpdate(df, type, typeChoice, first):
    dateTag = 'data'
    durationTag = 'durata'
    countTag = 'conteggio'
    quantileTag = 'quantile'
    filterTag = 'filtro'
    avgTag = 'media'
    sectionTag = 'sezione'
    subjectTag = 'materia'
    judgeTag = 'giudice'
    finishedTag = 'finito' 
    codeEventTag = 'codiceevento' 
    numProcessTag = 'numProcesso'
    df_temp = df.copy()
    if first == "PRIMO":
        df_temp = df_temp.groupby([type, numProcessTag]).first().reset_index()
    df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
    [allData, avgData] = frame.getAvgStdDataFrameByTypeChoice(df_temp, [codeEventTag], durationTag, countTag, quantileTag)      
    xticks = frame.getUniques(allData, codeEventTag)
    fig = px.box(allData, x = codeEventTag, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata evento', codeEventTag:'Codice evento'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
    fig.add_traces(
        px.line(avgData, x = codeEventTag, y = durationTag, markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = codeEventTag, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(xaxis_tickvals = xticks)
    fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
    return [fig]
        
