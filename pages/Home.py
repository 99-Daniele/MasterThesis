# this is the home page.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.html.H2('HOME'),
        ds.dcc.Link('EVENTS VISUALIZATION GRAPHS', href = '/eventgraph'),
        ds.html.Br(),
        ds.dcc.Link('DURATION COMPARISON GRAPHS', href = '/comparationgraph'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href = '/typeevent'),
        ds.html.Br(),
        ds.dcc.Link('USER PARAMETERS PREFERENCES', href = '/preference'),
        ds.html.Br(),
        ds.dcc.Link('PREDICTION DURATION PAGE', href = '/prediction')
    ])
    return layout
