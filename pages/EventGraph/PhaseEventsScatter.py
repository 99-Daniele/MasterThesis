# this page shows phase events.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.EventsGraph as event
import utils.utilities.Utilities as utilities

# get dataframe with phase events. 
# get must phases from text file.
df = getter.getPhaseEvents()
phaseTag = utilities.getTagName('phaseTag') 

# return initial layout of page.
def pageLayout():
    dateTag = utilities.getTagName('dateTag') 
    eventTag = utilities.getTagName('eventTag') 
    judge = utilities.getPlaceholderName('judge') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    numProcessTag = utilities.getTagName('numProcessTag')
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    maxYear = dt.datetime.strptime(df[dateTag].max(), '%Y-%m-%d %H:%M:%S').year
    maxDateStart = dt.date(maxYear - 1, 1, 1)
    maxDateEnd = dt.date(maxYear, 1, 1)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    fig = px.scatter(df, x = dateTag, y = numProcessTag, color = eventTag, labels = {numProcessTag:'Codice Processo', dateTag:'Data inizio processo'}, width = 1400, height = 1200)
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici eventi', href='/eventgraph'),
        ds.html.H2('EVENTI INIZIO FASE DEL PROCESSO'),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-phes',
            start_date = maxDateStart,
            end_date = maxDateEnd,
            min_date_allowed = df[dateTag].min(),
            max_date_allowed = df[dateTag].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = 'reset-button-phes'),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-phes', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-phes', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-phes', placeholder = judge, style = {'width': 400}),
        ds.dcc.Graph(figure = fig, id = 'events-graph-phes')
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('events-graph-phes', 'figure'),
        ds.Output('event-dateranger-phes', 'start_date'), 
        ds.Output('event-dateranger-phes', 'end_date'),
        ds.Output('section-dropdown-phes', 'options'),
        ds.Output('subject-dropdown-phes', 'options'),
        ds.Output('judge-dropdown-phes', 'options')],
    [ds.Input('event-dateranger-phes', 'start_date'), 
        ds.Input('event-dateranger-phes', 'end_date'), 
        ds.Input('event-dateranger-phes', 'min_date_allowed'), 
        ds.Input('event-dateranger-phes', 'max_date_allowed'), 
        ds.Input('reset-button-phes', 'n_clicks'),
        ds.Input('section-dropdown-phes', 'value'),
        ds.Input('subject-dropdown-phes', 'value'),
        ds.Input('judge-dropdown-phes', 'value')])

# return updated data based on user choice.
def updateOutput(startDate, endDate, minDate, maxDate, button, sections, subjects, judges):
    df[phaseTag] = df[phaseTag].astype(str)
    return event.eventUpdate(df, startDate, endDate, phaseTag, None, minDate, maxDate, sections, subjects, judges)
