# this page allows user to change events parameters.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with events names. 
df = getter.getEventNamesDataframe()
codeEventTag = utilities.getTagName('codeEventTag')
countTag = utilities.getTagName('countTag')
df_temp = df[df[countTag] > 0]

# return initial layout of page.
def pageLayout():
    code = utilities.getPlaceholderName("code")
    count = utilities.getPlaceholderName('count')
    duration = utilities.getPlaceholderName('duration')
    durationTag = utilities.getTagName('durationTag')
    event = utilities.getPlaceholderName('event')
    eventTag = utilities.getTagName('eventTag')
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
            df_temp.to_dict('records'), columns = [
                {'name': code, 'id': codeEventTag, 'editable': False}, 
                {'name': event, 'id': eventTag, 'editable': False},  
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            style_cell = {'textAlign': 'left'},
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
    return data, False