# this page contains links to duration graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('Grafici durata'),
        ds.dcc.Link('Durata processi', href = '/durationgraph/processduration'),
        ds.html.Br(),
        ds.dcc.Link('Durata udienze', href = '/durationgraph/courthearingsduration')
    ])
    return layout
