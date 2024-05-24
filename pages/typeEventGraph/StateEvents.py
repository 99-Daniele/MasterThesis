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
    countTag = utilities.getTagName('countTag')
    phaseTag = utilities.getTagName('phaseTag')
    df_temp = df.sort_values(by = [phaseTag]).reset_index(drop = True)
    types = frame.getGroupBy(df_temp, codeStateTag, countTag)
    df_temp = pd.DataFrame({'A' : (), 'B': ()})
    fig = px.box(df_temp, x = 'A', y = 'B')
    layout = ds.html.Div([
        ds.dcc.Link('Home', href='/'),
        ds.html.Br(),
        ds.dcc.Link('Grafici tipo eventi', href='/typeevent'),
        ds.html.H2('EVENTI STATO'),
        ds.dcc.Dropdown(types, value = types[0], multi = False, searchable = True, clearable = False, id = 'type-dropdown-se', placeholder = 'STATO', style = {'width': 400}),
        ds.dcc.RadioItems(['PRIMO', 'TUTTI'], value = 'TUTTI', id = 'display-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.RadioItems(['media', 'mediana'], value = 'media', id = 'avg-radioitem-se', inline = True, inputStyle = {'margin-left': "20px"}),
        ds.dcc.Checklist(['TESTO'], value = ['TESTO'], id = 'text-checklist-se'),
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
    return typeEvent.typeEventUpdate(df, codeStateTag, state, display, avg, text)
