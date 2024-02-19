from utils.DatabaseConnection import connectToDatabase

import utils.Getters as gt
import utils.Graphs as gr

def displayAllEvents(connection):
    e = gt.getAllEvents(connection)
    gr.displayEvents(e, "EVENTI")

def displayImportantEvents(connection):
    e = gt.getImportantEvents(connection)
    gr.displayEvents(e, "EVENTI")

def displayCourtHearingEvents(connection):
    e = gt.getCourtHearingsEvents(connection)
    gr.displayEvents(e, "EVENTI")

def displayAllProcesses(connection):
    p = gt.getAllProcesses(connection)
    gr.displayProcesses(p, "DURATA PROCESSI")

def displayFinishedProcesses(connection):
    p = gt.getFinishedProcesses(connection)
    gr.displayProcesses(p, "DURATA PROCESSI")

def displayUnfinishedProcesses(connection):
    p = gt.getUnfinishedProcesses(connection)
    gr.displayProcesses(p, "DURATA PROCESSI")

def displayStoppedProcesses(connection):
    p = gt.getStoppedProcesses(connection)
    gr.displayProcesses(p, "DURATA PROCESSI")

def displayStuckedProcesses(connection):
    p = gt.getStuckedProcesses(connection)
    gr.displayProcesses(p, "DURATA PROCESSI")

if __name__ == '__main__':
    connection = connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    displayFinishedProcesses(connection)