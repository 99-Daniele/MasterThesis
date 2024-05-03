# this page shows all events.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.EventsGraph as event

# get dataframe with all events. 
# get maxYear as the maximum year belong dataframe events and calc maxDateStart and maxDateEnd as the first and last date of the maximun 1-year interval.
# get important events from text file.
df = getter.getAllEvents()
maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
maxDateStart = dt.date(maxYear - 1, 1, 1)
maxDateEnd = dt.date(maxYear, 1, 1)
try:
    importantEvents = file.getDataFromTextFile('utils/Preferences/importantEvents.txt')
except:
    importantEvents = None

# return initial layout of page.
def pageLayout():
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    fig = px.scatter(df, x = "data", y = "numProcesso", color = 'evento', labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2('TUTTI GLI EVENTI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-ae',
            start_date = maxDateStart,
            end_date = maxDateEnd,
            min_date_allowed = df['data'].min(),
            max_date_allowed = df['data'].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button-ae"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ae', placeholder = 'SEZIONE', style = {'width': 285}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ae', placeholder = 'MATERIA', style = {'width': 285}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ae', placeholder = 'GIUDICE', style = {'width': 285}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-ae')
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('events-graph-ae', 'figure'),
        ds.Output('event-dateranger-ae', 'start_date'), 
        ds.Output('event-dateranger-ae', 'end_date'),
        ds.Output('section-dropdown-ae', 'options'),
        ds.Output('subject-dropdown-ae', 'options'),
        ds.Output('judge-dropdown-ae', 'options')],
    [ds.Input('event-dateranger-ae', 'start_date'), 
        ds.Input('event-dateranger-ae', 'end_date'), 
        ds.Input('event-dateranger-ae', 'min_date_allowed'), 
        ds.Input('event-dateranger-ae', 'max_date_allowed'), 
        ds.Input('reset-button-ae', 'n_clicks'),
        ds.Input('section-dropdown-ae', 'value'),
        ds.Input('subject-dropdown-ae', 'value'),
        ds.Input('judge-dropdown-ae', 'value')])

# return updated data based on user choice.
def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    return event.eventUpdate(df, startDate, endDate, 'evento', importantEvents, minDate, maxDate, sections, subjects, judges)
