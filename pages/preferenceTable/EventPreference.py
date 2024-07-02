# this page allows user to change events parameters.

import dash as ds
import pandas as pd

import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.TypeEventsPreference as typeEvents

# get dataframe with events names. 
df = getter.getEventNamesDataframe()
codeEventTag = utilities.getTagName('codeEventTag')
countTag = utilities.getTagName('countTag')
# for better readability only events that are registered at least one time in the database are shown.
df = df[df[countTag] > 0]

# return initial layout of page.
def pageLayout():
    code = utilities.getPlaceholderName("code")
    count = utilities.getPlaceholderName('count')
    duration = utilities.getPlaceholderName('duration')
    durationTag = utilities.getTagName('durationTag')
    event = utilities.getPlaceholderName('event')
    eventTag = utilities.getTagName('eventTag')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('EVENTS USER PREFERENCES'),
        ds.html.Button("DOWNLOAD", id = 'download-button-ep'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': code, 'id': codeEventTag, 'editable': False}, 
                {'name': event, 'id': eventTag, 'editable': False},  
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = 'multi',
            style_cell = {'textAlign': 'left'},
            id = "eventtable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    ds.Output('eventtable', 'selected_rows'),
    [ds.Input('eventtable', 'selected_rows'),
     ds.Input('download-button-ep', 'n_clicks')],
    ds.State('eventtable', 'data')
)

# return updated data based on user choice.
def update_dateframe(importantIndex, downloadButton, data):
    if ds.ctx.triggered_id != None and 'download-button' in ds.ctx.triggered_id:
        dataDF = pd.DataFrame(data)
        dataDF.to_csv('cache/eventsInfo.csv')
    importantIndex = typeEvents.updateImportant(ds.ctx.triggered_id, data, codeEventTag, importantIndex, 'utils/preferences/importantEvents.txt')
    return importantIndex