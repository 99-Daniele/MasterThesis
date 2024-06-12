# this page contains links to preferences pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href = '/'),
        ds.html.H2('PARAMETER SELECTION'),
        ds.dcc.Link('Select State Preference', href = '/preference/statepreference'),
        ds.html.Br(),
        ds.dcc.Link('Select Event Preference', href = '/preference/eventpreference'),
        ds.html.Br(),
        ds.dcc.Link('Select Subject Preference', href = '/preference/subjectpreference')
    ])
    return layout