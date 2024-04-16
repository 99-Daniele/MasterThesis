import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.EventsGraph as event

df = getter.getAllEvents()
maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
minYear = maxYear - 1
importantEvents = file.getDataFromTextFile('utils/Preferences/importantEvents.txt')

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
            start_date = dt.date(minYear, 1, 1),
            end_date = dt.date(maxYear, 1, 1),
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

def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    return event.eventUpdate(df, startDate, endDate, 'evento', importantEvents, minDate, maxDate, sections, subjects, judges)
