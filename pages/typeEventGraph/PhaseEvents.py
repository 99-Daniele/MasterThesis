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
phaseTag = utilities.getTagName('phaseTag')

# return initial layout of page.
def pageLayout():
    all = utilities.getPlaceholderName('all')
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    first = utilities.getPlaceholderName('first')
    median = utilities.getPlaceholderName('median')
    phase = utilities.getPlaceholderName('phase')
    text = utilities.getPlaceholderName('text')
    df_temp = df.sort_values(by = [phaseTag]).reset_index(drop = True)
    types = frame.getGroupBy(df_temp, phaseTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('EVENTI FASE'),
        ds.dcc.Dropdown(types, value = types[0], multi = False, searchable = True, clearable = False, id = 'type-dropdown-phe', placeholder = phase, style = {'width': 400}),
        ds.dcc.RadioItems([first, all], value = all, id = 'display-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems([avgTag, median], value = avgTag, id = 'avg-radioitem-phe', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist([text], value = [text], id = 'text-checklist-phe'),
        ds.dcc.Graph(id = 'typeevent-graph-phe', figure = fig)
    ])
    return layout

# callback with input and output.
@ds.callback(
    [ds.Output('typeevent-graph-phe', 'figure')],
    [ds.Input('type-dropdown-phe', 'value'),
     ds.Input('display-radioitem-phe', 'value'),
     ds.Input('avg-radioitem-phe', 'value'),
     ds.Input('text-checklist-phe', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, display, avg, text):
    return typeEvent.typeEventUpdate(df, phaseTag, state, display, avg, text)
