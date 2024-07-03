# this page shows all events.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.EventsGraph as event

# get dataframe with all events. 
df = getter.getAllEvents()
codeEventTag = utilities.getTagName("codeEventTag")
codeStateTag = utilities.getTagName('codeStateTag')

# return initial layout of page.
def pageLayout():
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    dateTag = utilities.getTagName('dateTag') 
    judge = utilities.getPlaceholderName('judge') 
    numProcessTag = utilities.getTagName('numProcessTag')
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    # maxYear is the year of the las registered event. 
    # The time interval selected for initial analysis is the year preceding maxYear.
    # So start date is 1/1/(maxYear - 1) and end date is 1/1/maxYear.
    maxYear = dt.datetime.strptime(df[dateTag].max(), '%Y-%m-%d %H:%M:%S').year
    maxDateStart = dt.date(maxYear - 1, 1, 1)
    maxDateEnd = dt.date(maxYear, 1, 1)
    judges = frame.getGroupBy(df, codeJudgeTag)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    fig = px.scatter(df, x = dateTag, y = numProcessTag, color = codeStateTag, labels = {numProcessTag:'Process ID', dateTag:'Process Start Date'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('EVENTS VISUALIZATION GRAPH', href='/event'),
        ds.html.H2('VISUALIZATION OF ALL PROCESS EVENTS'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-aes',
            start_date = maxDateStart,
            end_date = maxDateEnd,
            min_date_allowed = df[dateTag].min(),
            max_date_allowed = df[dateTag].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = 'reset-button-aes'),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-aes', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-aes', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-aes', placeholder = judge, style = {'width': 400}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-aes')
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('events-graph-aes', 'figure'),
        ds.Output('event-dateranger-aes', 'start_date'), 
        ds.Output('event-dateranger-aes', 'end_date'),
        ds.Output('section-dropdown-aes', 'options'),
        ds.Output('subject-dropdown-aes', 'options'),
        ds.Output('judge-dropdown-aes', 'options')],
    [ds.Input('event-dateranger-aes', 'start_date'), 
        ds.Input('event-dateranger-aes', 'end_date'), 
        ds.Input('event-dateranger-aes', 'min_date_allowed'), 
        ds.Input('event-dateranger-aes', 'max_date_allowed'), 
        ds.Input('reset-button-aes', 'n_clicks'),
        ds.Input('section-dropdown-aes', 'value'),
        ds.Input('subject-dropdown-aes', 'value'),
        ds.Input('judge-dropdown-aes', 'value')])

# return updated data based on user choice.
def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    global df
    # filter important events chosen by user. Those are taken from stored file.
    importantEvents = file.getDataFromTextFile('utils/preferences/importantEvents.txt')
    if importantEvents != None and len(importantEvents) > 0:
        df = df[df[codeEventTag].isin(importantEvents)]
    return event.eventUpdate(df, startDate, endDate, True, codeStateTag, minDate, maxDate, sections, subjects, judges)
