# this page shows processes comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation

# get dataframe with all processes duration.
df = getter.getProcessesDuration()

# return initial layout of page.
def pageLayout():
    importantSubjects = getter.getImportantSubjects()
    subjects = frame.getGroupBy(df, 'materia')
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    sections = frame.getGroupBy(df, 'sezione')
    judges = frame.getGroupBy(df, 'giudice')
    finished = frame.getGroupBy(df, 'finito')
    sequences = frame.getGroupBy(df, 'sequenza')
    phaseSequences = frame.getGroupBy(df, 'fasi')
    events = frame.getGroupByFromString(df, 'eventi')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI"),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'MESE', id = "date-store-pr"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-pr', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-pr', placeholder = 'MATERIA', style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-pr', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-pr', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-pr', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-pr', placeholder = 'FASI', style = {'width': 400}),
        ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'events-dropdown-pr', placeholder = 'EVENTI', style = {'width': 400}),
        ds.dcc.RadioItems(['CON', 'SENZA'], value = 'CON', id = "events-radioitem-pr", inline = True, style = {'display': 'none'}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'sequenza', 'fasi'], value = ['sezione'], id = "choice-checklist-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'sezione', id = "choice-store-pr"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Graph(id = 'comparation-graph-pr', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-pr', 'figure'),
        ds.Output('date-checklist-pr', 'value'),
        ds.Output('date-store-pr', 'data'),
        ds.Output('section-dropdown-pr', 'style'),
        ds.Output('subject-dropdown-pr', 'style'),
        ds.Output('judge-dropdown-pr', 'style'),
        ds.Output('finished-dropdown-pr', 'style'),
        ds.Output('sequence-dropdown-pr', 'style'),
        ds.Output('phaseSequence-dropdown-pr', 'style'),
        ds.Output('events-dropdown-pr', 'style'),
        ds.Output('events-radioitem-pr', 'style'),
        ds.Output('section-dropdown-pr', 'options'),
        ds.Output('subject-dropdown-pr', 'options'),
        ds.Output('judge-dropdown-pr', 'options'),
        ds.Output('finished-dropdown-pr', 'options'),
        ds.Output('sequence-dropdown-pr', 'options'),
        ds.Output('phaseSequence-dropdown-pr', 'options'),
        ds.Output('events-dropdown-pr', 'options'),
        ds.Output('choice-checklist-pr', 'value'),
        ds.Output('choice-checklist-pr', 'options'),
        ds.Output('choice-store-pr', 'data')],
    [ds.Input('date-checklist-pr', 'value'),
        ds.Input('date-store-pr', 'data'),
        ds.Input('section-dropdown-pr', 'value'),
        ds.Input('subject-dropdown-pr', 'value'),
        ds.Input('judge-dropdown-pr', 'value'),
        ds.Input('finished-dropdown-pr', 'value'),
        ds.Input('sequence-dropdown-pr', 'value'),
        ds.Input('phaseSequence-dropdown-pr', 'value'),
        ds.Input('events-dropdown-pr', 'value'),
        ds.Input('events-radioitem-pr', 'value'),
        ds.Input('choice-checklist-pr', 'value'),
        ds.Input('choice-checklist-pr', 'options'),
        ds.Input('choice-store-pr', 'data'),
        ds.Input('order-radioitem-pr', 'value')]
    )

# return updated data based on user choice.
def updateOutput(dateType, dateTypeStore, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, choiceStore, order):
    return comparation.processComparationUpdate(df, dateType, dateTypeStore, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, choiceStore, order)
