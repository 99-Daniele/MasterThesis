# this page shows phase events.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.Utilities as utilities

# get dataframe with all events duration.
df = getter.getStatesDuration()
eventTag = utilities.getTagName('eventTag')
stateTag = utilities.getTagName('stateTag')
phaseTag = utilities.getTagName('phaseTag')
df[phaseTag] = df[phaseTag].astype(str)

# return initial layout of page.
def pageLayout():
    all = utilities.getPlaceholderName('all')
    avgTag = utilities.getTagName('avgTag')
    first = utilities.getPlaceholderName('first')
    judge = utilities.getPlaceholderName('judge') 
    last = utilities.getPlaceholderName('last') 
    median = utilities.getPlaceholderName('median')
    phase = utilities.getPlaceholderName('phase')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    subject = utilities.getPlaceholderName('subject') 
    text = utilities.getPlaceholderName('text')
    types = frame.getUniques(df, phaseTag)
    finishedTag = utilities.getTagName('finishedTag') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    median = utilities.getPlaceholderName('median') 
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('codeSubjectTag') 
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    finished = frame.getGroupBy(df, finishedTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    types = sorted(types)
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href='/typeevent'),
        ds.html.H2('PHASE COMPOSITION'),
        ds.dcc.Dropdown(types, value = ['2'], multi = True, searchable = True, clearable = True, id = 'type-dropdown-phe', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-phe', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-phe', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-phe', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-phe', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([first, all, last], value = all, id = 'display-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([stateTag, eventTag], value = stateTag, id = 'choice-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-phe'),
        ds.dcc.Graph(id = 'typeevent-graph-phe', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-phe', 'figure'),
        ds.Output('section-dropdown-phe', 'options'),
        ds.Output('subject-dropdown-phe', 'options'),
        ds.Output('judge-dropdown-phe', 'options'),
        ds.Output('finished-dropdown-phe', 'options')],
    [ds.Input('type-dropdown-phe', 'value'),
        ds.Input('display-radioitem-phe', 'value'),
        ds.Input('choice-radioitem-phe', 'value'),
        ds.Input('avg-radioitem-phe', 'value'),
        ds.Input('text-checklist-phe', 'value'),
        ds.Input('section-dropdown-phe', 'value'),
        ds.Input('subject-dropdown-phe', 'value'),
        ds.Input('judge-dropdown-phe', 'value'),
        ds.Input('finished-dropdown-phe', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, display, tagChoice, avg, text, section, subject, judge, finished):
    if tagChoice == eventTag:
        df = getter.getEventsDuration()
    else:
        df = getter.getStatesDuration()
    df[phaseTag] = df[phaseTag].astype(str)
    return typeEvent.typeEventUpdate(df, phaseTag, state, tagChoice, display, avg, text, section, subject, judge, finished)
