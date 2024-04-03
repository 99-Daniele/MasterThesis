import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Utilities as utilities

df = getter.getProcessesDuration()

def pageLayout():
    sections = frame.getSections(df)
    subjects = frame.getSubjects(df)
    judges = frame.getJudges(df)
    sequences = frame.getSequences(df)
    phaseSequences = frame.getPhaseSequences(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INIZIO PROCESSO"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-my', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-my', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-my', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-my', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-my', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-my', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-my', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-my", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store-my"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-my", inline = True, style = {'padding-left':'85%'}),
        ds.dcc.Graph(id = 'comparation-graph-my', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('comparation-graph-my', 'figure'),
        ds.Output('section-dropdown-my', 'style'),
        ds.Output('subject-dropdown-my', 'style'),
        ds.Output('judge-dropdown-my', 'style'),
        ds.Output('finished-dropdown-my', 'style'),
        ds.Output('change-dropdown-my', 'style'),
        ds.Output('sequence-dropdown-my', 'style'),
        ds.Output('phaseSequence-dropdown-my', 'style'),
        ds.Output('section-dropdown-my', 'options'),
        ds.Output('subject-dropdown-my', 'options'),
        ds.Output('judge-dropdown-my', 'options'),
        ds.Output('sequence-dropdown-my', 'options'),
        ds.Output('phaseSequence-dropdown-my', 'options'),
        ds.Output('choice-checklist-my', 'value'),
        ds.Output('choice-store-my', 'data')],
    [ds.Input('section-dropdown-my', 'value'),
        ds.Input('subject-dropdown-my', 'value'),
        ds.Input('judge-dropdown-my', 'value'),
        ds.Input('finished-dropdown-my', 'value'),
        ds.Input('change-dropdown-my', 'value'),
        ds.Input('sequence-dropdown-my', 'value'),
        ds.Input('phaseSequence-dropdown-my', 'value'),
        ds.Input('choice-checklist-my', 'value'),
        ds.Input('choice-store-my', 'data'),
        ds.Input('order-radioitem-my', 'value')]
)

def updateOutput(sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
        return comparation.comparationUpdate(df, "MY", sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order)