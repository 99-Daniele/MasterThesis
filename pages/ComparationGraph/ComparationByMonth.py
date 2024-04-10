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
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DI INIZIO PROCESSO"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-m', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-m', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-m', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-m', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-m', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-m', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-m', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-m", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store-m"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-m", inline = True, style = {'paddingLeft':'85%'}),

        ds.dcc.Graph(id = 'comparation-graph-m', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('comparation-graph-m', 'figure'),
        ds.Output('section-dropdown-m', 'style'),
        ds.Output('subject-dropdown-m', 'style'),
        ds.Output('judge-dropdown-m', 'style'),
        ds.Output('finished-dropdown-m', 'style'),
        ds.Output('change-dropdown-m', 'style'),
        ds.Output('sequence-dropdown-m', 'style'),
        ds.Output('phaseSequence-dropdown-m', 'style'),
        ds.Output('section-dropdown-m', 'options'),
        ds.Output('subject-dropdown-m', 'options'),
        ds.Output('judge-dropdown-m', 'options'),
        ds.Output('sequence-dropdown-m', 'options'),
        ds.Output('phaseSequence-dropdown-m', 'options'),
        ds.Output('choice-checklist-m', 'value'),
        ds.Output('choice-store-m', 'data')],
    [ds.Input('section-dropdown-m', 'value'),
        ds.Input('subject-dropdown-m', 'value'),
        ds.Input('judge-dropdown-m', 'value'),
        ds.Input('finished-dropdown-m', 'value'),
        ds.Input('change-dropdown-m', 'value'),
        ds.Input('sequence-dropdown-m', 'value'),
        ds.Input('phaseSequence-dropdown-m', 'value'),
        ds.Input('choice-checklist-m', 'value'),
        ds.Input('choice-store-m', 'data'),
        ds.Input('order-radioitem-m', 'value')]
)

def updateOutput(sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
        return comparation.comparationUpdate(df, "M", sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order)