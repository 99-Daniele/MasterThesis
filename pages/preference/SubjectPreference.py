# this page allows user to change subject names.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
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
        ds.dcc.ConfirmDialog(
            id = 'update-su',
            message = 'Subjects names table correctly updated',
        ),
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI MATERIA'),
        ds.html.Button("REFRESH", id = 'refresh-button-su'),
        ds.dash_table.DataTable(
            df_temp.to_dict('records'), columns = [
                {'name': code, 'id': codeSubjectTag, 'editable': False},
                {'name': subjectTag, 'id': subjectTag, 'editable': False},
                {'name': ritualTag, 'id': ritualTag, 'editable': False},
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            style_cell = {'textAlign': 'left'},
            id = "subjecttable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('subjecttable', 'data'),
     ds.Output('update-su', 'displayed')],
    ds.Input('refresh-button-su', 'n_clicks'),
    ds.State('subjecttable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, data):
    return data, False
