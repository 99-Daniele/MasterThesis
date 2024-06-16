# this page shows phases duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.utilities.Utilities as utilities

# get dataframe with all phases duration.
df = getter.getStatesDurationFiltered()
codeStateTag = utilities.getTagName('codeStateTag') 
phaseTag = utilities.getTagName('phaseTag') 
stateTag = utilities.getTagName('stateTag') 

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
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    state = utilities.getPlaceholderName('state')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text') 
    trimester = utilities.getPlaceholderName('trimester') 
    trimesterYear = utilities.getPlaceholderName('trimesterYear')
    week = utilities.getPlaceholderName('week')
    year = utilities.getPlaceholderName('year') 
    importantStates = file.getDataFromTextFile('preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df_temp = df[df[codeStateTag].isin(importantStates)]
    types = frame.getGroupBy(df_temp, stateTag)
    sections = frame.getGroupBy(df_temp, sectionTag)
    subjects = frame.getGroupBy(df_temp, subjectTag)
    judges = frame.getGroupBy(df_temp, codeJudgeTag)
    finished = frame.getGroupBy(df_temp, finishedTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('DURATION COMPARISON GRAPHS', href='/comparationgraph'),
        ds.html.H2('PROCESS STATES DURATION', id = 'title-s'),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-s', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([week, month, monthYear, trimester, trimesterYear, year], value = month, id = 'date-radioitem-s', inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.html.Div(children = [
            ds.dcc.DatePickerRange(
                id = 'event-dateranger-s',
                start_date = df[dateTag].min(),
                end_date = df[dateTag].max(),
                min_date_allowed = df[dateTag].min(),
                max_date_allowed = df[dateTag].max(),
                display_format = 'DD MM YYYY',
                style = {'width': 300, 'display':'none'}
            ),        
            ds.html.Button("RESET", id = 'reset-button-s', style = {'display':'none'})
            ],
            style = {'display':'flex'}
        ),
        ds.dcc.Dropdown(types, multi = False, searchable = False, id = 'type-dropdown-s', placeholder = state, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-s', placeholder = section, style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-s', placeholder = subject, style = {'display': 'none'}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-s', placeholder = judge, style = {'display': 'none'}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-s', placeholder = process, style = {'display': 'none'}),
        ds.dcc.Checklist([sectionTag, subjectTag, codeJudgeTag, finishedTag], value = [], id = "choice-checklist-s", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([countTag, avgTag], value = countTag, id = "order-radioitem-s", inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = "text-checklist-s"),
        ds.dcc.Graph(id = 'comparation-graph-s', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-s', 'figure'),
        ds.Output('event-dateranger-s', 'start_date'), 
        ds.Output('event-dateranger-s', 'end_date'),
        ds.Output('event-dateranger-s', 'style'),
        ds.Output('reset-button-s', 'style'),
        ds.Output('date-radioitem-s', 'style'),
        ds.Output('section-dropdown-s', 'style'),
        ds.Output('subject-dropdown-s', 'style'),
        ds.Output('judge-dropdown-s', 'style'),
        ds.Output('finished-dropdown-s', 'style'),
        ds.Output('choice-checklist-s', 'style'),
        ds.Output('order-radioitem-s', 'style'),
        ds.Output('section-dropdown-s', 'options'),
        ds.Output('subject-dropdown-s', 'options'),
        ds.Output('judge-dropdown-s', 'options'),
        ds.Output('finished-dropdown-s', 'options'),
        ds.Output('title-s', 'children')],
    [ds.Input('type-dropdown-s', 'value'),
        ds.Input('avg-radioitem-s', 'value'),
        ds.Input('date-radioitem-s', 'value'),
        ds.Input('event-dateranger-s', 'start_date'), 
        ds.Input('event-dateranger-s', 'end_date'), 
        ds.Input('event-dateranger-s', 'min_date_allowed'), 
        ds.Input('event-dateranger-s', 'max_date_allowed'), 
        ds.Input('reset-button-s', 'n_clicks'),
        ds.Input('section-dropdown-s', 'value'),
        ds.Input('subject-dropdown-s', 'value'),
        ds.Input('judge-dropdown-s', 'value'),
        ds.Input('finished-dropdown-s', 'value'),
        ds.Input('choice-checklist-s', 'value'),
        ds.Input('order-radioitem-s', 'value'),
        ds.Input('text-checklist-s', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, choices, order, text):
    importantStates = file.getDataFromTextFile('preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df_temp = df[df[codeStateTag].isin(importantStates)]
    else:
        df_temp = df
    return comparation.typeComparationUpdate(df_temp, typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, stateTag, sections, subjects, judges, finished, choices, order, text)
