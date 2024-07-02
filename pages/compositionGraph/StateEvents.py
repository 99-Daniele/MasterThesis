# this page shows state events.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.Utilities as utilities

# get dataframe with all events duration.
df = getter.getEventsDurationFiltered()
codeEventTag = utilities.getTagName('codeEventTag')
codeStateTag = utilities.getTagName('codeStateTag')
eventTag = utilities.getTagName('eventTag')
stateTag = utilities.getTagName('stateTag')

# return initial layout of page.
def pageLayout():
    all = utilities.getPlaceholderName('all')
    avgTag = utilities.getTagName('avgTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    finishedTag = utilities.getTagName('finishedTag') 
    first = utilities.getPlaceholderName('first')
    judge = utilities.getPlaceholderName('judge') 
    last = utilities.getPlaceholderName('last')
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
        ds.html.H2('STATE COMPOSITION'),
        ds.dcc.Dropdown(states, value = [states[0]], multi = True, searchable = True, clearable = True, id = 'type-dropdown-se', placeholder = state, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-se', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-se', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-se', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-se', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([first, all, last], value = all, id = 'display-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-se'),
        ds.dcc.Graph(id = 'typeevent-graph-se', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-se', 'figure'),
        ds.Output('section-dropdown-se', 'options'),
        ds.Output('subject-dropdown-se', 'options'),
        ds.Output('judge-dropdown-se', 'options'),
        ds.Output('finished-dropdown-se', 'options')],
    [ds.Input('type-dropdown-se', 'value'),
        ds.Input('display-radioitem-se', 'value'),
        ds.Input('avg-radioitem-se', 'value'),
        ds.Input('text-checklist-se', 'value'),
        ds.Input('section-dropdown-se', 'value'),
        ds.Input('subject-dropdown-se', 'value'),
        ds.Input('judge-dropdown-se', 'value'),
        ds.Input('finished-dropdown-se', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, display, avg, text, section, subject, judge, finished):
    # filter important states chosen by user. Those are taken from stored file. Those are taken from stored file.
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df = df[df[codeStateTag].isin(importantStates)]
    return typeEvent.typeUpdate(df, stateTag, state, eventTag, display, avg, text, section, subject, judge, finished)
