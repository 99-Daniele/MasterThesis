# this page shows state events.

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
    types = frame.getGroupBy(df, codeStateTag)
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
        ds.html.H2('EVENTI STATO'),
        ds.dcc.Dropdown(types, value = "UT", multi = False, searchable = True, clearable = False, id = 'type-dropdown-se', placeholder = phase, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-se', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-se', placeholder = subject, style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-se', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-se', placeholder = process, style = {'width': 400}),
        ds.dcc.RadioItems([first, all], value = all, id = 'display-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-se'),
        ds.dcc.Graph(id = 'typeevent-graph-se', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-se', 'figure')],
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
    return typeEvent.typeEventUpdate(df, codeStateTag, state, codeEventTag, display, avg, text, section, subject, judge, finished)
