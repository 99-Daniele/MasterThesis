# this page allows user to change state preferences.

import dash as ds
import pandas as pd

import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.TypeEventsPreference as typeEvents

# get dataframe with state names. 
df = getter.getStateNamesDataframe()
codeStateTag = utilities.getTagName('codeStateTag')
countTag = utilities.getTagName('countTag')
phaseTag = utilities.getTagName('phaseTag')
phaseDBTag = utilities.getTagName('phaseDBTag')
stateTag = utilities.getTagName('stateTag')

# return initial layout of page.
def pageLayout():
    code = utilities.getPlaceholderName('code')
    codeStateTag = utilities.getTagName('codeStateTag')
    count = utilities.getPlaceholderName('count')
    durationTag = utilities.getTagName('durationTag')
    duration = utilities.getPlaceholderName('duration')
    phase = utilities.getPlaceholderName('phase')
    phaseDB = utilities.getPlaceholderName('phaseDB')
    state = utilities.getPlaceholderName('state')
    layout = ds.html.Div([
        ds.dcc.ConfirmDialog(
            id = 'update-stp',
            message = 'State names table correctly updated',
        ),
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('STATES USER PREFERENCES'),
        ds.html.Button("REFRESH", id = 'refresh-button-stp'),
        ds.html.Button("RESET", id = 'reset-button-stp'),
        ds.html.Button("DOWNLOAD", id = 'download-button-stp'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': code, 'id': codeStateTag, 'editable': False}, 
                {'name': state, 'id': stateTag, 'editable': True},  
                {'name': phaseDB, 'id': phaseDBTag, 'editable': False}, 
                {'name': phase, 'id': phaseTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = 'multi',
            style_cell = {'textAlign': 'left'},
            id = "statetable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('statetable', 'data'),
     ds.Output('update-stp', 'displayed'),
     ds.Output('statetable', 'selected_rows')],
    [ds.Input('refresh-button-stp', 'n_clicks'),
     ds.Input('reset-button-stp', 'n_clicks'),
     ds.Input('download-button-stp', 'n_clicks'),
     ds.Input('statetable', 'selected_rows')],
    ds.State('statetable', 'data')
)

# return updated data based on user choice.
def update_dateframe(refreshButton, resetButton, downloadButton, importantIndex, data):
    if ds.ctx.triggered_id != None and 'download-button' in ds.ctx.triggered_id:
        dataDF = pd.DataFrame(data)
        dataDF.to_csv('cache/statesInfo.csv')
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        for d in data:
            d.update({phaseTag: d.get(phaseDBTag)})
        newData, display = typeEvents.updateData(data, df, codeStateTag, 'statesInfo.json')
        return newData, display, importantIndex
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        newData, display = typeEvents.updateData(data, df, codeStateTag, 'statesInfo.json')
        return newData, display, importantIndex
    importantIndex = typeEvents.updateImportant(ds.ctx.triggered_id, data, codeStateTag, importantIndex, 'utils/preferences/importantStates.txt')
    return data, False, importantIndex
