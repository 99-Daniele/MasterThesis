# this page shows processes duration.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities.Utilities as utilities

# get dataframe with all processes duration.
df = getter.getProcessesDuration()

# return initial layout of page.
def pageLayout():
    df_temp = df.copy()
    finished = frame.getGroupBy(df_temp, 'finito')
    years = frame.getAllYears(df_temp)
    sequences = frame.getGroupBy(df_temp, 'sequenza')
    phases = frame.getGroupBy(df_temp, 'fasi')
    changes = frame.getGroupBy(df_temp, 'cambio')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA PROCESSI'),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-prd", inline = True, style = {'display':'inline'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'MESE', id = "date-store-prd"),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-prd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-prd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-prd', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown-prd', placeholder = 'Seleziona fasi...', style = {'width': 400}),
        ds.dcc.Dropdown(changes, multi = True, searchable = False, id = 'change-dropdown-prd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'process-graph', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('process-graph', 'figure'), 
        ds.Output('date-checklist-prd', 'value'),
        ds.Output('date-store-prd', 'data'),
        ds.Output('finished-dropdown-prd', 'options'), 
        ds.Output('year-dropdown-prd', 'options'),
        ds.Output('sequence-dropdown-prd', 'options'),
        ds.Output('phase-dropdown-prd', 'options'),
        ds.Output('change-dropdown-prd', 'options')],
    [ds.Input('date-checklist-prd', 'value'),
        ds.Input('date-store-prd', 'data'),
        ds.Input('finished-dropdown-prd', 'value'), 
        ds.Input('year-dropdown-prd', 'value'),
        ds.Input('sequence-dropdown-prd', 'value'),
        ds.Input('phase-dropdown-prd', 'value'),
        ds.Input('change-dropdown-prd', 'value')]
    )

# return updated data based on user choice.
def updateOutput(dateChoice, dateStore, finished, year, sequence, phase, change):
    return duration.durationProcessUpdate(df, dateChoice, dateStore, finished, year, sequence, phase, change)
