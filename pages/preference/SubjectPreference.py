# this page allows user to change subject names.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with judge names. 
df = getter.getSubjectNamesDataframe()
countTag = utilities.getTagName('countTag')
durationTag = utilities.getTagName('durationTag')

# return initial layout of page.
def pageLayout():
    codeSubjectTag = utilities.getTagName('codeSubjectTag')
    count = utilities.getPlaceholderName('count')
    descriptionSubjectTag = utilities.getTagName('descriptionSubjectTag')
    duration = utilities.getPlaceholderName('duration')
    ritualTag = utilities.getTagName('ritualTag')
    tagSubjectTag = utilities.getTagName('tagSubjectTag')
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
            df.to_dict('records'), columns = [
                {'name': codeSubjectTag, 'id': codeSubjectTag, 'editable': False},
                {'name': descriptionSubjectTag, 'id': descriptionSubjectTag, 'editable': False},
                {'name': ritualTag, 'id': ritualTag, 'editable': False},
                {'name': tagSubjectTag, 'id': tagSubjectTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
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
    return typeEvents.updateDatabase(data, df, [countTag, durationTag], 'preferences/subjectsName.json')
