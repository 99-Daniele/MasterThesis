import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getEventsDuration()

def pageLayout():
    years = frame.getAllYears(df)
    events = frame.getUniques(df, 'evento')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA EVENTI DEL PROCESSO'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-ed', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'event-dropdown-ed', placeholder = 'Seleziona evento...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-ed', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-ed', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'event-graph', figure = fig)
    ])
    return layout

@ds.callback(
    ds.Output('event-graph', 'figure'),
    [ds.Input('finished-dropdown-ed', 'value'),
        ds.Input('event-dropdown-ed', 'value'), 
        ds.Input('year-dropdown-ed', 'value'),
        ds.Input('change-dropdown-ed', 'value')]
)

def updateOutput(finished, event, year, change):
    return duration.durationEventUpdate(df, finished, event, year, change)