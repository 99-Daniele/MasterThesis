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
codeStateTag = utilities.getTagName('codeStateTag')

# return initial layout of page.
def pageLayout():
    all = utilities.getPlaceholderName('all')
    avgTag = utilities.getTagName('avgTag')
    countTag = utilities.getTagName('countTag')
    first = utilities.getPlaceholderName('first')
    median = utilities.getPlaceholderName('median')
    state = utilities.getPlaceholderName('state')
    text = utilities.getPlaceholderName('text')
    df_temp = df.sort_values(by = [codeStateTag]).reset_index(drop = True)
    types = frame.getGroupBy(df_temp, codeStateTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('EVENTI STATI'),
        ds.dcc.Dropdown(types, value = types[0], multi = False, searchable = True, clearable = False, id = 'type-dropdown-se', placeholder = state, style = {'width': 400}),
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
     ds.Input('text-checklist-se', 'value')]
)

# return updated data based on user choice.
def updateOutput(state, display, avg, text):
    return typeEvent.typeEventUpdate(df, phaseTag, state, display, avg, text)
