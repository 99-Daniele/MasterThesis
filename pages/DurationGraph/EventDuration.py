import dash as ds
import pandas as pd
import plotly.express as px

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

def pageLayout():
    df = getter.getEventsDuration()
    years = frame.getAllYears(df)
    events = frame.getAllEvents(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H1('DURATA MEDIA EVENTI DEL PROCESSO'),
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'event-dropdown', placeholder = 'Seleziona evento...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'event-graph', figure = fig)
    ])
    @ds.callback(
        ds.Output('event-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'),
            ds.Input('event-dropdown', 'value'), 
            ds.Input('year-dropdown', 'value'),
            ds.Input('change-dropdown', 'value')]
    )
    def update_output(finished, event, year, change):
        duration.durationEventUpdate(df, finished, event, year, change)