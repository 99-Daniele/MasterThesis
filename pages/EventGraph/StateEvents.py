import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Graph.EventsGraph as event

df = getter.getStateEvents()
sections = frame.getGroupBy(df, 'sezione')
subjects = frame.getGroupBy(df, 'materia')
judges = frame.getGroupBy(df, 'giudice')
maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
minYear = maxYear - 1
mustStates = file.getDataFromTextFile('utils/Preferences/mustStates.txt')

def pageLayout():
    fig = px.scatter(df, x = "data", y = "numProcesso", color = 'evento', labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2('EVENTI INIZIO STATI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-se',
            start_date = dt.date(minYear, 1, 1),
            end_date = dt.date(maxYear, 1, 1),
            min_date_allowed = df['data'].min(),
            max_date_allowed = df['data'].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button-se"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-se', placeholder = 'SEZIONE', style = {'width': 285}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-se', placeholder = 'MATERIA', style = {'width': 285}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-se', placeholder = 'GIUDICE', style = {'width': 285}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-se')
    ])
    return layout

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

def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    return event.eventUpdate(df, startDate, endDate, 'stato', mustStates, minDate, maxDate, sections, subjects, judges)
