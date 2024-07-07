# this is the main file.

import dash as ds
import os

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

# display processes comparison graph.
def displayProcessComparison():
    import pages.comparisonGraph.ProcessComparison as processComparisonPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = processComparisonPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phases comparison graph.
def displayPhaseComparison():
    import pages.comparisonGraph.PhaseComparison as phaseComparisonPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseComparisonPage.pageLayout())
    ])
    app.run_server(debug = True)

# display states comparison graph.
def displayStateComparison():
    import pages.comparisonGraph.StateComparison as stateComparisonPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateComparisonPage.pageLayout())
    ])
    app.run_server(debug = True)

# display events comparison graph.
def displayEventComparison():
    import pages.comparisonGraph.EventComparison as eventComparisonPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventComparisonPage.pageLayout())
    ])
    app.run_server(debug = True)

# display types comparison graph.
def displayTypeComparison():
    import pages.comparisonGraph.ProcessComparisonByType as typeComparisonPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = typeComparisonPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state events graph.
def displayStatesEvents():
    import pages.compositionGraph.StateEvents as stateEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase events graph.
def displayPhasesEvents():
    import pages.compositionGraph.PhaseEvents as phaseEventsPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseEventsPage.pageLayout())
    ])
    app.run_server(debug = True)

# display state sequence graph.
def displayStatesSequence():
    import pages.compositionGraph.StateSequence as stateSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = stateSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display phase sequence graph.
def displayPhaseSequence():
    import pages.compositionGraph.PhaseSequence as phaseSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = phaseSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display event sequence graph.
def displayEventSequence():
    import pages.compositionGraph.EventSequence as eventSequencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventSequencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display state names.
def displayStatePreferences():
    import pages.preferenceTable.StatePreference as statePreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = statePreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display event names.
def displayEventPreferences():
    import pages.preferenceTable.EventPreference as eventPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = eventPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display subject names.
def displaySubjectPreferences():
    import pages.preferenceTable.SubjectPreference as subjectPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = subjectPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display sections.
def displaySectionPreferences():
    import pages.preferenceTable.SectionPreference as sectionPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = sectionPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display process types.
def displayProcessTypePreferences():
    import pages.preferenceTable.FinishedPreference as finishedPreferencePage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = finishedPreferencePage.pageLayout())
    ])
    app.run_server(debug = True)

# display prediction error pagse.
def displayPredictionError():
    import pages.predictionGraph.PredictionError as predictionErrorPage
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.Div(children = predictionErrorPage.pageLayout())
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

# test unfinished processes predictor. Test on all processes.
def predictTotalTest():
    import utils.DataUpdate as update
    update.predictTotalTest()

# test unfinished processes predictor. Test on 80-20 processes.
def predict8020Test():
    import utils.DataUpdate as update
    update.predict8020Test()

# predicts duration of unfinished processes.
def predictDuration():
    import utils.DataUpdate as update
    update.predictDuration()
    update.refreshData()

# start app to allow user select graph to be displayed.
def startApp():
    import utils.App as app
    app.start()

if not os.path.isdir('cache'):
    restartData()

if __name__ == '__main__':
    displayStatePreferences()