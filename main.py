import dash as ds

def refreshData():
    import utils.DatabaseConnection as connect
    import utils.DataUpdate as update
    import utils.Getters as getter
    connection = connect.getDatabaseConnection()
    update.refreshData(connection)
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
    import pages.ComparationGraph.ComparationByMonthYear as processComparationPage
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
    
def displayEventDuration():
    import pages.DurationGraph.EventDuration as eventDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventDurationPage.pageLayout())
    ])
    app.run_server(debug = True)
    
def displayPhaseDuration():
    import pages.DurationGraph.PhaseDuration as phaseDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseDurationPage.pageLayout())
    ])
    app.run_server(debug = True)

def displayStateDuration():
    import pages.DurationGraph.StateDuration as stateDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateDurationPage.pageLayout())
    ])
    app.run_server(debug = True)
    
def displayCourtHearingsDuration():
    import pages.DurationGraph.CourtHearingDuration as courtHearingDurationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = courtHearingDurationPage.pageLayout())
    ])
    app.run_server(debug = True)

def startApp():
    import utils.App as app
    app.start()

if __name__ == '__main__':
    import utils.Getters as g
    g.testSpeed()
