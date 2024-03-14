import utils.DataUpdate as update
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Graph.DurationGraph as duration
import utils.Graph.EventsGraph as event

import pages.Home as homePage
import pages.Comparation as comparationPage
import pages.Duration as durationPage
import pages.Event as eventPage
import pages.DurationGraph.CourtHearingDuration as courtHearingDurationPage
import pages.DurationGraph.EventDuration as eventDurationPage
import pages.DurationGraph.PhaseDuration as phaseDurationPage
import pages.DurationGraph.ProcessDuration as processDurationPage
import pages.DurationGraph.StateDuration as stateDurationPage

import dash as ds
import dash_bootstrap_components as dbc
from dash import html

def refreshData(connection):
    update.refreshData(connection)

def displayAllEvents(connection):
    events = getter.getAllEvents(connection)
    importantEventsType = getter.getImportantEventsType(connection)
    event.displayEvents(events, importantEventsType)

def displayImportantEvents(connection):
    importantEvents = getter.getImportantEvents(connection)
    importantEventsType = getter.getImportantEventsType(connection)
    event.displayEvents(importantEvents, importantEventsType)

def displayCourtHearingEvents(connection):
    courtHearingEvents = getter.getCourtHearingEvents(connection)
    courtHearingEventsType = getter.getCourtHearingEventsType(connection)
    event.displayEvents(courtHearingEvents, courtHearingEventsType)

def displayProcessesDuration():
    processes = getter.getProcessesDuration()
    duration.displayProcessesDuration(processes)

def displayStatesDuration(connection):
    states = getter.getStatesDuration(connection)
    duration.displayStatesDuration(states)

def displayPhasesDuration(connection):
    phases = getter.getPhasesDuration(connection)
    duration.displayPhasesDuration(phases)

def displayEventsDuration(connection):
    events = getter.getEventsDuration(connection)
    duration.displayEventsDuration(events)
    
def displayCourtHearingsDuration(connection):
    courtHearings = getter.getCourtHearingsDuration(connection)
    duration.displayCourtHearingsDuration(courtHearings)

def displayComparationByWeek(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparation(processes, "W", "CONFRONTO DURATA MEDIA PROCESSI IN BASE ALLA SETTIMANA DI INIZIO PROCESSO")

def displayComparationByMonth(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparation(processes, "M", "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DI INIZIO PROCESSO")

def displayComparationByMonthYear(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparation(processes, "MY", "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INIZIO PROCESSO")

def startApp():
    app = ds.Dash(__name__, suppress_callback_exceptions=True)
    app.layout = html.Div([
        ds.dcc.Location(id='url', refresh=False),
        html.Div(id = 'page-content')
    ])
    @app.callback(
            ds.Output('page-content', 'children'),
            ds.Input('url', 'pathname'))
    def display_page(pathname):
        match pathname:
            case '/comparationgraph':
                return comparationPage.layout
            case '/durationgraph':
                return durationPage.layout
            case '/eventpage':
                return eventPage.layout
            case '/durationgraph/courthearingduration':
                return courtHearingDurationPage.layout
            case '/durationgraph/eventduration':
                return eventDurationPage.layout
            case '/durationgraph/phaseduration':
                return phaseDurationPage.layout
            case '/durationgraph/processduration':
                return processDurationPage.layout
            case '/durationgraph/stateduration':
                return stateDurationPage.layout
            case _:
                return homePage.layout
    app.run(debug = True)

if __name__ == '__main__':
    startApp()