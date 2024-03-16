import dash as ds
import pandas as pd
import plotly.express as px

import utils.Getters as getter
import utils.Graph.EventsGraph as event
import utils.Utilities as utilities

df = getter.getImportantEvents()

def pageLayout():
    importantEventsType = getter.getImportantEventsType()
    fig = px.scatter(df, x = "data", y = "numProcesso", color = "fase", color_discrete_sequence = Utilities.phaseColorList(df), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 600)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2("EVENTI IMPORTANTI DEI PROCESSI"),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-ie',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            min_date_allowed = df['data'].min().date(),
            max_date_allowed = df['data'].max().date(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.dcc.Dropdown(importantEventsType, multi = True, id = 'event-dropdown-ie', placeholder = 'Seleziona tipo di evento...', style = {'width': 300}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-ie')
    ])
    return layout

@ds.callback(
    ds.Output('events-graph-ie', 'figure'),
    [ds.Input('event-dateranger-ie', 'start_date'), 
        ds.Input('event-dateranger-ie', 'end_date'), 
        ds.Input('event-dropdown-ie', 'value')])

def updateOutput(startDate, endDate, e):
    return event.eventUpdate(df, startDate, endDate, e)