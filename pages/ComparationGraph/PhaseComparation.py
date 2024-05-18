# this page shows phases duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation

# get dataframe with all phases duration.
df = getter.getPhasesDuration()
typeTag = 'fase'

# return initial layout of page.
def pageLayout():
    dateTag = df.columns[0]
    sectionTag = df.columns[4]
    subjectTag = df.columns[3]
    judgeTag = df.columns[2]
    finishedTag = df.columns[5]
    countTag = 'conteggio'
    types = frame.getGroupBy(df, typeTag, countTag)
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, sectionTag, countTag)
    importantSubjects = getter.getImportantSubjects()
    subjects = frame.getGroupBy(df, subjectTag, countTag)
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    judges = frame.getGroupBy(df, judgeTag, countTag)
    finished = frame.getGroupBy(df, finishedTag, countTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2('DURATA MEDIA FASI DEL PROCESSO', id = 'title-ph'),
        ds.dcc.RadioItems(['media', 'mediana'], value = 'media', id = 'avg-radioitem-ph', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = 'MESE', id = 'date-radioitem-ph', inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.html.Div(children = [
            ds.dcc.DatePickerRange(
                id = 'event-dateranger-ph',
                start_date = df[dateTag].min(),
                end_date = df[dateTag].max(),
                min_date_allowed = df[dateTag].min(),
                max_date_allowed = df[dateTag].max(),
                display_format = 'DD MM YYYY',
                style = {'width': 300, 'display':'none'}
            ),        
            ds.html.Button("RESET", id = 'reset-button-ph', style = {'display':'none'})
            ],
            style = {'display':'flex'}
        ),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-ph', placeholder = 'FASE', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ph', placeholder = 'SEZIONE', style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ph', placeholder = 'MATERIA', style = {'display': 'none'}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ph', placeholder = 'GIUDICE', style = {'display': 'none'}),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-ph', placeholder = 'PROCESSO', style = {'display': 'none'}),
        ds.dcc.Checklist([sectionTag, subjectTag, judgeTag, finishedTag], value = [], id = 'choice-checklist-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = 'order-radioitem-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.Checklist(['TESTO'], value = ['TESTO'], id = 'text-checklist-ph'),
        ds.dcc.Graph(id = 'comparation-graph-ph', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-ph', 'figure'),
        ds.Output('event-dateranger-ph', 'start_date'), 
        ds.Output('event-dateranger-ph', 'end_date'),
        ds.Output('event-dateranger-ph', 'style'),
        ds.Output('reset-button-ph', 'style'),
        ds.Output('date-radioitem-ph', 'style'),
        ds.Output('section-dropdown-ph', 'style'),
        ds.Output('subject-dropdown-ph', 'style'),
        ds.Output('judge-dropdown-ph', 'style'),
        ds.Output('finished-dropdown-ph', 'style'),
        ds.Output('choice-checklist-ph', 'style'),
        ds.Output('order-radioitem-ph', 'style'),
        ds.Output('section-dropdown-ph', 'options'),
        ds.Output('subject-dropdown-ph', 'options'),
        ds.Output('judge-dropdown-ph', 'options'),
        ds.Output('finished-dropdown-ph', 'options'),
        ds.Output('title-ph', 'children')],
    [ds.Input('type-dropdown-ph', 'value'),
        ds.Input('avg-radioitem-ph', 'value'),
        ds.Input('date-radioitem-ph', 'value'),
        ds.Input('event-dateranger-ph', 'start_date'), 
        ds.Input('event-dateranger-ph', 'end_date'), 
        ds.Input('event-dateranger-ph', 'min_date_allowed'), 
        ds.Input('event-dateranger-ph', 'max_date_allowed'), 
        ds.Input('reset-button-ph', 'n_clicks'),
        ds.Input('section-dropdown-ph', 'value'),
        ds.Input('subject-dropdown-ph', 'value'),
        ds.Input('judge-dropdown-ph', 'value'),
        ds.Input('finished-dropdown-ph', 'value'),
        ds.Input('choice-checklist-ph', 'value'),
        ds.Input('order-radioitem-ph', 'value'),
        ds.Input('text-checklist-ph', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, choices, order, text):
    return comparation.typeComparationUpdate(df, typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, typeTag, sections, subjects, judges, finished, choices, order, text)
