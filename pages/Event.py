import dash as ds

def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.H2('Grafici eventi'),
        ds.dcc.Link('Tutti gli eventi', href='/eventgraph/allevents'),
        ds.html.Br(),
        ds.dcc.Link('Eventi importanti', href='/eventgraph/importantevents'),
        ds.html.Br(),
        ds.dcc.Link('Eventi fasi', href='/eventgraph/phaseevents'),
        ds.html.Br(),
        ds.dcc.Link('Eventi stati', href='/eventgraph/stateevents')
    ])
    return layout