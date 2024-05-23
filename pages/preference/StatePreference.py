# this page contains links to preferences pages.

import dash as ds
import pandas as pd

import utils.FileOperation as file
import utils.Getters as getter
import utils.DataUpdate as update

df = getter.getStateNamesDataframe()

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href='/preference'),
        ds.html.H2('PARAMETRI STATI'),
        ds.html.Button("REFRESH", id = 'refresh-button-s'),
        ds.dash_table.DataTable(
            df.to_dict('records'), columns = [
                {'name': 'stato', 'id': 'codicestato', 'editable': False}, 
                {'name': 'descrizione', 'id': 'descrizione', 'editable': False}, 
                {'name': 'etichetta', 'id': 'etichetta', 'editable': True}, 
                {'name': 'fase_db', 'id': 'fase_db', 'editable': False}, 
                {'name': 'fase', 'id': 'fase', 'editable': True}, 
                {'name': 'conteggio', 'id': 'conteggio', 'editable': False},  
                {'name': 'durata [gg]', 'id': 'durata', 'editable': False}],
            filter_action = "native",
            sort_action = "native",
            id = "statetable"
        )
    ])
    return layout

@ds.callback(
    ds.Output('statetable', 'data'),
    ds.Input('refresh-button-s', 'n_clicks'),
    ds.State('statetable', 'data')
)

def update_dateframe(button, data):
    dbData = df.to_dict('records')
    pairs = zip(data, dbData)
    if any(x != y for x, y in pairs):
        newDataDf = pd.DataFrame(data)
        newDataDf = newDataDf.drop(['conteggio', 'fase_db', 'durata'], axis = 1)
        listData = str(list(newDataDf.itertuples(index = False, name = None)))
        file.writeOnTextFile('preferences/statesName.txt', listData)
        update.refreshData()
    return data