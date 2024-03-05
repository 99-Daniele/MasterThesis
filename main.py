import utils.Getters as getter
import utils.Graph.EventsGraph as event
import utils.Graph.DurationGraph as duration
import utils.Graph.ComparationGraph as comparation
import utils.DatabaseConnection as connect
import utils.DataUpdate as update

def refreshData(connection):
    update.refreshData(connection)

def displayEvents(connection):
    events = getter.getAllEvents(connection)
    importantEventsType = getter.getImportantEventsType(connection)
    event.displayEvents(events, importantEventsType, "EVENTI DEI PROCESSI")

def displayProcessesDuration(connection):
    processes = getter.getProcessesDuration(connection)
    duration.displayProcessesDuration(processes, "DURATA MEDIA PROCESSI")

def displayStatesDuration(connection):
    states = getter.getStatesDuration(connection)
    duration.displayStatesDuration(states, "DURATA MEDIA STATI DEL PROCESSO")

def displayPhasesDuration(connection):
    phases = getter.getPhasesDuration(connection)
    duration.displayPhasesDuration(phases, "DURATA MEDIA FASI DEL PROCESSO")

def displayEventsDuration(connection):
    events = getter.getEventsDuration(connection)
    duration.displayEventsDuration(events, "DURATA MEDIA EVENTI DEL PROCESSO")

if __name__ == '__main__':
    connection = connect.connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayEvents(connection)