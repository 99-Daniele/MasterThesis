import dash as ds
import plotly.express as px
import pandas as pd

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

df = getter.getStatesDuration()
years = frame.getAllYears(df)
states = frame.getAllStates(df)
df_temp = pd.DataFrame({'A' : [], 'B': []})
fig = px.box(df_temp, x = 'A', y = 'B')
layout = ds.html.Div([
    ds.dcc.Link('Home', href='/'),
    ds.html.Br(),
    ds.dcc.Link('Grafici durata', href='/durationgraph'),
    ds.html.H1('DURATA MEDIA STATI DEL PROCESSO'),
    ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
    ds.dcc.Dropdown(states, multi = False, searchable = False, id = 'state-dropdown', placeholder = 'Seleziona stato...', style = {'width': 400}),
    ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
    ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
    ds.dcc.Graph(id = 'state-graph', figure = fig)
])
@ds.callback(
    ds.Output('state-graph', 'figure'),
    [ds.Input('finished-dropdown', 'value'),
        ds.Input('state-dropdown', 'value'), 
        ds.Input('year-dropdown', 'value'),
        ds.Input('change-dropdown', 'value')]
)
def update_output(finished, state, year, change):
    return duration.durationStateUpdate(df, finished, state, year, change)