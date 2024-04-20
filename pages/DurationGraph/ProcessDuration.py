import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities as utilities

df = getter.getProcessesDuration()

def pageLayout():
    years = frame.getAllYears(df)
    sequences = frame.getGroupBy(df, 'sequenza')
    phases = frame.getGroupBy(df, 'fasi')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA PROCESSI'),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-prd", inline = True, style = {'display':'inline'}),
        ds.dcc.Store(data = 'MESE', id = "date-store-prd"),
        ds.dcc.Dropdown(utilities.getAllProcessState(), value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-prd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-prd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-prd', placeholder = 'Seleziona sequenza...', style = {'width': 400}),
        ds.dcc.Dropdown(phases, multi = True, searchable = False, id = 'phase-dropdown-prd', placeholder = 'Seleziona fasi...', style = {'width': 400}),
        ds.dcc.Dropdown(['NO', 'SI'], multi = True, searchable = False, id = 'change-dropdown-prd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'process-graph', figure = fig)
    ])
    return layout

@ds.callback(
    [ds.Output('process-graph', 'figure'), 
        ds.Output('date-checklist-prd', 'value'),
        ds.Output('date-store-prd', 'data'),
        ds.Output('sequence-dropdown-prd', 'options'), 
        ds.Output('phase-dropdown-prd', 'options')],
    [ds.Input('finished-dropdown-prd', 'value'), 
        ds.Input('date-checklist-prd', 'value'),
        ds.Input('date-store-prd', 'data'),
        ds.Input('year-dropdown-prd', 'value'),
        ds.Input('sequence-dropdown-prd', 'value'),
        ds.Input('phase-dropdown-prd', 'value'),
        ds.Input('change-dropdown-prd', 'value')]
    )

def updateOutput(finished, dateChoice, dateStore, year, sequence, phase, change):
    return duration.durationProcessUpdate(df, dateChoice, dateStore, finished, year, sequence, phase, change)
