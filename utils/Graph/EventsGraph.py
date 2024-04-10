import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def updateEvents(df, startDate, endDate, events):
    if not (startDate == None or endDate == None):
        df = frame.getDateDataFrame(df, startDate, endDate)
    if not (events == None or len(events) == 0):
        df = frame.getTypesDataFrame(df, 'evento', events)
    return df

def displayEvents(df, importantEventsType):
    fig = px.scatter(df, x = "data", y = "numProcesso", color = "fase", color_discrete_sequence = utilities.phaseColorList(df), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 600)
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('EVENTI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger',
            start_date = df['data'].min().date(),
            end_date = df['data'].max().date(),
            min_date_allowed = df['data'].min().date(),
            max_date_allowed = df['data'].max().date(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.dcc.Dropdown(importantEventsType, multi = True, id = 'event-dropdown', placeholder = 'Seleziona tipo di evento...', style = {'width': 300}),
        ds.dcc.Graph(figure = fig, id = 'events-graph')
    ])
    @app.callback(
        ds.Output('events-graph', 'figure'),
        [ds.Input('event-dateranger', 'start_date'), 
         ds.Input('event-dateranger', 'end_date'), 
         ds.Input('event-dropdown', 'value')])
    def updateOutput(startDate, endDate, event):
         return eventUpdate(df, startDate, endDate, event)
    app.run_server(debug = True)

def eventUpdate(df, startDate, endDate, event):
    df_temp = df.copy()
    df_temp = updateEvents(df_temp, startDate, endDate, event)
    fig = px.scatter(df_temp, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = utilities.phaseColorList(df_temp), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 600)
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "right",
            x = 1.05,
            bgcolor = None
        ),
        xaxis = dict(
            rangeselector = dict(
                buttons = list([
                    dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
                    dict(count = 18, label = "1y6m", step = "month", stepmode = "backward"),
                    dict(count = 2, label = "2y", step = "year", stepmode = "backward"),
                    dict(step = "all")
                ]),
                yanchor = "top",
                y = 1.09,
                xanchor = "right",
                x = 0.99,
            ),
            rangeslider = dict(
                visible = True
            ),
            type = "date"
        ),
        yaxis = dict(
            showticklabels = False
        )
    )
    fig.update_xaxes(
        dtick = "M1",
        tickformat = "%b\n%Y",
        ticklabelmode = "period"
    )   
    return fig