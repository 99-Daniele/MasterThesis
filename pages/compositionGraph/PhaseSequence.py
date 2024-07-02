# this page shows phase sequences.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.Utilities as utilities

# get dataframe with all events duration.
df = getter.getPhasesDurationFiltered()
phaseTag = utilities.getTagName('phaseTag')

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    finishedTag = utilities.getTagName('finishedTag') 
    judge = utilities.getPlaceholderName('judge') 
    median = utilities.getPlaceholderName('median')
    phase = utilities.getPlaceholderName('phase')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject') 
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text') 
    finished = frame.getGroupBy(df, finishedTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    phases = frame.getUniques(df, phaseTag)
    phases = sorted(phases)
    # since figure is constantly updated, initial data are empty for faster graph creation
    df_start = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_start, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('COMPOSITION GRAPHS', href='/composition'),
        ds.html.H2('PHASE SEQUENCES'),
        ds.dcc.Dropdown(phases, value = ['2'], multi = True, searchable = True, clearable = True, id = 'type-dropdown-phsq', placeholder = phase, style = {'width': 400}),
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
