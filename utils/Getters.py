from utils.DatabaseConnection import getDataFromDatabase
import utils.DataFrame as df

def getAllEvents(connection):
    query = "SELECT numProcesso, data, fase, etichetta FROM eventi AS e, elencoeventiimportanti AS ei WHERE numProcesso IN (SELECT * FROM processifiniti) AND e.codice = ei.evento ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return df.createEventsDataFrame(events)

def getImportantEvents(connection):
    query = "SELECT numProcesso, data, fase, evento FROM eventiimportanti WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return df.createEventsDataFrame(events)

def getCourtHearingsEvents(connection):
    query = "SELECT numProcesso, data, fase, evento FROM udienze WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return df.createEventsDataFrame(events)

def getProcessesDuration(connection):
    query = "SELECT * FROM durataprocessiinfo ORDER BY numProcesso, dataInizioProcesso"
    processes = getDataFromDatabase(connection, query)
    return df.createProcessesDurationDataFrame(processes)

def getStatesDuration(connection):
    query = "SELECT * FROM duratastatiinfo ORDER BY numProcesso, dataInizioStato"
    processes = getDataFromDatabase(connection, query)
    return df.createStatesDurationsDataFrame(processes)

def getPhasesDuration(connection):
    query = "SELECT * FROM duratafasiinfo ORDER BY numProcesso, dataInizioFase"
    processes = getDataFromDatabase(connection, query)
    return df.createPhasesDurationsDataFrame(processes)

def getEventsDuration(connection):
    query = "SELECT * FROM durataeventiinfo ORDER BY numProcesso, dataInizio"
    processes = getDataFromDatabase(connection, query)
    return df.createEventsDurationsDataFrame(processes)