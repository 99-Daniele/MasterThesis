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
    sequences = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DI INIZIO PROCESSO"),
        ds.dcc.Dropdown(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = "MESE", multi = False, searchable = False, id = 'date-dropdown', placeholder = 'PERIODO', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem", inline = True, style = {'paddingLeft':'85%'}),
        ds.dcc.Graph(id = 'comparation-graph', figure = fig)
    ])
    return layout

@ds.callback(
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
        ds.Output('finished-dropdown', 'options'),
        ds.Output('change-dropdown', 'options'),
        ds.Output('sequence-dropdown', 'options'),
        ds.Output('phaseSequence-dropdown', 'options'),
        ds.Output('choice-checklist', 'value'),
        ds.Output('choice-store', 'data')],
    [ds.Input('date-dropdown', 'value'),
        ds.Input('section-dropdown', 'value'),
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

def updateOutput(dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order):
    return comparation.comparationUpdate(df, dateType, sections, subjects, judges, finished, changes, sequences, phaseSequences, choices, choiceStore, order)
