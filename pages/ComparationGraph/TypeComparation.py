# this page shows type comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.Utilities as utilities

# get dataframe with all processes duration.
df = getter.getProcessesDuration()
codeSubjectTag = utilities.getTagName('codeSubjectTag')  
df[codeSubjectTag] = df[codeSubjectTag].astype(str)

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag')  
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    judge = utilities.getPlaceholderName('judge') 
    month = utilities.getPlaceholderName('month') 
    median = utilities.getPlaceholderName('median') 
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag')  
    text = utilities.getPlaceholderName('text') 
    typeTag = utilities.getPlaceholderName('type') 
    sections = frame.getGroupBy(df, sectionTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    subjects = frame.getGroupBy(df, subjectTag)
    months = utilities.getMonths()
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('DURATION COMPARISON GRAPHS', href='/comparationgraph'),
        ds.html.H2("COMPARISON OF PROCESSES DURATION BASED ON " + section, id = 'title-tr'),        
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-tr', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Dropdown([sectionTag, codeJudgeTag, codeSubjectTag], value = sectionTag, multi = False, searchable = False, clearable = False, id = 'type-dropdown-tr', placeholder = typeTag, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, clearable = True, id = 'type-dropdown-se', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, clearable = True, id = 'type-dropdown-j', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, clearable = True, id = 'type-dropdown-su', placeholder = subject, style = {'width': 400}),
        ds.dcc.Dropdown(months, multi = True, searchable = True, clearable = True, id = 'type-dropdown-mt', placeholder = month, style = {'width': 400}),
        ds.dcc.Checklist([text], value = [], id = "text-checklist-tr"),
        ds.dcc.Graph(id = 'comparation-graph-tr', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-tr', 'figure'),
        ds.Output('title-tr', 'children')],
    [ds.Input('avg-radioitem-tr', 'value'),
        ds.Input('type-dropdown-tr', 'value'),
        ds.Input('type-dropdown-se', 'value'),
        ds.Input('type-dropdown-j', 'value'),
        ds.Input('type-dropdown-su', 'value'),
        ds.Input('type-dropdown-mt', 'value'),
        ds.Input('text-checklist-tr', 'value')]
    )

# return updated data based on user choice.
def updateOutput(avgChoice, typeChoice, sections, judges, subjects, months, text):
    return comparation.parameterComparationUpdate(df, avgChoice, typeChoice, sections, judges, subjects, months, text)
