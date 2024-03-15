import dash as ds
import plotly.express as px

import utils.DataFrame as frame
import utils.Legenda as legenda

def addCountToName(name, df, type):
    if type == 'finito':
        count = df[df[type] == int(name)]['size'].item()
        name = legenda.processState[int(name)]
    elif type == 'cambio':
        count = df[df[type] == int(name)]['size'].item()
        if int(name) == 0:
            name = "NO"
        else:
            name = "SI"
    else:
        count = df[df[type] == name]['size'].item()
    newName = name + " (" + str(count) + ")"
    return newName

def addMaxCountToName(df):
    newName = "TUTTI (" + str(df['size'].sum()) + ")"
    return newName

def getPosition(name, df, type):
    pos = df.index.get_loc(df[df[type] == name].index[0])
    return pos

def hideChosen(choice):
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
        case 'materia':
            subjectStyle = {'width': 200, 'display': 'none'}
        case 'giudice':
            judgeStyle = {'width': 200, 'display': 'none'}
        case 'finito':
            finishedStyle = {'width': 200, 'display': 'none'}
        case 'cambio':
            changeStyle = {'width': 200, 'display': 'none'}
        case 'sequenza':
            sequenceStyle = {'width': 200, 'display': 'none'}
        case 'fasi':
            phaseSequenceStyle = {'width': 200, 'display': 'none'}
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle]

def updateProcessData(df, sections, subjects, judges, finished, change, sequences, phaseSequences):
    df_temp = df
    if not (sections == None or len(sequences) == 0):
        df_temp = frame.getSectionsdDataFrame(df_temp, sections)
    if not (subjects == None or len(subjects) == 0):
        df_temp = frame.getSubjectsdDataFrame(df_temp, subjects)
    if not (judges == None or len(judges) == 0):
        df_temp = frame.getJudgesdDataFrame(df_temp, judges)
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getFinishedDataFrame(df_temp, finished)
    if not (change == None):
        df_temp = frame.getChangeJudgeDataFrame(df_temp, change)
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getSequencesDataFrame(df_temp, sequences)
    if not (phaseSequences == None or len(phaseSequences) == 0):
        df_temp = frame.getPhaseSequencesDataFrame(df_temp, phaseSequences)
    return df_temp

def displayComparation(df, dateType, title):
    df_temp = df.copy()
    sections = frame.getTop20Sections(df_temp)
    subjects = frame.getTop20Subjects(df_temp)
    judges = frame.getTop20Judges(df_temp)
    sequences = frame.getTop20Sequences(df_temp)
    phaseSequences = frame.getTop20PhaseSequences(df_temp)
    [typeData, allData, countData] = frame.getAvgDataFrameByType(df_temp, dateType, 'sezione')
    fig = px.line(typeData, x = "data", y = "durata", color = "sezione", markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, title = title, width = 1400, height = 600)
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.RadioItems(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = 'sezione', id = "choice-radioitem", inline = True),
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
         ds.Input('choice-radioitem', 'value')]
    )
    def update_output(sections, subjects, judges, finished, changes, sequences, phaseSequences, choice):
        [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle] = hideChosen(choice)
        df_temp = df.copy()
        df_temp = updateProcessData(df_temp, sections, subjects, judges, finished, changes, sequences, phaseSequences)
        sections = frame.getTop20Sections(df_temp)
        subjects = frame.getTop20Subjects(df_temp)
        judges = frame.getTop20Judges(df_temp)
        sequences = frame.getTop20Sequences(df_temp)
        phaseSequences = frame.getTop20PhaseSequences(df_temp)
        [typeData, allData, countData] = frame.getAvgDataFrameByType(df_temp, dateType, choice)
        fig = px.line(typeData, x = "data", y = "durata", color = choice, markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, title = title, width = 1400, height = 600)
        fig.update_traces(visible = "legendonly", selector = (lambda t: t))
        fig.for_each_trace(
            lambda t: t.update(
                name = addCountToName(t.name, countData, choice)
            )
        )
        fig.add_traces(
            px.line(allData, x = "data", y = "durata").update_traces(showlegend = True, name = addMaxCountToName(countData), line_color = 'rgb(0, 0, 0)', line = {'width': 3}).data
        )
        fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, sequences, phaseSequences
    
    app.run_server(debug = True)