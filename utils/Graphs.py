import plotly.express as px
import dash as ds
import pandas as pd

import utils.Legenda as lg
import utils.DataFrame as dfm

def displayEvents(df, judges, subjects, t):
    df_data = df
    fig = px.scatter(df_data, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = lg.phaseColorList(df_data), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600)
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
        ds.dcc.Dropdown(lg.importantEvents, multi = True, id = 'tag-dropdown', placeholder = 'Seleziona tipo di evento...', style = {'width': 300}),
        ds.dcc.Graph(
             figure = fig, 
             id = 'events-graph'
        )
    ])

    @app.callback(
    ds.Output('events-graph', 'figure'),
    [ds.Input('date-ranger', 'start_date'), ds.Input('date-ranger', 'end_date'), ds.Input('tag-dropdown', 'value')])
    def update_graph(start_date, end_date, t_value):
        if t_value is None:
            df_data = df[(df['data'] > start_date) & (df['data'] < end_date)]
        else:
            df_data = df[(df['data'] > start_date) & (df['data'] < end_date) & (df['etichetta'].isin(t_value))]
        fig = px.scatter(df_data, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = lg.phaseColorList(df_data), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600)
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
            dtick="M1",
            tickformat="%b\n%Y",
            ticklabelmode="period"
        )
        return fig
    
    app.run(debug=True)

def displayProcessDuration(df, t):
    years = dfm.getAllYears(df)
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(lg.processState, value = [lg.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Graph(id = 'processes-graph')
    ])
    @app.callback(
        ds.Output('processes-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value')]
    )
    def update_output(finished, year):
        df_temp = dfm.getFinishedDataFrame(df, finished)
        df_temp = dfm.getYearDataFrame(df_temp, year)
        df_data = dfm.getAvgStdDataFrame(df_temp, "MY")
        fig = px.box(df_data[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)

def displayStatesDuration(df, t):
    years = dfm.getAllYears(df)
    states = dfm.getAllStates(df)
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(lg.processState, value = [lg.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(states, multi = True, searchable = False, id = 'states-dropdown', placeholder = 'Seleziona stato...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Graph(id = 'processes-graph')
    ])
    @app.callback(
        ds.Output('processes-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('states-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value')]
    )
    def update_output(finished, state, year):
        df_temp = dfm.getFinishedDataFrame(df, finished)
        df_temp = dfm.getStatesDataFrame(df, state)
        df_temp = dfm.getYearDataFrame(df_temp, year)
        df_data = dfm.getAvgStdDataFrame(df_temp, "MY")
        fig = px.box(df_data[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)

def displayProcessDuration(df, t):
    years = dfm.getAllYears(df)
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(lg.processState, value = [lg.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Graph(
             id = 'processes-graph'
        )
    ])
    @app.callback(
        ds.Output('processes-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value')])
    def update_output(finished, year):
        df_temp = dfm.getFinishedDataFrame(df, finished)
        df_temp = dfm.getYearDataFrame(df_temp, year)
        df_data = dfm.getAvgStdDataFrame(df_temp, "MY")
        fig = px.box(df_data[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)

def displayProcessDuration(df, t):
    years = dfm.getAllYears(df)
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(lg.processState, value = [lg.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Graph(
             id = 'processes-graph'
        )
    ])
    @app.callback(
        ds.Output('processes-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value')])
    def update_output(finished, year):
        df_temp = dfm.getFinishedDataFrame(df, finished)
        df_temp = dfm.getYearDataFrame(df_temp, year)
        df_data = dfm.getAvgStdDataFrame(df_temp, "MY")
        fig = px.box(df_data[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(df_data[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "W")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "M")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataFrame(df_temp, "MY")[0]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['durata'], dfm.getAvgStdDataFrame(df_temp, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataFrame(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)

