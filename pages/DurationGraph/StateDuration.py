import dash as ds
import plotly.express as px
import pandas as pd

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

ds.register_page(__name__)
df = getter.getStatesDuration()
years = frame.getAllYears(df)
states = frame.getAllStates(df)
df_temp = pd.DataFrame({'A' : [], 'B': []})
fig = px.box(df_temp, x = 'A', y = 'B')
layout = ds.html.Div([
    ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
    ds.dcc.Dropdown(states, multi = False, searchable = False, id = 'state-dropdown', placeholder = 'Seleziona stato...', style = {'width': 400}),
    ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
    ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
    ds.dcc.Graph(id = 'states-graph', figure = fig)
])
@ds.callback(
    ds.Output('states-graph', 'figure'),
    [ds.Input('finished-dropdown', 'value'),
        ds.Input('state-dropdown', 'value'), 
        ds.Input('year-dropdown', 'value'),
        ds.Input('change-dropdown', 'value')]
)
def update_output(finished, state, year, change):
    df_temp = df.copy()
    df_temp = duration.updateStatesDuration(df_temp, state, finished, year, change)
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