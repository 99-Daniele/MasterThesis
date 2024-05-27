# this file handles data getters.

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Dataframe as frame
import utils.FileOperation as file

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
endPhaseQuery = "SELECT fase FROM tribunali2020.statinome WHERE stato = 'DF'"
eventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.codice AS codiceEvento, en.etichetta AS evento, gn.giudice AS giudice, gn.alias AS alias, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso, sn.stato AS codiceStato, sn.etichetta AS stato, sn.fase AS faseStato, mn.codice AS codiceMateria, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn, giudicinome AS gn, materienome AS mn WHERE e.numProcesso = p.numProcesso AND e.codice = en.codice AND e.statofinale = sn.stato AND e.giudice = gn.giudice AND p.materia = mn.codice ORDER BY numProcesso, data, numEvento"
importantSubjectsQuery = "SELECT codice FROM materienome WHERE LENGTH(codice) = 6 AND codice LIKE '1%' AND rituale = '4O'"
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
stateNamesQuery = "SELECT sn.stato AS codice, ts.CDESCR AS descrizione, sn.etichetta AS etichetta, ts.FKFASEPROCESSO AS fase_db, sn.fase AS fase FROM statinome AS sn, tipostato AS ts WHERE sn.stato = ts.CCODST"

# courtHearingEvents are taken from text file. This are court hearings type events. Thay can be changed or removed directly from courtHearingEvents.txt file.
try:
    courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
except:
    courtHearingsEvents = None

# get min date from all events of user database.
def getMinDate():
    minDate = connect.getDataFromDatabase(connection, minDateQuery)
    return minDate[0][0]

# get max date from all events of user database.
def getMaxDate():
    maxDate = connect.getDataFromDatabase(connection, maxDateQuery)
    return maxDate[0][0]

# get end phase from all events of user database.
def getEndPhase():
    endPhase = connect.getDataFromDatabase(connection, endPhaseQuery)
    return endPhase[0][0]

# get all events.
def getEvents():
    events = connect.getDataFromDatabase(connection, eventsQuery)
    return events

# get important subjects.
def getImportantSubjects():
    subjects = connect.getDataFromDatabase(connection, importantSubjectsQuery)
    subjects = [s for subject in subjects for s in subject]
    return subjects

# get all events from cache file.
def getAllEvents():
    allEventsDataframe = cache.getData('allEvents.json')
    if allEventsDataframe is None:
        update.refreshData()
        allEventsDataframe = cache.getData('allEvents.json')
    
    return allEventsDataframe

# get important events from cache file.
def getImportantEvents():
    importantEventsDataframe = cache.getData('importantEvents.json')
    if importantEventsDataframe is None:
        update.refreshData()
        importantEventsDataframe = cache.getData('importantEvents.json')
    return importantEventsDataframe

# get phases events from cache file.
def getPhaseEvents():
    phaseEventsDataframe = cache.getData('phaseEvents.json')
    if phaseEventsDataframe is None:
        update.refreshData()
        phaseEventsDataframe = cache.getData('phaseEvents.json')
    return phaseEventsDataframe

# get states events from cache file.
def getStateEvents():
    stateEventsDataframe = cache.getData('stateEvents.json')
    if stateEventsDataframe is None:
        update.refreshData()
        stateEventsDataframe = cache.getData('stateEvents.json')
    return stateEventsDataframe

# get court hearings events from cache file.
def getCourtHearingsEvents():
    courtHearingsEventsDataframe = cache.getData('courtHearingEvents.json')
    if courtHearingsEventsDataframe is None:
        update.refreshData()
        courtHearingsEventsDataframe = cache.getData('courtHearingEvents.json')
    return courtHearingsEventsDataframe

# get processes events from cache file.
def getProcessesDuration():
    processDurationDataframe = cache.getData('processesDuration.json')
    if processDurationDataframe is None:
        update.refreshData()
        processDurationDataframe = cache.getData('processesDuration.json')
    return processDurationDataframe

# get states duration from cache file.
def getStatesDuration():
    stateDurationDataframe = cache.getData('statesDuration.json')
    if stateDurationDataframe is None:
        update.refreshData()
        stateDurationDataframe = cache.getData('statesDuration.json')
    return stateDurationDataframe

# get phases duration from cache file.
def getPhasesDuration():
    phaseDurationDataframe = cache.getData('phasesDuration.json')
    if phaseDurationDataframe is None:
        update.refreshData()
        phaseDurationDataframe = cache.getData('phasesDuration.json')
    return phaseDurationDataframe

# get events duration from cache file.
def getEventsDuration():
    eventDurationDataframe = cache.getData('eventsDuration.json')
    if eventDurationDataframe is None:
        update.refreshData()
        eventDurationDataframe = cache.getData('eventsDuration.json')
    return eventDurationDataframe

# get court hearings duration from cache file.
def getCourtHearingsDuration():
    courtHearingsDurationDataframe = cache.getData('courtHearingsDuration.json')
    if courtHearingsDurationDataframe is None:
        update.refreshData()
        courtHearingsDurationDataframe = cache.getData('courtHearingsDuration.json')
    return courtHearingsDurationDataframe

# get states name dataframe.
def getStateNamesDataframe():
    stateDurationDataframe = getStatesDuration()
    stateNames = connect.getDataFromDatabase(connection, stateNamesQuery)
    stateNamesDataframe = frame.createStateNameDataframe(stateNames)
    df = frame.createStateNameDataframeWithInfo(stateDurationDataframe, stateNamesDataframe)
    return df