# this page allows user to change subject names.

import dash as ds
import pandas as pd

import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities as utilities
import utils.graph.TypeEventsPreference as typeEvents

# get dataframe with judge names. 
df = getter.getSubjectNamesDataframe()
codeSubjectTag = utilities.getTagName('codeSubjectTag')
countTag = utilities.getTagName('countTag')
newDF = df[df[countTag] > 0]

# return initial layout of page.
def pageLayout():
    code = utilities.getPlaceholderName("code")
    codeSubjectTag = utilities.getTagName('codeSubjectTag')
    count = utilities.getPlaceholderName('count')
    duration = utilities.getPlaceholderName('duration')
    durationTag = utilities.getTagName('durationTag')
    ritualTag = utilities.getTagName('ritualTag')
    subjectTag = utilities.getTagName('subjectTag')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href='/preference'),
        ds.html.H2('SUBJECTS USER PREFERENCES'),
        ds.html.Button("DOWNLOAD", id = 'download-button-sbp'),
        ds.dash_table.DataTable(
            newDF.to_dict('records'), columns = [
                {'name': code, 'id': codeSubjectTag, 'editable': False},
                {'name': subjectTag, 'id': subjectTag, 'editable': False},
                {'name': ritualTag, 'id': ritualTag, 'editable': False},
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            row_selectable = 'multi',
            style_cell = {'textAlign': 'left'},
            id = "subjecttable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    ds.Output('subjecttable', 'selected_rows'),
    [ds.Input('subjecttable', 'selected_rows'),
     ds.Input('download-button-sbp', 'n_clicks')],
    ds.State('subjecttable', 'data')
)

# return updated data based on user choice.
def update_dateframe(importantIndex, downloadButton, data):
    if ds.ctx.triggered_id != None and 'download-button' in ds.ctx.triggered_id:
        dataDF = pd.DataFrame(data)
        dataDF.to_csv('cache/subjectsInfo.csv')
    typeEvents.updateImportant(data, codeSubjectTag, importantIndex, 'utils/preferences/importantSubjects.txt')
    return importantIndex
