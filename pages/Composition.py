# this page contains links to composition graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('COMPOSITION GRAPHS'),
        ds.dcc.Link('State Compositions', href = '/composition/stateevent'),
        ds.html.Br(),
        ds.dcc.Link('Phase Compositions', href = '/composition/phaseevent'),
        ds.html.Br(),
        ds.dcc.Link('State Sequence', href = '/composition/statesequence'),
        ds.html.Br(),
        ds.dcc.Link('Phase Sequence', href = '/composition/phasesequence'),
        ds.html.Br(),
        ds.dcc.Link('Event Sequence', href = '/composition/eventsequence')
    ])
    return layout