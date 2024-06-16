# this page shows prediction error.

import dash as ds
import datetime as dt
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.graph.EventsGraph as event
import utils.Utilities as utilities

# get dataframe with predictions.
df = getter.getPredictedDurationDataframe()

# return initial layout of page.
def pageLayout():
    finalDurationTag = utilities.getTagName('finalDurationTag')  
    numProcessTag = utilities.getTagName('numProcessTag') 
    predictedDurationTag = utilities.getTagName('durationPredictedTag')
    df_temp = df.sort_values(by = numProcessTag).reset_index(drop = True)
    fig = px.scatter(df_temp, x = numProcessTag, y = predictedDurationTag, color_discrete_sequence = [utilities.getPointColor()], labels = {numProcessTag:'processID', predictedDurationTag:'Predicted duration of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
    fig.add_traces(
        px.line(df_temp, x = numProcessTag, y = finalDurationTag).update_traces(line_color = utilities.getLineColor()).data
    )
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.H2('PREDICTED DURATION ERROR GRAPH'),
        ds.dcc.Graph(figure = fig, id = 'prediction-graph')
    ])
    return layout
