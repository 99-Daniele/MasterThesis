import dash as ds

def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.H1('Grafici confronto'),
        ds.dcc.Link('Confronto per settimana', href='/comparationgraph/weekcomparation'),
        ds.html.Br(),
        ds.dcc.Link('Confronto per mese', href='/comparationgraph/monthcomparation'),
        ds.html.Br(),
        ds.dcc.Link('Confronto per mese dell anno', href='/comparationgraph/monthyearcomparation')
    ])
    return layout