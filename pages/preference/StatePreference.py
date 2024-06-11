# this page allows user to change state parameters.

import dash as ds

import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with state names. 
df = getter.getStateNamesDataframe()
codeStateTag = utilities.getTagName('codeStateTag')
countTag = utilities.getTagName('countTag')
phaseTag = utilities.getTagName('phaseTag')
phaseDBTag = utilities.getTagName('phaseDBTag')
df_temp = df[df[countTag] > 0]

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
    stateTag = utilities.getTagName('stateTag')
    layout = ds.html.Div([
        ds.dcc.ConfirmDialog(
            id = 'update-s',
            message = 'State names table correctly updated',
        ),
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI STATI'),
        ds.html.Button("REFRESH", id = 'refresh-button-s'),
        ds.html.Button("RESET", id = 'reset-button-s'),
        ds.dash_table.DataTable(
            df_temp.to_dict('records'), columns = [
                {'name': code, 'id': codeStateTag, 'editable': False}, 
                {'name': state, 'id': stateTag, 'editable': False}, 
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
     ds.Output('update-s', 'displayed'),
     ds.Output('statetable', 'selected_rows')],
    [ds.Input('refresh-button-s', 'n_clicks'),
     ds.Input('reset-button-s', 'n_clicks'),
     ds.Input('statetable', 'selected_rows')],
    ds.State('statetable', 'data')
)

# return updated data based on user choice.
def update_dateframe(refreshButton, resetButton, importantIndex, data):
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        for d in data:
            d.update({phaseTag: d.get(phaseDBTag)})
        return typeEvents.updateDatabase(data, df, codeStateTag, 'statesInfo.json'), importantIndex
    if ds.ctx.triggered_id != None and 'refresh-button' in ds.ctx.triggered_id:
        return typeEvents.updateDatabase(data, df, codeStateTag, 'statesInfo.json'), importantIndex
    oldImportantStates = file.getDataFromTextFile('preferences/importantStates.txt')
    if oldImportantStates == None:
        oldImportantIndex = []
    else:
        oldImportantIndex = []
        for i in range(len(data)):
            d = data[i]
            if d.get(codeStateTag) in oldImportantStates:
                oldImportantIndex.extend([i])
    if ds.ctx.triggered_id == None:
        importantIndex = oldImportantIndex
    else:
        if importantIndex == None:
            importantIndex = []
        importantStates = [data[x].get(codeStateTag) for x in importantIndex]
        if len(list(set(importantStates) - set(oldImportantStates))) > 0 or len(list(set(oldImportantStates) - set(importantStates))) > 0:
            file.writeOnTextFile('preferences/importantStates.txt', utilities.fromListToString(importantStates))
    return data, False, importantIndex
