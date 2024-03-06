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

def displayComparationByWeek(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByMonthYear(processes, "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DI INIZIO")

def displayComparationByMonth(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByMonthYear(processes, "CONFRONTO DURATA MEDIA PROCESSI IN BASE ALLA SETTIMANA DI INIZIO")

def displayComparationByMonthYear(connection):
    processes = getter.getProcessesDuration(connection)
    comparation.displayComparationByMonthYear(processes, "CONFRONTO DURATA MEDIA PROCESSI IN BASE AL MESE DELL'ANNO DI INZIO")

if __name__ == '__main__':
    connection = connect.connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayComparationByMonthYear(connection)