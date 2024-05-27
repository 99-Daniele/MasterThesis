# this file handles comparation graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.utilities.Utilities as utilities

# hide page components if user select it.
def hideChosen(choices, tags, styles, parameters):
    for i in range(len(tags)):
        if tags[i] in choices:
            styles[i] = {'display':'none'}
            parameters[i] = None
    return [styles, parameters]

# return the style of dropdown as hidden or not based on user choices: if user choices one, then corresponding dropdown will be hidden and his values will reset.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, event):
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
    eventStyle = {'width': 400}
    eventRadioStyle = {'display': 'contents'}
    finishedTag = utilities.getTagName('finishedTag')
    judgeTag = utilities.getTagName('judgeTag')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    sequenceTag = utilities.getTagName('sequenceTag')
    [[sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences]] = hideChosen(choices, [sectionTag, subjectTag, judgeTag, finishedTag, sequenceTag, phaseSequenceTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences])
    if event == None:
        eventRadioStyle = {'display': 'none'}
    elif event in choices:
        eventStyle = {'display': 'none'}
        eventRadioStyle = {'display': 'none'}
        event = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event]

# show all hidden object such as dropdown, radioitem, checklist.
def showAll():
    dateRangeStyle = {'display':'block'}
    resetStyle = {'display':'block'}
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'display': 'block'}
    return [dateRangeStyle, resetStyle, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# hide all shown object such as dropdown, radioitem, checklist.
def hideAll():
    dateRangeStyle = {'display':'none'}
    resetStyle = {'display':'none'}
    dateCheckStyle = {'display': 'none'}
    sectionStyle = {'display': 'none'}
    subjectStyle = {'display': 'none'}
    judgeStyle = {'display': 'none'}
    finishedStyle = {'display': 'none'}
    choiceCheckStyle = {'display': 'none'}
    orderRadioStyle = {'display': 'none'}
    return [dateRangeStyle, dateCheckStyle, resetStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# update data base on user choices on different parameters.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessData(df, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio):
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    sequenceTag = utilities.getTagName("sequenceTag")
    subjectTag = utilities.getTagName("codeSubjectTag")
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, dateTag, startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, judgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    df_temp = frame.getTypesDataFrame(df_temp, sequenceTag, sequences)
    df_temp = frame.getTypesDataFrame(df_temp, phaseSequenceTag, phaseSequences)
    if eventChoice != None:
        df_temp = frame.getEventDataFrame(df_temp, eventChoice)
        return df_temp[df_temp[eventTag] == eventRadio + " " + eventChoice]
    return df_temp

# update data base on user choices on different parameters.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeData(df, startDate, endDate, sections, subjects, judges, finished):
    dateTag = utilities.getTagName("dateTag")
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("codeSubjectTag")
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, dateTag, startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, judgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    return df_temp

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessDataframeFromSelection(choice, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio):
    eventsTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    sequenceTag = utilities.getTagName("sequenceTag")
    subjectTag = utilities.getTagName("codeSubjectTag")
    if choice != None and 'section-dropdown' in choice:
        df_temp_1 = updateProcessData(df_temp, startDate, endDate, None, subjects, judges, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_1 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    if choice != None and 'subject-dropdown' in choice:
        df_temp_2 = updateProcessData(df_temp, startDate, endDate, sections, None, judges, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_2 = df_data
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    if choice != None and 'judge-dropdown' in choice:
        df_temp_3 = updateProcessData(df_temp, startDate, endDate, sections, subjects, None, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_3 = df_data
    judges = frame.getGroupBy(df_temp_3, judgeTag)
    if choice != None and 'finished-dropdown' in choice:
        df_temp_4 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, None, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_4 = df_data
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    if choice != None and 'sequence-dropdown' in choice:
        df_temp_5 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, None, phaseSequences, event, eventRadio)
    else:
        df_temp_5 = df_data
    sequences = frame.getGroupBy(df_temp_5, sequenceTag)
    if choice != None and 'phaseSequence-dropdown' in choice:
        df_temp_6 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, None, event, eventRadio)
    else:
        df_temp_6 = df_data
    phaseSequences = frame.getGroupBy(df_temp_6, phaseSequenceTag)
    if choice != None and ('events-dropdown' in choice or 'events-radioitem' in choice):
        df_temp_7 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, None, None)
    else:
        df_temp_7 = df_data
    event = frame.getGroupByFromString(df_temp_7, eventsTag)
    return [sections, subjects, judges, finished, sequences, phaseSequences, event]

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeDataframeFromSelection(choice, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("codeSubjectTag")
    if choice != None and 'section-dropdown' in choice:
        df_temp_1 = updateTypeData(df_temp, startDate, endDate, None, subjects, judges, finished)
    else:
        df_temp_1 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    if choice != None and 'subject-dropdown' in choice:
        df_temp_2 = updateTypeData(df_temp, startDate, endDate, sections, None, judges, finished)
    else:
        df_temp_2 = df_data
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    if choice != None and 'judge-dropdown' in choice:
        df_temp_3 = updateTypeData(df_temp, startDate, endDate, sections, subjects, None, finished)
    else:
        df_temp_3 = df_data
    judges = frame.getGroupBy(df_temp_3, judgeTag)
    if choice != None and 'finished-dropdown' in choice:
        df_temp_4 = updateTypeData(df_temp, startDate, endDate, sections, subjects, judges, None)
    else:
        df_temp_4 = df_data
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    return [sections, subjects, judges, finished]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparation graph.
def processComparationUpdate(df, avgChoice, dateType, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, order, text):
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    if event != None:
        eventChoice = event
        if len(choicesOptions) == 6:
            choicesOptions.append(event)
        else:
            choicesOptions[-1] = event
    else:
        eventChoice = None
        if len(choicesOptions) == 7:
            choicesOptions.pop()
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    filterTag = utilities.getTagName('filterTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event] = hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice)
    df_data = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio)
    [sections, subjects, judges, finished, sequences, phaseSequences, event] = updateProcessDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio)
    if choices == None or len(choices) == 0:
        orderRadioStyle = {'display': 'none'}
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
        xticks = frame.getUniques(avgData, dateTag)
        fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata del processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
        fig.add_traces(
            px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = 'red').data
        )
        if text == [textTag]:
            fig.add_traces(
                px.line(avgData, x = dateTag, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        else:
            fig.add_traces(
                px.line(avgData, x = dateTag, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choicesOptions
    else:
        orderRadioStyle = {'display': 'block'}
        [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, avgChoice, dateType, choices, order, eventChoice)
        xticks = frame.getUniques(allData, dateTag)
        if text == [textTag]:
            fig = px.line(allData, x = dateTag, y = durationTag, text = countTag, labels = {durationTag:'Durata processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = dateTag, y = durationTag, text = countTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
            )
        else:
            fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Durata processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = dateTag, y = durationTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
            )
        fig.for_each_trace(
            lambda t: t.update(name = frame.addCountToName(infoData, t.name, filterTag, countTag)) if t.name != frame.addTotCountToName(allData, countTag) else False
        )
        fig.for_each_trace(
            lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 14)
        )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != frame.addTotCountToName(allData, countTag) else False))
        fig.update_xaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choicesOptions

# return all needed parameters in order to change graph after any user choice.
# this method is only for all comparation graphs except process ones.
def typeComparationUpdate(df, typeChoice, avgChoice, dateType, startDate, endDate, minDate, maxDate, type, sections, subjects, judges, finished, choices, order, text):
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    filterTag = utilities.getTagName('filterTag')
    finishedTag = utilities.getTagName('finishedTag')
    judgeTag = utilities.getTagName('judgeTag')
    quantileTag = utilities.getTagName('quantileTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    if typeChoice == None:
        title = 'DURATA MEDIA ' + type[0:-1].upper() + 'I DEL PROCESSO'
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, [type], avgChoice)        
        xticks = frame.getUniques(allData, type)
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_temp, startDate, endDate, sections, subjects, judges, finished)
        fig = px.box(allData, x = type, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata ' + type[0:-1] + 'i del processo [giorni]', type:type.title() + ' del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
        fig.add_traces(
            px.line(avgData, x = type, y = durationTag, markers = True).update_traces(line_color = 'red').data
        )
        if text == [textTag]:
            fig.add_traces(
                px.line(avgData, x = type, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        else:
            fig.add_traces(
                px.line(avgData, x = type, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
    else:
        title = 'CONFRONTO DURATA ' + type.upper() + ' ' + str(typeChoice).upper()            
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = showAll()
        [[sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished]] = hideChosen(choices, [sectionTag, subjectTag, judgeTag, finishedTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished])
        df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
        df_data = updateTypeData(df_temp, startDate, endDate, sections, subjects, judges, finished)
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished)
        if choices == None or len(choices) == 0:
            orderRadioStyle = {'display': 'none'}
            [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
            xticks = frame.getUniques(avgData, dateTag)
            fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata ' + type + " " + str(typeChoice) + ' [giorni]', dateTag:'Data inizio ' + type + " " + str(typeChoice)}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
            fig.add_traces(
                px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = 'red').data
            )
            if text == [textTag]:
                fig.add_traces(
                    px.line(avgData, x = dateTag, y = quantileTag, text = countTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
                )
            else:
                fig.add_traces(
                    px.line(avgData, x = dateTag, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
                )
            fig.update_layout(xaxis_tickvals = xticks)
            fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
            return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
        else:
            orderRadioStyle = {'display': 'block'}
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, avgChoice, dateType, choices, order, None)
            xticks = frame.getUniques(allData, dateTag)
            if text == [textTag]:
                fig = px.line(allData, x = dateTag, y = durationTag, text = countTag, labels = {durationTag:'Durata processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
                fig.add_traces(
                    px.line(typeData, x = dateTag, y = durationTag, text = countTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
                )
            else:
                fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Durata processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
                fig.add_traces(
                    px.line(typeData, x = dateTag, y = durationTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
                )
            fig.for_each_trace(
                lambda t: t.update(name = frame.addCountToName(infoData, t.name, filterTag, countTag)) if t.name != frame.addTotCountToName(allData, countTag) else False
            )
            fig.for_each_trace(
                lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 14)
            )
            fig.update_layout(xaxis_tickvals = xticks)
            fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != frame.addTotCountToName(allData, countTag) else False))
            fig.update_xaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
            fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
            return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
