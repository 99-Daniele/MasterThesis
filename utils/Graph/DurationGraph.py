import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def updateFinishYearChangeDuration(df, finished, year, change):
    df_temp = df
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    if not (year == None or len(year) == 0):
        df_temp = frame.getYearDataFrame(df_temp, year)
    if not (change == None or len(change) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    return df_temp

def updateProcessesDuration(df, sequences, phases, finished, year, change):
    df_temp = df
    if not (sequences == None or len(sequences) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'sequenza', sequences)
    if not (phases == None or len(phases) == 0):
        df_temp = frame.getTypesDataFrame(df_temp, 'fasi', phases)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updateStatesDuration(df, state, finished, year, change):
    df_temp = df
    if not state == None:
        df_temp = frame.getTypeDataFrame(df_temp, 'stato', state)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updatePhasesDuration(df, phase, finished, year, change):
    df_temp = df
    if not phase == None:
        df_temp = frame.getTypeDataFrame(df_temp, 'fase', phase)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updateEventsDuration(df, event, finished, year, change):
    df_temp = df
    if not event == None:
        df_temp = frame.getTypeDataFrame(df_temp, 'evento', event)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def displayProcessesDuration(df):
    years = frame.getAllYears(df)
    sequences = frame.getGroupBy(df, 'sequenza')
    phases = frame.getGroupBy(df, 'fasi')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA PROCESSI'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fasi...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'processes-graph', figure = fig)
    ])
    @app.callback(
        [ds.Output('processes-graph', 'figure'), 
         ds.Output('sequence-dropdown', 'options'), 
         ds.Output('phase-dropdown', 'options')],
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value'),
         ds.Input('sequence-dropdown', 'value'),
         ds.Input('phase-dropdown', 'value'),
         ds.Input('change-dropdown', 'value')]
    )
    def updateOutput(finished, year, sequence, phase, change):
        return durationProcessUpdate(df, finished, year, sequence, phase, change)
    app.run_server(debug = True)

def durationProcessUpdate(df, finished, year, sequence, phase, change):
    df_temp = df.copy()
    df_temp = updateProcessesDuration(df_temp, sequence, phase, finished, year, change)
    sequences = frame.getGroupBy(df, 'sequenza')
    phases = frame.getGroupBy(df, 'fasi')
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600, points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(
        updatemenus = [
            dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                buttons = list([
                    dict(
                        label = 'W', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'M', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'MY', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['conteggio']]}]
                    )
                ])
            )
        ]
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig, sequences, phases

def displayStatesDuration(df):
    years = frame.getAllYears(df)
    states = frame.getUniques(df, 'stato')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA STATI'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(states, multi = False, searchable = False, id = 'state-dropdown', placeholder = 'Seleziona stato...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'states-graph', figure = fig)
    ])
    @app.callback(
        ds.Output('states-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'),
         ds.Input('state-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value'),
         ds.Input('change-dropdown', 'value')]
    )
    def updateOutput(finished, state, year, change):
        return durationStateUpdate(df, finished, state, year, change)
    app.run_server(debug = True)

def durationStateUpdate(df, finished, state, year, change):
    df_temp = df.copy()
    df_temp = updateStatesDuration(df_temp, state, finished, year, change)
    if state == None:
        [allData, avgData] = frame.getAvgStdDataFrameByState(df_temp)
        fig = px.box(allData, x = "stato", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata stati del processo [giorni]', 'stato':'Stati del processo'}, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "stato", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "stato", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    else:
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
        fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA STATO <b>" + state, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig

def displayPhasesDuration(df):
    years = frame.getAllYears(df)
    phases = frame.getUniques(df, 'fase')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA FASI'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = False, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fase...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'phases-graph', figure = fig)
    ])
    @app.callback(
        ds.Output('phases-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'),
         ds.Input('phase-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value'),
         ds.Input('change-dropdown', 'value')]
    )
    def updateOutput(finished, phase, year, change):
        return durationPhaseUpdate(df, finished, phase, year, change)
    app.run_server(debug = True)

def durationPhaseUpdate(df, finished, phase, year, change):
    df_temp = df.copy()
    df_temp = updatePhasesDuration(df_temp, phase, finished, year, change)
    if phase == None:
        [allData, avgData] = frame.getAvgStdDataFrameByPhase(df_temp)
        fig = px.box(allData, x = "fase", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "fase", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "fase", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    else:
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
        fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA FASE <b>" + phase, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig

def displayEventsDuration(df):
    years = frame.getAllYears(df)
    events = frame.getUniques(df, 'evento')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA EVENTI'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'event-dropdown', placeholder = 'Seleziona evento...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'events-graph', figure = fig)
    ])
    @app.callback(
        ds.Output('events-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'),
         ds.Input('event-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value'),
         ds.Input('change-dropdown', 'value')]
    )
    def updateOutput(finished, event, year, change):
        return durationEventUpdate(df, finished, event, year, change)
    app.run_server(debug = True)

def durationEventUpdate(df, finished, event, year, change):
    df_temp = df.copy()
    df_temp = updateEventsDuration(df_temp, event, finished, year, change)
    if event == None:
        [allData, avgData] = frame.getAvgStdDataFrameByPhase(df_temp)
        fig = px.box(allData, x = "fase", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "fase", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "fase", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    else:
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
        fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA EVENTO <b>" + event, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                            label = 'W', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            ]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig

def displayCourtHearingsDuration(df):
    years = frame.getAllYears(df)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA UDIENZE'),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'processes-graph', figure = fig)
    ])
    @app.callback(
        ds.Output('processes-graph', 'figure'),
        [ds.Input('finished-dropdown', 'value'), 
         ds.Input('year-dropdown', 'value'),
         ds.Input('change-dropdown', 'value')]
    )
    def updateOutput(finished, year, change):
        return durationCourtHearingUpdate(df, finished, year, change)
    app.run_server(debug = True)

def durationCourtHearingUpdate(df, finished, year, change):
    df_temp = df.copy()
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':"Durata dell' udienza [giorni]", 'data':'Data inizio udienza'}, width = 1400, height = 600, points = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(
        updatemenus = [
            dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                buttons = list([
                    dict(
                        label = 'W', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "W")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "W")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'M', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "M")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "M")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'MY', method = 'update',
                        args = [{'x' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['data']], 'y' : [frame.getAvgStdDataFrameByDate(df_temp, "MY")[0]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['durata'], frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['quantile']], 'text': [frame.getAvgStdDataFrameByDate(df_temp, "MY")[1]['conteggio']]}]
                    )
                ])
            )
        ]
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    return fig

def hideAll(sections, subjects, judges, finished, changes):
    sectionStyle = {'width': 200, 'display': 'none'}
    subjectStyle = {'width': 200, 'display': 'none'}
    judgeStyle = {'width': 200, 'display': 'none'}
    finishedStyle = {'width': 200, 'display': 'none'}
    changeStyle = {'width': 200, 'display': 'none'}
    checkStyle = {'width': 200, 'display': 'none'}
    radioStyle = {'width': 200, 'display': 'none'}
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes]

def hideChosen(choices, sections, subjects, judges, finished, changes):
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    changeStyle = {'width': 400}
    checkStyle = {'display':'inline'}
    radioStyle = {'paddingLeft':'85%'}
    if 'sezione' in choices:
        sectionStyle = {'width': 200, 'display': 'none'}
        sections = None
    if 'materia' in choices:
        subjectStyle = {'width': 200, 'display': 'none'}
        subjects = None
    if 'giudice' in choices:
        judgeStyle = {'width': 200, 'display': 'none'}
        judges = None
    if 'finito' in choices:
        finishedStyle = {'width': 200, 'display': 'none'}
        finished = None
    if 'cambio' in choices:
        changeStyle = {'width': 200, 'display': 'none'}
        changes = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes]

def updateData(df, sections, subjects, judges, finished, change):
    df_temp = df
    df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    df_temp = frame.getTypesDataFrame(df_temp, 'finito', finished)
    df_temp = frame.getTypesDataFrame(df_temp, 'cambio', change)
    return df_temp

def addCountToName(name, df, choices):
    if choices == 'finito':
        count = df[df[type] == int(name)]['conteggio'].item()
        name = utilities.processState[int(name)]
    elif choices == 'cambio':
        count = df[df[type] == int(name)]['conteggio'].item()
        if int(name) == 0:
            name = "NO"
        else:
            name = "SI"
    else:
        count = df[df['filtro'] == name]['conteggio'].item()
    newName = name + " (" + str(count) + ")"
    return newName

def addTotCountToName(df):
    totCount = df['conteggio'].sum()
    newName = "TUTTI (" + str(totCount) + ")"
    return newName

def displayDuration(df, type):
    types = frame.getUniques(df, type)
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    if type == 'stato':
            typeList = ['stato', 'fase']
    else:
        typeList = [type]
    [allData, avgData] = frame.getAvgStdDataFrameByType(df, typeList)
    fig = px.box(allData, x = type, y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata eventi del processo [giorni]', 'evento':'Eventi del processo'}, width = 1400, height = 600, points  = False)
    fig.add_traces(
        px.line(avgData, x = type, y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = type, y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('DURATA MEDIA ' + type),
        ds.dcc.Dropdown(types, multi = False, searchable = False, id = 'type-dropdown', placeholder = 'Seleziona...', style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown', placeholder = 'SEZIONE', style = {'width': 200, 'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown', placeholder = 'MATERIA', style = {'width': 200, 'display': 'none'}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown', placeholder = 'GIUDICE', style = {'width': 200, 'display': 'none'}),
        ds.dcc.Dropdown(utilities.processState, value = [utilities.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'PROCESSO', style = {'width': 200, 'display': 'none'}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'CAMBIO', style = {'width': 200, 'display': 'none'}),
        ds.dcc.Checklist(['sezione', 'materia', 'giudice', 'finito', 'cambio'], value = ['sezione'], id = "choice-checklist", inline = True, style = {'display':'none'}),
        ds.dcc.Store(data = ['sezione'], id = "choice-store"),
        ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = "order-radioitem", inline = True, style = {'paddingLeft':'85%', 'display':'none'}),
        ds.dcc.Graph(id = 'duration-graph', figure = fig)
    ])
    @app.callback(
        [ds.Output('duration-graph', 'figure'),
         ds.Output('section-dropdown', 'style'),
         ds.Output('subject-dropdown', 'style'),
         ds.Output('judge-dropdown', 'style'),
         ds.Output('finished-dropdown', 'style'),
         ds.Output('change-dropdown', 'style'),
         ds.Output('choice-checklist', 'style'),
         ds.Output('order-radioitem', 'style'),
         ds.Output('section-dropdown', 'options'),
         ds.Output('subject-dropdown', 'options'),
         ds.Output('judge-dropdown', 'options'),
         ds.Output('finished-dropdown', 'options'),
         ds.Output('change-dropdown', 'options'),
         ds.Output('choice-checklist', 'value'),
         ds.Output('choice-store', 'data')],
        [ds.Input('type-dropdown', 'value'),
         ds.Input('section-dropdown', 'value'),
         ds.Input('subject-dropdown', 'value'),
         ds.Input('judge-dropdown', 'value'),
         ds.Input('finished-dropdown', 'value'),
         ds.Input('change-dropdown', 'value'),
         ds.Input('choice-checklist', 'value'),
         ds.Input('choice-store', 'data'),
         ds.Input('order-radioitem', 'value')]
    )
    def updateOutput(typeChoice, sections, subjects, judges, finished, changes, choices, choiceStore, order):
        return durationUpdate(df, type, typeChoice, sections, subjects, judges, finished, changes, choices, choiceStore, order)
    app.run_server(debug = True)

def durationUpdate(df, type, typeChoice, sections, subjects, judges, finished, changes, choices, choiceStore, order):
    if typeChoice == None:
        if type == 'stato':
            typeList = ['stato', 'fase']
        else:
            typeList = [type]
        df_temp = df.copy()
        [allData, avgData] = frame.getAvgStdDataFrameByType(df_temp, typeList)
        fig = px.box(allData, x = type, y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata eventi del processo [giorni]', 'evento':'Eventi del processo'}, width = 1400, height = 600, points  = False)
        fig.add_traces(
            px.line(avgData, x = type, y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(avgData, x = type, y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes] = hideAll(sections, subjects, judges, finished, changes)
        return fig, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes, choices, choiceStore
    else:
        if ds.ctx.triggered_id == 'type-dropdown':
            df_temp = df.copy()
            df_data = df.copy()
            df_temp = frame.getTypeDataFrame(df_temp, type, typeChoice)
            sections = frame.getGroupBy(df_temp, 'sezione')
            subjects = frame.getGroupBy(df_temp, 'materia')
            judges = frame.getGroupBy(df_temp, 'giudice')
            finished = utilities.processState
            changes = ['NO', 'SI']
            df_data = updateData(df_data, sections, subjects, judges, finished, changes)
            [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes] = hideChosen(choices, sections, subjects, judges, finished, changes)
        else:
            if choices != None and len(choices) < 1:
                choices = [choiceStore]
            elif choices != None and len(choices) == 1:
                choiceStore = choices[0]
            [sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes] = hideChosen(choices, sections, subjects, judges, finished, changes)
            df_temp = df.copy()
            df_temp = frame.getTypeDataFrame(df_temp, 'fase', '4')
            df_data = updateData(df_temp, sections, subjects, judges, finished, changes)
            if ds.ctx.triggered_id != None and 'section-dropdown' in ds.ctx.triggered_id:
                df_temp = updateData(df_temp, None, subjects, judges, finished, changes)
            elif ds.ctx.triggered_id != None and 'subject-dropdown' in ds.ctx.triggered_id:
                df_temp = updateData(df_temp, sections, None, judges, finished, changes)
            elif ds.ctx.triggered_id != None and 'judge-dropdown' in ds.ctx.triggered_id:
                df_temp = updateData(df_temp, sections, subjects, None, finished, changes)
            else:
                df_temp = df_data
            sections = frame.getGroupBy(df_temp, 'sezione')
            subjects = frame.getGroupBy(df_temp, 'materia')
            judges = frame.getGroupBy(df_temp, 'giudice')
            finished = utilities.processState
            changes = ['NO', 'SI']
        [typeData, allData, infoData] = frame.getAvgDataFrameByType(df_data, "MY", choices, order)
        fig = px.line(allData, x = "data", y = "durata", height = 800).update_traces(showlegend = True, name = addTotCountToName(infoData), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
        fig.add_traces(
            px.line(typeData, x = "data", y = "durata", color = 'filtro', markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, width = 1400, height = 600).data
        )
        fig.for_each_trace(
            lambda t: t.update(name = addCountToName(t.name, infoData, choices)) if t.name != addTotCountToName(infoData) else False
        )
        fig.update_layout(legend = dict(yanchor = "bottom", y = -1.5, xanchor = "left", x = 0))
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != addTotCountToName(infoData) else False))
        fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig, sectionStyle, subjectStyle, judgeStyle, finishedStyle, changeStyle, checkStyle, radioStyle, sections, subjects, judges, finished, changes, choices, choiceStore 