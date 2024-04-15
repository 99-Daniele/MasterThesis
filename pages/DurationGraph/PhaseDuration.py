import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getPhasesDuration()

def pageLayout():
    years = frame.getAllYears(df)
    phases = frame.getUniques(df, 'fase')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA FASI DEL PROCESSO'),
        ds.dcc.Dropdown(utilities.getAllProcessState, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-phd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = False, searchable = False, id = 'phase-dropdown-phd', placeholder = 'Seleziona fase...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-phd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-phd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'phase-graph', figure = fig)
    ])
    return layout

@ds.callback(
    ds.Output('phase-graph', 'figure'),
    [ds.Input('finished-dropdown-phd', 'value'),
        ds.Input('phase-dropdown-phd', 'value'), 
        ds.Input('year-dropdown-phd', 'value'),
        ds.Input('change-dropdown-phd', 'value')]
)

def updateOutput(finished, phase, year, change):
    return duration.durationPhaseUpdate(df, finished, phase, year, change)