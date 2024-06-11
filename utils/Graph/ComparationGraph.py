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
def hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase):
    judgeStyle = {'width': 400}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    finishedStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
    eventStyle = {'width': 400}
    eventRadioStyle = {'display': 'contents'}
    stateStyle = {'width': 400}
    stateRadioStyle = {'display': 'contents'}
    phaseStyle = {'width': 400}
    phaseRadioStyle = {'display': 'contents'}
    finishedTag = utilities.getTagName('finishedTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    stateSequenceTag = utilities.getTagName('stateSequenceTag')
    [[sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences]] = hideChosen(choices, [sectionTag, subjectTag, codeJudgeTag, finishedTag, stateSequenceTag, phaseSequenceTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences])
    if event == None:
        eventRadioStyle = {'display': 'none'}
    elif event in choices:
        eventStyle = {'display': 'none'}
        eventRadioStyle = {'display': 'none'}
        event = None
    if state == None:
        stateRadioStyle = {'display': 'none'}
    elif state in choices:
        stateStyle = {'display': 'none'}
        stateRadioStyle = {'display': 'none'}
        state = None
    if phase == None:
        phaseRadioStyle = {'display': 'none'}
    elif phase in choices:
        phaseStyle = {'display': 'none'}
        phaseRadioStyle = {'display': 'none'}
        phase = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase]

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
def updateProcessData(df, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, stateChoice, stateRadio, phaseChoice, phaseRadio):
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    subjectTag = utilities.getTagName("subjectTag")
    withOut = utilities.getPlaceholderName("without")
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, dateTag, startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, codeJudgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    df_temp = frame.getTypesDataFrame(df_temp, stateSequenceTag, sequences)
    df_temp = frame.getTypesDataFrame(df_temp, phaseSequenceTag, phaseSequences)
    if eventChoice != None:
        df_temp = frame.getEventDataFrame(df_temp, eventChoice)
        if eventRadio == withOut:
            return df_temp[df_temp[eventTag] == withOut + " " + eventChoice]
        else:
            return df_temp[df_temp[eventTag] != withOut + " " + eventChoice]
    if stateChoice != None:
        df_temp = frame.getStateDataFrame(df_temp, stateChoice)
        if stateRadio == withOut:
            return df_temp[df_temp[stateTag] == withOut + " " + stateChoice]
        else:
            return df_temp[df_temp[stateTag] != withOut + " " + stateChoice]
    if phaseChoice != None:
        df_temp = frame.getPhaseDataFrame(df_temp, phaseChoice)
        if phaseRadio == withOut:
            return df_temp[df_temp[phaseTag] == withOut + " FASE " + phaseChoice]
        else:
            return df_temp[df_temp[phaseTag] != withOut + " FASE " + phaseChoice]
    return df_temp

# update data base on user choices on different parameters.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeData(df, startDate, endDate, sections, subjects, judges, finished):
    dateTag = utilities.getTagName("dateTag")
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, dateTag, startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, sectionTag, sections)
    df_temp = frame.getTypesDataFrame(df_temp, subjectTag, subjects)
    df_temp = frame.getTypesDataFrame(df_temp, codeJudgeTag, judges)
    df_temp = frame.getTypesDataFrame(df_temp, finishedTag, finished)
    return df_temp

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessDataframeFromSelection(df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio):
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    subjectTag = utilities.getTagName("subjectTag")
    if sections != None and len(sections) > 0:
        df_temp_1 = updateProcessData(df_temp, startDate, endDate, None, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_1 = df_data
    if subjects != None and len(subjects) > 0:
        df_temp_2 = updateProcessData(df_temp, startDate, endDate, sections, None, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_2 = df_data
    if judges != None and len(judges) > 0:
        df_temp_3 = updateProcessData(df_temp, startDate, endDate, sections, subjects, None, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_3 = df_data
    if finished != None and len(finished) > 0:
        df_temp_4 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, None, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_4 = df_data
    if sequences != None and len(sequences) > 0:
        df_temp_5 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, None, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_5 = df_data
    if phaseSequences != None and len(phaseSequences) > 0:
        df_temp_6 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, None, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_6 = df_data
    if event != None and len(event) > 0:
        df_temp_7 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, None, None, state, stateRadio, phase, phaseRadio)
    else:
        df_temp_7 = df_data
    if state != None and len(state) > 0:
        df_temp_8 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, None, None, phase, phaseRadio)
    else:
        df_temp_8 = df_data
    if phase != None and len(phase) > 0:
        df_temp_9 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, None, None)
    else:
        df_temp_9 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    judges = frame.getGroupBy(df_temp_3, codeJudgeTag)
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    sequences = frame.getGroupBy(df_temp_5, stateSequenceTag)
    phaseSequences = frame.getGroupBy(df_temp_6, phaseSequenceTag)
    event = frame.getGroupByFromString(df_temp_7, eventSequenceTag)
    state = frame.getGroupByFromString(df_temp_8, phaseSequenceTag)
    phase = frame.getGroupByFromString(df_temp_9, stateSequenceTag)
    return [sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase]

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeDataframeFromSelection(df_temp, df_data, startDate, endDate, sections, subjects, judges, finished):
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    if sections != None and len(sections) > 0:
        df_temp_1 = updateTypeData(df_temp, startDate, endDate, None, subjects, judges, finished)
    else:
        df_temp_1 = df_data
    if subjects != None and len(subjects) > 0:
        df_temp_2 = updateTypeData(df_temp, startDate, endDate, sections, None, judges, finished)
    else:
        df_temp_2 = df_data
    if judges != None and len(judges) > 0:
        df_temp_3 = updateTypeData(df_temp, startDate, endDate, sections, subjects, None, finished)
    else:
        df_temp_3 = df_data
    if finished != None and len(finished) > 0:
        df_temp_4 = updateTypeData(df_temp, startDate, endDate, sections, subjects, judges, None)
    else:
        df_temp_4 = df_data
    sections = frame.getGroupBy(df_temp_1, sectionTag)
    subjects = frame.getGroupBy(df_temp_2, subjectTag)
    judges = frame.getGroupBy(df_temp_3, codeJudgeTag)
    finished = frame.getGroupBy(df_temp_4, finishedTag)
    return [sections, subjects, judges, finished]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparation graph.
def processComparationUpdate(df, avgChoice, dateType, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio, choices, choicesOptions, order, text):
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    choicesOptions = choicesOptions[:6]
    if event != None:
        eventChoice = event
        choicesOptions.append(event)
    else:
        eventChoice = None
    if state != None:
        stateChoice = state
        choicesOptions.append(state)
    else:
        stateChoice = None
    if phase != None:
        phaseChoice = phase
        choicesOptions.append(phase)
    else:
        phaseChoice = None
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    filterTag = utilities.getTagName('filterTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase] = hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, stateChoice, phaseChoice)
    df_data = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    [sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase] = updateProcessDataframeFromSelection(df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, stateChoice, stateRadio, phaseChoice, phaseRadio)
    if choices == None or len(choices) == 0:
        orderRadioStyle = {'display': 'none'}
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
        xticks = frame.getUniques(avgData, dateTag)
        fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata del processo [giorni]', dateTag:'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
        fig.add_traces(
            px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = 'black').data
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
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choicesOptions
    else:
        orderRadioStyle = {'display': 'block'}
        [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, avgChoice, dateType, choices, order, eventChoice, stateChoice, phaseChoice)
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
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choicesOptions

# return all needed parameters in order to change graph after any user choice.
# this method is only for all comparation graphs except process ones.
def typeComparationUpdate(df, typeChoice, avgChoice, dateType, startDate, endDate, minDate, maxDate, type, sections, subjects, judges, finished, choices, order, text):
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    filterTag = utilities.getTagName('filterTag')
    finishedTag = utilities.getTagName('finishedTag')
    quantileTag = utilities.getTagName('quantileTag')
    phaseTag = utilities.getTagName('phaseTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    textTag = utilities.getPlaceholderName("text")
    df_temp = df.copy()
    if typeChoice == None:
        title = 'DURATA MEDIA ' + type[0:-1].upper() + 'I DEL PROCESSO'
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, type, avgChoice) 
        xticks = frame.getUniques(allData, type)
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(df_temp, df_temp, startDate, endDate, sections, subjects, judges, finished)
        if text == [textTag]:
            if type == eventTag:   
                fig = px.histogram(allData, x = type, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Numero di ' + type[0:-1] + 'i del processo', type:type.title() + ' del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
            else:
                colorMap = utilities.phaseColorMap(type)
                fig = px.histogram(allData, x = type, color = type, color_discrete_map = colorMap, labels = {durationTag:'Numero di ' + type[0:-1] + 'i del processo', type:type.title() + ' del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
        else:
            if type == eventTag:        
                fig = px.box(allData, x = type, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata ' + type[0:-1] + 'i del processo [giorni]', type:type.title() + ' del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            else:
                colorMap = utilities.phaseColorMap(type)
                fig = px.box(allData, x = type, y = durationTag, color = type, color_discrete_map = colorMap, labels = {durationTag:'Durata ' + type[0:-1] + 'i del processo [giorni]', type:type.title() + ' del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
            fig.add_traces(
                px.line(avgData, x = type, y = durationTag, markers = True).update_traces(line_color = 'black').data
            )
            fig.add_traces(
                px.line(avgData, x = type, y = quantileTag, markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False)
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
    else:
        title = 'CONFRONTO DURATA ' + type.upper() + ' ' + str(typeChoice).upper()            
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = showAll()
        [[sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished]] = hideChosen(choices, [sectionTag, subjectTag, codeJudgeTag, finishedTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished])
        df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
        df_data = updateTypeData(df_temp, startDate, endDate, sections, subjects, judges, finished)
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(df_temp, df_data, startDate, endDate, sections, subjects, judges, finished)
        if choices == None or len(choices) == 0:
            orderRadioStyle = {'display': 'none'}
            [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
            xticks = frame.getUniques(avgData, dateTag)
            fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = ['#91BBF3'], labels = {durationTag:'Durata ' + type + " " + str(typeChoice) + ' [giorni]', dateTag:'Data inizio ' + type + " " + str(typeChoice)}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = False)
            fig.add_traces(
                px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = 'black').data
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
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, avgChoice, dateType, choices, order, None, None, None)
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
