# this page shows processes comparation.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Dataframe as frame
import utils.Getters as getter
import utils.graph.ComparationGraph as comparation
import utils.utilities.Utilities as utilities

# get dataframe with all processes duration.
df = getter.getProcessesDurationFiltered()

# return initial layout of page.
def pageLayout():
    avgTag = utilities.getTagName('avgTag') 
    countTag = utilities.getTagName('countTag') 
    dateTag = utilities.getTagName('dateTag') 
    eventSequence = utilities.getPlaceholderName('eventSequence')
    eventSequenceTag = utilities.getTagName('eventSequenceTag')
    finishedTag = utilities.getTagName('finishedTag') 
    judge = utilities.getPlaceholderName('judge') 
    codeJudgeTag = utilities.getTagName('codeJudgeTag') 
    median = utilities.getPlaceholderName('median') 
    month = utilities.getPlaceholderName('month')
    monthYear = utilities.getPlaceholderName('monthYear') 
    phase = utilities.getPlaceholderName('phase')
    phaseSequence = utilities.getPlaceholderName('phaseSequence')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    process = utilities.getPlaceholderName('process')  
    section = utilities.getPlaceholderName('section') 
    sectionTag = utilities.getTagName('sectionTag')
    sequence = utilities.getPlaceholderName('sequence')
    state = utilities.getPlaceholderName('state')
    stateSequenceTag = utilities.getTagName('stateSequenceTag')
    subject = utilities.getPlaceholderName('subject')  
    subjectTag = utilities.getTagName('subjectTag') 
    text = utilities.getPlaceholderName('text') 
    trimester = utilities.getPlaceholderName('trimester') 
    trimesterYear = utilities.getPlaceholderName('trimesterYear')
    week = utilities.getPlaceholderName('week')
    withTag = utilities.getPlaceholderName('with')
    withOut = utilities.getPlaceholderName('without')
    year = utilities.getPlaceholderName('year') 
    subjects = frame.getGroupBy(df, subjectTag)
    sections = frame.getGroupBy(df, sectionTag)
    judges = frame.getGroupBy(df, codeJudgeTag)
    finished = frame.getGroupBy(df, finishedTag)
    sequences = frame.getGroupBy(df, stateSequenceTag)
    phaseSequences = frame.getGroupBy(df, phaseSequenceTag)
    events = frame.getGroupByFromString(df, eventSequenceTag)
    states = frame.getGroupByFromString(df, stateSequenceTag)
    phases = frame.getGroupByFromString(df, phaseSequenceTag)
    df_temp = pd.DataFrame({'A' : [], 'B': []})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici confronto', href='/comparationgraph'),
        ds.html.H2("CONFRONTO DURATA MEDIA PROCESSI"),        
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-pr', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([week, month, monthYear, trimester, trimesterYear, year], value = month, id = 'date-radioitem-pr', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.DatePickerRange(
            id = 'event-dateranger-pr',
            start_date = df[dateTag].min(),
            end_date = df[dateTag].max(),
            min_date_allowed = df[dateTag].min(),
            max_date_allowed = df[dateTag].max(),
            display_format = 'DD MM YYYY',
            style = {'width': 300}
        ),
        ds.html.Button("RESET", id = "reset-button-pr"),
        ds.dcc.Dropdown(sections, multi = True, searchable = True, id = 'section-dropdown-pr', placeholder = section, style = {'width': 400}),
        ds.dcc.Dropdown(subjects, multi = True, searchable = True, id = 'subject-dropdown-pr', placeholder = subject, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(judges, multi = True, searchable = True, id = 'judge-dropdown-pr', placeholder = judge, style = {'width': 400}),
        ds.dcc.Dropdown(finished, multi = True, searchable = True, id = 'finished-dropdown-pr', placeholder = process, style = {'width': 400}),
        ds.dcc.Dropdown(sequences, multi = True, searchable = False, id = 'sequence-dropdown-pr', placeholder = sequence, style = {'width': 400}, optionHeight = 80),
        ds.dcc.Dropdown(phaseSequences, multi = True, searchable = False, id = 'phaseSequence-dropdown-pr', placeholder = phaseSequence, style = {'width': 400}),
        ds.html.Div(children = [
            ds.dcc.Dropdown(events, multi = False, searchable = True, id = 'events-dropdown-pr', placeholder = eventSequence, style = {'width': 400}),
            ds.dcc.RadioItems([withTag, withOut], value = withTag, id = "events-radioitem-pr", inline = True, style = {'display': 'none'}, inputStyle = {'margin-left': "20px"})
            ],
            style = {'display': 'inline-flex', 'width': '100%'}
        ),
        ds.html.Div(children = [
            ds.dcc.Dropdown(states, multi = False, searchable = True, id = 'states-dropdown-pr', placeholder = state, style = {'width': 400}),
            ds.dcc.RadioItems([withTag, withOut], value = withTag, id = "states-radioitem-pr", inline = True, style = {'display': 'none'}, inputStyle = {'margin-left': "20px"})
            ],
            style = {'display': 'inline-flex', 'width': '100%'}
        ),
        ds.html.Div(children = [
            ds.dcc.Dropdown(phases, multi = False, searchable = True, id = 'phases-dropdown-pr', placeholder = phase, style = {'width': 400}),
            ds.dcc.RadioItems([withTag, withOut], value = withTag, id = "phases-radioitem-pr", inline = True, style = {'display': 'none'}, inputStyle = {'margin-left': "20px"})
            ],
            style = {'display': 'inline-flex', 'width': '100%'}
        ),
        ds.dcc.Checklist([sectionTag, subjectTag, codeJudgeTag, finishedTag, stateSequenceTag, phaseSequenceTag], value = [], id = "choice-checklist-pr", inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([countTag, avgTag], value = countTag, id = "order-radioitem-pr", inline = True, style = {'display':'none'}, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = "text-checklist-pr"),
        ds.dcc.Graph(id = 'comparation-graph-pr', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('comparation-graph-pr', 'figure'),
        ds.Output('event-dateranger-pr', 'start_date'), 
        ds.Output('event-dateranger-pr', 'end_date'),
        ds.Output('section-dropdown-pr', 'style'),
        ds.Output('subject-dropdown-pr', 'style'),
        ds.Output('judge-dropdown-pr', 'style'),
        ds.Output('finished-dropdown-pr', 'style'),
        ds.Output('sequence-dropdown-pr', 'style'),
        ds.Output('phaseSequence-dropdown-pr', 'style'),
        ds.Output('events-dropdown-pr', 'style'),
        ds.Output('events-radioitem-pr', 'style'),
        ds.Output('states-dropdown-pr', 'style'),
        ds.Output('states-radioitem-pr', 'style'),
        ds.Output('phases-dropdown-pr', 'style'),
        ds.Output('phases-radioitem-pr', 'style'),
        ds.Output('order-radioitem-pr', 'style'),
        ds.Output('section-dropdown-pr', 'options'),
        ds.Output('subject-dropdown-pr', 'options'),
        ds.Output('judge-dropdown-pr', 'options'),
        ds.Output('finished-dropdown-pr', 'options'),
        ds.Output('sequence-dropdown-pr', 'options'),
        ds.Output('phaseSequence-dropdown-pr', 'options'),
        ds.Output('events-dropdown-pr', 'options'),
        ds.Output('choice-checklist-pr', 'options')],
    [ds.Input('avg-radioitem-pr', 'value'),
        ds.Input('date-radioitem-pr', 'value'),
        ds.Input('event-dateranger-pr', 'start_date'), 
        ds.Input('event-dateranger-pr', 'end_date'), 
        ds.Input('event-dateranger-pr', 'min_date_allowed'), 
        ds.Input('event-dateranger-pr', 'max_date_allowed'), 
        ds.Input('reset-button-pr', 'n_clicks'),
        ds.Input('section-dropdown-pr', 'value'),
        ds.Input('subject-dropdown-pr', 'value'),
        ds.Input('judge-dropdown-pr', 'value'),
        ds.Input('finished-dropdown-pr', 'value'),
        ds.Input('sequence-dropdown-pr', 'value'),
        ds.Input('phaseSequence-dropdown-pr', 'value'),
        ds.Input('events-dropdown-pr', 'value'),
        ds.Input('events-radioitem-pr', 'value'),
        ds.Input('states-dropdown-pr', 'value'),
        ds.Input('states-radioitem-pr', 'value'),
        ds.Input('phases-dropdown-pr', 'value'),
        ds.Input('phases-radioitem-pr', 'value'),
        ds.Input('choice-checklist-pr', 'value'),
        ds.Input('choice-checklist-pr', 'options'),
        ds.Input('order-radioitem-pr', 'value'),
        ds.Input('text-checklist-pr', 'value')]
    )

# return updated data based on user choice.
def updateOutput(avgChoice, dateType, startDate, endDate, minDate, maxDate, button, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio, choices, choicesOptions, order, text):
    return comparation.processComparationUpdate(df, avgChoice, dateType, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio, choices, choicesOptions, order, text)
