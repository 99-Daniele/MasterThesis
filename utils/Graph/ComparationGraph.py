import plotly.express as px
import dash as ds

import utils.DataFrame as frame
import utils.Legenda as legenda

def addCountToName(name, df, type):
    if type == 'finito':
        count = df[df[type] == int(name)]['size'].item()
        name = legenda.processState[int(name)]
    elif type == 'cambio':
        count = df[df[type] == int(name)]['size'].item()
        if int(name) == 0:
            name = "NO"
        else:
            name = "SI"
    else:
        count = df[df[type] == name]['size'].item()
    newName = name + " (" + str(count) + ")"
    return newName

def addMaxCountToName(df):
    newName = "TUTTI (" + str(df['size'].sum()) + ")"
    return newName

def getPosition(name, df, type):
    pos = df.index.get_loc(df[df[type] == name].index[0])
    return pos

def displayComparationByMonthYear(df):
    df_temp = df.copy()
    [typeData, allData, countData] = frame.getAvgDataFrameByType(df_temp, "MY", 'sezione')
    fig = px.line(typeData, x = "data", y = "durata", color = "sezione", markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, title = "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INZIO PROCESSO", width = 1400, height = 600)
    app = ds.Dash()
    app.layout = ds.html.Div([
        #ds.dcc.Dropdown(legenda.processState, value = [legenda.processState[0]], multi = True, searchable = False, id = 'finished-dropdown', placeholder = 'Seleziona tipo di processo...', style = {'width': 400}),
        #ds.dcc.Dropdown(events, multi = False, searchable = False, id = 'event-dropdown', placeholder = 'Seleziona evento...', style = {'width': 400}),
        #ds.dcc.Dropdown(years, multi = True, searchable = False, id = 'year-dropdown', placeholder = 'Seleziona anno...', style = {'width': 400}),
        #ds.dcc.Dropdown(['NO', 'SI'], multi = False, searchable = False, id = 'change-dropdown', placeholder = 'Cambio giudice', style = {'width': 400}),
        ds.dcc.RadioItems(['sezione', 'materia', 'giudice', 'finito', 'cambio', 'sequenza'], value = 'sezione', id = "choice-radioitem", inline = True),
        ds.dcc.Graph(id = 'events-graph', figure = fig)
    ])
    @app.callback(
        ds.Output('events-graph', 'figure'),
        [ds.Input('choice-radioitem', 'value')]
    )
    def update_output(choice):
        df_temp = df.copy()
        [typeData, allData, countData] = frame.getAvgDataFrameByType(df_temp, "MY", choice)
        fig = px.line(typeData, x = "data", y = "durata", color = choice, markers = True, labels = {'durata':'Durata processo [giorni]', 'data':'Data inizio processo'}, title = "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INZIO PROCESSO", width = 1400, height = 600)
        fig.update_traces(visible = "legendonly", selector = (lambda t: t))
        fig.for_each_trace(
            lambda t: t.update(
                name = addCountToName(t.name, countData, choice)
            )
        )
        fig.add_traces(
            px.line(allData, x = "data", y = "durata").update_traces(showlegend = True, name = addMaxCountToName(countData), line_color = 'rgb(0, 0, 0)', line = {'width': 3}).data
        )
        fig.update_xaxes(gridcolor = 'grey', griddash = 'dash')
        fig.update_yaxes(gridcolor = 'grey', griddash = 'dash')
        return fig
    
    app.run(debug = True)