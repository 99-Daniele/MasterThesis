# this is the main file.

import dash as ds

# display all events.
def displayAllEventsScatter():
    import pages.eventGraph.AllEventsScatter as allEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = allEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase events.
def displayPhaseEventsScatter():
    import pages.eventGraph.PhaseEventsScatter as phaseEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state events.
def displayStateEventsScatter():
    import pages.eventGraph.StateEventsScatter as stateEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display processes comparation graph.
def displayProcessComparation():
    import pages.comparationGraph.ProcessComparation as processComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phases comparation graph.
def displayPhaseComparation():
    import pages.comparationGraph.PhaseComparation as phaseComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display states comparation graph.
def displayStateComparation():
    import pages.comparationGraph.StateComparation as stateComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display events comparation graph.
def displayEventComparation():
    import pages.comparationGraph.EventComparation as eventComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display types comparation graph.
def displayTypeComparation():
    import pages.comparationGraph.TypeComparation as typeComparationPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = typeComparationPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state events graph.
def displayStatesEvents():
    import pages.typeEventGraph.StateEvents as stateEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase events graph.
def displayPhasesEvents():
    import pages.typeEventGraph.PhaseEvents as phaseEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state sequence graph.
def displayStatesSequence():
    import pages.typeEventGraph.StateSequence as stateSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase sequence graph.
def displayPhaseSequence():
    import pages.typeEventGraph.PhaseSequence as phaseSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display event sequence graph.
def displayEventSequence():
    import pages.typeEventGraph.EventSequence as eventSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display state names.
def displayStatePreferences():
    import pages.preference.StatePreference as statePreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = statePreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display event names.
def displayEventPreferences():
    import pages.preference.EventPreference as eventPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display subject names.
def displaySubjectPreferences():
    import pages.preference.SubjectPreference as subjectPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = subjectPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# refresh database and cache data.
def restartData():
    import utils.DataUpdate as update
    update.restartData()

# refresh database and cache data.
def refreshData():
    import utils.DataUpdate as update
    update.refreshData()

# start app to allow user select graph to be displayed.
def startApp():
    import App as app
    app.start()

if __name__ == '__main__':
    displayStatesSequence()