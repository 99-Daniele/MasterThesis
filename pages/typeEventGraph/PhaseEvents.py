# this page shows phase events.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent
import utils.utilities.Utilities as utilities

# get dataframe with all events duration.
df = getter.getEventsDuration()
codeEventTag = utilities.getTagName('codeEventTag')
codeStateTag = utilities.getTagName('codeStateTag')
eventTag = utilities.getTagName('eventTag')
stateTag = utilities.getTagName('stateTag')
phaseTag = utilities.getTagName('phaseTag')
eventTagChoice = eventTag
stateTagChoice = stateTag

# return initial layout of page.
def pageLayout():
    all = utilities.getPlaceholderName('all')
    avgTag = utilities.getTagName('avgTag')
    first = utilities.getPlaceholderName('first')
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
        ds.html.H2('EVENTI FASE'),
        ds.dcc.Dropdown(types, value = "2", multi = False, searchable = True, clearable = False, id = 'type-dropdown-phe', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-phe', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-phe', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-phe', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-phe', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([first, all], value = all, id = 'display-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([eventTagChoice, stateTagChoice], value = eventTagChoice, id = 'choice-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-phe'),
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
    if tagChoice == eventTagChoice:
        df = getter.getEventsDuration()
        filename = 'preferences/eventsName.json'
    else:
        df = getter.getStatesDuration()
        filename = 'preferences/statesName.json'
    return typeEvent.typeEventUpdate(df, filename, False, phaseTag, state, tagChoice, display, avg, text, section, subject, judge, finished)
