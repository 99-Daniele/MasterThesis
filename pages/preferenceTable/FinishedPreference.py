# this page allows user to change process type preferences.

import dash as ds
import pandas as pd

import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.TypeEventsPreference as typeEvents

# get dataframe with judge names. 
df = getter.getFinishedDataframe()
finishedTag = utilities.getTagName('finishedTag')

# return initial layout of page.
def pageLayout():
    count = utilities.getPlaceholderName('count')
    duration = utilities.getPlaceholderName('duration')
    durationTag = utilities.getTagName('durationTag')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('PROCESS TYPE USER PREFERENCES'),
        ds.html.Button("DOWNLOAD", id = 'download-button-fp'),
        ds.dash_table.DataTable(
            newDF.to_dict('records'), columns = [
                {'name': finishedTag, 'id': finishedTag, 'editable': False},
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = 'multi',
            style_cell = {'textAlign': 'left'},
            id = "finishedtable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    ds.Output('finishedtable', 'selected_rows'),
    [ds.Input('finishedtable', 'selected_rows'),
     ds.Input('download-button-fp', 'n_clicks')],
    ds.State('finishedtable', 'data')
)

# return updated data based on user choice.
def update_dateframe(importantIndex, downloadButton, data):
    if ds.ctx.triggered_id != None and 'download-button' in ds.ctx.triggered_id:
        dataDF = pd.DataFrame(data)
        dataDF.to_csv('cache/finishedInfo.csv')
    importantIndex = typeEvents.updateImportant(ds.ctx.triggered_id, data, finishedTag, importantIndex, 'utils/preferences/importantProcessStates.txt')
    return importantIndex
