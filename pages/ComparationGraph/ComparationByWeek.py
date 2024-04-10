import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Utilities as utilities

df = getter.getProcessesDuration()

def pageLayout():
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    subjects = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI IN BASE ALLA SETTIMANA DI INIZIO PROCESSO"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-w', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-w', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-w', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-w', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-w', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-w', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-w', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-w", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store-w"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-w", inline = True, style = {'paddingLeft':'85%'}),
        ds.dcc.Graph(id = 'comparation-graph-w', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('comparation-graph-w', 'figure'),
        ds.Output('section-dropdown-w', 'style'),
        ds.Output('subject-dropdown-w', 'style'),
        ds.Output('judge-dropdown-w', 'style'),
        ds.Output('finished-dropdown-w', 'style'),
        ds.Output('change-dropdown-w', 'style'),
        ds.Output('sequence-dropdown-w', 'style'),
        ds.Output('phaseSequence-dropdown-w', 'style'),
        ds.Output('section-dropdown-w', 'options'),
        ds.Output('subject-dropdown-w', 'options'),
        ds.Output('judge-dropdown-w', 'options'),
        ds.Output('sequence-dropdown-w', 'options'),
        ds.Output('phaseSequence-dropdown-w', 'options'),
        ds.Output('choice-checklist-w', 'value'),
        ds.Output('choice-store-w', 'data')],
    [ds.Input('section-dropdown-w', 'value'),
        ds.Input('subject-dropdown-w', 'value'),
        ds.Input('judge-dropdown-w', 'value'),
        ds.Input('finished-dropdown-w', 'value'),
        ds.Input('change-dropdown-w', 'value'),
        ds.Input('sequence-dropdown-w', 'value'),
        ds.Input('phaseSequence-dropdown-w', 'value'),
        ds.Input('choice-checklist-w', 'value'),
        ds.Input('choice-store-w', 'data'),
        ds.Input('order-radioitem-w', 'value')]
)

def updateOutput(sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
        return comparation.comparationUpdate(df, "W", sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order)