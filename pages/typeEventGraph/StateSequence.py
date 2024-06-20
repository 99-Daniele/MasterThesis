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
    avgTag = utilities.getTagName('avgTag')
    median = utilities.getPlaceholderName('median')
    state = utilities.getPlaceholderName('state')
    text = utilities.getPlaceholderName('text')
    judge = utilities.getPlaceholderName('judge') 
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    subject = utilities.getPlaceholderName('subject')  
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df_temp = df[df[codeStateTag].isin(importantStates)]
    types = frame.getGroupBy(df_temp, stateTag)
    finishedTag = utilities.getTagName('finishedTag') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    median = utilities.getPlaceholderName('median') 
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('codeSubjectTag') 
    sections = frame.getGroupBy(df_temp, sectionTag)
    subjects = frame.getGroupBy(df_temp, subjectTag)
    judges = frame.getGroupBy(df_temp, codeJudgeTag)
    finished = frame.getGroupBy(df_temp, finishedTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    types = sorted(types)
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href='/typeevent'),
        ds.html.H2('STATE SEQUENCE'),
        ds.dcc.Dropdown(types, value = [types[0]], multi = True, searchable = True, clearable = True, id = 'type-dropdown-ssq', placeholder = state, style = {'width': 400}),
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
    
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        df_temp = df[df[codeStateTag].isin(importantStates)]
    else:
        df_temp = df
    return typeEvent.typeSequenceUpdate(df_temp, state, stateTag, avg, text, section, subject, judge, finished)
