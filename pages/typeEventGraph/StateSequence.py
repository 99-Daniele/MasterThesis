# this page shows state sequences.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.utilities.Utilities as utilities

# get dataframe with all events duration.
df = getter.getStatesDuration()
codeStateTag = utilities.getTagName('codeStateTag')
df = frame.keepOnlyRelevant(df, 0.005, codeStateTag)
stateTag = utilities.getTagName('stateTag')
stateTagChoice = stateTag

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag')
    median = utilities.getPlaceholderName('median')
    phase = utilities.getPlaceholderName('phase')
    text = utilities.getPlaceholderName('text')
    judge = utilities.getPlaceholderName('judge') 
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    subject = utilities.getPlaceholderName('subject')  
    types = frame.getGroupBy(df, stateTagChoice)
    finishedTag = utilities.getTagName('finishedTag') 
    judgeTag = utilities.getTagName('judgeTag') 
    median = utilities.getPlaceholderName('median') 
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('codeSubjectTag') 
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    judges = frame.getGroupBy(df, judgeTag)
    finished = frame.getGroupBy(df, finishedTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    types = sorted(types)
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('SEQUENZA STATI'),
        ds.dcc.Dropdown(types, value = types[0], multi = False, searchable = True, clearable = False, id = 'type-dropdown-ssq', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-ssq', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-ssq', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-ssq', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-ssq', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-ssq', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-ssq'),
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
    return typeEvent.typeSequenceUpdate(df, 'preferences/statesName.json', False, state, stateTagChoice, avg, text, section, subject, judge, finished)
