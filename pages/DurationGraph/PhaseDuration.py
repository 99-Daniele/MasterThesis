import dash as ds
import plotly.express as px
import pandas as pd

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

def pageLayout():
    df = getter.getPhasesDuration()
    years = frame.getAllYears(df)
    phases = frame.getAllPhases(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H1('DURATA MEDIA FASI DEL PROCESSO'),
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = False, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fase...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'phase-graph', figure = fig)
    ])
    @ds.callback(
        ds.Output('phase-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'),
            ds.Input('phase-dropdown', 'value'), 
            ds.Input('year-dropdown', 'value'),
            ds.Input('change-dropdown', 'value')]
    )
    def update_output(finished, phase, year, change):
        return duration.durationPhaseUpdate(df, finished, phase, year, change)