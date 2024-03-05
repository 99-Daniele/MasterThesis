import utils.DataFrame as df
import time as tm

import utils.DatabaseConnection as connect

def getAllEvents(connection):
    query = "SELECT * FROM eventiinfo ORDER BY fase"
    events = connect.getDataFromDatabase(connection, query)
    return df.createEventsDataFrame(events)

def getProcessesDuration(connection):
    query = "SELECT * FROM durataprocessiinfo ORDER BY numProcesso, dataInizioProcesso"
    processes = connect.getDataFromDatabase(connection, query)
    return df.createProcessesDurationDataFrame(processes)

def getStatesDuration(connection):
    query = "SELECT * FROM duratastatiinfo ORDER BY numProcesso, dataInizioStato"
    processes = connect.getDataFromDatabase(connection, query)
    return df.createStatesDurationsDataFrame(processes)

def getPhasesDuration(connection):
    query = "SELECT * FROM duratafasiinfo ORDER BY numProcesso, dataInizioFase"
    processes = connect.getDataFromDatabase(connection, query)
    return df.createPhasesDurationsDataFrame(processes)

def getEventsDuration(connection):
    query = "SELECT * FROM durataeventiinfo WHERE evento IN (SELECT evento FROM durataeventiinfo GROUP BY evento HAVING COUNT(*) > 50) ORDER BY numProcesso, dataInizio"
    processes = connect.getDataFromDatabase(connection, query)
    return df.createEventsDurationsDataFrame(processes)