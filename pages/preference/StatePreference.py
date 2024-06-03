# this page allows user to change state parameters.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with state names. 
df = getter.getStateNamesDataframe()
codeStateTag = utilities.getTagName('codeStateTag')
countTag = utilities.getTagName('countTag')
df_temp = df[df[countTag] > 0]

# return initial layout of page.
def pageLayout():
    code = utilities.getPlaceholderName('code')
    codeStateTag = utilities.getTagName('codeStateTag')
    count = utilities.getPlaceholderName('count')
    descriptionTag = utilities.getTagName('descriptionTag')
    durationTag = utilities.getTagName('durationTag')
    description = utilities.getPlaceholderName('description')
    duration = utilities.getPlaceholderName('duration')
    phase = utilities.getPlaceholderName('phase')
    phaseDB = utilities.getPlaceholderName('phaseDB')
    phaseTag = utilities.getTagName('phaseTag')
    phaseDBTag = utilities.getTagName('phaseDBTag')
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
        ds.dash_table.DataTable(
            df_temp.to_dict('records'), columns = [
                {'name': code, 'id': codeStateTag, 'editable': False}, 
                {'name': description, 'id': descriptionTag, 'editable': False}, 
                {'name': state, 'id': stateTag, 'editable': True}, 
                {'name': phaseDB, 'id': phaseDBTag, 'editable': False}, 
                {'name': phase, 'id': phaseTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            id = "statetable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('statetable', 'data'),
     ds.Output('update-s', 'displayed')],
    ds.Input('refresh-button-s', 'n_clicks'),
    ds.State('statetable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, data):
    return typeEvents.updateDatabase(data, df, codeStateTag, 'statesInfo.json')
