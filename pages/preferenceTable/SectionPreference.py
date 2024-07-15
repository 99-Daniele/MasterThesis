# this page allows user to change section preferences.

import dash as ds
import pandas as pd

import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.TypeEventsPreference as typeEvents

# get dataframe with judge names. 
df = getter.getSectionDataframe()
sectionTag = utilities.getTagName('sectionTag')

# return initial layout of page.
def pageLayout():
    count = utilities.getPlaceholderName('count')
    countTag = utilities.getTagName('countTag')
    duration = utilities.getPlaceholderName('duration')
    durationTag = utilities.getTagName('durationTag')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('SECTION USER PREFERENCES'),
        ds.html.Button("DOWNLOAD", id = 'download-button-scp'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': sectionTag, 'id': sectionTag, 'editable': False},
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = 'multi',
            style_cell = {'textAlign': 'left'},
            id = "sectiontable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    ds.Output('sectiontable', 'selected_rows'),
    [ds.Input('sectiontable', 'selected_rows'),
     ds.Input('download-button-scp', 'n_clicks')],
    ds.State('sectiontable', 'data')
)

# return updated data based on user choice.
def update_dateframe(importantIndex, downloadButton, data):
    if ds.ctx.triggered_id != None and 'download-button' in ds.ctx.triggered_id:
        dataDF = pd.DataFrame(data)
        dataDF.to_csv('cache/sectionInfo.csv')
    importantIndex = typeEvents.updateImportant(ds.ctx.triggered_id, data, sectionTag, importantIndex, 'utils/preferences/importantSections.txt')
    return importantIndex
