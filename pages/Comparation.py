# this page contains links to comparation graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('DURATION COMPARISON GRAPHS'),
        ds.dcc.Link('Comparison of Processes Duration', href = '/comparationgraph/processcomparation'),
        ds.html.Br(),
        ds.dcc.Link('Comparison of Phases Duration', href = '/comparationgraph/phasecomparation'),
        ds.html.Br(),
        ds.dcc.Link('Comparison of States Duration', href = '/comparationgraph/statecomparation'),        
        ds.html.Br(),
        ds.dcc.Link('Comparison of Events Duration', href = '/comparationgraph/eventcomparation'),    
        ds.html.Br(),
        ds.dcc.Link('Comparison of Duration Based on Type', href = '/comparationgraph/typecomparation')
    ])
    return layout
