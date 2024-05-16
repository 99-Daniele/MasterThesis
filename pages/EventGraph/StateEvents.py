# this page shows state events.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.EventsGraph as event

# get dataframe with state events. 
# get sections, subject, judges based on dataframe events.
# get maxYear as the maximum year belong dataframe events and calc maxDateStart and maxDateEnd as the first and last date of the maximun 1-year interval.
# get must states from text file.
df = getter.getStateEvents()
try:
    mustStates = file.getDataFromTextFile('preferences/mustStates.txt')
except:
    mustStates = None

# return initial layout of page.
def pageLayout():
    dateTag = df.columns[0]
    numProcessTag = df.columns[1]
    eventTag = df.columns[3]
    sectionTag = df.columns[8]
    subjectTag = df.columns[9]
    judgeTag = df.columns[7]
    countTag = 'conteggio'
    maxYear = dt.datetime.strptime(df[dateTag].max(), '%Y-%m-%d %H:%M:%S').year
    maxDateStart = dt.date(maxYear - 1, 1, 1)
    maxDateEnd = dt.date(maxYear, 1, 1)
    sections = frame.getGroupBy(df, sectionTag, countTag)
    subjects = frame.getGroupBy(df, subjectTag, countTag)
    judges = frame.getGroupBy(df, judgeTag, countTag)
    fig = px.scatter(df, x = dateTag, y = numProcessTag, color = eventTag, labels = {numProcessTag:'Codice Processo', dateTag:'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2('TUTTI GLI EVENTI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-se',
            start_date = maxDateStart,
            end_date = maxDateEnd,
            min_date_allowed = df[dateTag].min(),
            max_date_allowed = df[dateTag].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = 'reset-button-se'),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-se', placeholder = 'SEZIONE', style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-se', placeholder = 'MATERIA', style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-se', placeholder = 'GIUDICE', style = {'width': 400}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-se')
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('events-graph-se', 'figure'),
        ds.Output('event-dateranger-se', 'start_date'), 
        ds.Output('event-dateranger-se', 'end_date'),
        ds.Output('section-dropdown-se', 'options'),
        ds.Output('subject-dropdown-se', 'options'),
        ds.Output('judge-dropdown-se', 'options')],
    [ds.Input('event-dateranger-se', 'start_date'), 
        ds.Input('event-dateranger-se', 'end_date'), 
        ds.Input('event-dateranger-se', 'min_date_allowed'), 
        ds.Input('event-dateranger-se', 'max_date_allowed'), 
        ds.Input('reset-button-se', 'n_clicks'),
        ds.Input('section-dropdown-se', 'value'),
        ds.Input('subject-dropdown-se', 'value'),
        ds.Input('judge-dropdown-se', 'value')])

# return updated data based on user choice.
def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    return event.eventUpdate(df, startDate, endDate, 'stato', mustStates, minDate, maxDate, sections, subjects, judges)
