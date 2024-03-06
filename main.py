import utils.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Getters as getter
import utils.Graph.ComparationGraph as comparation
import utils.Graph.DurationGraph as duration
import utils.Graph.EventsGraph as event

def refreshData(connection):
    update.refreshData(connection)

def displayEvents(connection):
    events = getter.getAllEvents(connection)
    importantEventsType = getter.getImportantEventsType(connection)
    event.displayEvents(events, importantEventsType)

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

def displayComparationByWeek(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByWeek(processes)

def displayComparationByMonth(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByMonth(processes)

def displayComparationByMonthYear(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByMonthYear(processes)

if __name__ == '__main__':
    connection = connect.connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayComparationByMonthYear(connection)