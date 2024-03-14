import dash as ds

layout = ds.html.Div([
    ds.dcc.Link('Home', href='/'),
    ds.html.H1('Grafici eventi'),
    ds.dcc.Link('Tutti gli eventi', href='/eventgraph/allevents'),
    ds.html.Br(),
    ds.dcc.Link('Eventi importanti', href='/eventgraph/importantevents'),
    ds.html.Br(),
    ds.dcc.Link('Udienze', href='/eventgraph/courthearings')
])