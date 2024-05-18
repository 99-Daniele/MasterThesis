# this page shows processes comparation.

import dash as ds
import datetime as dt
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation

# get dataframe with all processes duration.
df = getter.getProcessesDuration()

# return initial layout of page.
def pageLayout():
    dateTag = df.columns[0]
    sectionTag = df.columns[4]
    subjectTag = df.columns[3]
    judgeTag = df.columns[2]
    finishedTag = df.columns[5]
    sequenceTag = df.columns[6]
    phaseSequenceTag = df.columns[7]
    eventsTag = df.columns[8]
    countTag = 'conteggio'
    importantSubjects = getter.getImportantSubjects()
    subjects = frame.getGroupBy(df, subjectTag, countTag)
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    sections = frame.getGroupBy(df, sectionTag, countTag)
    judges = frame.getGroupBy(df, judgeTag, countTag)
    finished = frame.getGroupBy(df, finishedTag, countTag)
    sequences = frame.getGroupBy(df, sequenceTag, countTag)
    phaseSequences = frame.getGroupBy(df, phaseSequenceTag, countTag)
    events = frame.getGroupByFromString(df, eventsTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI"),        
        ds.dcc.RadioItems(['media', 'mediana'], value = 'media', id = "avg-radioitem-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = 'MESE', id = "date-radioitem-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-pr',
            start_date = df[dateTag].min(),
            end_date = df[dateTag].max(),
            min_date_allowed = df[dateTag].min(),
            max_date_allowed = df[dateTag].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button-pr"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-pr', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-pr', placeholder = 'MATERIA', style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-pr', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-pr', placeholder = 'PROCESSO', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-pr', placeholder = 'SEQUENZA', style = {'width': 400}),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-pr', placeholder = 'FASI', style = {'width': 400}),
        ds.html.Div(children = [
            ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'events-dropdown-pr', placeholder = 'EVENTI', style = {'width': 400}),
            ds.dcc.RadioItems(['CON', 'SENZA'], value = 'CON', id = "events-radioitem-pr", inline = True, style = {'display': 'none'}, inputStyle = {'margin-left': "20px"})
            ],
            style = {'display': 'inline-flex'}
        ),
        ds.dcc.Checklist([sectionTag, subjectTag, judgeTag, finishedTag, sequenceTag, phaseSequenceTag], value = [], id = "choice-checklist-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem-pr", inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist(['TESTO'], value = ['TESTO'], id = "text-checklist-pr"),
        ds.dcc.Graph(id = 'comparation-graph-pr', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-pr', 'figure'),
        ds.Output('event-dateranger-pr', 'start_date'), 
        ds.Output('event-dateranger-pr', 'end_date'),
        ds.Output('section-dropdown-pr', 'style'),
        ds.Output('subject-dropdown-pr', 'style'),
        ds.Output('judge-dropdown-pr', 'style'),
        ds.Output('finished-dropdown-pr', 'style'),
        ds.Output('sequence-dropdown-pr', 'style'),
        ds.Output('phaseSequence-dropdown-pr', 'style'),
        ds.Output('events-dropdown-pr', 'style'),
        ds.Output('events-radioitem-pr', 'style'),
        ds.Output('order-radioitem-pr', 'style'),
        ds.Output('section-dropdown-pr', 'options'),
        ds.Output('subject-dropdown-pr', 'options'),
        ds.Output('judge-dropdown-pr', 'options'),
        ds.Output('finished-dropdown-pr', 'options'),
        ds.Output('sequence-dropdown-pr', 'options'),
        ds.Output('phaseSequence-dropdown-pr', 'options'),
        ds.Output('events-dropdown-pr', 'options'),
        ds.Output('choice-checklist-pr', 'options')],
    [ds.Input('avg-radioitem-pr', 'value'),
        ds.Input('date-radioitem-pr', 'value'),
        ds.Input('event-dateranger-pr', 'start_date'), 
        ds.Input('event-dateranger-pr', 'end_date'), 
        ds.Input('event-dateranger-pr', 'min_date_allowed'), 
        ds.Input('event-dateranger-pr', 'max_date_allowed'), 
        ds.Input('reset-button-pr', 'n_clicks'),
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
        ds.Input('order-radioitem-pr', 'value'),
        ds.Input('text-checklist-pr', 'value')]
    )

# return updated data based on user choice.
def updateOutput(avgChoice, dateType, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, order, text):
    return comparation.processComparationUpdate(df, avgChoice, dateType, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, choices, choicesOptions, order, text)
