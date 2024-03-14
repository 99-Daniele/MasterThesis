import utils.DatabaseConnection as connect
import utils.DataFrame as frame
import utils.Cache as cache
import time as tm

def getAllEvents():
    query = "SELECT * FROM eventiinfo ORDER BY fase"
    events = cache.getData('eventi', query)
    return frame.createEventsDataFrame(events)

def getImportantEvents():
    query = "SELECT * FROM eventiimportantiinfo ORDER BY fase"
    events = cache.getData('eventiimportanti', query)
    return frame.createEventsDataFrame(events)

def getCourtHearingEvents():
    query = "SELECT * FROM eventiudienzeinfo ORDER BY fase"
    events = cache.getData('eventiudienze', query)
    return frame.createEventsDataFrame(events)

def getImportantEventsType():
    query = "SELECT DISTINCT etichetta FROM elencoeventiimportanti"
    importantEventsType = cache.getData('tipoeventiimportanti', query)
    importantEventsType = [e[0] for e in importantEventsType]
    return importantEventsType

def getCourtHearingEventsType():
    query = "SELECT DISTINCT etichetta FROM elencoeventiudienze"
    courtHearingsEventsType = cache.getData('tipoeventiudienze', query)
    courtHearingsEventsType = [e[0] for e in courtHearingsEventsType]
    return courtHearingsEventsType

def getEventsType():
    query = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta, s.abbreviazione FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato ORDER BY numEvento"
    eventsType = cache.getData('tipoeventi', query)
    return eventsType

def getTestEventsType():
    query = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta, s.abbreviazione FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato AND (numProcesso = 109848 OR numProcesso = 109855 OR numProcesso = 109850 OR numProcesso = 109959) ORDER BY numEvento"
    eventsType = connect.getDataFromDatabase(query)
    return eventsType

def getProcessesDuration():
    query = "SELECT * FROM durataprocessiinfo ORDER BY numProcesso, dataInizioProcesso"
    processes = cache.getData('durataprocessi', query)
    return frame.createProcessesDurationDataFrame(processes)

def getStatesDuration():
    query = "SELECT * FROM duratastatiinfo ORDER BY numProcesso, dataInizioStato"
    processes = cache.getData('duratastati', query)
    return frame.createStatesDurationsDataFrame(processes)

def getPhasesDuration():
    query = "SELECT * FROM duratafasiinfo ORDER BY numProcesso, dataInizioFase"
    processes = cache.getData('duratafasi', query)
    return frame.createPhasesDurationsDataFrame(processes)

def getEventsDuration():
    query = "SELECT * FROM durataeventiinfo WHERE evento IN (SELECT evento FROM durataeventiinfo GROUP BY evento HAVING COUNT(*) > 50) ORDER BY numProcesso, dataInizio"
    processes = cache.getData('durataeventi', query)
    return frame.createEventsDurationsDataFrame(processes)

def getCourtHearingsDuration():
    query = "SELECT * FROM durataudienzeinfo ORDER BY numProcesso, dataInizioUdienza"
    courtHearings = cache.getData('durataudienze', query)
    return frame.createCourtHearingsDurationDataFrame(courtHearings)
