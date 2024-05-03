# this file handles data getters.

import utils.Cache.Cache as cache
import utils.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file

# connection is user database connection.
connection = connect.getDatabaseConnection()

# importantEvents, courtHearingsEvents, importantStates taken from text file.
importantEvents = str(tuple(file.getDataFromTextFile('utils/Preferences/importantEvents.txt')))
courtHearingsEvents = str(tuple(file.getDataFromTextFile('utils/Preferences/courtHearingsEvents.txt')))
importantStates = str(tuple(file.getDataFromTextFile('utils/Preferences/importantStates.txt')))

# queries to obtain data from database.
maxDateQuery = "SELECT MAX(data) FROM eventi"
eventsQuery = "SELECT e.numEvento AS numEvento, en.etichetta AS tipoEvento, s.stato AS codiceStato, s.fase AS faseStato, e.numProcesso AS numProcesso, e.data AS dataEvento, s.etichetta AS tipoStato, s.abbreviazione AS statoAbbr FROM eventi AS e, eventinome AS en, statinome AS s WHERE ((e.codice = en.codice) AND (e.statofinale = s.stato)) ORDER BY e.numProcesso, e.data, e.numEvento"
allEventsQuery = "SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, en.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, processicambiogiudice as pcg, eventinome AS en WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (pcg.numProcesso = p.numProcesso) AND (e.codice = en.codice)) ORDER BY en.fase"
importantEventsQuery = "SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, en.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, processicambiogiudice as pcg, eventinome AS en WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (pcg.numProcesso = p.numProcesso) AND (e.codice = en.codice) AND (et.evento IN " + importantEvents + ")) ORDER BY en.fase"
phaseEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, processicambiogiudice as pcg WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (pcg.numProcesso = p.numProcesso))) AS tuttieventi JOIN duratafasi AS df ON numEvento = numEventoInizioFase ORDER BY df.fase"
stateEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, processicambiogiudice as pcg WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (pcg.numProcesso = p.numProcesso)  AND (et.stato IN " + importantStates + "))) AS tuttieventi JOIN duratastati AS df ON numEvento = numEventoInizioStato ORDER BY fase"
courtHearingsEventsQuery = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, p.dataInizio AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, processicambiogiudice as pcg WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (pcg.numProcesso = p.numProcesso) AND (et.evento IN " + courtHearingsEvents + ")) ORDER BY et.fase"
processDurationQuery = "SELECT DATE_FORMAT(d.dataInizioProcesso,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso, d.durata AS durataProcesso, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambioGiudice, p.numProcesso AS numProcesso, pt.sequenzaCorta AS sequenzaStati, pt.sequenzaFasi AS sequenzaFasi FROM durataprocessi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioProcesso"
stateDurationQuery = "SELECT DATE_FORMAT(d.dataInizioStato,'%Y-%m-%d %H:%i:%S') AS dataInizioStato, d.durata AS durataStato, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambiogiudice, p.numProcesso AS numProcesso, d.etichetta AS tipoStato, d.stato AS codiceStato, sn.fase AS faseStato FROM duratastati AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, statinome AS sn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (d.stato = sn.stato) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioStato"
phaseDurationQuery = "SELECT DATE_FORMAT(d.dataInizioFase,'%Y-%m-%d %H:%i:%S') AS dataInizioFase, d.durata AS duratFase, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambiogiudice, p.numProcesso AS numProcesso, d.fase AS fase, d.ordine AS ordineFase FROM duratafasi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambioGiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (d.fase <> 0) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioFase"
eventDurationQuery = "SELECT DATE_FORMAT(d.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioEvento, d.durata AS durataEvento, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, e.numEvento AS numEvento, p.numProcesso AS numProcesso, et.evento AS tipoEvento, e.codice AS codiceEvento, et.fase AS faseEvento FROM durataeventi AS d, eventi AS e, eventitipo AS et, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((d.numEvento = e.numEvento) AND (e.numProcesso = p.numProcesso) AND (e.numEvento = et.numEvento) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizio"
courtHearingsDurationQuery = "SELECT DATE_FORMAT(d.dataInizioUdienza,'%Y-%m-%d %H:%i:%S') AS dataInizioUdienza, d.durata AS durataUdienza, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambioGiudice, p.numProcesso AS numProcesso FROM durataudienze AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioUdienza"

# get max date from all events of user database.
def getMaxDate():
    maxDate = connect.getDataFromDatabase(connection, maxDateQuery)
    return maxDate[0][0]

# get all events.
def getEvents():
    events = connect.getDataFromDatabase(connection, eventsQuery)
    return events

# get dataframe of all events from dataframe.
def getEventsDataframeFromDatabase(query):
    events = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDataFrame(events)

# get dataframe of all events from cache.
# if is not present in cache, get it from database and add to cache.
def getEventsDataframe(filename, query):
    eventsDataframe = cache.getData(filename)
    if eventsDataframe is None:
        eventsDataframe = getEventsDataframeFromDatabase(query)
        cache.cacheUpdate(filename, eventsDataframe)
    return eventsDataframe

# get dataframe of processes duration from dataframe.
def getProcessDurationDataframeFromDatabase(query):
    processDuration = connect.getDataFromDatabase(connection, query)
    return frame.createProcessesDurationDataFrame(processDuration)

# get dataframe of processes duration from cache.
# if is not present in cache, get it from database and add to cache.
def getProcessDurationDataframe(filename, query):
    processDurationDataframe = cache.getData(filename)
    if processDurationDataframe is None:
        processDurationDataframe = getProcessDurationDataframeFromDatabase(query)
        cache.cacheUpdate(filename, processDurationDataframe)
    return processDurationDataframe

# get dataframe of states duration from dataframe.
def getStateDurationDataframeFromDatabase(query):
    stateDuration = connect.getDataFromDatabase(connection, query)
    return frame.createStatesDurationsDataFrame(stateDuration)

# get dataframe of states duration from cache.
# if is not present in cache, get it from database and add to cache.
def getStateDurationDataframe(filename, query):
    stateDurationDataframe = cache.getData(filename)
    if stateDurationDataframe is None:
        stateDurationDataframe = getStateDurationDataframeFromDatabase(query)
        cache.cacheUpdate(filename, stateDurationDataframe)
    return stateDurationDataframe

# get dataframe of phases duration from dataframe.
def getPhaseDurationDataframeFromDatabase(query):
    phaseDuration = connect.getDataFromDatabase(connection, query)
    return frame.createPhasesDurationsDataFrame(phaseDuration)

# get dataframe of phases duration from cache.
# if is not present in cache, get it from database and add to cache.
def getPhaseDurationDataframe(filename, query):
    phaseDurationDataframe = cache.getData(filename)
    if phaseDurationDataframe is None:
        phaseDurationDataframe = getPhaseDurationDataframeFromDatabase(query)
        cache.cacheUpdate(filename, phaseDurationDataframe)
    return phaseDurationDataframe

# get dataframe of events duration from dataframe.
def getEventDurationDataframeFromDatabase(query):
    eventDuration = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDurationsDataFrame(eventDuration)

# get dataframe of events duration from cache.
# if is not present in cache, get it from database and add to cache.
def getEventDurationDataframe(filename, query):
    eventDurationDataframe = cache.getData(filename)
    if eventDurationDataframe is None:
        eventDurationDataframe = getEventDurationDataframeFromDatabase(query)
        cache.cacheUpdate(filename, eventDurationDataframe)
    return eventDurationDataframe

# get dataframe of court hearings duration from dataframe.
def getCourtHearingsDurationDataframeFromDatabase(query):
    courtHearingsDuration = connect.getDataFromDatabase(connection, query)
    return frame.createCourtHearingsDurationDataFrame(courtHearingsDuration)

# get dataframe of court hearings duration from cache.
# if is not present in cache, get it from database and add to cache.
def getCourtHearingsDurationDataframe(filename, query):
    courtHearingsDurationDataframe = cache.getData(filename)
    if courtHearingsDurationDataframe is None:
        courtHearingsDurationDataframe = getCourtHearingsDurationDataframeFromDatabase(query)
        cache.cacheUpdate(courtHearingsDurationDataframe)
    return courtHearingsDurationDataframe

# get all events from cache file.
def getAllEvents():
    return getEventsDataframe('allEvents.json', allEventsQuery)

# get important events from cache file.
def getImportantEvents():
    return getEventsDataframe('importantEvents.json', importantEventsQuery)

# get phases events from cache file.
def getPhaseEvents():
    return getEventsDataframe('phaseEvents.json', phaseEventsQuery)

# get states events from cache file.
def getStateEvents():
    return getEventsDataframe('stateEvents.json', stateEventsQuery)

# get court hearings events from cache file.
def getCourtHearingsEvents():
    return getEventsDataframe('courtHearingsEvents.json', courtHearingsEventsQuery)

# get processes events from cache file.
def getProcessesDuration():
    return getProcessDurationDataframe('processesDuration.json', processDurationQuery)

# get states duration from cache file.
def getStatesDuration():
    return getStateDurationDataframe('statesDuration.json', stateDurationQuery)

# get phases duration from cache file.
def getPhasesDuration():
    return getPhaseDurationDataframe('phasesDuration.json', phaseDurationQuery)

# get events duration from cache file.
def getEventsDuration():
    return getEventDurationDataframe('eventsDuration.json', eventDurationQuery)

# get court hearings duration from cache file.
def getCourtHearingsDuration():
    return getCourtHearingsDurationDataframe('courtHearingsDuration.json', courtHearingsDurationQuery)

# update cache with user database current data.
def updateCache():
    allEventsDataframe = getEventsDataframeFromDatabase(allEventsQuery)
    cache.updateCache('allEvents.json', allEventsDataframe)
    importantEventsDataframe = getEventsDataframeFromDatabase(importantEventsQuery)
    cache.updateCache('importantEvents.json', importantEventsDataframe)
    stateEventsDataframe = getEventsDataframeFromDatabase(stateEventsQuery)
    cache.updateCache('stateEvents.json', stateEventsDataframe)
    phaseEventsDataframe = getEventsDataframeFromDatabase(phaseEventsQuery)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)
    courtHearingsEventsDataframe = getEventsDataframeFromDatabase(courtHearingsEventsQuery)
    cache.updateCache('courtHearingsEvents.json', courtHearingsEventsDataframe)
    processDurationDataframe = getProcessDurationDataframeFromDatabase(processDurationQuery)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    stateDurationDataframe = getStateDurationDataframeFromDatabase(stateDurationQuery)
    cache.updateCache('statesDuration.json', stateDurationDataframe)
    phaseDurationDataframe = getPhaseDurationDataframeFromDatabase(phaseDurationQuery)
    print(phaseDurationDataframe)
    cache.updateCache('phasesDuration.json', phaseDurationDataframe)
    eventDurationDataframe = getEventDurationDataframeFromDatabase(eventDurationQuery)
    cache.updateCache('eventsDuration.json', eventDurationDataframe)
    courtHearingsDurationDataframe = getCourtHearingsDurationDataframeFromDatabase(courtHearingsDurationQuery)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    