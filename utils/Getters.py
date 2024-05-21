# this file handles data getters.

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
#eventsQuery = "SELECT e.numEvento AS numEvento, en.etichetta AS tipoEvento, s.stato AS codiceStato, s.fase AS faseStato, e.numProcesso AS numProcesso, e.data AS dataEvento, s.etichetta AS tipoStato, s.abbreviazione AS statoAbbr, p.giudice AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, eventinome AS en, statinome AS s, processi AS p, materienome AS mn WHERE ((e.codice = en.codice) AND (e.statofinale = s.stato) AND (e.numProcesso = p.numProcesso) AND (p.materia = mn.codice)) ORDER BY e.numProcesso, e.data, e.numEvento"
eventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.etichetta AS evento, e.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, sn.etichetta AS stato, sn.fase AS faseStato, p.materia AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn WHERE e.numProcesso = p.numProcesso AND e.codice = en.codice AND e.statofinale = sn.stato ORDER BY numProcesso, data, numEvento"
importantSubjectsQuery = "SELECT descrizione FROM materienome WHERE LENGTH(codice) = 6 AND codice LIKE '1%' AND rituale = '4O'"
#allEventsQuery = "SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, en.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, eventinome AS en WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (e.codice = en.codice)) ORDER BY en.fase"
allEventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.etichetta AS evento, e.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, e.statofinale AS codiceStato, sn.fase AS faseStato, p.materia AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn WHERE e.numProcesso = p.numProcesso AND e.statofinale = s.stato  AND e.codice = en.codice"
processDurationQuery = "SELECT DATE_FORMAT(d.dataInizioProcesso,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso, d.durata AS durataProcesso, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, pt.sequenzaCorta AS sequenzaStati, pt.sequenzaFasi AS sequenzaFasi, pt.sequenzaEventi AS sequenzaEventi FROM durataprocessi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice)) ORDER BY p.numProcesso, d.dataInizioProcesso"
stateDurationQuery = "SELECT DATE_FORMAT(d.dataInizioStato,'%Y-%m-%d %H:%i:%S') AS dataInizioStato, d.durata AS durataStato, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, d.etichetta AS tipoStato, d.stato AS codiceStato, sn.fase AS faseStato FROM duratastati AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, statinome AS sn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (d.stato = sn.stato)) ORDER BY p.numProcesso, d.dataInizioStato"
phaseDurationQuery = "SELECT DATE_FORMAT(d.dataInizioFase,'%Y-%m-%d %H:%i:%S') AS dataInizioFase, d.durata AS duratFase, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, d.fase AS fase, d.ordine AS ordineFase FROM duratafasi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (d.fase <> 0) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizioFase"
eventDurationQuery = "SELECT DATE_FORMAT(d.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioEvento, d.durata AS durataEvento, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, e.numEvento AS numEvento, p.numProcesso AS numProcesso, et.evento AS tipoEvento, e.codice AS codiceEvento, et.fase AS faseEvento FROM durataeventi AS d, eventi AS e, eventitipo AS et, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((d.numEvento = e.numEvento) AND (e.numProcesso = p.numProcesso) AND (e.numEvento = et.numEvento) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizio"
courtHearingsDurationQuery = "SELECT DATE_FORMAT(d.dataInizioUdienza,'%Y-%m-%d %H:%i:%S') AS dataInizioUdienza, d.durata AS durataUdienza, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso FROM durataudienze AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizioUdienza"
phaseEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice))) AS tuttieventi JOIN duratafasi AS df ON numEvento = numEventoInizioFase ORDER BY df.fase"

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

# get all events.
def getEvents():
    events = connect.getDataFromDatabase(connection, eventsQuery)
    return events

# get important subjects.
def getImportantSubjects():
    subjects = connect.getDataFromDatabase(connection, importantSubjectsQuery)
    subjects = [s for subject in subjects for s in subject]
    return subjects

# get dataframe of events from dataframe.
def getEventsDataframeFromDatabase(query, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    events = connect.getDataFromDatabase(connection, query)
    return frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)

# get dataframe of all events from dataframe.
def getAllEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    events = getEventsDataframeFromDatabase(eventsQuery, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return events

# get dataframe of important events from dataframe.
def getImportantEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    events = getEventsDataframeFromDatabase(eventsQuery, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    if importantEvents != None:
        events = events[events[eventTag].isin(importantEvents)]
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return events

# get dataframe of state events from dataframe.
def getStateEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    events = getEventsDataframeFromDatabase(eventsQuery, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    events = events.groupby([numProcessTag, stateTag], as_index = False).first()
    if importantStates != None:
        events = events[events[stateTag].isin(importantStates)]
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return events

# get dataframe of phase events from dataframe.
def getPhaseEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    events = getEventsDataframeFromDatabase(eventsQuery, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    events = events.groupby([numProcessTag, phaseTag], as_index = False).first()
    events = events.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    return events

# get dataframe of events from cache.
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
    numEventTag = 'numEvento'
    numProcessTag = 'numProcesso'
    eventTag = 'evento'
    judgeTag = 'giudice'
    dateTag = 'data'
    stateTag = 'stato'
    phaseTag = 'fase'
    subjectTag = 'materia'
    sectionTag = 'sezione'
    endPhase = '4.0'
    allEventsDataframe = getAllEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    cache.updateCache('allEvents.json', allEventsDataframe)
    importantEventsDataframe = getImportantEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    cache.updateCache('importantEvents.json', importantEventsDataframe)
    stateEventsDataframe = getStateEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    cache.updateCache('stateEvents.json', stateEventsDataframe)
    phaseEventsDataframe = getPhaseEventsDataframeFromDatabase(numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)
    courtHearingsEventsDataframe = getEventsDataframeFromDatabase(courtHearingsEventsQuery)
    cache.updateCache('courtHearingsEvents.json', courtHearingsEventsDataframe)
    processDurationDataframe = getProcessDurationDataframeFromDatabase(processDurationQuery)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    stateDurationDataframe = getStateDurationDataframeFromDatabase(stateDurationQuery)
    cache.updateCache('statesDuration.json', stateDurationDataframe)
    phaseDurationDataframe = getPhaseDurationDataframeFromDatabase(phaseDurationQuery)
    cache.updateCache('phasesDuration.json', phaseDurationDataframe)
    eventDurationDataframe = getEventDurationDataframeFromDatabase(eventDurationQuery)
    eventDurationDataframe = frame.keepOnlyRelevant(eventDurationDataframe, 0.005, 'evento', 'conteggio')
    cache.updateCache('eventsDuration.json', eventDurationDataframe)
    courtHearingsDurationDataframe = getCourtHearingsDurationDataframeFromDatabase(courtHearingsDurationQuery)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    