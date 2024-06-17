# this page shows prediction error.

import dash as ds
import pandas as pd
import plotly.express as px

import utils.Getters as getter
import utils.Utilities as utilities

# get dataframe with predictions.
df = getter.getPredictedDurationDataframe()
durationFinalTag = utilities.getTagName('durationFinalTag') 
numProcessTag = utilities.getTagName('numProcessTag') 
predictedDurationTag = utilities.getTagName('durationPredictedTag')
df = df.sort_values(by = durationFinalTag).reset_index(drop = True)
order_dict = df.set_index(numProcessTag)[durationFinalTag].to_dict()
df['sort_column'] = df[numProcessTag].map(order_dict)
df = df.sort_values( by = 'sort_column').drop(columns = 'sort_column').reset_index(drop = True)
df['plus30'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.3)).astype(int)
df['plus15'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.15)).astype(int)
df['minus30'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.3)).astype(int)
df['minus15'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.15)).astype(int)
df15 = df[df[predictedDurationTag] >= df['minus15']]
df15 = df15[df15[predictedDurationTag] <= df15['plus15']]
df30 = df[df[predictedDurationTag] >= df['minus30']]
df30 = df30[df30[predictedDurationTag] <= df30['plus30']]
df30 = pd.concat([df30, df15]).drop_duplicates(keep = False)
dfOut = pd.concat([df, df30]).drop_duplicates(keep = False)
dfOut = pd.concat([dfOut, df15]).drop_duplicates(keep = False)

# return initial layout of page.
def pageLayout():
    fig = px.scatter(df15, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['green'], labels = {durationFinalTag:'Duration of process', predictedDurationTag:'Predicted duration of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
    fig.data[-1].name = 'predictionInside15 (' + str(len(df15)) + ")"
    fig.data[-1].legendgroup = '1'
    fig.add_traces(
        px.scatter(df30, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['orange']).data
    )
    fig.data[-1].name = 'predictionInside30 (' + str(len(df30)) + ")"
    fig.data[-1].legendgroup = '2'
    fig.add_traces(
        px.scatter(dfOut, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['red']).data
    )
    fig.data[-1].name = 'predictionOutside (' + str(len(dfOut)) + ")"
    fig.data[-1].legendgroup = '3'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = durationFinalTag).update_traces(line_color = utilities.getLineColor()).data
    )
    fig.data[-1].name = 'prediction'
    fig.data[-1].legendgroup = '4'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus15').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'prediction15'
    fig.data[-1].legendgroup = '5'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus30').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'prediction30'
    fig.data[-1].legendgroup = '6'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus15').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'prediction15'
    fig.data[-1].legendgroup = '5'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus30').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'prediction30'
    fig.data[-1].legendgroup = '6'
    fig.update_traces(showlegend = True)
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.H2('PREDICTED DURATION ERROR GRAPH'),
        ds.dcc.Graph(figure = fig, id = 'prediction-graph')
    ])
    return layout
