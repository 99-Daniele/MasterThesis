# this page shows phases duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.utilities.Utilities as utilities

# get dataframe with all phases duration.
df = getter.getPhasesDurationFiltered()
phaseTag = utilities.getTagName('phaseTag') 

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag') 
    countTag = utilities.getTagName('countTag') 
    dateTag = utilities.getTagName('dateTag') 
    finishedTag = utilities.getTagName('finishedTag') 
    judge = utilities.getPlaceholderName('judge') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    median = utilities.getPlaceholderName('median') 
    month = utilities.getPlaceholderName('month')
    monthYear = utilities.getPlaceholderName('monthYear') 
    phase = utilities.getPlaceholderName('phase') 
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text') 
    trimester = utilities.getPlaceholderName('trimester') 
    trimesterYear = utilities.getPlaceholderName('trimesterYear')
    week = utilities.getPlaceholderName('week')
    year = utilities.getPlaceholderName('year') 
    types = frame.getUniques(df, phaseTag)
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    finished = frame.getGroupBy(df, finishedTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2('DURATA MEDIA FASI DEL PROCESSO', id = 'title-ph'),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-ph', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([week, month, monthYear, trimester, trimesterYear, year], value = month, id = 'date-radioitem-ph', inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.html.Div(children = [
            ds.dcc.DatePickerRange(
                id = 'event-dateranger-ph',
                start_date = df[dateTag].min(),
                end_date = df[dateTag].max(),
                min_date_allowed = df[dateTag].min(),
                max_date_allowed = df[dateTag].max(),
                display_format = 'DD MM YYYY',
                style = {'width': 300, 'display':'none'}
            ),        
            ds.html.Button("RESET", id = 'reset-button-ph', style = {'display':'none'})
            ],
            style = {'display':'flex'}
        ),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-ph', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ph', placeholder = section, style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ph', placeholder = subject, style = {'display': 'none'}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ph', placeholder = judge, style = {'display': 'none'}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-ph', placeholder = process, style = {'display': 'none'}),
        ds.dcc.Checklist([sectionTag, subjectTag, codeJudgeTag, finishedTag], value = [], id = 'choice-checklist-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.RadioItems([countTag, avgTag], value = countTag, id = 'order-radioitem-ph', inline = True, style = {'display': 'none'}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-ph'),
        ds.dcc.Graph(id = 'comparation-graph-ph', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-ph', 'figure'),
        ds.Output('event-dateranger-ph', 'start_date'), 
        ds.Output('event-dateranger-ph', 'end_date'),
        ds.Output('event-dateranger-ph', 'style'),
        ds.Output('reset-button-ph', 'style'),
        ds.Output('date-radioitem-ph', 'style'),
        ds.Output('section-dropdown-ph', 'style'),
        ds.Output('subject-dropdown-ph', 'style'),
        ds.Output('judge-dropdown-ph', 'style'),
        ds.Output('finished-dropdown-ph', 'style'),
        ds.Output('choice-checklist-ph', 'style'),
        ds.Output('order-radioitem-ph', 'style'),
        ds.Output('section-dropdown-ph', 'options'),
        ds.Output('subject-dropdown-ph', 'options'),
        ds.Output('judge-dropdown-ph', 'options'),
        ds.Output('finished-dropdown-ph', 'options'),
        ds.Output('title-ph', 'children')],
    [ds.Input('type-dropdown-ph', 'value'),
        ds.Input('avg-radioitem-ph', 'value'),
        ds.Input('date-radioitem-ph', 'value'),
        ds.Input('event-dateranger-ph', 'start_date'), 
        ds.Input('event-dateranger-ph', 'end_date'), 
        ds.Input('event-dateranger-ph', 'min_date_allowed'), 
        ds.Input('event-dateranger-ph', 'max_date_allowed'), 
        ds.Input('reset-button-ph', 'n_clicks'),
        ds.Input('section-dropdown-ph', 'value'),
        ds.Input('subject-dropdown-ph', 'value'),
        ds.Input('judge-dropdown-ph', 'value'),
        ds.Input('finished-dropdown-ph', 'value'),
        ds.Input('choice-checklist-ph', 'value'),
        ds.Input('order-radioitem-ph', 'value'),
        ds.Input('text-checklist-ph', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, choices, order, text):
    df[phaseTag] = df[phaseTag].astype(str)
    return comparation.typeComparationUpdate(df, typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, phaseTag, sections, subjects, judges, finished, choices, order, text)
