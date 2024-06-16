# this page allows user to change subject names.

import dash as ds
import pandas as pd

import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# get dataframe with judge names. 
df = getter.getSubjectNamesDataframe()
codeSubjectTag = utilities.getTagName('codeSubjectTag')
countTag = utilities.getTagName('countTag')
df_temp = df[df[countTag] > 0]

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
            df_temp.to_dict('records'), columns = [
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
    oldImportantSubjects = file.getDataFromTextFile('preferences/importantSubjects.txt')
    if oldImportantSubjects == None:
        oldImportantIndex = []
    else:
        oldImportantIndex = []
        for i in range(len(data)):
            d = data[i]
            if str(d.get(codeSubjectTag)) in oldImportantSubjects:
                oldImportantIndex.extend([i])
    if ds.ctx.triggered_id == None:
        importantIndex = oldImportantIndex
    else:
        if importantIndex == None:
            importantIndex = []
        importantSubjects = [data[x].get(codeSubjectTag) for x in importantIndex]
        if len(list(set(importantSubjects) - set(oldImportantSubjects))) > 0 or len(list(set(oldImportantSubjects) - set(importantSubjects))) > 0:
            file.writeOnTextFile('preferences/importantSubjects.txt', utilities.fromListToString(importantSubjects))
    return importantIndex
