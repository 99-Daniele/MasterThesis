# this file handles events graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.Utilities.Utilities as utilities

# return all needed parameters in order to change graph after any user choice.
def eventUpdate(df, startDate, endDate, type, mustEvents, minDate, maxDate, sections, subjects, judges):
    df_temp = df.copy()
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    df_temp = frame.getDateDataFrame(df_temp, 'dataInizioProcesso', startDate, endDate)
    if sections != None and len(sections) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'sezione', sections)
    if subjects != None and len(subjects) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'materia', subjects)
    if judges != None and len(judges) > 0:
        df_temp = frame.getTypesDataFrame(df_temp, 'giudice', judges)
    sections = frame.getGroupBy(df_temp, 'sezione')
    subjects = frame.getGroupBy(df_temp, 'materia')
    judges = frame.getGroupBy(df_temp, 'giudice')
    fig = px.scatter(df_temp, x = "data", y = "numProcesso", color = type, color_discrete_sequence = utilities.phaseColorList(df_temp, type), labels = {'numProcesso':'Codice Processo', 'data':'Data inizio processo'}, width = 1200)
    fig.update_layout(
        legend = dict(
            yanchor = "top",
            y = 0.99
        ),
        yaxis = dict(
            showticklabels = False
        )
    )
    fig.update_xaxes(
        dtick = "M1",
        tickformat = "%b\n%Y",
        ticklabelmode = "period"
    )   
    if mustEvents != None:
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name not in mustEvents else False))
    return fig, startDate, endDate, sections, subjects, judges
