import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def displayEvents(df, type, mustEvents):
    fig = px.scatter(df, x = "data", y = "numProcesso", color = type, labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
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
        ds.dcc.Graph(figure = fig, id = 'events-graph')
    ])
    @app.callback(
        ds.Output('events-graph', 'figure'),
        [ds.Input('event-dateranger', 'start_date'), 
         ds.Input('event-dateranger', 'end_date')])
    def updateOutput(startDate, endDate):
         return eventUpdate(df, startDate, endDate, type, mustEvents)
    app.run_server(debug = True)

def eventUpdate(df, startDate, endDate, type, mustEvents):
    df_temp = df.copy()
    df_temp = frame.getDateDataFrame(df, startDate, endDate)
    fig = px.scatter(df_temp, x = "data", y = "numProcesso", color = type, color_discrete_sequence = utilities.phaseColorList(df_temp, type), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, height = 1200)
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
                visible = False
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
    fig.update_layout(legend = dict(xanchor = "left", x = 0.1))
    fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name not in mustEvents else False))
    return fig