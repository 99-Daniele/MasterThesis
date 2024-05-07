# this page shows court hearings duration.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.Graph.DurationGraph as duration
import utils.Utilities.Utilities as utilities

# get dataframe with all court hearings duration.
df = getter.getCourtHearingsDuration()

# return initial layout of page.
def pageLayout():
    df_temp = df.copy()
    finished = frame.getGroupBy(df_temp, 'finito')
    years = frame.getAllYears(df_temp)
    changes = frame.getGroupBy(df_temp, 'cambio')
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.H2('DURATA MEDIA UDIENZE'),
        ds.dcc.Checklist(["SETTIMANA", "MESE", "MESE DELL'ANNO", "TRIMESTRE", "TRIMESTRE DELL'ANNO", "ANNO"], value = ['MESE'], id = "date-checklist-chd", inline = True, style = {'display':'inline'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Store(data = 'MESE', id = "date-store-chd"),
        ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-chd', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown-chd', placeholder = 'Seleziona anno...', style = {'width': 400}),
        ds.dcc.Dropdown(changes, multi = True, searchable = False, id = 'change-dropdown-chd', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.Graph(id = 'courthearings-graph', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('courthearings-graph', 'figure'),
        ds.Output('date-checklist-chd', 'value'),
        ds.Output('date-store-chd', 'data'),
        ds.Output('finished-dropdown-chd', 'options'),
        ds.Output('year-dropdown-chd', 'options'),
        ds.Output('change-dropdown-chd', 'options')],
    [ds.Input('date-checklist-chd', 'value'),
        ds.Input('date-store-chd', 'data'), 
        ds.Input('finished-dropdown-chd', 'value'),
        ds.Input('year-dropdown-chd', 'value'),
        ds.Input('change-dropdown-chd', 'value')]
)

# return updated data based on user choice.
def updateOutput(dateChoice, dateStore, finished, year, change):
    return duration.durationCourtHearingsUpdate(df, dateChoice, dateStore, finished, year, change)
