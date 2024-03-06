import plotly.express as px
import dash as ds

import utils.DataFrame as frame

def addCountToLegend(name, df, type):
    newName = name + " (" + str(df[df[type] == name]['size'].item()) + ")"
    return newName

def getPosition(name, df, type):
    pos = df.index.get_loc(df[df[type] == name].index[0])
    return pos

def displayComparationByMonthYear(df):
    [sectionData, allData, countData] = frame.getAvgDataFrameBySection(df, "MY")
    fig = px.line(sectionData, x = "data", y = "durata", color = "sezione", markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, title = "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INZIO PROCESSO", width = 1400, height = 600)
    fig.update_traces(visible = "legendonly", selector = (lambda t: not getPosition(t.name, countData, 'sezione') == 0))
    fig.for_each_trace(
        lambda t: t.update(
            name = addCountToLegend(t.name, countData, 'sezione')
        )
    )
    fig.add_traces(
        px.line(allData, x = "data", y = "durata").update_traces(line_color = 'rgb(0, 0, 0)', line = {'width': 3}).data
    )
    fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    app = ds.Dash()
    app.layout = ds.html.Div([
        #ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        #ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'event-dropdown', placeholder = 'Seleziona evento...', style = {'width': 400}),
        #ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        #ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'events-graph', figure = fig)
    ])
    '''@app.callback(
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
            fig = px.box(allData, x = "evento", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata eventi del processo [giorni]', 'evento':'Eventi del processo'}, title = title, width = 1400, height = 600, points  = False)
            fig.update_layout(hovermode = False)
            fig.add_traces(
                px.line(avgData, x = "evento", y = "durata", markers = True).update_traces(line_color = 'red').data
            )
            fig.add_traces(
                px.line(avgData, x = "evento", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
            )
            fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
            fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
            return fig
        else:
            [allData, avgData] = frame.getAvgStdDataFrameByDate(df_temp, "MY")
            fig = px.box(allData, x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = "DURATA MEDIA EVENTO: " + event, width = 1400, height = 600, points  = False)
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
            fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
            fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
            return fig'''
    
    app.run(debug = True)