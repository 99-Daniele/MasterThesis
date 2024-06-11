# this page shows events duration and comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.utilities.Utilities as utilities

# get dataframe with all events duration.
df = getter.getEventsDurationFiltered()
codeEventTag = utilities.getTagName('codeEventTag')
eventTag = utilities.getTagName('eventTag')
importantEvents = file.getDataFromTextFile('preferences/importantEvents.txt')
if importantEvents != None and len(importantEvents) > 0:
    df = df[df[codeEventTag].isin(importantEvents)]

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag') 
    countTag = utilities.getTagName('countTag') 
    dateTag = utilities.getTagName('dateTag') 
    event = utilities.getPlaceholderName('event') 
    finishedTag = utilities.getTagName('finishedTag') 
    judge = utilities.getPlaceholderName('judge') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    median = utilities.getPlaceholderName('median') 
    month = utilities.getPlaceholderName('month')
    monthYear = utilities.getPlaceholderName('monthYear') 
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text') 
    trimester = utilities.getPlaceholderName('trimester') 
    trimesterYear = utilities.getPlaceholderName('trimesterYear')
    week = utilities.getPlaceholderName('week')
    year = utilities.getPlaceholderName('year')
    types = frame.getGroupBy(df, eventTag)
    typesSorted = sorted(types)
    sections = frame.getGroupBy(df, sectionTag)
    subjects = frame.getGroupBy(df, subjectTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    finished = frame.getGroupBy(df, finishedTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2('DURATA MEDIA EVENTI DEL PROCESSO', id = 'title-e'),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-e', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([week, month, monthYear, trimester, trimesterYear, year], value = month, id = 'date-radioitem-e', inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.html.Div(children = [
            ds.dcc.DatePickerRange(
                id = 'event-dateranger-e',
                start_date = df[dateTag].min(),
                end_date = df[dateTag].max(),
                min_date_allowed = df[dateTag].min(),
                max_date_allowed = df[dateTag].max(),
                display_format = 'DD MM YYYY',
                style = {'width': 300, 'display':'none'}
            ),        
            ds.html.Button("RESET", id = 'reset-button-e', style = {'display':'none'})
            ],
            style = {'display':'flex'}
        ),
        ds.dcc.Dropdown(typesSorted, multi = False, searchable = False, id = 'type-dropdown-e', placeholder = event, style = {'width': 400}),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-e', placeholder = section, style = {'display': 'none'}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-e', placeholder = subject, style = {'display': 'none'}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-e', placeholder = judge, style = {'display': 'none'}),
        ds.dcc.Dropdown(finished, multi = True, searchable = False, id = 'finished-dropdown-e', placeholder = process, style = {'display': 'none'}),
        ds.dcc.Checklist([sectionTag, subjectTag, codeJudgeTag, finishedTag], value = [], id = 'choice-checklist-e', inline = True, style = {'display': 'none'}),
        ds.dcc.RadioItems([countTag, avgTag], value = countTag, id = 'order-radioitem-e', inline = True, style = {'display': 'none'}),
        ds.dcc.Checklist([text], value = [], id = 'text-checklist-e'),
        ds.dcc.Graph(id = 'comparation-graph-e', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-e', 'figure'),
        ds.Output('event-dateranger-e', 'start_date'), 
        ds.Output('event-dateranger-e', 'end_date'),
        ds.Output('event-dateranger-e', 'style'),
        ds.Output('reset-button-e', 'style'),
        ds.Output('date-radioitem-e', 'style'),
        ds.Output('section-dropdown-e', 'style'),
        ds.Output('subject-dropdown-e', 'style'),
        ds.Output('judge-dropdown-e', 'style'),
        ds.Output('finished-dropdown-e', 'style'),
        ds.Output('choice-checklist-e', 'style'),
        ds.Output('order-radioitem-e', 'style'),
        ds.Output('section-dropdown-e', 'options'),
        ds.Output('subject-dropdown-e', 'options'),
        ds.Output('judge-dropdown-e', 'options'),
        ds.Output('finished-dropdown-e', 'options'),
        ds.Output('title-e', 'children')],
    [ds.Input('type-dropdown-e', 'value'),
        ds.Input('avg-radioitem-e', 'value'),
        ds.Input('date-radioitem-e', 'value'),
        ds.Input('event-dateranger-e', 'start_date'), 
        ds.Input('event-dateranger-e', 'end_date'), 
        ds.Input('event-dateranger-e', 'min_date_allowed'), 
        ds.Input('event-dateranger-e', 'max_date_allowed'), 
        ds.Input('reset-button-e', 'n_clicks'),
        ds.Input('section-dropdown-e', 'value'),
        ds.Input('subject-dropdown-e', 'value'),
        ds.Input('judge-dropdown-e', 'value'),
        ds.Input('finished-dropdown-e', 'value'),
        ds.Input('choice-checklist-e', 'value'),
        ds.Input('order-radioitem-e', 'value'),
        ds.Input('text-checklist-e', 'value')]
)

# return updated data based on user choice.
def updateOutput(typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, choices, order, text):
    return comparation.typeComparationUpdate(df, typeChoice, avgChoice, typeDate, startDate, endDate, minDate, maxDate, eventTag, sections, subjects, judges, finished, choices, order, text)
