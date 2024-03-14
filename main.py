import utils.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Graph.DurationGraph as duration
import utils.Graph.EventsGraph as event

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

def displayProcessesDuration(connection):
    processes = getter.getProcessesDuration(connection)
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

def getConnection():
    return connect.connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')

def startApp():
    app = ds.Dash(__name__, use_pages = True)

    app.layout = html.Div([
        html.H1('Multi-page app with Dash Pages'),
        html.Div([
            html.Div(
                ds.dcc.Link(f"{page['name']} - {page['path']}", href = page["relative_path"])
            ) for page in ds.page_registry.values()
        ]),
        ds.page_container
    ])
    app.run(debug = True)

if __name__ == '__main__':
    startApp()