import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getPhasesDuration()

def pageLayout():
    types = frame.getGroupBy(df, 'fase')
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA FASI DEL PROCESSO'),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-p', placeholder = 'FASE', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-p', placeholder = 'SEZIONE', style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-p', placeholder = 'MATERIA', style = {'display': 'none'}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-p', placeholder = 'GIUDICE', style = {'display': 'none'}),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-p', placeholder = 'PROCESSO', style = {'display': 'none'}),
        ds.dcc.Dropdown(utilities.months, multi = True, searchable = False, id = 'month-dropdown-p', placeholder = 'MESE INIZIO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-p', placeholder = 'CAMBIO', style = {'display': 'none'}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-p", inline = True, style = {'display': 'none'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store-p"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-p", inline = True, style = {'display': 'none'}),
        ds.dcc.Graph(id = 'comparation-graph-p', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('comparation-graph-p', 'figure'),
        ds.Output('section-dropdown-p', 'style'),
        ds.Output('subject-dropdown-p', 'style'),
        ds.Output('judge-dropdown-p', 'style'),
        ds.Output('finished-dropdown-p', 'style'),
        ds.Output('change-dropdown-p', 'style'),
        ds.Output('section-dropdown-p', 'options'),
        ds.Output('subject-dropdown-p', 'options'),
        ds.Output('judge-dropdown-p', 'options'),
        ds.Output('choice-checklist-p', 'value'),
        ds.Output('choice-store-p', 'data')],
    [ds.Input('type-dropdown-p', 'value'),
        ds.Input('section-dropdown-p', 'value'),
        ds.Input('subject-dropdown-p', 'value'),
        ds.Input('judge-dropdown-p', 'value'),
        ds.Input('finished-dropdown-p', 'value'),
        ds.Input('change-dropdown-p', 'value'),
        ds.Input('choice-checklist-p', 'value'),
        ds.Input('choice-store-p', 'data'),
        ds.Input('order-radioitem-p', 'value')]
)

def updateOutput(typeChoice, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    return duration.typeUpdate(df, "M", typeChoice, 'fase', sections, subjects, judges, finished, changes, choices, choiceStore, order)
