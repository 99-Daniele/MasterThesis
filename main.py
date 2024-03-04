import utils.Getters as getter
import utils.Graph.EventsGraph as event
import utils.Graph.DurationGraph as duration
import utils.Graph.ComparationGraph as comparation
import utils.DatabaseConnection as connect
import utils.DataUpdate as update

def refreshData(connection):
    update.refreshData(connection)

def displayAllEvents(connection):
    e = getter.getAllEvents(connection)
    j = getter.getTop10Judges(connection)
    s = getter.getTop10Subjects(connection)
    event.displayEvents(e, j, s, "EVENTI")

def displayImportantEvents(connection):
    e = getter.getImportantEvents(connection)
    j = getter.getTop10Judges(connection)
    s = getter.getTop10Subjects(connection)
    event.displayEvents(e, j, s, "EVENTI IMPORTANTI")

def displayCourtHearingEvents(connection):
    e = getter.getCourtHearingsEvents(connection)
    j = getter.getTop10Judges(connection)
    s = getter.getTop10Subjects(connection)
    event.displayEvents(e, j, s, "UDIENZE")

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
    displayImportantEvents(connection)