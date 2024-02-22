import plotly.express as px
import dash as ds
import pandas as pd

import utils.Legenda as lg

def getAvgStdDataframe(df, c):
    match c:
        case "W":
            dft = df[['data', 'durata']].copy()
            dft['data'] = dft['data'].map(lambda x: x.week)
            df1 = dft.groupby(['data'], as_index = False).mean()
            df2 = dft.groupby(['data'], as_index = False).std()
            df1['data'] = df1['data'].map(lambda x: lg.weeks[x - 1])
            #df1['data'] = df1['data'].map(lambda x: lg.getWeekDate(x))
            return calcDataframeDifference(df1, df2)
        case "M":
            dft = df[['data', 'durata']].copy()
            dft['data'] = dft['data'].map(lambda x: x.month)
            df1 = dft.groupby(['data'], as_index = False).mean()
            df2 = dft.groupby(['data'], as_index = False).std()
            df1['data'] = df1['data'].map(lambda x: lg.months[x - 1])
            #df1['data'] = df1['data'].map(lambda x: lg.getMonthDate(x))
            return calcDataframeDifference(df1, df2)
        case "MY":
            dft = df[['data', 'durata']].copy()
            dft['mese'] = dft['data'].dt.to_period("M")
            df1 = dft.groupby(['mese'], as_index = False).mean()
            df2 = dft.groupby(['mese'], as_index = False).std()
            df1['data'] = df1['data'].map(lambda x: lg.getMonthYearDate(x))
            #df2['tick'] = df1['data']
            return calcDataframeDifference(df1, df2)
        case "Y":
            dft = df[['data', 'durata']].copy()
            dft['anno'] = dft['data'].dt.to_period("Y")
            df1 = dft.groupby(['anno'], as_index = False).mean()
            df2 = dft.groupby(['anno'], as_index = False).std()
            df1['data'] = df1['data'].map(lambda x: lg.getYearDate(x))
            #df2['tick'] = df1['data']
            return calcDataframeDifference(df1, df2)

def calcDataframeDifference(df1, df2):
    df2['data'] = df1['data']
    df2['durata max'] = df1['durata'] + df2['durata']
    df2['durata min'] = df1['durata'] - df2['durata']
    df2['durata min'] = df2['durata min'].apply(lambda x : 0 if x < 0 else x)
    return [df1, df2]

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
    dft = df
    dff = getAvgStdDataframe(dft, "MY")
    fig = px.bar(dff[1], x = "data", y = ["durata max", "durata min"], labels = {'value':'Durata del processo [giorni]', 'data':'Data inizio processo'}, barmode = 'overlay',  title = t, width = 1400, height = 600)
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
                            args = [{'x' : [getAvgStdDataframe(dft, "W")[1]['data'], getAvgStdDataframe(dft, "W")[0]['data']], 'y' : [getAvgStdDataframe(dft, "W")[1]['durata max'], getAvgStdDataframe(dft, "W")[1]['durata min'], getAvgStdDataframe(dft, "W")[0]['durata']]}]
                        ),
                        dict(
                            label = 'M',
                            method = 'update',
                            args = [{'x' : [getAvgStdDataframe(dft, "M")[1]['data'], getAvgStdDataframe(dft, "M")[0]['data']], 'y' : [getAvgStdDataframe(dft, "M")[1]['durata max'], getAvgStdDataframe(dft, "M")[1]['durata min'], getAvgStdDataframe(dft, "M")[0]['durata']]}]
                        ),
                        dict(
                            label = 'MY',
                            method = 'update',
                            args = [{'x' : [getAvgStdDataframe(dft, "MY")[1]['data'], getAvgStdDataframe(dft, "MY")[0]['data']], 'y' : [getAvgStdDataframe(dft, "MY")[1]['durata max'], getAvgStdDataframe(dft, "MY")[1]['durata min'], getAvgStdDataframe(dft, "MY")[0]['durata']]}]
                        ),
                        dict(
                            label = 'Y',
                            method = 'update',
                            args = [{'x' : [getAvgStdDataframe(dft, "Y")[1]['data'], getAvgStdDataframe(dft, "Y")[0]['data']], 'y' : [getAvgStdDataframe(dft, "Y")[1]['durata max'], getAvgStdDataframe(dft, "Y")[1]['durata min'], getAvgStdDataframe(dft, "Y")[0]['durata']]}]
                        )
                    ]
                )
            )
        )]
    )
    fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
    judges = getTop10Judges(dft)['giudice']
    subjects = getTop10Subjects(dft)['materia']
    app = ds.Dash()
    app.layout = ds.html.Div([
        ds.dcc.Dropdown(judges, multi = False, id = 'judge-dropdown', placeholder = 'Seleziona giudice...', style = {'width': 300}),
        ds.dcc.Dropdown(subjects, multi = False, id = 'subject-dropdown', placeholder = 'Seleziona materia...', style = {'width': 300}),
        ds.dcc.Dropdown(lg.sectionList, multi = False, id = 'section-dropdown', placeholder = 'Seleziona sezione...', style = {'width': 300}),
        ds.dcc.Graph(
             figure = fig, 
             id = 'processes-graph'
        )
    ])

    @app.callback(
    ds.Output('processes-graph', 'figure'),
    [ds.Input('judge-dropdown', 'value'), ds.Input('subject-dropdown', 'value'), ds.Input('section-dropdown', 'value')])
    def update_graph(ju_drop, su_drop, se_drop):
        if ju_drop is None:
            if su_drop is None:
                if se_drop is None:
                    dft = df
                else:
                    dft = df[df['sezione'] == se_drop]
            else:
                if se_drop is None:
                    dft = df[df['materia'] == su_drop]
                else:
                    dft = df[(df['materia'] == su_drop) & (df['sezione'] == se_drop)]
        else:
            if su_drop is None:
                if se_drop is None:
                    dft = df[df['giudice'] == ju_drop]
                else:
                    dft = df[(df['giudice'] == ju_drop) & (df['sezione'] == se_drop)]
            else:
                if se_drop is None:
                    dft = df[(df['giudice'] == ju_drop) & (df['materia'] == su_drop)]
                else:
                    dft = df[(df['giudice'] == ju_drop) & (df['materia'] == su_drop) & (df['sezione'] == se_drop)]
        judges = getTop10Judges(dft)['giudice']
        subjects = getTop10Subjects(dft)['materia']
        dff = getAvgStdDataframe(dft, "MY")
        fig = px.bar(dff[1], x = "data", y = ["durata max", "durata min"], labels = {'value':'Durata del processo [giorni]', 'data':'Data inizio processo'}, barmode = 'overlay',  title = t, width = 1400, height = 600)
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
                                args = [{'x' : [getAvgStdDataframe(dft, "W")[1]['data'], getAvgStdDataframe(dft, "W")[0]['data']], 'y' : [getAvgStdDataframe(dft, "W")[1]['durata max'], getAvgStdDataframe(dft, "W")[1]['durata min'], getAvgStdDataframe(dft, "W")[0]['durata']]}]
                            ),
                            dict(
                                label = 'M',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(dft, "M")[1]['data'], getAvgStdDataframe(dft, "M")[0]['data']], 'y' : [getAvgStdDataframe(dft, "M")[1]['durata max'], getAvgStdDataframe(dft, "M")[1]['durata min'], getAvgStdDataframe(dft, "M")[0]['durata']]}]
                            ),
                            dict(
                                label = 'MY',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(dft, "MY")[1]['data'], getAvgStdDataframe(dft, "MY")[0]['data']], 'y' : [getAvgStdDataframe(dft, "MY")[1]['durata max'], getAvgStdDataframe(dft, "MY")[1]['durata min'], getAvgStdDataframe(dft, "MY")[0]['durata']]}]
                            ),
                            dict(
                                label = 'Y',
                                method = 'update',
                                args = [{'x' : [getAvgStdDataframe(dft, "Y")[1]['data'], getAvgStdDataframe(dft, "Y")[0]['data']], 'y' : [getAvgStdDataframe(dft, "Y")[1]['durata max'], getAvgStdDataframe(dft, "Y")[1]['durata min'], getAvgStdDataframe(dft, "Y")[0]['durata']]}]
                            )
                        ]
                    )
                )
            )]
        )
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig

    app.run(debug=True)