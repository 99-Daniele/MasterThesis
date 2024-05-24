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
    phaseTag = utilities.getTagName('phaseTag')
    tagTag = utilities.getTagName('tagTag')
    codeStateTag = utilities.getTagName('codeStateTag')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI STATI'),
        ds.html.Button("REFRESH", id = 'refresh-button-s'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': 'stato', 'id': codeStateTag, 'editable': False}, 
                {'name': 'descrizione', 'id': descriptionTag, 'editable': False}, 
                {'name': 'etichetta', 'id': tagTag, 'editable': True}, 
                {'name': 'fase_db', 'id': phaseDBTag, 'editable': False}, 
                {'name': 'fase', 'id': phaseTag, 'editable': True}, 
                {'name': 'conteggio', 'id': countTag, 'editable': False},  
                {'name': 'durata [gg]', 'id': durationTag, 'editable': False}],
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