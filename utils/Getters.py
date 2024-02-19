from utils.DatabaseConnection import getDataFromDatabase
import pandas as pd

def createEventsDataFrame(events):
    pIds = []
    dates = []
    phases = []
    for e in events:
            pIds.append(e[0])
            dates.append(e[1])
            phases.append(e[2])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases})

def createProcessesDataFrame(processes):
    durations = []
    dates = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
    return pd.DataFrame(data = {"data": dates, "durata": durations})

def getAllEvents(connection):
    query = "SELECT numProcesso, data, fase FROM eventi WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getImportantEvents(connection):
    query = "SELECT numProcesso, data, fase FROM eventiimportanti WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getCourtHearingsEvents(connection):
    query = "SELECT numProcesso, data, fase FROM udienze WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getAllProcesses(connection):
    query = "SELECT dataInizioProcesso, durata FROM processicondurata"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getFinishedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata FROM processicondurata WHERE processofinito = 1"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getUnfinishedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata FROM processicondurata WHERE processofinito = 0"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getStoppedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata FROM processicondurata WHERE processofinito = 2"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getStuckedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata FROM processicondurata WHERE processofinito = -1"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)