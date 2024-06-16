# this page allows user to change events parameters.

import dash as ds
import pandas as pd

import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities as utilities

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
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('EVENTS USER PREFERENCES'),
        ds.html.Button("DOWNLOAD", id = 'download-button-ep'),
        ds.dash_table.DataTable(
            df_temp.to_dict('records'), columns = [
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
    oldImportantEvents = file.getDataFromTextFile('preferences/importantEvents.txt')
    if oldImportantEvents == None:
        oldImportantIndex = []
    else:
        oldImportantIndex = []
        for i in range(len(data)):
            d = data[i]
            if d.get(codeEventTag) in oldImportantEvents:
                oldImportantIndex.extend([i])
    if ds.ctx.triggered_id == None:
        importantIndex = oldImportantIndex
    else:
        if importantIndex == None:
            importantIndex = []
        importantEvents = [data[x].get(codeEventTag) for x in importantIndex]
        if len(list(set(importantEvents) - set(oldImportantEvents))) > 0 or len(list(set(oldImportantEvents) - set(importantEvents))) > 0:
            file.writeOnTextFile('preferences/importantEvents.txt', utilities.fromListToString(importantEvents))
    return importantIndex