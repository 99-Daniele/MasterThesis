import dash as ds
import pandas as pd
import plotly.express as px

import utils.Getters as getter
import utils.Graph.EventsGraph as event
import utils.Legenda as legenda

df = getter.getCourtHearingEvents()

def pageLayout():
    courtHearingEvents = getter.getCourtHearingEvents()
    fig = px.scatter(df, x = "data", y = "numProcesso", color = "fase", color_discrete_sequence = legenda.phaseColorList(df), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 600)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2("UDIENZE DEI PROCESSI"),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-che',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            min_date_allowed = df['data'].min().date(),
            max_date_allowed = df['data'].max().date(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.dcc.Dropdown(courtHearingEvents, multi = True, id = 'event-dropdown-che', placeholder = 'Seleziona tipo di evento...', style = {'width': 300}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-che')
    ])
    return layout

@ds.callback(
    ds.Output('events-graph-che', 'figure'),
    [ds.Input('event-dateranger-che', 'start_date'), 
        ds.Input('event-dateranger-che', 'end_date'), 
        ds.Input('event-dropdown-che', 'value')])

def updateOutput(startDate, endDate, e):
    return event.eventUpdate(df, startDate, endDate, e)