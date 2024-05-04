# this is the main file.

import dash as ds

# refresh database and cache data.
def refreshData():
    import utils.Database.DatabaseConnection as connect
    import utils.DataUpdate as update
    import utils.Getters as getter
    connection = connect.getDatabaseConnection()
    update.refreshData(connection)
    print("Database updated!")
    getter.updateCache()
    getter.updateCache()

# display all events.
def displayAllEvents():
    import pages.EventGraph.AllEvents as allEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = allEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display important events.
def displayImportantEvents():
    import pages.EventGraph.ImportantEvents as importantEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = importantEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase events.
def displayPhaseEvents():
    import pages.EventGraph.PhaseEvents as phaseEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state events.
def displayStateEvents():
    import pages.EventGraph.StateEvents as stateEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display processes comparation graph.
def displayProcessComparation():
    import pages.ComparationGraph.ProcessComparation as processComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phases comparation graph.
def displayPhaseComparation():
    import pages.ComparationGraph.PhaseComparation as phaseComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display states comparation graph.
def displayStateComparation():
    import pages.ComparationGraph.StateComparation as stateComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display processes duration graph.    
def displayProcessDuration():
    import pages.DurationGraph.ProcessDuration as processDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processDurationPage.pageLayout())
    ])
    app.run_server(debug = True)
    
# display processes court hearings graph.   
def displayCourtHearingsDuration():
    import pages.DurationGraph.CourtHearingsDuration as courtHearingsDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = courtHearingsDurationPage.pageLayout())
    ])
    app.run_server(debug = True)

# start app to allow user select graph to be displayed.
def startApp():
    import App as app
    app.start()

# action performed by main.
if __name__ == '__main__':
    refreshData()