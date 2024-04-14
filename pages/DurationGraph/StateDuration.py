import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getStatesDuration()

def pageLayout():
    years = frame.getAllYears(df)
    states = frame.getUniques(df, 'stato')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA STATI DEL PROCESSO'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-sd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(states, multi = False, searchable = False, id = 'state-dropdown-sd', placeholder = 'Seleziona stato...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-sd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-sd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'state-graph', figure = fig)
    ])
    return layout

@ds.callback(
    ds.Output('state-graph', 'figure'),
    [ds.Input('finished-dropdown-sd', 'value'),
        ds.Input('state-dropdown-sd', 'value'), 
        ds.Input('year-dropdown-sd', 'value'),
        ds.Input('change-dropdown-sd', 'value')]
)

def updateOutput(finished, state, year, change):
    return duration.durationStateUpdate(df, finished, state, year, change)