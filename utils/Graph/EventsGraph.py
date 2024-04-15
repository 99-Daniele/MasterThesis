import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities as utilities

def displayEvents(df, type, mustEvents):
    sections = frame.getGroupBy(df, 'sezione')
    subjects = frame.getGroupBy(df, 'materia')
    judges = frame.getGroupBy(df, 'giudice')
    maxYear = dt.datetime.strptime(df['data'].max(), '%Y-%m-%d %H:%M:%S').year
    minYear = maxYear - 1
    fig = px.scatter(df, x = "data", y = "numProcesso", color = type, labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1400, height = 1200)
    app = ds.Dash(suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('EVENTI DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger',
            start_date = dt.date(minYear, 1, 1),
            end_date = dt.date(maxYear, 1, 1),
            min_date_allowed = df['data'].min(),
            max_date_allowed = df['data'].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown', placeholder = 'SEZIONE', style = {'width': 285}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown', placeholder = 'MATERIA', style = {'width': 285}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown', placeholder = 'GIUDICE', style = {'width': 285}),
        ds.dcc.Graph(figure = fig, id = 'events-graph')
    ])
    @app.callback(
        [ds.Output('events-graph', 'figure'),
         ds.Output('event-dateranger', 'start_date'), 
         ds.Output('event-dateranger', 'end_date'),
         ds.Output('section-dropdown', 'options'),
         ds.Output('subject-dropdown', 'options'),
         ds.Output('judge-dropdown', 'options')],
        [ds.Input('event-dateranger', 'start_date'), 
         ds.Input('event-dateranger', 'end_date'), 
         ds.Input('event-dateranger', 'min_date_allowed'), 
         ds.Input('event-dateranger', 'max_date_allowed'), 
         ds.Input('reset-button', 'n_clicks'),
         ds.Input('section-dropdown', 'value'),
         ds.Input('subject-dropdown', 'value'),
         ds.Input('judge-dropdown', 'value')])
    def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
         return eventUpdate(df, startDate, endDate, type, mustEvents, minDate, maxDate, sections, subjects, judges)
    app.run_server(debug = True)

def eventUpdate(df, startDate, endDate, type, mustEvents, minDate, maxDate, sections, subjects, judges):
    df_temp = df.copy()
    if "reset-button" == ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    df_temp = frame.getDateDataFrame(df_temp, 'dataInizioProcesso', startDate, endDate)
    if sections != None and len(sections) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    if subjects != None and len(subjects) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    if judges != None and len(judges) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    sections = frame.getGroupBy(df_temp, 'sezione')
    subjects = frame.getGroupBy(df_temp, 'materia')
    judges = frame.getGroupBy(df_temp, 'giudice')
    fig = px.scatter(df_temp, x = "data", y = "numProcesso", color = type, color_discrete_sequence = utilities.phaseColorList(df_temp, type), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, height = 1200)
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99
        ),
        yaxis = dict(
            showticklabels = False
        )
    )
    fig.update_xaxes(
        dtick = "M1",
        tickformat = "%b\n%Y",
        ticklabelmode = "period"
    )   
    fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name not in mustEvents else False))
    return fig, startDate, endDate, sections, subjects, judges