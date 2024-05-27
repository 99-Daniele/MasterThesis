# this page allows user to change judge names.

import dash as ds

import utils.Getters as getter
import utils.graph.TypeEventsPreference as typeEvents
import utils.utilities.Utilities as utilities

# get dataframe with judge names. 
df = getter.getJudgeNamesDataframe()
countTag = utilities.getTagName('countTag')
durationTag = utilities.getTagName('durationTag')

# return initial layout of page.
def pageLayout():
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    count = utilities.getPlaceholderName('count')
    duration = utilities.getPlaceholderName('duration')
    judgeTag = utilities.getTagName('judgeTag')
    layout = ds.html.Div([
        ds.dcc.ConfirmDialog(
            id = 'update-j',
            message = 'Judge names table correctly updated',
        ),
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI GIUDICE'),
        ds.html.Button("REFRESH", id = 'refresh-button-j'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': codeJudgeTag, 'id': codeJudgeTag, 'editable': False},
                {'name': judgeTag, 'id': judgeTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            id = "judgetable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('judgetable', 'data'),
     ds.Output('update-j', 'displayed')],
    ds.Input('refresh-button-j', 'n_clicks'),
    ds.State('judgetable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, data):
    return typeEvents.updateDatabase(data, df, [countTag, durationTag], 'preferences/judgesName.txt')
