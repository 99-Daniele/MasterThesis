# this page contains links to type events graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('COMPOSITION GRAPHS'),
        ds.dcc.Link('State Compositions', href = '/typeevent/stateevent'),
        ds.html.Br(),
        ds.dcc.Link('Phase Compositions', href = '/typeevent/phaseevent'),
        ds.html.Br(),
        ds.dcc.Link('State Sequence', href = '/typeevent/statesequence'),
        ds.html.Br(),
        ds.dcc.Link('Phase Sequence', href = '/typeevent/phasesequence'),
        ds.html.Br(),
        ds.dcc.Link('Event Sequence', href = '/typeevent/eventsequence')
    ])
    return layout