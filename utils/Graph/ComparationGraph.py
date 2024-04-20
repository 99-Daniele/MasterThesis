import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def addCountToName(name, df, choices):
    if choices == 'finito':
        count = df[df[type] == int(name)]['conteggio'].item()
        name = utilities.getProcessState(int(name))
    elif choices == 'cambio':
        count = df[df[type] == int(name)]['conteggio'].item()
        if int(name) == 0:
            name = "NO"
        else:
            name = "SI"
    else:
        count = df[df['filtro'] == name]['conteggio'].item()
    newName = name + " (" + str(count) + ")"
    return newName

def addTotCountToName(df):
    totCount = df['conteggio'].sum()
    newName = "TUTTI (" + str(totCount) + ")"
    return newName

def getPosition(name, df, type):
    pos = df.index.get_loc(df[df[type] == name].index[0])
    return pos

def hideProcessChosen(choices, sections, subjects, judges, finished, changes, sequences, phaseSequences):
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
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
    if 'cambio' in choices:
        changeStyle = {'display': 'none'}
        changes = None
    if 'sequenza' in choices:
        sequenceStyle = {'display': 'none'}
        sequences = None
    if 'fasi' in choices:
        phaseSequenceStyle = {'display': 'none'}
        phaseSequences = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences]

def hideTypeChosen(choices, sections, subjects, judges, finished, changes):
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'paddingLeft': '85%'}
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
    if 'cambio' in choices:
        changeStyle = {'display': 'none'}
        changes = None
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes]

def showAll():
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'paddingLeft': '85%'}
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle]

def hideAll():
    dateCheckStyle = {'display': 'none'}
    sectionStyle = {'display': 'none'}
    subjectStyle = {'display': 'none'}
    judgeStyle = {'display': 'none'}
    finishedStyle = {'display': 'none'}
    changeStyle = {'display': 'none'}
    choiceCheckStyle = {'display': 'none'}
    orderRadioStyle = {'display': 'none'}
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle]

def updateProcessData(df, sections, subjects, judges, finished, change, sequences, phaseSequences):
    df_temp = df.copy()
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phaseSequences)
    return df_temp

def updateTypeData(df, sections, subjects, judges, finished, change):
    df_temp = df
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    return df_temp

def updateProcessDataframeFromSelection(choice, df_temp, df_data, sections, subjects, judges, finished, changes, sequences, phaseSequences):
    if choice != None and 'section-dropdown' in choice:
        df_temp = updateProcessData(df_temp, None, subjects, judges, finished, changes, sequences, phaseSequences)
    elif choice != None and 'subject-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, None, judges, finished, changes, sequences, phaseSequences)
    elif choice != None and 'judge-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, subjects, None, finished, changes, sequences, phaseSequences)
    elif choice != None and 'finished-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, None, changes, sequences, phaseSequences)
    elif choice != None and 'change-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, None, sequences, phaseSequences)
    elif choice != None and 'sequence-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, changes, None, phaseSequences)
    elif choice != None and 'phaseSequence-dropdown' in choice:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, changes, sequences, None)
    else:
        df_temp = df_data
    return df_temp

def updateTypeDataframeFromSelection(choice, df_temp, df_data, sections, subjects, judges, finished, changes):
    if choice != None and 'section-dropdown' in choice:
        df_temp = updateTypeData(df_temp, None, subjects, judges, finished, changes)
    elif choice != None and 'subject-dropdown' in choice:
        df_temp = updateTypeData(df_temp, sections, None, judges, finished, changes)
    elif choice != None and 'judge-dropdown' in choice:
        df_temp = updateTypeData(df_temp, sections, subjects, None, finished, changes)
    elif choice != None and 'finished-dropdown' in choice:
        df_temp = updateTypeData(df_temp, sections, subjects, judges, None, changes)
    elif choice != None and 'change-dropdown' in choice:
        df_temp = updateTypeData(df_temp, sections, subjects, judges, finished, None)
    else:
        df_temp = df_data
    return df_temp

def updateProcessTypes(df):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    finished = frame.getGroupBy(df, 'finito')
    changes = frame.getGroupBy(df, 'cambio')
    sequences = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
    return [sections, subjects, judges, finished, changes, sequences, phaseSequences]

def updateTypes(df):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    finished = frame.getGroupBy(df, 'finito')
    changes = frame.getGroupBy(df, 'cambio')
    return [sections, subjects, judges, finished, changes]

def processComparationUpdate(df, dateType, date, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
    if len(dateType) >= 1:
        date = dateType[-1]
    dateType = [date]
    if len(choices) < 1:
        choices = [choiceStore]
    elif len(choices) == 1:
        choiceStore = choices[0]
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences] = hideProcessChosen(choices, sections, subjects, judges, finished, changes, sequences, phaseSequences)
    df_temp = df.copy()
    df_data = updateProcessData(df_temp, sections, subjects, judges, finished, changes, sequences, phaseSequences)
    df_temp = updateProcessDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, sections, subjects, judges, finished, changes, sequences, phaseSequences)
    [sections, subjects, judges, finished, changes, sequences, phaseSequences] = updateProcessTypes(df_temp)
    [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, date, choices, order)
    fig = px.line(allData, x = "data", y = "durata", height = 800).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
    fig.add_traces(
        px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600).data
    )
    fig.for_each_trace(
        lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
    )
    fig.update_layout(legend = dict(yanchor = "bottom", y = -1.5, xanchor = "left", x = 0))
    fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
    fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore

def typeComparationUpdate(df, dateType, date, typeChoice, type, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    df_temp = df.copy()
    if typeChoice == None:
        title = 'DURATA MEDIA ' + type[0:-1].upper() + 'I DEL PROCESSO'
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, [type])
        [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        fig = px.box(allData, x = type, y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = type, y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = type, y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        [sections, subjects, judges, finished, changes] = updateTypes(df_temp)
        return fig, dateType, date, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes, choices, choiceStore, title
    else:
        title = 'CONFRONTO DURATA ' + type.upper() + ' ' + str(typeChoice).upper()
        df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
        if ds.ctx.triggered_id != None and 'type-dropdown' in ds.ctx.triggered_id:
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle] = showAll()
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_temp, date, choices, order)
        else:
            if len(dateType) >= 1:
                date = dateType[-1]
            dateType = [date]
            if choices != None and len(choices) < 1:
                choices = [choiceStore]
            elif choices != None and len(choices) == 1:
                choiceStore = choices[0]
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes] = hideTypeChosen(choices, sections, subjects, judges, finished, changes)
            df_temp = df.copy()
            df_temp = frame.getTypesDataFrame(df_temp, type, [typeChoice])
            df_data = updateTypeData(df_temp, sections, subjects, judges, finished, changes)
            df_temp = updateTypeDataframeFromSelection(ds.ctx.triggered_id, df_temp, df_data, sections, subjects, judges, finished, changes)
            [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, date, choices, order)
        [sections, subjects, judges, finished, changes] = updateTypes(df_temp)
        fig = px.line(allData, x = "data", y = "durata", height = 800).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
        fig.add_traces(
            px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600).data
        )
        fig.for_each_trace(
            lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
        )
        fig.update_layout(legend = dict(yanchor = "bottom", y = -1.5, xanchor = "left", x = 0))
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
        fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig, dateType, date, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes, choices, choiceStore, title
