# this page contains links to events graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('EVENTS VISUALIZATION GRAPHS'),
        ds.dcc.Link('Visualize All Events', href = '/eventgraph/allevents'),
        ds.html.Br(),
        ds.dcc.Link('Visualiza Phase Events', href = '/eventgraph/phaseevents'),
        ds.html.Br(),
        ds.dcc.Link('Visualize State Events', href = '/eventgraph/stateevents')
    ])
    return layout
