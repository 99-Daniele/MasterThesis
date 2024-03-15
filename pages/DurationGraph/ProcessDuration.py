import dash as ds
import pandas as pd
import plotly.express as px

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

def pageLayout():
    df = getter.getProcessesDuration()
    years = frame.getAllYears(df)
    sequences = frame.getTop20Sequences(df)
    phases = frame.getTop20PhaseSequences(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H1('DURATA MEDIA PROCESSI'),
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fasi...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'process-graph', figure = fig)
    ])
    @ds.callback(
        [ds.Output('process-graph', 'figure'), 
            ds.Output('sequence-dropdown', 'options'), 
            ds.Output('phase-dropdown', 'options')],
        [ds.Input('finished-dropdown', 'value'), 
            ds.Input('year-dropdown', 'value'),
            ds.Input('sequence-dropdown', 'value'),
            ds.Input('phase-dropdown', 'value'),
            ds.Input('change-dropdown', 'value')]
    )
    def update_output(finished, year, sequence, phase, change):
        return duration.durationProcessUpdate(df, finished, year, sequence, phase, change)