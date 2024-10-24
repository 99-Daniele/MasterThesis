# this page shows event sequences.

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
eventTag = utilities.getTagName('eventTag')

# return initial layout of page.
def pageLayout():
    global df
    avgTag = utilities.getTagName('avgTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    event = utilities.getPlaceholderName('event')
    finishedTag = utilities.getTagName('finishedTag')  
    judge = utilities.getPlaceholderName('judge') 
    median = utilities.getPlaceholderName('median')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject') 
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text')
    # filter important events chosen by user. Those are taken from stored file. Those are taken from stored file.
    importantEvents = file.getDataFromTextFile('utils/preferences/importantEvents.txt')
    if importantEvents != None and len(importantEvents) > 0:
        df = df[df[codeEventTag].isin(importantEvents)]
    finished = frame.getGroupBy(df, finishedTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    events = frame.getUniques(df, eventTag)
    events = sorted(events)
    # since figure is constantly updated, initial data are empty for faster graph creation
    df_start = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_start, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href='/composition'),
        ds.html.H2('EVENT SEQUENCE'),
        ds.dcc.Dropdown(events, value = [events[0]], multi = True, searchable = True, clearable = True, id = 'type-dropdown-esq', placeholder = event, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-esq', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-esq', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-esq', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-esq', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-esq', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-esq'),
        ds.dcc.Graph(id = 'typeevent-graph-esq', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-esq', 'figure'),
        ds.Output('section-dropdown-esq', 'options'),
        ds.Output('subject-dropdown-esq', 'options'),
        ds.Output('judge-dropdown-esq', 'options'),
        ds.Output('finished-dropdown-esq', 'options')],
    [ds.Input('type-dropdown-esq', 'value'),
        ds.Input('avg-radioitem-esq', 'value'),
        ds.Input('text-checklist-esq', 'value'),
        ds.Input('section-dropdown-esq', 'value'),
        ds.Input('subject-dropdown-esq', 'value'),
        ds.Input('judge-dropdown-esq', 'value'),
        ds.Input('finished-dropdown-esq', 'value')]
)

# return updated data based on user choice.
def updateOutput(event, avg, text, section, subject, judge, finished):
    global df
    # filter important events chosen by user. Those are taken from stored file. Those are taken from stored file.
    importantEvents = file.getDataFromTextFile('utils/preferences/importantEvents.txt')
    if importantEvents != None and len(importantEvents) > 0:
        df = df[df[codeEventTag].isin(importantEvents)]
    return typeEvent.typeSequenceUpdate(df, event, eventTag, avg, text, section, subject, judge, finished)
