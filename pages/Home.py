import dash as ds

def pageLayout():
    layout = ds.html.Div([
        ds.html.H1('Progetto Tribunali'),
        ds.dcc.Link('Grafici durata', href='/durationgraph'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph')
    ])