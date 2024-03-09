import utils.DatabaseConnection as connect
import utils.DataFrame as frame

def getAllEvents(connection):
    query = "SELECT * FROM eventiinfo ORDER BY fase"
    events = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDataFrame(events)

def getImportantEvents(connection):
    query = "SELECT * FROM eventiimportantiinfo ORDER BY fase"
    events = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDataFrame(events)

def getCourtHearingEvents(connection):
    query = "SELECT * FROM eventiudienzeinfo ORDER BY fase"
    events = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDataFrame(events)

def getImportantEventsType(connection):
    query = "SELECT DISTINCT etichetta FROM elencoeventiimportanti"
    importantEventsType = connect.getDataFromDatabase(connection, query)
    importantEventsType = [e[0] for e in importantEventsType]
    return importantEventsType

def getCourtHearingEventsType(connection):
    query = "SELECT DISTINCT etichetta FROM elencoeventiudienze"
    courtHearingsEventsType = connect.getDataFromDatabase(connection, query)
    courtHearingsEventsType = [e[0] for e in courtHearingsEventsType]
    return courtHearingsEventsType

def getEventsType(connection):
    query = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta, s.abbreviazione FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato ORDER BY numEvento"
    eventsType = connect.getDataFromDatabase(connection, query)
    return eventsType

def getTestEventsType(connection):
    query = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta, s.abbreviazione FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato AND (numProcesso = 109848 OR numProcesso = 109855 OR numProcesso = 109850 OR numProcesso = 109959) ORDER BY numEvento"
    eventsType = connect.getDataFromDatabase(connection, query)
    return eventsType

def getProcessesDuration(connection):
    query = "SELECT * FROM durataprocessiinfo ORDER BY numProcesso, dataInizioProcesso"
    processes = connect.getDataFromDatabase(connection, query)
    return frame.createProcessesDurationDataFrame(processes)

def getStatesDuration(connection):
    query = "SELECT * FROM duratastatiinfo ORDER BY numProcesso, dataInizioStato"
    processes = connect.getDataFromDatabase(connection, query)
    return frame.createStatesDurationsDataFrame(processes)

def getPhasesDuration(connection):
    query = "SELECT * FROM duratafasiinfo ORDER BY numProcesso, dataInizioFase"
    processes = connect.getDataFromDatabase(connection, query)
    return frame.createPhasesDurationsDataFrame(processes)

def getEventsDuration(connection):
    query = "SELECT * FROM durataeventiinfo WHERE evento IN (SELECT evento FROM durataeventiinfo GROUP BY evento HAVING COUNT(*) > 50) ORDER BY numProcesso, dataInizio"
    processes = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDurationsDataFrame(processes)

def getCourtHearingsDuration(connection):
    query = "SELECT * FROM durataudienzeinfo ORDER BY numProcesso, dataInizioUdienza"
    courtHearings = connect.getDataFromDatabase(connection, query)
    return frame.createCourtHearingsDurationDataFrame(courtHearings)
