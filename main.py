from utils.DatabaseConnection import connectToDatabase

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

def displayAllProcesses(connection):
    p = gt.getAllProcesses(connection)
    gr.displayProcesses(p, "DURATA MEDIA DI TUTTI I PROCESSI")

if __name__ == '__main__':
    connection = connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayAllProcesses(connection)