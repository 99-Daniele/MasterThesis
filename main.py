import utils.Getters as gt
import utils.Graphs as gr
import utils.DatabaseConnection as dbc

def displayAllEvents(connection):
    e = gt.getAllEvents(connection)
    j = gt.getTop10Judges(connection)
    s = gt.getTop10Subjects(connection)
    gr.displayEvents(e, j, s, "EVENTI")

def displayImportantEvents(connection):
    e = gt.getImportantEvents(connection)
    j = gt.getTop10Judges(connection)
    s = gt.getTop10Subjects(connection)
    gr.displayEvents(e, j, s, "EVENTI IMPORTANTI")

def displayCourtHearingEvents(connection):
    e = gt.getCourtHearingsEvents(connection)
    j = gt.getTop10Judges(connection)
    s = gt.getTop10Subjects(connection)
    gr.displayEvents(e, j, s, "UDIENZE")

def displayProcessesDuration(connection):
    processes = gt.getProcessesDuration(connection)
    gr.displayProcessesDuration(processes, "DURATA MEDIA PROCESSI")

def displayStatesDuration(connection):
    states = gt.getStatesDuration(connection)
    gr.displayStatesDuration(states, "DURATA MEDIA STATI DEL PROCESSO")

def displayPhasesDuration(connection):
    phases = gt.getPhasesDuration(connection)
    gr.displayProcesses(phases, "DURATA MEDIA FASI DEL PROCESSO")

def displayEventsDuration(connection):
    events = gt.getEventsDuration(connection)
    gr.displayProcesses(events, "DURATA MEDIA EVENTI DEL PROCESSO")

if __name__ == '__main__':
    connection = dbc.connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayProcessesDuration(connection)