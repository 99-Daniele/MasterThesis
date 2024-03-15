import dash as ds
import pandas as pd
import plotly.express as px

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

df = getter.getCourtHearingsDuration()
def pageLayout():
    years = frame.getAllYears(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H1('DURATA MEDIA UDIENZE'),
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown-chd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-chd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown-chd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'courthearing-graph', figure = fig)
    ])
    return layout

@ds.callback(
    ds.Output('courthearing-graph', 'figure'),
    [ds.Input('finished-dropdown-chd', 'value'), 
        ds.Input('year-dropdown-chd', 'value'),
        ds.Input('change-dropdown-chd', 'value')]
)
def update_output(finished, year, change):
    return duration.durationCourtHearingUpdate(df, finished, year, change)