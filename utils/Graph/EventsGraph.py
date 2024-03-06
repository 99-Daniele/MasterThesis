import dash as ds
import plotly.express as px

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Legenda as legenda

def updateEvents(df, startDate, endDate, events):
    if not (startDate == None or endDate == None):
        df = frame.getDateDataFrame(df, startDate, endDate)
    if not (events == None or len(events) == 0):
        df = frame.getEventsDataFrame(df, events)
    return df

def displayEvents(df, importantEventsType):
    fig = px.scatter(df, x = "data", y = "numProcesso", color = "fase", color_discrete_sequence = legenda.phaseColorList(df), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = "EVENTI DEI PROCESSI", width = 1400, height = 600)
    app = ds.Dash()
    app.layout = ds.html.Div([
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
    [ds.Input('event-dateranger', 'start_date'), ds.Input('event-dateranger', 'end_date'), ds.Input('event-dropdown', 'value')])
    def update_graph(startDate, endDate, event):
        df_data = df.copy()
        df_data = updateEvents(df_data, startDate, endDate, event)
        fig = px.scatter(df_data, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = legenda.phaseColorList(df_data), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = "EVENTI DEI PROCESSI", width = 1400, height = 600)
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
    
    app.run(debug = True)