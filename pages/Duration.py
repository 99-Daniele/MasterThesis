import dash as ds

def pageLayout():
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.H2('Grafici durata'),
        ds.dcc.Link('Durata processi', href='/durationgraph/processduration'),
        ds.html.Br(),
        ds.dcc.Link('Durata udienze', href='/durationgraph/courthearingsduration'),
        ds.html.Br(),
        ds.dcc.Link('Durata fasi', href='/durationgraph/phaseduration'),
        ds.html.Br(),
        ds.dcc.Link('Durata stati', href='/durationgraph/stateduration'),
        ds.html.Br(),
        ds.dcc.Link('Durata eventi', href='/durationgraph/eventduration')
    ])
    return layout
