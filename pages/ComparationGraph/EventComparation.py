# this page shows events duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation

# get dataframe with all events duration.
df = getter.getEventsDuration()
typeTag = 'evento'

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
        ds.html.H2('DURATA MEDIA EVENTI DEL PROCESSO', id = 'title-e'),
        ds.dcc.RadioItems(['media', 'mediana'], value = 'media', id = 'avg-radioitem-e', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = 'MESE', id = 'date-radioitem-e', inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.html.Div(children = [
            ds.dcc.DatePickerRange(
                id = 'event-dateranger-e',
                start_date = df[dateTag].min(),
                end_date = df[dateTag].max(),
                min_date_allowed = df[dateTag].min(),
                max_date_allowed = df[dateTag].max(),
                display_format = 'DD MM YYYY',
                style = {'width': 300, 'display':'none'}
            ),        
            ds.html.Button("RESET", id = 'reset-button-e', style = {'display':'none'})
            ],
            style = {'display':'flex'}
        ),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-e', placeholder = 'EVENTO', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-e', placeholder = 'SEZIONE', style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-e', placeholder = 'MATERIA', style = {'display': 'none'}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-e', placeholder = 'GIUDICE', style = {'display': 'none'}),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-e', placeholder = 'PROCESSO', style = {'display': 'none'}),
        ds.dcc.Checklist([sectionTag, subjectTag, judgeTag, finishedTag], value = [], id = 'choice-checklist-e', inline = True, style = {'display': 'none'}),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = 'order-radioitem-e', inline = True, style = {'display': 'none'}),
        ds.dcc.Checklist(['TESTO'], value = ['TESTO'], id = 'text-checklist-e'),
        ds.dcc.Graph(id = 'comparation-graph-e', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-e', 'figure'),
        ds.Output('event-dateranger-e', 'start_date'), 
        ds.Output('event-dateranger-e', 'end_date'),
        ds.Output('event-dateranger-e', 'style'),
        ds.Output('reset-button-e', 'style'),
        ds.Output('date-radioitem-e', 'style'),
        ds.Output('section-dropdown-e', 'style'),
        ds.Output('subject-dropdown-e', 'style'),
        ds.Output('judge-dropdown-e', 'style'),
        ds.Output('finished-dropdown-e', 'style'),
        ds.Output('choice-checklist-e', 'style'),
        ds.Output('order-radioitem-e', 'style'),
        ds.Output('section-dropdown-e', 'options'),
        ds.Output('subject-dropdown-e', 'options'),
        ds.Output('judge-dropdown-e', 'options'),
        ds.Output('finished-dropdown-e', 'options'),
        ds.Output('title-e', 'children')],
    [ds.Input('type-dropdown-e', 'value'),
        ds.Input('avg-radioitem-e', 'value'),
        ds.Input('date-radioitem-e', 'value'),
        ds.Input('event-dateranger-e', 'start_date'), 
        ds.Input('event-dateranger-e', 'end_date'), 
        ds.Input('event-dateranger-e', 'min_date_allowed'), 
        ds.Input('event-dateranger-e', 'max_date_allowed'), 
        ds.Input('reset-button-e', 'n_clicks'),
        ds.Input('section-dropdown-e', 'value'),
        ds.Input('subject-dropdown-e', 'value'),
        ds.Input('judge-dropdown-e', 'value'),
        ds.Input('finished-dropdown-e', 'value'),
        ds.Input('choice-checklist-e', 'value'),
        ds.Input('order-radioitem-e', 'value'),
        ds.Input('text-checklist-e', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, choices, order, text):
    return comparation.typeComparationUpdate(df, typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, typeTag, sections, subjects, judges, finished, choices, order, text)
