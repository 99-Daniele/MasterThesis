# this page shows state events.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.TypeEventsGraph as typeEvent

# get dataframe with all events duration.
df = getter.getEventsDuration()
typeTag = 'fase'

# return initial layout of page.
def pageLayout():
    sectionTag = 'sezione'
    subjectTag = 'materia'
    judgeTag = 'giudice'
    finishedTag = 'finito'
    countTag = 'conteggio'
    phaseTag = 'fase'
    df_temp = df.sort_values(by = [phaseTag]).reset_index(drop = True)
    types = frame.getGroupBy(df_temp, typeTag, countTag)
    sections = frame.getGroupBy(df_temp, sectionTag, countTag)
    importantSubjects = getter.getImportantSubjects()
    subjects = frame.getGroupBy(df_temp, subjectTag, countTag)
    if importantSubjects != None:
        subjects = list(set(subjects) & set(importantSubjects))
    judges = frame.getGroupBy(df_temp, judgeTag, countTag)
    finished = frame.getGroupBy(df_temp, finishedTag, countTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('EVENTI FASE'),
        ds.dcc.Dropdown(types, value = types[0], multi = False, searchable = True, clearable = False, id = 'type-dropdown-phe', placeholder = 'FASE', style = {'width': 400}),
        #ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-e', placeholder = 'SEZIONE', style = {'display': 'none'}),
        #ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-e', placeholder = 'MATERIA', style = {'display': 'none'}, optionHeight = 80),
        #ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-e', placeholder = 'GIUDICE', style = {'display': 'none'}),
        #ds.dcc.Dropdown(finished, value = ['FINITO'], multi = True, searchable = False, id = 'finished-dropdown-e', placeholder = 'PROCESSO', style = {'display': 'none'}),
        #ds.dcc.Checklist([sectionTag, subjectTag, judgeTag, finishedTag], value = [], id = 'choice-checklist-e', inline = True, style = {'display': 'none'}),
        #ds.dcc.RadioItems(['conteggio', 'media'], value = 'conteggio', id = 'order-radioitem-e', inline = True, style = {'display': 'none'}),
        #ds.dcc.Checklist(['TESTO'], value = ['TESTO'], id = 'text-checklist-e'),
        ds.dcc.RadioItems(['PRIMO', 'TUTTI'], value = 'TUTTI', id = 'display-radioitem-phe', inline = True),
        ds.dcc.Graph(id = 'typeevent-graph-phe', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-phe', 'figure')],
    [ds.Input('type-dropdown-phe', 'value'),
     ds.Input('display-radioitem-phe', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, display):
    return typeEvent.typeEventUpdate(df, typeTag, state, display)
