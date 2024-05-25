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
eventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.codice AS codiceEvento, en.etichetta AS evento, gn.giudice AS giudice, gn.alias AS alias, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, sn.stato AS codiceStato, sn.etichetta AS stato, sn.fase AS faseStato, mn.codice AS codiceMateria, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn, giudicinome AS gn, materienome AS mn WHERE e.numProcesso = p.numProcesso AND e.codice = en.codice AND e.statofinale = sn.stato AND e.giudice = gn.giudice AND p.materia = mn.codice ORDER BY numProcesso, data, numEvento"
importantSubjectsQuery = "SELECT descrizione FROM materienome WHERE LENGTH(codice) = 6 AND codice LIKE '1%' AND rituale = '4O'"
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
stateNamesQuery = "SELECT sn.stato AS codice, ts.CDESCR AS descrizione, sn.etichetta AS etichetta, ts.FKFASEPROCESSO AS fase_db, sn.fase AS fase FROM statinome AS sn, tipostato AS ts WHERE sn.stato = ts.CCODST"

# importantEvents are taken from text file. This are type of events that are the most important. Thay can be changed or removed directly from importantEvents.txt file.
try:
    importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
    #importantEventsQuery = "SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, en.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, eventinome AS en WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (e.codice = en.codice) AND (et.evento IN " + importantEvents + ")) ORDER BY en.fase"
    #importantEventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.etichetta AS evento, e.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, e.statofinale AS codiceStato, s.FKFASEPROCESSO AS faseStato, p.materia AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, tipostato AS s, eventinome AS en WHERE e.numProcesso = p.numProcesso AND e.statofinale = s.CCODST AND e.codice = en.codice AND en.etichetta IN " + importantEvents + ""
except:
    importantEvents = None
    #importantEventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.etichetta AS evento, e.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, e.statofinale AS codiceStato, s.FKFASEPROCESSO AS faseStato, p.materia AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, tipostato AS s, eventinome AS en WHERE e.numProcesso = p.numProcesso AND e.statofinale = s.CCODST AND e.codice = en.codice"

# importantStates are taken from text file. This are type of states that are the most important. Thay can be changed or removed directly from importantStates.txt file.
try:
    importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
    #stateEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (et.stato IN " + importantStates + "))) AS tuttieventi JOIN duratastati AS df ON numEvento = numEventoInizioStato ORDER BY fase"
except:
    importantStates = None
    #stateEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice))) AS tuttieventi JOIN duratastati AS df ON numEvento = numEventoInizioStato ORDER BY fase"  

# courtHearingEvents are taken from text file. This are court hearings type events. Thay can be changed or removed directly from courtHearingEvents.txt file.
try:
    courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    #courtHearingsEventsQuery = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, p.dataInizio AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (et.evento IN " + courtHearingsEvents + ")) ORDER BY et.fase"
except:
    courtHearingsEvents = None
    #courtHearingsEventsQuery = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, p.dataInizio AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice)) ORDER BY et.fase"

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
    stateNamesDataframe = frame.createStateNameDataframe(stateNames, 'codicestato', 'descrizione', 'etichetta', 'fase_db', 'fase')
    df = frame.createStateNameDataframeWithInfo(stateDurationDataframe, stateNamesDataframe, 'codicestato', 'durata', 'conteggio')
    return df