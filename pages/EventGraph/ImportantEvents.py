# this page shows important events.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.EventsGraph as event

# get dataframe with important events. 
# get sections, subject, judges based on dataframe events.
# get maxYear as the maximum year belong dataframe events and calc maxDateStart and maxDateEnd as the first and last date of the maximun 1-year interval.
# get must events from text file.
df = getter.getImportantEvents()
try:
    mustEvents = file.getDataFromTextFile('preferences/mustEvents.txt')
except:
    mustEvents = None

# return initial layout of page.
def pageLayout():
    sections = frame.getGroupBy(df, 'sezione', 'conteggio')
    subjects = frame.getGroupBy(df, 'materia', 'conteggio')
    judges = frame.getGroupBy(df, 'giudice', 'conteggio')
    maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
    maxDateStart = dt.date(maxYear - 1, 1, 1)
    maxDateEnd = dt.date(maxYear, 1, 1)
    fig = px.scatter(df, x = "data", y = "numProcesso", color = 'evento', labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2('EVENTI IMPORTANTI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-ie',
            start_date = maxDateStart,
            end_date = maxDateEnd,
            min_date_allowed = df['data'].min(),
            max_date_allowed = df['data'].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button-ie"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ie', placeholder = 'SEZIONE', style = {'width': 285}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ie', placeholder = 'MATERIA', style = {'width': 285}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ie', placeholder = 'GIUDICE', style = {'width': 285}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-ie')
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('events-graph-ie', 'figure'),
        ds.Output('event-dateranger-ie', 'start_date'), 
        ds.Output('event-dateranger-ie', 'end_date'),
        ds.Output('section-dropdown-ie', 'options'),
        ds.Output('subject-dropdown-ie', 'options'),
        ds.Output('judge-dropdown-ie', 'options')],
    [ds.Input('event-dateranger-ie', 'start_date'), 
        ds.Input('event-dateranger-ie', 'end_date'), 
        ds.Input('event-dateranger-ie', 'min_date_allowed'), 
        ds.Input('event-dateranger-ie', 'max_date_allowed'), 
        ds.Input('reset-button-ie', 'n_clicks'),
        ds.Input('section-dropdown-ie', 'value'),
        ds.Input('subject-dropdown-ie', 'value'),
        ds.Input('judge-dropdown-ie', 'value')])

# return updated data based on user choice.
def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    return event.eventUpdate(df, startDate, endDate, 'evento', mustEvents, minDate, maxDate, sections, subjects, judges)
