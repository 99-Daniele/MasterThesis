import dash as ds
import plotly.express as px
import pandas as pd

import utils.DataFrame as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Legenda as legenda

ds.register_page(__name__)
df = getter.getProcessesDuration()
years = frame.getAllYears(df)
sequences = frame.getTop20Sequences(df)
phases = frame.getTop20PhaseSequences(df)
df_temp = pd.DataFrame({'A' : [], 'B': []})
fig = px.box(df_temp, x = 'A', y = 'B')
layout = ds.html.Div([
    ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[1]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
    ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
    ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
    ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown', placeholder = 'Seleziona fasi...', style = {'width': 400}),
    ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
    ds.dcc.Graph(id = 'processes-graph', figure = fig)
])
@ds.callback(
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
    df_temp = duration.updateProcessesDuration(df_temp, sequence, phase, finished, year, change)
    sequences = frame.getTop20Sequences(df_temp)
    phases = frame.getTop20PhaseSequences(df_temp)
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