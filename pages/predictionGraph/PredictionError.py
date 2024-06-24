# this page shows prediction error.

import dash as ds
import pandas as pd
import plotly.express as px
import sklearn.metrics as mtc

import utils.Getters as getter
import utils.Utilities as utilities

# get dataframe with predictions.
df = getter.getPredictedDurationDataframe()
avgTag = utilities.getTagName('avgTag') 
countTag = utilities.getTagName('countTag') 
durationFinalTag = utilities.getTagName('durationFinalTag') 
errorTag = utilities.getTagName('errorTag') 
medianTag = utilities.getPlaceholderName('median')
numProcessTag = utilities.getTagName('numProcessTag') 
predictedDurationTag = utilities.getTagName('durationPredictedTag')
df = df.sort_values(by = durationFinalTag).reset_index(drop = True)
order_dict = df.set_index(numProcessTag)[durationFinalTag].to_dict()
df['sort_column'] = df[numProcessTag].map(order_dict)
df = df.sort_values( by = 'sort_column').drop(columns = 'sort_column').reset_index(drop = True)
df['plus50'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.5))
df['plus20'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.2))
df['minus50'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.5))
df['minus20'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.2))
dfError = df.agg(Size = (errorTag, 'size'), Median = (errorTag, 'median'), Mean = (errorTag, 'mean')).transpose().rename(columns = {"Size":countTag, "Median": medianTag + " " + errorTag, "Mean": avgTag + " " + errorTag})
errorR2 = mtc.r2_score(df[durationFinalTag], df[predictedDurationTag])
dfError['R2'] = errorR2
df20 = df[df[errorTag] <= 20.0]
df50 = df[df[errorTag] <= 50.0]
df50 = pd.concat([df50, df20]).drop_duplicates(keep = False)
dfOut = pd.concat([df, df50]).drop_duplicates(keep = False)
dfOut = pd.concat([dfOut, df20]).drop_duplicates(keep = False)

# return initial layout of page.
def pageLayout():
    fig = px.scatter(df20, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['green'], labels = {durationFinalTag:'Duration of process', predictedDurationTag:'Predicted duration of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
    fig.data[-1].name = 'errorBelow20 (' + str(len(df20)) + ")"
    fig.data[-1].legendgroup = '1'
    fig.add_traces(
        px.scatter(df50, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['orange']).data
    )
    fig.data[-1].name = 'errorBelow50 (' + str(len(df50)) + ")"
    fig.data[-1].legendgroup = '2'
    fig.add_traces(
        px.scatter(dfOut, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['red']).data
    )
    fig.data[-1].name = 'errorMoreThan50 (' + str(len(dfOut)) + ")"
    fig.data[-1].legendgroup = '3'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = durationFinalTag).update_traces(line_color = utilities.getLineColor(), line = {'width': 3}).data
    )
    fig.data[-1].name = 'realDuration'
    fig.data[-1].legendgroup = '4'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus20').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'error20'
    fig.data[-1].legendgroup = '5'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus50').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'error50'
    fig.data[-1].legendgroup = '6'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus20').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'error20'
    fig.data[-1].legendgroup = '5'
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus50').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'error50'
    fig.data[-1].legendgroup = '6'
    fig.update_layout(font = dict(size = 22))
    fig.update_traces(showlegend = True)
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.H2('PREDICTED DURATION ERROR GRAPH'),
        ds.dash_table.DataTable(
            dfError.to_dict('records'),
            style_cell = {
                'font-size': 25,
                'text-align': 'center'
            }),
        ds.dcc.Graph(figure = fig, id = 'prediction-graph')
    ])
    return layout
