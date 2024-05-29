# this page shows phase sequences.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.utilities.Utilities as utilities

# get dataframe with all events duration.
df = getter.getPhasesDuration()
codeStateTag = utilities.getTagName('codeStateTag')
phaseTag = utilities.getTagName('phaseTag')

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
    types = frame.getGroupBy(df, phaseTag)
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
        ds.html.H2('SEQUENZA FASI'),
        ds.dcc.Dropdown(types, value = "2", multi = False, searchable = True, clearable = False, id = 'type-dropdown-phq', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-phq', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-phq', placeholder = subject, style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-phq', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-phq', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-phq', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-phq'),
        ds.dcc.Graph(id = 'typeevent-graph-phq', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-phq', 'figure')],
    [ds.Input('type-dropdown-phq', 'value'),
        ds.Input('avg-radioitem-phq', 'value'),
        ds.Input('text-checklist-phq', 'value'),
        ds.Input('section-dropdown-phq', 'value'),
        ds.Input('subject-dropdown-phq', 'value'),
        ds.Input('judge-dropdown-phq', 'value'),
        ds.Input('finished-dropdown-phq', 'value')]
)

# return updated data based on user choice.
def updateOutput(phase, avg, text, section, subject, judge, finished):
    return typeEvent.typeSequenceUpdate(df, 'preferences/statesName.txt', phase, phaseTag, avg, text, section, subject, judge, finished)
