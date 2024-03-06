import dash as ds
import plotly.express as px

import utils.DataFrame as frame
import utils.Legenda as legenda

def updateFinishYearChangeDuration(df, finished, year, change):
    df_temp = df
    if not (finished == None or len(finished) == 0):
        df_temp = frame.getFinishedDataFrame(df_temp, finished)
    if not (year == None or len(year) == 0):
        df_temp = frame.getYearDataFrame(df_temp, year)
    if not (change == None or len(change) == 0):
        df_temp = frame.getChangeJudgeDataFrame(df_temp, change)
    return df_temp

def updateProcessesDuration(df, sequence, phase, finished, year, change):
    df_temp = df
    if not sequence == None:
        df_temp = frame.getSequenceDataFrame(df_temp, sequence)
    if not phase == None:
        df_temp = frame.getPhaseSequenceDataFrame(df_temp, phase)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updateStatesDuration(df, state, finished, year, change):
    df_temp = df
    if not state == None:
        df_temp = frame.getStateDataFrame(df_temp, state)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updatePhasesDuration(df, phase, finished, year, change):
    df_temp = df
    if not phase == None:
        df_temp = frame.getPhaseDataFrame(df_temp, phase)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def updateEventsDuration(df, event, finished, year, change):
    df_temp = df
    if not event == None:
        df_temp = frame.getEventDataFrame(df_temp, event)
    df_temp = updateFinishYearChangeDuration(df_temp, finished, year, change)
    return df_temp

def displayProcessesDuration(df):
    df_temp = df.copy()
    years = frame.getAllYears(df_temp)
    sequences = frame.getAllSequences(df_temp)
    phases = frame.getAllPhaseSequences(df_temp)
    app = ds.Dash()
    [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
    fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA PROCESSI", width = 1400, height = 600, points  = False)
    fig.update_layout(hovermode = False)
    fig.add_traces(
        px.line(avgData, x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = False, searchable = False, id = 'sequence-dropdown', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = False, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fasi...', style = {'width': 400}),
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
    def update_output(finished, year, sequence, phase, change):
        df_temp = df.copy()
        df_temp = updateProcessesDuration(df_temp, sequence, phase, finished, year, change)
        sequences = frame.getAllSequences(df_temp)
        phases = frame.getAllPhaseSequences(df_temp)
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
        fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA PROCESSI",  width = 1400, height = 600, points = False)
        fig.update_layout(hovermode = False)
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
    
    app.run(debug = True)

def displayStatesDuration(df):
    df_temp = df.copy()
    years = frame.getAllYears(df_temp)
    states = frame.getAllStates(df_temp)
    [allData, avgData] = frame.getAvgStdDataFrameByState(df_temp)
    fig = px.box(allData, x = "etichetta", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata stati del processo [giorni]', 'etichetta':'Stati del processo'}, title = "DURATA MEDIA STATI DEL PROCESSO", width = 1400, height = 600, points  = False)
    fig.update_layout(hovermode = False)
    fig.add_traces(
        px.line(avgData, x = "etichetta", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "etichetta", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
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
    def update_output(finished, state, year, change):
        df_temp = df.copy()
        df_temp = updateStatesDuration(df_temp, state, finished, year, change)
        if state == None:
            [allData, avgData] = frame.getAvgStdDataFrameByState(df_temp)
            fig = px.box(allData, x = "etichetta", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata stati del processo [giorni]', 'etichetta':'Stati del processo'}, title = "DURATA MEDIA STATI DEL PROCESSO", width = 1400, height = 600, points  = False)
            fig.update_layout(hovermode = False)
            fig.add_traces(
                px.line(avgData, x = "etichetta", y = "durata", markers = True).update_traces(line_color = 'red').data
            )
            fig.add_traces(
                px.line(avgData, x = "etichetta", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
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
    
    app.run(debug = True)

def displayPhasesDuration(df):
    df_temp = df.copy()
    years = frame.getAllYears(df_temp)
    phases = frame.getAllPhases(df_temp)
    [allData, avgData] = frame.getAvgStdDataFrameByPhase(df_temp)
    fig = px.box(allData, x = "fase", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, title = "DURATA MEDIA FASI DEL PROCESSO", width = 1400, height = 600, points  = False)
    fig.update_layout(hovermode = False)
    fig.add_traces(
        px.line(avgData, x = "fase", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "fase", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
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
    def update_output(finished, phase, year, change):
        df_temp = df.copy()
        df_temp = updatePhasesDuration(df_temp, phase, finished, year, change)
        if phase == None:
            [allData, avgData] = frame.getAvgStdDataFrameByPhase(df_temp)
            fig = px.box(allData, x = "fase", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata fasi del processo [giorni]', 'fase':'Fase del processo'}, title = "DURATA MEDIA FASI DEL PROCESSO", width = 1400, height = 600, points  = False)
            fig.update_layout(hovermode = False)
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
            fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA FASE " + phase + " IN BASE AL MESE DELL'ANNO DI INIZIO PROCESSO", width = 1400, height = 600, points  = False)
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
    
    app.run(debug = True)

def displayEventsDuration(df):
    df_temp = df.copy()
    years = frame.getAllYears(df_temp)
    events = frame.getAllEvents(df_temp)
    [allData, avgData] = frame.getAvgStdDataFrameByEvent(df_temp)
    fig = px.box(allData, x = "evento", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata eventi del processo [giorni]', 'evento':'Eventi del processo'}, title = "DURATA MEDIA EVENTI DEL PROCESSO", width = 1400, height = 600, points  = False)
    fig.update_layout(hovermode = False)
    fig.add_traces(
        px.line(avgData, x = "evento", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(avgData, x = "evento", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
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
    def update_output(finished, event, year, change):
        df_temp = df.copy()
        df_temp = updateEventsDuration(df_temp, event, finished, year, change)
        if event == None:
            [allData, avgData] = frame.getAvgStdDataFrameByEvent(df_temp)
            fig = px.box(allData, x = "evento", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata eventi del processo [giorni]', 'evento':'Eventi del processo'}, title = "DURATA MEDIA EVENTI DEL PROCESSO", width = 1400, height = 600, points  = False)
            fig.update_layout(hovermode = False)
            fig.add_traces(
                px.line(avgData, x = "evento", y = "durata", markers = True).update_traces(line_color = 'red').data
            )
            fig.add_traces(
                px.line(avgData, x = "evento", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
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
    
    app.run(debug = True)
