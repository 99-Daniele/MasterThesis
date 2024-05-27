# this page contains links to preferences pages.

import dash as ds
import pandas as pd

import utils.DataUpdate as update
import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# get dataframe with state names. 
df = getter.getStateNamesDataframe()
descriptionTag = utilities.getTagName('descriptionTag')
phaseDBTag = utilities.getTagName('phaseDBTag')
countTag = utilities.getTagName('countTag')
durationTag = utilities.getTagName('durationTag')

# return initial layout of page.
def pageLayout():
    codeStateTag = utilities.getTagName('codeStateTag')
    count = utilities.getPlaceholderName('count')
    description = utilities.getPlaceholderName('description')
    duration = utilities.getPlaceholderName('duration')
    phase = utilities.getPlaceholderName('phase')
    phaseDB = utilities.getPlaceholderName('phaseDB')
    phaseTag = utilities.getTagName('phaseTag')
    state = utilities.getPlaceholderName('state')
    tag = utilities.getPlaceholderName('tag')
    tagTag = utilities.getTagName('tagTag')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI STATI'),
        ds.html.Button("REFRESH", id = 'refresh-button-s'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': state, 'id': codeStateTag, 'editable': False}, 
                {'name': description, 'id': descriptionTag, 'editable': False}, 
                {'name': tag, 'id': tagTag, 'editable': True}, 
                {'name': phaseDB, 'id': phaseDBTag, 'editable': False}, 
                {'name': phase, 'id': phaseTag, 'editable': True}, 
                {'name': count, 'id': countTag, 'editable': False},  
                {'name': duration, 'id': durationTag, 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            id = "statetable"
        )
    ])
    return layout

# callback with input and output.
@ds.callback(
    ds.Output('statetable', 'data'),
    ds.Input('refresh-button-s', 'n_clicks'),
    ds.State('statetable', 'data')
)

# return updated data based on user choice.
def update_dateframe(button, data):
    dbData = df.to_dict('records')
    pairs = zip(data, dbData)
    if any(x != y for x, y in pairs):
        newDataDf = pd.DataFrame(data)
        newDataDf = newDataDf.drop([countTag, descriptionTag, phaseDBTag, durationTag], axis = 1)
        strData = utilities.fromListToString(list(newDataDf.itertuples(index = False, name = None)))
        file.writeOnTextFile('preferences/statesName.txt', strData)
        update.refreshData()
    return data