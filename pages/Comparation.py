# this page contains links to comparison graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('DURATION COMPARISON GRAPHS'),
        ds.dcc.Link('Comparison of Processes Duration', href = '/comparison/processcomparison'),
        ds.html.Br(),
        ds.dcc.Link('Comparison of Phases Duration', href = '/comparison/phasecomparison'),
        ds.html.Br(),
        ds.dcc.Link('Comparison of States Duration', href = '/comparison/statecomparison'),        
        ds.html.Br(),
        ds.dcc.Link('Comparison of Events Duration', href = '/comparison/eventcomparison'),    
        ds.html.Br(),
        ds.dcc.Link('Comparison of Processes Duration Based on Type', href = '/comparison/typecomparison')
    ])
    return layout
