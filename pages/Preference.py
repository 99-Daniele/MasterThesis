# this page contains links to preferences pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('Parametri'),
        ds.dcc.Link('Stati', href = '/preference/statepreference'),
        ds.html.Br(),
        ds.dcc.Link('Eventi', href = '/preference/eventpreference'),
        ds.html.Br(),
        ds.dcc.Link('Materie', href = '/preference/subjectpreference')
    ])
    return layout