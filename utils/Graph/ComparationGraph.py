# this file handles comparation graph management.

import dash as ds
import plotly.express as px
import textwrap

import utils.Dataframe as frame
import utils.Utilities.Utilities as utilities

# returns a string with input name followed by how many times is present in the dataframe.
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

# return the style of dropdown as hidden or not based on user choices: if user choices one, then corresponding dropdown will be hidden and his values will reset.
# this method is for all comparation graphs except process ones since they use different parameters.
def hideTypeChosen(choices, sections, subjects, judges, finished, changes):
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
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
    if 'cambio' in choices:
        changeStyle = {'display': 'none'}
        changes = None
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes]

# show all hidden object such as dropdown, radioitem, checklist.
def showAll():
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'display': 'block'}
    return [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle]

# hide all shown object such as dropdown, radioitem, checklist.
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

# update data base on user choices on different parameters.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
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

# update data base on user choices on different parameters.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypeData(df, sections, subjects, judges, finished, change):
    df_temp = df
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    return df_temp

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
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

# update data base on user choices on different parameters. In order to do that is use 'updateProcessData' method with chosen parameter as None. 
# this is done because if user wants to compare on chosen parameter, data must be updated without any filter on chosen parameter.
# this method is for all comparation graphs except process ones since they use different parameters.
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

# return all different types based on current dataframe.
# this method is only for process comparation graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessTypes(df):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    finished = frame.getGroupBy(df, 'finito')
    changes = frame.getGroupBy(df, 'cambio')
    sequences = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
    return [sections, subjects, judges, finished, changes, sequences, phaseSequences]

# return all different types based on current dataframe.
# this method is for all comparation graphs except process ones since they use different parameters.
def updateTypes(df):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    finished = frame.getGroupBy(df, 'finito')
    changes = frame.getGroupBy(df, 'cambio')
    return [sections, subjects, judges, finished, changes]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparation graph.
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
    fig = px.line(allData, x = "data", y = "durata", width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
    fig.add_traces(
        px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
    )
    fig.for_each_trace(
        lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
    )
    fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
    fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, dateType, date, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore

# return all needed parameters in order to change graph after any user choice.
# this method is only for all comparation graphs except process ones.
def typeComparationUpdate(df, dateType, date, typeChoice, type, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    df_temp = df.copy()
    if typeChoice == None:
        title = 'DURATA MEDIA ' + type[0:-1].upper() + 'I DEL PROCESSO'
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, [type])
        [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        fig = px.box(allData, x = type, y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9), points  = False)
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
            choices = ['sezione']
            [dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes] = hideTypeChosen(choices, sections, subjects, judges, finished, changes)
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
        fig = px.line(allData, x = "data", y = "durata", width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
        fig.add_traces(
            px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9)).data
        )
        fig.for_each_trace(
            lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
        )
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
        fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig, dateType, date, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, changes, choices, choiceStore, title
