# this page contains links to comparation graph pages.

import dash as ds

# return initial layout of page.
def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href = '/'),
        ds.html.H2('Grafici confronto'),
        ds.dcc.Link('Confronto processi', href = '/comparationgraph/processcomparation'),
        ds.html.Br(),
        ds.dcc.Link('Confronto fasi', href = '/comparationgraph/phasecomparation'),
        ds.html.Br(),
        ds.dcc.Link('Confronto stati', href = '/comparationgraph/statecomparation'),        
        ds.html.Br(),
        ds.dcc.Link('Confronto eventi', href = '/comparationgraph/eventcomparation'),    
        ds.html.Br(),
        ds.dcc.Link('Confronto tipi', href = '/comparationgraph/typecomparation')
    ])
    return layout
