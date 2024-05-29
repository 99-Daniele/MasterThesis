# this page allows user to change events parameters.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with events names. 
df = getter.getEventNamesDataframeWithInfo()
descriptionTag = utilities.getTagName('descriptionTag')
countTag = utilities.getTagName('countTag')
durationTag = utilities.getTagName('durationTag')

# return initial layout of page.
def pageLayout():
    codeEventTag = utilities.getTagName('codeEventTag')
    count = utilities.getPlaceholderName('count')
    description = utilities.getPlaceholderName('description')
    duration = utilities.getPlaceholderName('duration')
    eventTag = utilities.getTagName('eventTag')
    phase = utilities.getPlaceholderName('phase')
    phaseTag = utilities.getTagName('phaseTag')
    layout = ds.html.Div([
        ds.dcc.ConfirmDialog(
            id = 'update-e',
            message = 'Event names table correctly updated',
        ),
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI EVENTI'),
        ds.html.Button("REFRESH", id = 'refresh-button-e'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': codeEventTag, 'id': codeEventTag, 'editable': False}, 
                {'name': description, 'id': descriptionTag, 'editable': False}, 
                {'name': eventTag, 'id': eventTag, 'editable': True},  
                {'name': phase, 'id': phaseTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            id = "eventtable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('eventtable', 'data'),
     ds.Output('update-e', 'displayed')],
    ds.Input('refresh-button-e', 'n_clicks'),
    ds.State('eventtable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, data):
    return typeEvents.updateDatabase(data, df, [countTag, descriptionTag, durationTag], 'preferences/eventsName.txt')
