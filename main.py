import dash as ds

import utils.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Graph.DurationGraph as duration
import utils.Graph.EventsGraph as event
import utils.Utilities as utilities

import pages.Home as homePage
import pages.Comparation as comparationPage
import pages.Duration as durationPage
import pages.Event as eventPage
import pages.ComparationGraph.ComparationByMonth as comparationMonthPage
import pages.ComparationGraph.ComparationByMonthYear as comparationMonthYearPage
import pages.ComparationGraph.ComparationByWeek as comparationWeekPage
import pages.DurationGraph.PhaseDuration as phaseDurationPage
import pages.DurationGraph.CourtHearingDuration as courtHearingDurationPage
import pages.DurationGraph.EventDuration as eventDurationPage
import pages.DurationGraph.PhaseDuration as phaseDurationPage
import pages.DurationGraph.ProcessDuration as processDurationPage
import pages.DurationGraph.StateDuration as stateDurationPage
import pages.EventGraph.AllEvents as allEventsPage
import pages.EventGraph.CourtHearingEvents as courtHearingEventsPage
import pages.EventGraph.ImportantEvents as importantEventsPage

def refreshData():
    database = utilities.dataBaseInfo
    connection = connect.connectToDatabase(database[0], database[1], database[2], database[3])
    update.refreshData(connection)

def displayAllEvents():
    events = getter.getAllEvents()
    importantEventsType = getter.getImportantEventsType()
    event.displayEvents(events, importantEventsType)

def displayImportantEvents():
    importantEvents = getter.getImportantEvents()
    importantEventsType = getter.getImportantEventsType()
    event.displayEvents(importantEvents, importantEventsType)

def displayCourtHearingEvents():
    courtHearingEvents = getter.getCourtHearingEvents()
    courtHearingEventsType = getter.getCourtHearingEventsType()
    event.displayEvents(courtHearingEvents, courtHearingEventsType)

def displayProcessesDuration():
    processes = getter.getProcessesDuration()
    duration.displayProcessesDuration(processes)

def displayStatesDuration():
    states = getter.getStatesDuration()
    duration.displayStatesDuration(states)

def displayPhasesDuration():
    phases = getter.getPhasesDuration()
    duration.displayPhasesDuration(phases)

def displayEventsDuration():
    events = getter.getEventsDuration()
    duration.displayEventsDuration(events)
    
def displayCourtHearingsDuration():
    courtHearings = getter.getCourtHearingsDuration()
    duration.displayCourtHearingsDuration(courtHearings)

def displayComparationByWeek():
    processes = getter.getProcessesDuration()
    comparation.displayComparation(processes, "W")

def displayComparationByMonth():
    processes = getter.getProcessesDuration()
    comparation.displayComparation(processes, "M")

def displayComparationByMonthYear():
    processes = getter.getProcessesDuration()
    comparation.displayComparation(processes, "MY")

def startApp():
    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('PROGETTO TRIBUNALI'),
        ds.dcc.Location(id = 'url', refresh = False),
        ds.html.Div(id = 'page-content')
    ])
    @ds.callback(
            ds.Output('page-content', 'children'),
            ds.Input('url', 'pathname'))
    def display_page(pathname):
        match pathname:
            case '/comparationgraph':
                return comparationPage.pageLayout()
            case '/durationgraph':
                return durationPage.pageLayout()
            case '/eventpage':
                return eventPage.pageLayout()
            case '/comparationgraph/weekcomparation':
                return comparationWeekPage.pageLayout()
            case '/comparationgraph/monthcomparation':
                return comparationMonthPage.pageLayout()
            case '/comparationgraph/monthyearcomparation':
                return comparationMonthYearPage.pageLayout()
            case '/durationgraph/courthearingduration':
                return courtHearingDurationPage.pageLayout()
            case '/durationgraph/eventduration':
                return eventDurationPage.pageLayout()
            case '/durationgraph/phaseduration':
                return phaseDurationPage.pageLayout()
            case '/durationgraph/processduration':
                return processDurationPage.pageLayout()
            case '/durationgraph/stateduration':
                return stateDurationPage.pageLayout()
            case '/eventgraph/allevents':
                return allEventsPage.pageLayout()
            case 'eventgraph/courthearings':
                return courtHearingEventsPage.pageLayout()
            case '/eventgraph/importantevents':
                return importantEventsPage.pageLayout()
            case _:
                return homePage.pageLayout()
    app.run_server(debug = True)

if __name__ == '__main__':
    startApp()