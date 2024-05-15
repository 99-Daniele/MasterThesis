# this file handles comparation graph management.

import dash as ds
import plotly.express as px
import textwrap

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Utilities.Utilities as utilities

# returns a string with input name followed by how many times is present in the dataframe.
def addCountToName(name, df, choices):
    if choices == 'finito':
        count = df[df['filtro'] == int(name)]['conteggio'].item()
        name = utilities.getProcessState(int(name))
    else:
        count = df[df['filtro'].astype(str) == name]['conteggio'].item()
    newName = name + " (" + str(count) + ")"
    newName = '<br>'.join(textwrap.wrap(newName, width = 50))
    return newName

# returns a string with total sum of counts in dataframe.
def addTotCountToName(df):
    totCount = df['conteggio'].sum()
    newName = "TUTTI (" + str(totCount) + ")"
    return newName

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
    if 'sezione' in choices:
        sectionStyle = {'display': 'none'}
        sections = None
    if 'materia' in choices:
        subjectStyle = {'display': 'none'}
        subjects = None
    if 'giudice' in choices:
        judgeStyle = {'display': 'none'}
        judges = None
    if 'finito' in choices:
        finishedStyle = {'display': 'none'}
        finished = None
    if 'sequenza' in choices:
        sequenceStyle = {'display': 'none'}
        sequences = None
    if 'fasi' in choices:
        phaseSequenceStyle = {'display': 'none'}
        phaseSequences = None
    if event == None:
        eventRadioStyle = {'display': 'none'}
    elif event in choices:
        eventStyle = {'display': 'none'}
        eventRadioStyle = {'display': 'none'}
        event = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event]

# return the style of dropdown as hidden or not based on user choices: if user choices one, then corresponding dropdown will be hidden and his values will reset.
# this method is for all comparation graphs except process ones since they use different parameters.
def hideTypeChosen(choices, sections, subjects, judges, finished):
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'display': 'block'}
    if 'sezione' in choices:
        sectionStyle = {'display': 'none'}
        sections = None
    if 'materia' in choices:
        subjectStyle = {'display': 'none'}
        subjects = None
    if 'giudice' in choices:
        judgeStyle = {'display': 'none'}
        judges = None
    if 'finito' in choices:
        finishedStyle = {'display': 'none'}
        finished = None
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished]

# show all hidden object such as dropdown, radioitem, checklist.
def showAll():
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'display': 'block'}
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# hide all shown object such as dropdown, radioitem, checklist.
def hideAll():
    dateCheckStyle = {'display': 'none'}
    sectionStyle = {'display': 'none'}
    subjectStyle = {'display': 'none'}
    judgeStyle = {'display': 'none'}
    finishedStyle = {'display': 'none'}
    choiceCheckStyle = {'display': 'none'}
    orderRadioStyle = {'display': 'none'}
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# update data base on user choices on different parameters.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessData(df, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio):
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df_temp, 'data', startDate, endDate)
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phaseSequences)
    if eventChoice != None:
        df_temp = frame.getEventDataFrame(df_temp, eventChoice)
        return df_temp[df_temp['evento'] == eventRadio + " " + eventChoice]
    return df_temp

# update data base on user choices on different parameters.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeData(df, sections, subjects, judges, finished):
    df_temp = df
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    return df_temp

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessDataframeFromSelection(choice, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, importantSubjects):
    if choice != None and 'section-dropdown' in choice:
        df_temp_1 = updateProcessData(df_temp, startDate, endDate, None, subjects, judges, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_1 = df_data
    sections = frame.getGroupBy(df_temp_1, 'sezione')
    if choice != None and 'subject-dropdown' in choice:
        df_temp_2 = updateProcessData(df_temp, startDate, endDate, sections, None, judges, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_2 = df_data
    subjects = frame.getGroupBy(df_temp_2, 'materia')
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    if choice != None and 'judge-dropdown' in choice:
        df_temp_3 = updateProcessData(df_temp, startDate, endDate, sections, subjects, None, finished, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_3 = df_data
    judges = frame.getGroupBy(df_temp_3, 'giudice')
    if choice != None and 'finished-dropdown' in choice:
        df_temp_4 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, None, sequences, phaseSequences, event, eventRadio)
    else:
        df_temp_4 = df_data
    finished = frame.getGroupBy(df_temp_4, 'finito')
    if choice != None and 'sequence-dropdown' in choice:
        df_temp_5 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, None, phaseSequences, event, eventRadio)
    else:
        df_temp_5 = df_data
    sequences = frame.getGroupBy(df_temp_5, 'sequenza')
    if choice != None and 'phaseSequence-dropdown' in choice:
        df_temp_6 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, None, event, eventRadio)
    else:
        df_temp_6 = df_data
    phaseSequences = frame.getGroupBy(df_temp_6, 'fasi')
    if choice != None and ('events-dropdown' in choice or 'events-radioitem' in choice):
        df_temp_7 = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, None, None)
    else:
        df_temp_7 = df_data
    event = frame.getGroupByFromString(df_temp_7, 'eventi')
    return [sections, subjects, judges, finished, sequences, phaseSequences, event]

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeDataframeFromSelection(choice, df_temp, df_data, sections, subjects, judges, finished, importantSubjects):
    if choice != None and 'section-dropdown' in choice:
        df_temp_1 = updateTypeData(df_temp, None, subjects, judges, finished)
    else:
        df_temp_1 = df_data
    sections = frame.getGroupBy(df_temp_1, 'sezione')
    if choice != None and 'subject-dropdown' in choice:
        df_temp_2 = updateTypeData(df_temp, sections, None, judges, finished)
    else:
        df_temp_2 = df_data
    subjects = frame.getGroupBy(df_temp_2, 'materia')
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    if choice != None and 'judge-dropdown' in choice:
        df_temp_3 = updateTypeData(df_temp, sections, subjects, None, finished)
    else:
        df_temp_3 = df_data
    judges = frame.getGroupBy(df_temp_3, 'giudice')
    if choice != None and 'finished-dropdown' in choice:
        df_temp_4 = updateTypeData(df_temp, sections, subjects, judges, None)
    else:
        df_temp_4 = df_data
    finished = frame.getGroupBy(df_temp_4, 'finito')
    return [sections, subjects, judges, finished]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparation graph.
def processComparationUpdate(df, avgChoice, dateType, date, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, choiceStore, order, text):
    importantSubjects = getter.getImportantSubjects()
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
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    df_temp = df.copy()
    if len(choices) == 0:
        [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event] = hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice)
        df_data = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio)
        [sections, subjects, judges, finished, sequences, phaseSequences, event] = updateProcessDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, importantSubjects)
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, date, avgChoice)
        xticks = frame.getUniques(avgData, 'data')
        fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8), points = 'suspectedoutliers')
        fig.add_traces(
            px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        if text == ['TESTO']:
            fig.add_traces(
                px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        else:
            fig.add_traces(
                px.line(avgData, x = "data", y = "quantile", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, dateType, date, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choices, choicesOptions, choiceStore
    else:
        [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event] = hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice)
        df_data = updateProcessData(df_temp, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio)
        [sections, subjects, judges, finished, sequences, phaseSequences, event] = updateProcessDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, importantSubjects)
        [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, avgChoice, date, choices, order, eventChoice)
        xticks = frame.getUniques(allData, 'data')
        if text == ['TESTO']:
            fig = px.line(allData, x = "data", y = "durata", text = "conteggio", labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = "data", y = "durata", text = "conteggio", color = 'filtro', markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
            )
        else:
            fig = px.line(allData, x = "data", y = "durata", labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.8)).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
            )
        fig.for_each_trace(
            lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
        )
        fig.for_each_trace(
            lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 14)
        )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
        fig.update_xaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, dateType, date, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, choices, choicesOptions, choiceStore

# return all needed parameters in order to change graph after any user choice.
# this method is only for all comparation graphs except process ones.
def typeComparationUpdate(df, dateType, date, typeChoice, type, sections, subjects, judges, finished, choices, choiceStore, order):
    df_temp = df.copy()
    importantSubjects = getter.getImportantSubjects()
    if typeChoice == None:
        title = 'DURATA MEDIA ' + type[0:-1].upper() + 'I DEL PROCESSO'
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, [type])        
        xticks = frame.getUniques(allData, type)
        [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        fig = px.box(allData, x = type, y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
        fig.add_traces(
            px.line(avgData, x = type, y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = type, y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_temp, sections, subjects, judges, finished, importantSubjects)
        return fig, dateType, date, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, choices, choiceStore, title
    else:
        title = 'CONFRONTO DURATA ' + type.upper() + ' ' + str(typeChoice).upper()
        df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
        if ds.ctx.triggered_id != None and 'type-dropdown' in ds.ctx.triggered_id:
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = showAll()
            choices = ['sezione']
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished] = hideTypeChosen(choices, sections, subjects, judges, finished)
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_temp, date, choices, order, None)
            df_data = df_temp
        else:
            if len(dateType) >= 1:
                date = dateType[-1]
            dateType = [date]
            if choices != None and len(choices) < 1:
                choices = [choiceStore]
            elif choices != None and len(choices) == 1:
                choiceStore = choices[0]
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished] = hideTypeChosen(choices, sections, subjects, judges, finished)
            df_data = updateTypeData(df_temp, sections, subjects, judges, finished)
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, date, choices, order, None)
        xticks = frame.getUniques(allData, 'data')
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, sections, subjects, judges, finished, importantSubjects)
        fig = px.line(allData, x = "data", y = "durata", text = "conteggio", labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
        fig.add_traces(
            px.line(typeData, x = "data", y = "durata", text = 'conteggio', color = 'filtro', markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
        )
        fig.for_each_trace(
            lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
        )
        fig.for_each_trace(
            lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 14)
        )
        fig.update_layout(xaxis_tickvals = xticks)
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
        fig.update_xaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'rgb(160, 160, 160)', griddash = 'dash')
        return fig, dateType, date, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, choices, choiceStore, title
