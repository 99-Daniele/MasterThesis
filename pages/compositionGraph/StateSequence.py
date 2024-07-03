# this page shows state sequences.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.Utilities as utilities

# get dataframe with all events duration.
df = getter.getStatesDurationFiltered()
codeStateTag = utilities.getTagName('codeStateTag')
stateTag = utilities.getTagName('stateTag')

# return initial layout of page.
def pageLayout():
    global df
    avgTag = utilities.getTagName('avgTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    finishedTag = utilities.getTagName('finishedTag') 
    judge = utilities.getPlaceholderName('judge') 
    median = utilities.getPlaceholderName('median')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    state = utilities.getPlaceholderName('state')
    subject = utilities.getPlaceholderName('subject')
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text')  
    # filter important states chosen by user. Those are taken from stored file. Those are taken from stored file.
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df = df[df[codeStateTag].isin(importantStates)]
    finished = frame.getGroupBy(df, finishedTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    states = frame.getGroupBy(df, stateTag)
    states = sorted(states)
    # since figure is constantly updated, initial data are empty for faster graph creation
    df_start = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_start, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href='/composition'),
        ds.html.H2('STATE SEQUENCE'),
        ds.dcc.Dropdown(states, value = [states[0]], multi = True, searchable = True, clearable = True, id = 'type-dropdown-ssq', placeholder = state, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ssq', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ssq', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ssq', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-ssq', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-ssq', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-ssq'),
        ds.dcc.Graph(id = 'typeevent-graph-ssq', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-ssq', 'figure'),
        ds.Output('section-dropdown-ssq', 'options'),
        ds.Output('subject-dropdown-ssq', 'options'),
        ds.Output('judge-dropdown-ssq', 'options'),
        ds.Output('finished-dropdown-ssq', 'options')],
    [ds.Input('type-dropdown-ssq', 'value'),
        ds.Input('avg-radioitem-ssq', 'value'),
        ds.Input('text-checklist-ssq', 'value'),
        ds.Input('section-dropdown-ssq', 'value'),
        ds.Input('subject-dropdown-ssq', 'value'),
        ds.Input('judge-dropdown-ssq', 'value'),
        ds.Input('finished-dropdown-ssq', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, avg, text, section, subject, judge, finished):
    global df
    # filter important states chosen by user. Those are taken from stored file. Those are taken from stored file.
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df = df[df[codeStateTag].isin(importantStates)]
    return typeEvent.typeSequenceUpdate(df, state, stateTag, avg, text, section, subject, judge, finished)
