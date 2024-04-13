import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def addCountToName(name, df, choices):
    if choices == 'finito':
        count = df[df[type] == int(name)]['conteggio'].item()
        name = utilities.processState[int(name)]
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

def hideChosen(choices, sections, subjects, judges, finished, changes, sequences, phaseSequences):
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
    if 'sezione' in choices:
        sectionStyle = {'width': 200, 'display': 'none'}
        sections = None
    if 'materia' in choices:
        subjectStyle = {'width': 200, 'display': 'none'}
        subjects = None
    if 'giudice' in choices:
        judgeStyle = {'width': 200, 'display': 'none'}
        judges = None
    if 'finito' in choices:
        finishedStyle = {'width': 200, 'display': 'none'}
        finished = None
    if 'cambio' in choices:
        changeStyle = {'width': 200, 'display': 'none'}
        changes = None
    if 'sequenza' in choices:
        sequenceStyle = {'width': 200, 'display': 'none'}
        sequences = None
    if 'fasi' in choices:
        phaseSequenceStyle = {'width': 200, 'display': 'none'}
        phaseSequences = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences]

def updateProcessData(df, sections, subjects, judges, finished, change, sequences, phaseSequences):
    df_temp = df
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phaseSequences)
    return df_temp

def displayComparation(df, dateType):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    sequences = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
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
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem", inline = True, style = {'paddingLeft':'85%'}),
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
         ds.Output('phaseSequence-dropdown', 'options'),
         ds.Output('choice-checklist', 'value'),
         ds.Output('choice-store', 'data')],
        [ds.Input('section-dropdown', 'value'),
         ds.Input('subject-dropdown', 'value'),
         ds.Input('judge-dropdown', 'value'),
         ds.Input('finished-dropdown', 'value'),
         ds.Input('change-dropdown', 'value'),
         ds.Input('sequence-dropdown', 'value'),
         ds.Input('phaseSequence-dropdown', 'value'),
         ds.Input('choice-checklist', 'value'),
         ds.Input('choice-store', 'data'),
         ds.Input('order-radioitem', 'value')]
    )
    def updateOutput(sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
        return comparationUpdate(df, dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order)
    app.run_server(debug = True)

def comparationUpdate(df, dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
    if len(choices) < 1:
        choices = [choiceStore]
    elif len(choices) == 1:
        choiceStore = choices[0]
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, finished, changes, sequences, phaseSequences] = hideChosen(choices, sections, subjects, judges, finished, changes, sequences, phaseSequences)
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
    sections = frame.getGroupBy(df_temp, 'sezione')
    subjects = frame.getGroupBy(df_temp, 'materia')
    judges = frame.getGroupBy(df_temp, 'giudice')
    subjects = frame.getGroupBy(df_temp, 'sequenza')
    phaseSequences = frame.getGroupBy(df_temp, 'fasi')
    [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, dateType, choices, order)
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
    return fig, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, sequenceStyle, phaseSequenceStyle, sections, subjects, judges, sequences, phaseSequences, choices, choiceStore