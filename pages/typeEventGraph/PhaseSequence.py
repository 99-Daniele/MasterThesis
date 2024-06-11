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
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('SEQUENZA FASI'),
        ds.dcc.Dropdown(types, value = "2", multi = False, searchable = True, clearable = False, id = 'type-dropdown-phsq', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-phsq', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-phsq', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-phsq', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-phsq', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-phsq', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-phsq'),
        ds.dcc.Graph(id = 'typeevent-graph-phsq', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-phsq', 'figure'),
        ds.Output('section-dropdown-phsq', 'options'),
        ds.Output('subject-dropdown-phsq', 'options'),
        ds.Output('judge-dropdown-phsq', 'options'),
        ds.Output('finished-dropdown-phsq', 'options')],
    [ds.Input('type-dropdown-phsq', 'value'),
        ds.Input('avg-radioitem-phsq', 'value'),
        ds.Input('text-checklist-phsq', 'value'),
        ds.Input('section-dropdown-phsq', 'value'),
        ds.Input('subject-dropdown-phsq', 'value'),
        ds.Input('judge-dropdown-phsq', 'value'),
        ds.Input('finished-dropdown-phsq', 'value')]
)

# return updated data based on user choice.
def updateOutput(phase, avg, text, section, subject, judge, finished):
    return typeEvent.typeSequenceUpdate(df, phase, phaseTag, avg, text, section, subject, judge, finished)
