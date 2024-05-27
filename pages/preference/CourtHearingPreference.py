# this page allows user to change events parameters.

import dash as ds

import utils.Dataframe as frame
import utils.DataUpdate as update
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with events names. 
df = getter.getEventNamesDataframe()
courtHearingEvents = file.getDataFromTextFile('preferences/courtHearingsEvents.txt')
codeEventTag = utilities.getTagName('codeEventTag')
descriptionTag = utilities.getTagName('descriptionTag')
phaseTag = utilities.getTagName('phaseTag')
tagTag = utilities.getTagName('tagTag')
selectedRows = frame.getSelectedRows(df, courtHearingEvents, tagTag)

# return initial layout of page.
def pageLayout():
    description = utilities.getPlaceholderName('description')
    event = utilities.getPlaceholderName('event')
    phase = utilities.getPlaceholderName('phase')
    tag = utilities.getPlaceholderName('tag')
    layout = ds.html.Div([
        ds.dcc.ConfirmDialog(
            id = 'update-ch',
            message = 'Court hearing names table correctly updated',
        ),
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI UDIENZE'),
        ds.html.Button("REFRESH", id = 'refresh-button-ch'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': event, 'id': codeEventTag, 'editable': False}, 
                {'name': description, 'id': descriptionTag, 'editable': False}, 
                {'name': tag, 'id': tagTag, 'editable': False, 'selectable': True}, 
                {'name': phase, 'id': phaseTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = "multi",
            selected_rows = selectedRows,
            id = "courthearingtable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('courthearingtable', 'data'),
     ds.Output('update-ch', 'displayed')],
    [ds.Input('refresh-button-ch', 'n_clicks'),
     ds.Input('courthearingtable', 'selected_rows')],
    ds.State('courthearingtable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, newSelectedRows, data):
    data, display = typeEvents.updateTextFile(data, selectedRows, newSelectedRows, 'preferences/courtHearingsEvents.txt')
    if display == True:
        update.refreshData()
    return data, display

