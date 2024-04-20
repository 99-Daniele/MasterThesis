import dash as ds

def refreshData():
    import utils.DatabaseConnection as connect
    import utils.DataUpdate as update
    import utils.Getters as getter
    connection = connect.getDatabaseConnection()
    update.refreshData(connection)
    print("Database updated!")
    getter.updateCache()

def displayAllEvents():
    import pages.EventGraph.AllEvents as allEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = allEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayImportantEvents():
    import pages.EventGraph.ImportantEvents as importantEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = importantEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayPhaseEvents():
    import pages.EventGraph.PhaseEvents as phaseEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayStateEvents():
    import pages.EventGraph.StateEvents as stateEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayProcessComparation():
    import pages.ComparationGraph.ProcessComparation as processComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayPhaseComparation():
    import pages.ComparationGraph.PhaseComparation as phaseComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayStateComparation():
    import pages.ComparationGraph.StateComparation as stateComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateComparationPage.pageLayout())
    ])
    app.run_server(debug = True)
    
def displayProcessDuration():
    import pages.DurationGraph.ProcessDuration as processDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processDurationPage.pageLayout())
    ])
    app.run_server(debug = True)
    
def displayCourtHearingsDuration():
    import pages.DurationGraph.CourtHearingsDuration as courtHearingsDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = courtHearingsDurationPage.pageLayout())
    ])
    app.run_server(debug = True)

def startApp():
    import utils.App as app
    app.start()

if __name__ == '__main__':
    displayPhaseComparation()