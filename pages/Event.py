# this page contains links to events graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('Grafici eventi'),
        ds.dcc.Link('Tutti gli eventi', href = '/eventgraph/allevents'),
        ds.html.Br(),
        ds.dcc.Link('Eventi fasi', href = '/eventgraph/phaseevents'),
        ds.html.Br(),
        ds.dcc.Link('Eventi stati', href = '/eventgraph/stateevents')
    ])
    return layout
