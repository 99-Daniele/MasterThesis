import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Utilities as utilities

df = getter.getStatesDuration()

def pageLayout():
    types = frame.getGroupBy(df, 'stato')
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2('CONFRONTO DURATA MEDIA STATI DEL PROCESSO'), ds.dcc.Dropdown(typesSorted, value = typesSorted[0], multi = False, searchable = False, id = 'type-dropdown-s', placeholder = 'FASE', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-s', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-s', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-s', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-s', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-s', placeholder = 'CAMBIO', style = {'width': 400}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-s", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store-s"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-s", inline = True, style = {'paddingLeft':'85%'}),
        ds.dcc.Graph(id = 'comparation-graph-s', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('comparation-graph-s', 'figure'),
        ds.Output('section-dropdown-s', 'style'),
        ds.Output('subject-dropdown-s', 'style'),
        ds.Output('judge-dropdown-s', 'style'),
        ds.Output('finished-dropdown-s', 'style'),
        ds.Output('change-dropdown-s', 'style'),
        ds.Output('section-dropdown-s', 'options'),
        ds.Output('subject-dropdown-s', 'options'),
        ds.Output('judge-dropdown-s', 'options'),
        ds.Output('choice-checklist-s', 'value'),
        ds.Output('choice-store-s', 'data')],
    [ds.Input('type-dropdown-s', 'value'),
        ds.Input('section-dropdown-s', 'value'),
        ds.Input('subject-dropdown-s', 'value'),
        ds.Input('judge-dropdown-s', 'value'),
        ds.Input('finished-dropdown-s', 'value'),
        ds.Input('change-dropdown-s', 'value'),
        ds.Input('choice-checklist-s', 'value'),
        ds.Input('choice-store-s', 'data'),
        ds.Input('order-radioitem-s', 'value')]
)

def updateOutput(typeChoice, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    return comparation.typeComparationUpdate(df, "M", typeChoice, 'stato', sections, subjects, judges, finished, changes, choices, choiceStore, order)
