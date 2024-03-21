import dash as ds
import pandas as pd
import plotly.express as px

import utils.DataFrame as frame
import utils.Utilities as utilities

def addCountToName(name, df, type):
    if type == 'finito':
        count = df[df[type] == int(name)]['conteggio'].item()
        name = utilities.processState[int(name)]
    elif type == 'cambio':
        count = df[df[type] == int(name)]['conteggio'].item()
        if int(name) == 0:
            name = "NO"
        else:
            name = "SI"
    else:
        count = df[df[type] == name]['conteggio'].item()
    newName = name + " (" + str(count) + ")"
    return newName

def addTotCountToName(df):
    totCount = df['conteggio'].sum()
    newName = "TUTTI (" + str(totCount) + ")"
    return newName

def getPosition(name, df, type):
    pos = df.index.get_loc(df[df[type] == name].index[0])
    return pos

def hideChosen(choice, sections, subjects, judges, finished, changes, sequences, phaseSequences):
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
    match choice:
        case 'sezione':
            sectionStyle = {'width': 200, 'display': 'none'}
            sections = None
        case 'materia':
            subjectStyle = {'width': 200, 'display': 'none'}
            subjects = None
        case 'giudice':
            judgeStyle = {'width': 200, 'display': 'none'}
            judges = None
        case 'finito':
            finishedStyle = {'width': 200, 'display': 'none'}
            finished = None
        case 'cambio':
            changeStyle = {'width': 200, 'display': 'none'}
            changes = None
        case 'sequenza':
            sequenceStyle = {'width': 200, 'display': 'none'}
            sequences = None
        case 'fasi':
            phaseSequenceStyle = {'width': 200, 'display': 'none'}
            phaseSequences = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences]

def updateProcessData(df, sections, subjects, judges, finished, change, sequences, phaseSequences):
    df_temp = df
    if not (sections == None or len(sections) == 0):
        df_temp = frame.getSectionsdDataFrame(df_temp, sections)
    if not (subjects == None or len(subjects) == 0):
        df_temp = frame.getSubjectsdDataFrame(df_temp, subjects)
    if not (judges == None or len(judges) == 0):
        df_temp = frame.getJudgesDataFrame(df_temp, judges)
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getFinishedDataFrame(df_temp, finished)
    if not (change == None):
        df_temp = frame.getChangeJudgeDataFrame(df_temp, change)
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getSequencesDataFrame(df_temp, sequences)
    if not (phaseSequences == None or len(phaseSequences) == 0):
        df_temp = frame.getPhaseSequencesDataFrame(df_temp, phaseSequences)
    return df_temp

def displayComparation(df, dateType):
    sections = frame.getSections(df)
    subjects = frame.getSubjects(df)
    judges = frame.getJudges(df)
    sequences = frame.getSequences(df)
    phaseSequences = frame.getPhaseSequences(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('CONFRONTO DURATA MEDIA PROCESSI'),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.RadioItems(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = 'sezione', id = "choice-radioitem", inline = True, style = {'display':'inline'}),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem", inline = True, style = {'padding-left':'85%'}),
        ds.dcc.Graph(id = 'comparation-graph', figure = fig)
    ])
    @app.callback(
        [ds.Output('comparation-graph', 'figure'),
         ds.Output('section-dropdown', 'style'),
         ds.Output('subject-dropdown', 'style'),
         ds.Output('judge-dropdown', 'style'),
         ds.Output('finished-dropdown', 'style'),
         ds.Output('change-dropdown', 'style'),
         ds.Output('sequence-dropdown', 'style'),
         ds.Output('phaseSequence-dropdown', 'style'),
         ds.Output('section-dropdown', 'options'),
         ds.Output('subject-dropdown', 'options'),
         ds.Output('judge-dropdown', 'options'),
         ds.Output('sequence-dropdown', 'options'),
         ds.Output('phaseSequence-dropdown', 'options')],
        [ds.Input('section-dropdown', 'value'),
         ds.Input('subject-dropdown', 'value'),
         ds.Input('judge-dropdown', 'value'),
         ds.Input('finished-dropdown', 'value'),
         ds.Input('change-dropdown', 'value'),
         ds.Input('sequence-dropdown', 'value'),
         ds.Input('phaseSequence-dropdown', 'value'),
         ds.Input('choice-radioitem', 'value'),
         ds.Input('order-radioitem', 'value')]
    )
    def updateOutput(sections, subjects, judges, finished, changes, sequences, phaseSequences, choice, order):
        return comparationUpdate(df, dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choice, order)
    app.run_server(debug = True)

def comparationUpdate(df, dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choice, order):
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences] = hideChosen(choice, sections, subjects, judges, finished, changes, sequences, phaseSequences)
    df_data = df.copy()
    df_data = updateProcessData(df_data, sections, subjects, judges, finished, changes, sequences, phaseSequences)
    df_temp = df.copy()
    if ds.ctx.triggered_id != None and 'section-dropdown' in ds.ctx.triggered_id:
        df_temp = updateProcessData(df_temp, None, subjects, judges, finished, changes, sequences, phaseSequences)
    elif ds.ctx.triggered_id != None and 'subject-dropdown' in ds.ctx.triggered_id:
        df_temp = updateProcessData(df_temp, sections, None, judges, finished, changes, sequences, phaseSequences)
    elif ds.ctx.triggered_id != None and 'judge-dropdown' in ds.ctx.triggered_id:
        df_temp = updateProcessData(df_temp, sections, subjects, None, finished, changes, sequences, phaseSequences)
    elif ds.ctx.triggered_id != None and 'sequence-dropdown' in ds.ctx.triggered_id:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, changes, None, phaseSequences)
    elif ds.ctx.triggered_id != None and 'phaseSequence-dropdown' in ds.ctx.triggered_id:
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, changes, sequences, None)
    else:
        df_temp = df_data
    sections = frame.getSections(df_temp)
    subjects = frame.getSubjects(df_temp)
    judges = frame.getJudges(df_temp)
    sequences = frame.getSequences(df_temp)
    phaseSequences = frame.getPhaseSequences(df_temp)
    [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, dateType, choice, order)
    fig = px.line(allData, x = "data", y = "durata").update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
    fig.add_traces(
        px.line(typeData, x = "data", y = "durata", color = choice, markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600).data
    )
    fig.for_each_trace(
        lambda t: t.update(name = addCountToName(t.name, infoData, choice)) if t.name != addTotCountToName(infoData) else False
    )
    fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
    fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, sequences, phaseSequences