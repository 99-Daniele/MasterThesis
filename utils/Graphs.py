import plotly.express as px
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import dash as ds

def getEvents(events):
    pIds = []
    dates = []
    phases = []
    for e in events:
            pIds.append(e[0])
            dates.append(e[1])
            phases.append(e[2])
    return pd.DataFrame(
        data = {"data": dates, "numProcesso": pIds, "fase": phases})

def displayEvents(events, t):
    df = getEvents(events)
    dff = df
    fig = px.scatter(dff, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = ['blue', 'orange', 'red', 'green', 'purple'], labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width=1080)
    fig.update_layout(
        legend=dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "left",
            x = 0.01,
            bgcolor = None
        ),
        yaxis = dict(
            showticklabels = False
        )
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period"
    )
    
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.DatePickerRange(
            id = 'date-ranger',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            min_date_allowed = df['data'].min().date(),
            max_date_allowed = df['data'].max().date(),
            display_format = 'DD MM YYYY'
        ),
        ds.dcc.Graph(
             figure = fig, 
             id = 'events-graph'
        )
    ])

    @app.callback(
    ds.Output('events-graph', 'figure'),
    [ds.Input('date-ranger', 'start_date'), ds.Input('date-ranger', 'end_date')])
    def update_graph(start_date, end_date):
        dff = df[(df['data'] > start_date) & (df['data'] < end_date)]
        fig = px.scatter(dff, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = ['blue', 'orange', 'red', 'green', 'purple'], labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width=1080)
        fig.update_layout(
            legend=dict(
                yanchor = "top",
                y = 0.99,
                xanchor = "left",
                x = 0.01,
                bgcolor = None
            ),
            yaxis = dict(
                showticklabels = False
            )
        )
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y",
            ticklabelmode="period"
        )

        return fig
    
    app.run(debug=True)

