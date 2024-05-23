# this page contains links to type events graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('Grafici tipo eventi'),
        ds.dcc.Link('Eventi in uno stato', href = '/typeevent/stateevent'),
        ds.html.Br(),
        ds.dcc.Link('Eventi in una fase', href = '/typeevent/phaseevent'),
        ds.html.Br(),
        ds.dcc.Link('Sequenza stati', href = '/typeevent/statesequence'),
        ds.html.Br(),
        ds.dcc.Link('Sequenza fasi', href = '/typeevent/phasesequence'),
        ds.html.Br(),
        ds.dcc.Link('Sequenza eventi', href = '/typeevent/eventsequence')
    ])
    return layout