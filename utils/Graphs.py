import plotly.express as px
import dash as ds

def getAvgStdDataframe(df, c):
    match c:
        case "W":
            df1 = df.groupby(df['data'].dt.to_period("W")).mean()
            df2 = df.groupby(df['data'].dt.to_period("W")).std()
            return calcDataframeDifference(df1, df2)
        case "M":
            df1 = df.groupby(df['data'].map(lambda x: x.month)).mean()
            df2 = df.groupby(df['data'].map(lambda x: x.month)).std()
            return calcDataframeDifference(df1, df2)
        case "MY":
            df1 = df.groupby(df['data'].dt.to_period("M")).mean()
            df2 = df.groupby(df['data'].dt.to_period("M")).std()
            return calcDataframeDifference(df1, df2)
        case "Y":
            df1 = df.groupby(df['data'].dt.to_period("Y")).mean()
            df2 = df.groupby(df['data'].dt.to_period("Y")).std()
            return calcDataframeDifference(df1, df2)

def calcDataframeDifference(df1, df2):
    df2['data'] = df1['data']
    df2['durata max'] = df1['durata'] + df2['durata']
    df2['durata min'] = df1['durata'] - df2['durata']
    df2['durata min'] = df2['durata min'].apply(lambda x : 0 if x < 0 else x)
    return [df1, df2]

def displayEvents(df, t):
    dff = df
    fig = px.scatter(dff, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = ['blue', 'orange', 'red', 'green', 'purple'], labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width=1080)
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99,
            xanchor = "left",
            x = 0.01,
            bgcolor = None
        ),
        xaxis = dict(
            rangeselector = dict(
                buttons = list([
                    dict(count = 3, label = "3m", step = "month", stepmode = "backward"),
                    dict(count = 6, label = "6m", step = "month", stepmode = "backward"),
                    dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
                    dict(step="all")
                ])
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
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count = 3, label = "3m", step = "month", stepmode = "backward"),
                        dict(count = 6, label = "6m", step = "month", stepmode = "backward"),
                        dict(count = 1, label = "1y", step = "year", stepmode = "backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
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

def displayProcesses(df, t):
    dff = getAvgStdDataframe(df, "MY")
    fig = px.bar(dff[1], x = "data", y = ["durata max", "durata min"], labels = {'value':'Durata del processo [giorni]', 'data':'Data inizio processo'}, barmode = 'overlay',  title = t, width=1080)
    fig.add_traces(
        px.line(dff[0], x = "data", y = "durata", markers = True).update_traces(showlegend = True, name = "durata media", line_color = 'black').data
    )
    fig.update_layout(
        updatemenus = [(
                dict(
                    type = 'buttons',
                    direction = 'right',
                    showactive = True,     
                    yanchor = "top",
                    y = 0.99,
                    xanchor = "right",
                    x = 0.99,
                    buttons = list(
                        [
                            dict(
                                label = 'W',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(df, "W")[1]['data'], getAvgStdDataframe(df, "W")[0]['data']], 'y' : [getAvgStdDataframe(df, "W")[1]['durata max'], getAvgStdDataframe(df, "W")[1]['durata min'], getAvgStdDataframe(df, "W")[0]['durata']]}]
                            ),
                            dict(
                                label = 'M',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(df, "M")[1]['data'], getAvgStdDataframe(df, "M")[0]['data']], 'y' : [getAvgStdDataframe(df, "M")[1]['durata max'], getAvgStdDataframe(df, "M")[1]['durata min'], getAvgStdDataframe(df, "M")[0]['durata']]}]
                            ),
                            dict(
                                label = 'MY',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(df, "MY")[1]['data'], getAvgStdDataframe(df, "MY")[0]['data']], 'y' : [getAvgStdDataframe(df, "MY")[1]['durata max'], getAvgStdDataframe(df, "MY")[1]['durata min'], getAvgStdDataframe(df, "MY")[0]['durata']]}]
                            ),
                            dict(
                                label = 'Y',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(df, "Y")[1]['data'], getAvgStdDataframe(df, "Y")[0]['data']], 'y' : [getAvgStdDataframe(df, "Y")[1]['durata max'], getAvgStdDataframe(df, "Y")[1]['durata min'], getAvgStdDataframe(df, "Y")[0]['durata']]}]
                            )
                        ]
                    )

                )
            )]
        )
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Graph(
             figure = fig, 
             id = 'processes-graph'
        )
    ])

    app.run(debug=True)