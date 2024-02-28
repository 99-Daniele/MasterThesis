import plotly.express as px
import dash as ds
import pandas as pd

import utils.Legenda as lg
import utils.Dataframe as dfm

def getAllYears(df):
    dft = df['data'].copy()
    dft = dft.map(lambda x: x.year).sort_values()
    years = dft.unique()
    return years

def getTop10Judges(df):
    judges = df.groupby(['giudice'])['giudice'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return judges

def getTop10Subjects(df):
    subjects = df.groupby(['materia'])['materia'].size().sort_values(ascending = False).reset_index(name = 'count').head(10)
    return subjects


def displayEvents(df, judges, subjects, t):
    dff = df
    fig = px.scatter(dff, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = lg.phaseColorList(dff), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600)
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
            dff = df[(df['data'] > start_date) & (df['data'] < end_date)]
        else:
            dff = df[(df['data'] > start_date) & (df['data'] < end_date) & (df['etichetta'].isin(t_value))]
        fig = px.scatter(dff, x = "data", y = "numProcesso", color = 'fase', color_discrete_sequence = lg.phaseColorList(dff), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600)
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

def displayProcesses(df, t):
    dft = df.copy()
    dff = dfm.dfm.getAvgStdDataframe(dft, "MY")
    fig = px.box(dff[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
    fig.add_traces(
        px.line(dff[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
    )
    fig.add_traces(
        px.line(dff[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
    )
    fig.update_layout(
        updatemenus = [
            dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                buttons = list([
                    dict(
                        label = 'W', method = 'update',
                        args = [{'x' : [dfm.getAvgStdDataframe(dft, "W")[0]['data'], dfm.getAvgStdDataframe(dft, "W")[1]['data'], dfm.getAvgStdDataframe(dft, "W")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "W")[0]['durata'], dfm.getAvgStdDataframe(dft, "W")[1]['durata'], dfm.getAvgStdDataframe(dft, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "W")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'M', method = 'update',
                        args = [{'x' : [dfm.getAvgStdDataframe(dft, "M")[0]['data'], dfm.getAvgStdDataframe(dft, "M")[1]['data'], dfm.getAvgStdDataframe(dft, "M")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "M")[0]['durata'], dfm.getAvgStdDataframe(dft, "M")[1]['durata'], dfm.getAvgStdDataframe(dft, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "M")[1]['conteggio']]}]
                    ),
                    dict(
                        label = 'MY', method = 'update',
                        args = [{'x' : [dfm.getAvgStdDataframe(dft, "MY")[0]['data'], dfm.getAvgStdDataframe(dft, "MY")[1]['data'], dfm.getAvgStdDataframe(dft, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "MY")[0]['durata'], dfm.getAvgStdDataframe(dft, "MY")[1]['durata'], dfm.getAvgStdDataframe(dft, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "MY")[1]['conteggio']]}]
                    )
                ])
            )
        ]
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    years = getAllYears(df)
    judges = getTop10Judges(dft)['giudice']
    subjects = getTop10Subjects(dft)['materia']
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(lg.processState, value = [lg.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        #ds.dcc.Dropdown(judges, multi = False, searchable = False, id = 'judge-dropdown', placeholder = 'Seleziona giudice...', style = {'width': 400}),
        #ds.dcc.Dropdown(subjects, multi = False, searchable = False, id = 'subject-dropdown', placeholder = 'Seleziona materia...', style = {'width': 400}),
        #ds.dcc.Dropdown(lg.sectionList, multi = False, searchable = False, id = 'section-dropdown', placeholder = 'Seleziona sezione...', style = {'width': 400}),
        ds.dcc.Graph(
             figure = fig, 
             id = 'processes-graph'
        )
    ])
    @app.callback(
    ds.Output('processes-graph', 'figure'),
    [ds.Input('finished-dropdown', 'value'), ds.Input('year-dropdown', 'value')])
    def update_graph(finished, year):
        dft = dfm.getFinishedDataframe(df, finished)
        dft = dfm.getYearDataframe(dft, year)
        dff = dfm.getAvgStdDataframe(dft, "MY")
        fig = px.box(dff[0], x = "data", y = "durata", color_discrete_sequence = ['#91BBF3'], labels = {'durata':'Durata del processo [giorni]', 'data':'Data inizio processo'}, title = t, width = 1400, height = 600, points=False)
        fig.add_traces(
            px.line(dff[1], x = "data", y = "durata", markers = True).update_traces(line_color = 'red').data
        )
        fig.add_traces(
            px.line(dff[1], x = "data", y = "quantile", text = "conteggio", markers = False).update_traces(line_color = 'rgba(0, 0, 0, 0)', textposition = "top center", textfont = dict(color = "black", size = 10)).data
        )
        fig.update_layout(
            updatemenus = [(
                dict(type = 'buttons', direction = 'right', showactive = True, yanchor = "top", y = 0.99, xanchor = "right", x = 0.99,
                    buttons = list([
                        dict(
                        label = 'W', method = 'update',
                        args = [{'x' : [dfm.getAvgStdDataframe(dft, "W")[0]['data'], dfm.getAvgStdDataframe(dft, "W")[1]['data'], dfm.getAvgStdDataframe(dft, "W")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "W")[0]['durata'], dfm.getAvgStdDataframe(dft, "W")[1]['durata'], dfm.getAvgStdDataframe(dft, "W")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "W")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'M', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataframe(dft, "M")[0]['data'], dfm.getAvgStdDataframe(dft, "M")[1]['data'], dfm.getAvgStdDataframe(dft, "M")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "M")[0]['durata'], dfm.getAvgStdDataframe(dft, "M")[1]['durata'], dfm.getAvgStdDataframe(dft, "M")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "M")[1]['conteggio']]}]
                        ),
                        dict(
                            label = 'MY', method = 'update',
                            args = [{'x' : [dfm.getAvgStdDataframe(dft, "MY")[0]['data'], dfm.getAvgStdDataframe(dft, "MY")[1]['data'], dfm.getAvgStdDataframe(dft, "MY")[1]['data']], 'y' : [dfm.getAvgStdDataframe(dft, "MY")[0]['durata'], dfm.getAvgStdDataframe(dft, "MY")[1]['durata'], dfm.getAvgStdDataframe(dft, "MY")[1]['quantile']], 'text': [dfm.getAvgStdDataframe(dft, "MY")[1]['conteggio']]}]
                        )
                    ])
                )
            )]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)