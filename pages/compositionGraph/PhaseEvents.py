# this page shows phase events.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.Utilities as utilities

# get dataframe with all events duration.
df = getter.getStatesDurationFiltered()
eventTag = utilities.getTagName('eventTag')
phaseTag = utilities.getTagName('phaseTag')

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
    phase = utilities.getPlaceholderName('phase')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag') 
    stateTag = utilities.getTagName('stateTag')
    subject = utilities.getPlaceholderName('subject') 
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
        ds.html.H2('PHASE COMPOSITION'),
        ds.dcc.Dropdown(phases, value = ['2'], multi = True, searchable = True, clearable = True, id = 'type-dropdown-phe', placeholder = phase, style = {'width': 400}),
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
        df = getter.getEventsDurationFiltered()
    else:
        df = getter.getStatesDurationFiltered()
    return typeEvent.typeUpdate(df, phaseTag, state, tagChoice, display, avg, text, section, subject, judge, finished)
