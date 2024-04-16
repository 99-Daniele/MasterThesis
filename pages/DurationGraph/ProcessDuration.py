import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getProcessesDuration()

def pageLayout():
    years = frame.getAllYears(df)
    sequences = frame.getSequences(df)
    phases = frame.getPhaseSequences(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA PROCESSI'),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-prd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-prd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-prd', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown-prd', placeholder = 'Seleziona fasi...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-prd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'process-graph', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('process-graph', 'figure'), 
        ds.Output('sequence-dropdown-prd', 'options'), 
        ds.Output('phase-dropdown-prd', 'options')],
    [ds.Input('finished-dropdown-prd', 'value'), 
        ds.Input('year-dropdown-prd', 'value'),
        ds.Input('sequence-dropdown-prd', 'value'),
        ds.Input('phase-dropdown-prd', 'value'),
        ds.Input('change-dropdown-prd', 'value')]
)

def updateOutput(finished, year, sequence, phase, change):
    return duration.durationProcessUpdate(df, finished, year, sequence, phase, change)