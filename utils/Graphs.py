import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

from utils.Legenda import getColourOfPhase

def displayEvents(events, t):
    pIds = []
    dates = []
    phases = []
    for e in events:
            pIds.append(e[1])
            dates.append(e[3])
            phases.append((e[4]))
    df = pd.DataFrame(
        data={"data": dates, "numProcesso": pIds, "fase": phases})
    fig = px.scatter(df, x="data", y="numProcesso", color = "fase", title=t)
    fig.update_xaxes(rangeslider_visible=True,
                     rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
    ))
    fig.show()
    return fig
