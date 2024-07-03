# this page shows prediction error.

import dash as ds
import pandas as pd
import plotly.express as px
import sklearn.metrics as mtc

import utils.Getters as getter
import utils.Utilities as utilities

# get dataframe with predictions.
df = getter.getPredictedDurationDataframe()

# return initial layout of page.
def pageLayout():
    global df
    avgTag = utilities.getTagName('avgTag') 
    countTag = utilities.getTagName('countTag') 
    durationFinalTag = utilities.getTagName('durationFinalTag') 
    errorTag = utilities.getTagName('errorTag') 
    medianTag = utilities.getPlaceholderName('median')
    numProcessTag = utilities.getTagName('numProcessTag') 
    predictedDurationTag = utilities.getTagName('durationPredictedTag')
    # sort values by duration ascending.
    df = df.sort_values(by = durationFinalTag).reset_index(drop = True)
    order_dict = df.set_index(numProcessTag)[durationFinalTag].to_dict()
    df['sort_column'] = df[numProcessTag].map(order_dict)
    df = df.sort_values( by = 'sort_column').drop(columns = 'sort_column').reset_index(drop = True)
    # calculate for each duration, the correlated values with +- 20% and 50% error.
    df['plus50'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.5))
    df['plus20'] = (df[durationFinalTag] + (df[durationFinalTag] * 0.2))
    df['minus50'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.5))
    df['minus20'] = (df[durationFinalTag] - (df[durationFinalTag] * 0.2))
    # aggregate by error and calculate size of dataframe, median error and mean error.
    dfError = df.agg(Size = (errorTag, 'size'), Median = (errorTag, 'median'), Mean = (errorTag, 'mean')).transpose().rename(columns = {"Size":countTag, "Median": medianTag + " " + errorTag, "Mean": avgTag + " " + errorTag})
    # calculate R2 coefficient of determination
    dfError['R2'] = mtc.r2_score(df[durationFinalTag], df[predictedDurationTag])
    # df20 is the dataframe with only preditions with error less than 20%.
    # df50 is the dataframe with only preditions with error between 20% and 50%.
    # dfOut is the dataframe with only preditions with error more then 50%.
    df20 = df[df[errorTag] <= 20.0]
    df50 = df[df[errorTag] <= 50.0]
    df50 = pd.concat([df50, df20]).drop_duplicates(keep = False)
    dfOut = pd.concat([df, df50]).drop_duplicates(keep = False)
    dfOut = pd.concat([dfOut, df20]).drop_duplicates(keep = False)
    # df20 points are shown in green.
    fig = px.scatter(df20, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['green'], labels = {durationFinalTag:'Duration of process', predictedDurationTag:'Predicted duration of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(0.9))
    fig.data[-1].name = 'errorBelow20 (' + str(len(df20)) + ")"
    fig.data[-1].legendgroup = '1'
    # df50 points are shown in orange.
    fig.add_traces(
        px.scatter(df50, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['orange']).data
    )
    fig.data[-1].name = 'errorBelow50 (' + str(len(df50)) + ")"
    fig.data[-1].legendgroup = '2'
    # dfOut points are shown in red.
    fig.add_traces(
        px.scatter(dfOut, x = durationFinalTag, y = predictedDurationTag, color_discrete_sequence = ['red']).data
    )
    fig.data[-1].name = 'errorMoreThan50 (' + str(len(dfOut)) + ")"
    fig.data[-1].legendgroup = '3'
    # real duration line.
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = durationFinalTag).update_traces(line_color = utilities.getLineColor(), line = {'width': 3}).data
    )
    fig.data[-1].name = 'realDuration'
    fig.data[-1].legendgroup = '4'
    # duration with +20% error line.
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus20').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'error20'
    fig.data[-1].legendgroup = '5'
    # duration with +50% error line.
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'plus50').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'error50'
    fig.data[-1].legendgroup = '6'
    # duration with -20% error line.
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus20').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dash')).data
    )
    fig.data[-1].name = 'error20'
    fig.data[-1].legendgroup = '5'
    # duration with -50% error line.
    fig.add_traces(
        px.line(df, x = durationFinalTag, y = 'minus50').update_traces(line = dict(color = utilities.getLineColor(), dash = 'dot')).data
    )
    fig.data[-1].name = 'error50'
    fig.data[-1].legendgroup = '6'
    fig.update_layout(font = dict(size = 16))
    fig.update_traces(showlegend = True)
    layout = ds.html.Div([
        ds.dcc.Link('HOME', href='/'),
        ds.html.H2('PREDICTED DURATION ERROR GRAPH'),
        ds.dash_table.DataTable(
            dfError.to_dict('records'),
            style_cell = {
                'font-size': 16,
                'text-align': 'center'
            }),
        ds.dcc.Graph(figure = fig, id = 'prediction-graph')
    ])
    return layout
