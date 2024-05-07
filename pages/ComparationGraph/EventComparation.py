# this page shows events duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Utilities.Utilities as utilities

# get dataframe with all events duration.
df = getter.getEventsDuration()

# return initial layout of page.
def pageLayout():
    types = frame.getGroupBy(df, 'evento')
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, 'sezione')
    try:
        importantSubjects = file.getDataFromTextFile('preferences/importantSubjects.txt')
    except:
        importantSubjects = None
    subjects = frame.getGroupBy(df, 'materia')
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    judges = frame.getGroupBy(df, 'giudice')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2('DURATA MEDIA EVENTI DEL PROCESSO', id = 'title-e'),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-e", inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'MESE', id = "date-store-e"),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-e', placeholder = 'EVENTO', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-e', placeholder = 'SEZIONE', style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-e', placeholder = 'MATERIA', style = {'display': 'none'}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-e', placeholder = 'GIUDICE', style = {'display': 'none'}),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-e', placeholder = 'PROCESSO', style = {'display': 'none'}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-e', placeholder = 'CAMBIO', style = {'display': 'none'}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio'], value = ['sezione'], id = 'choice-checklist-e', inline = True, style = {'display': 'none'}),
        ds.dcc.Store(data = ['sezione'], id = 'choice-store-e'),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = 'order-radioitem-e', inline = True, style = {'display': 'none'}),
        ds.dcc.Graph(id = 'comparation-graph-e', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-e', 'figure'),
        ds.Output('date-checklist-e', 'value'),
        ds.Output('date-store-e', 'data'),
        ds.Output('date-checklist-e', 'style'),
        ds.Output('section-dropdown-e', 'style'),
        ds.Output('subject-dropdown-e', 'style'),
        ds.Output('judge-dropdown-e', 'style'),
        ds.Output('finished-dropdown-e', 'style'),
        ds.Output('change-dropdown-e', 'style'),
        ds.Output('choice-checklist-e', 'style'),
        ds.Output('order-radioitem-e', 'style'),
        ds.Output('section-dropdown-e', 'options'),
        ds.Output('subject-dropdown-e', 'options'),
        ds.Output('judge-dropdown-e', 'options'),
        ds.Output('finished-dropdown-e', 'options'),
        ds.Output('change-dropdown-e', 'options'),
        ds.Output('choice-checklist-e', 'value'),
        ds.Output('choice-store-e', 'data'),
        ds.Output('title-e', 'children')],
    [ds.Input('type-dropdown-e', 'value'),
        ds.Input('date-checklist-e', 'value'),
        ds.Input('date-store-e', 'data'),
        ds.Input('section-dropdown-e', 'value'),
        ds.Input('subject-dropdown-e', 'value'),
        ds.Input('judge-dropdown-e', 'value'),
        ds.Input('finished-dropdown-e', 'value'),
        ds.Input('change-dropdown-e', 'value'),
        ds.Input('choice-checklist-e', 'value'),
        ds.Input('choice-store-e', 'data'),
        ds.Input('order-radioitem-e', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, typeDate, typeDateStore, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    return comparation.typeComparationUpdate(df, typeDate, typeDateStore, typeChoice, 'evento', sections, subjects, judges, finished, changes, choices, choiceStore, order)
