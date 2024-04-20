import dash as ds

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
        ds.dcc.Link('Confronto eventi', href = '/comparationgraph/eventcomparation')
    ])
    return layout
