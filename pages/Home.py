# this is the home page.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.html.H2('Progetto Tribunali'),
        ds.dcc.Link('Grafici eventi', href = '/eventgraph'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href = '/comparationgraph'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href = '/typeevent'),
        ds.html.Br(),
        ds.dcc.Link('Parametri', href = '/preference')
    ])
    return layout
