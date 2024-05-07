# this page shows phases duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Utilities.Utilities as utilities

# get dataframe with all phases duration.
df = getter.getPhasesDuration()

# return initial layout of page.
def pageLayout():
    types = frame.getGroupBy(df, 'fase')
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
        ds.html.H2('DURATA MEDIA FASI DEL PROCESSO', id = 'title-ph'),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-ph", inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'MESE', id = "date-store-ph"),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-ph', placeholder = 'FASE', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ph', placeholder = 'SEZIONE', style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ph', placeholder = 'MATERIA', style = {'display': 'none'}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ph', placeholder = 'GIUDICE', style = {'display': 'none'}),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-ph', placeholder = 'PROCESSO', style = {'display': 'none'}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-ph', placeholder = 'CAMBIO', style = {'display': 'none'}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio'], value = ['sezione'], id = 'choice-checklist-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.Store(data = ['sezione'], id = 'choice-store-ph'),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = 'order-radioitem-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.Graph(id = 'comparation-graph-ph', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-ph', 'figure'),
        ds.Output('date-checklist-ph', 'value'),
        ds.Output('date-store-ph', 'data'),
        ds.Output('date-checklist-ph', 'style'),
        ds.Output('section-dropdown-ph', 'style'),
        ds.Output('subject-dropdown-ph', 'style'),
        ds.Output('judge-dropdown-ph', 'style'),
        ds.Output('finished-dropdown-ph', 'style'),
        ds.Output('change-dropdown-ph', 'style'),
        ds.Output('choice-checklist-ph', 'style'),
        ds.Output('order-radioitem-ph', 'style'),
        ds.Output('section-dropdown-ph', 'options'),
        ds.Output('subject-dropdown-ph', 'options'),
        ds.Output('judge-dropdown-ph', 'options'),
        ds.Output('finished-dropdown-ph', 'options'),
        ds.Output('change-dropdown-ph', 'options'),
        ds.Output('choice-checklist-ph', 'value'),
        ds.Output('choice-store-ph', 'data'),
        ds.Output('title-ph', 'children')],
    [ds.Input('type-dropdown-ph', 'value'),
        ds.Input('date-checklist-ph', 'value'),
        ds.Input('date-store-ph', 'data'),
        ds.Input('section-dropdown-ph', 'value'),
        ds.Input('subject-dropdown-ph', 'value'),
        ds.Input('judge-dropdown-ph', 'value'),
        ds.Input('finished-dropdown-ph', 'value'),
        ds.Input('change-dropdown-ph', 'value'),
        ds.Input('choice-checklist-ph', 'value'),
        ds.Input('choice-store-ph', 'data'),
        ds.Input('order-radioitem-ph', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, typeDate, typeDateStore, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    return comparation.typeComparationUpdate(df, typeDate, typeDateStore, typeChoice, 'fase', sections, subjects, judges, finished, changes, choices, choiceStore, order)
