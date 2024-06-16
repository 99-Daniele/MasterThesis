# this page shows type comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.Utilities as utilities

# get dataframe with all processes duration.
df = getter.getProcessesDurationFiltered()
codeJudgeTag = utilities.getTagName('codeJudgeTag') 
judge = utilities.getPlaceholderName('judge') 
median = utilities.getPlaceholderName('median') 
section = utilities.getPlaceholderName('section') 
sectionTag = utilities.getTagName('sectionTag')
subject = utilities.getPlaceholderName('subject')  
codeSubjectTag = utilities.getTagName('codeSubjectTag') 

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag')  
    text = utilities.getPlaceholderName('text') 
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.Br(),
        ds.dcc.Link('DURATION COMPARISON GRAPHS', href='/comparationgraph'),
        ds.html.H2("COMPARISON OF PROCESSES DURATION BASED ON " + section, id = 'title-tr'),        
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-tr', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Dropdown([section, judge, subject], value = section, multi = False, searchable = False, clearable = False, id = 'type-dropdown-tr', placeholder = section, style = {'width': 400}),
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
        ds.Input('text-checklist-tr', 'value')]
    )

# return updated data based on user choice.
def updateOutput(avgChoice, typeChoice, text):
    if typeChoice == section:
        typeID = sectionTag
        title = "COMPARISON OF PROCESSES DURATION BASED ON " + section
    elif typeChoice == judge:
        typeID = codeJudgeTag
        title = "COMPARISON OF PROCESSES DURATION BASED ON " + judge
    else:
        typeID = codeSubjectTag
        title = "COMPARISON OF PROCESSES DURATION BASED ON " + subject
        df[codeSubjectTag] = df[codeSubjectTag].astype(str)
    return comparation.parameterComparationUpdate(df, avgChoice, typeID, text), title
