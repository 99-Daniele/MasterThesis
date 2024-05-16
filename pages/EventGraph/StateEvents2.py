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
sections = frame.getGroupBy(df, 'sezione', 'conteggio')
subjects = frame.getGroupBy(df, 'materia', 'conteggio')
judges = frame.getGroupBy(df, 'giudice', 'conteggio')
maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
maxDateStart = dt.date(maxYear - 1, 1, 1)
maxDateEnd = dt.date(maxYear, 1, 1)
try:
    mustStates = file.getDataFromTextFile('preferences/mustStates.txt')
except:
    mustStates = None

# return initial layout of page.
def pageLayout():
    fig = px.scatter(df, x = "data", y = "numProcesso", color = 'evento', labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href = '/eventgraph'),
        ds.html.H2('EVENTI INIZIO STATI DEL PROCESSO'),
        ds.html.Div(children = [
            ds.html.Div(children = [
                ds.dcc.DatePickerRange(
                    id = 'event-dateranger-se',
                    start_date = maxDateStart,
                    end_date = maxDateEnd,
                    min_date_allowed = df['data'].min(),
                    max_date_allowed = df['data'].max(),
                    display_format = 'DD MM YYYY',
                    style = {'width': 300}
                ),
                ds.html.Button("RESET", id = "reset-button-se"),
                ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-se', placeholder = 'SEZIONE', style = {'width': 285}),
                ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-se', placeholder = 'MATERIA', style = {'width': 285}),
                ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-se', placeholder = 'GIUDICE', style = {'width': 285})
                ],
                className = 'filter'
            ),
            ds.dcc.Graph(figure = fig, id = 'events-graph-se', className = 'graph')
        ],
        className = 'page')
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