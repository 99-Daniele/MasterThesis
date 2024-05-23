# this file handles data getters.

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Dataframe as frame
import utils.FileOperation as file

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
#eventsQuery = "SELECT e.numEvento AS numEvento, en.etichetta AS tipoEvento, s.stato AS codiceStato, s.fase AS faseStato, e.numProcesso AS numProcesso, e.data AS dataEvento, s.etichetta AS tipoStato, s.abbreviazione AS statoAbbr, p.giudice AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, eventinome AS en, statinome AS s, processi AS p, materienome AS mn WHERE ((e.codice = en.codice) AND (e.statofinale = s.stato) AND (e.numProcesso = p.numProcesso) AND (p.materia = mn.codice)) ORDER BY e.numProcesso, e.data, e.numEvento"
eventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.codice AS codiceEvento, en.etichetta AS evento, gn.giudice AS giudice, gn.alias AS alias, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, sn.stato AS codiceStato, sn.etichetta AS stato, sn.fase AS faseStato, mn.codice AS codiceMateria, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn, giudicinome AS gn, materienome AS mn WHERE e.numProcesso = p.numProcesso AND e.codice = en.codice AND e.statofinale = sn.stato AND e.giudice = gn.giudice AND p.materia = mn.codice ORDER BY numProcesso, data, numEvento"
importantSubjectsQuery = "SELECT descrizione FROM materienome WHERE LENGTH(codice) = 6 AND codice LIKE '1%' AND rituale = '4O'"
#allEventsQuery = "SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, en.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn, eventinome AS en WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (e.codice = en.codice)) ORDER BY en.fase"
allEventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, en.etichetta AS evento, e.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, e.statofinale AS codiceStato, sn.fase AS faseStato, p.materia AS materiaProcesso, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, eventinome AS en, statinome AS sn WHERE e.numProcesso = p.numProcesso AND e.statofinale = s.stato  AND e.codice = en.codice"
processDurationQuery = "SELECT DATE_FORMAT(d.dataInizioProcesso,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso, d.durata AS durataProcesso, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, pt.sequenzaCorta AS sequenzaStati, pt.sequenzaFasi AS sequenzaFasi, pt.sequenzaEventi AS sequenzaEventi FROM durataprocessi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice)) ORDER BY p.numProcesso, d.dataInizioProcesso"
stateDurationQuery = "SELECT DATE_FORMAT(d.dataInizioStato,'%Y-%m-%d %H:%i:%S') AS dataInizioStato, d.durata AS durataStato, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, d.etichetta AS tipoStato, d.stato AS codiceStato, sn.fase AS faseStato FROM duratastati AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, statinome AS sn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (d.stato = sn.stato)) ORDER BY p.numProcesso, d.dataInizioStato"
phaseDurationQuery = "SELECT DATE_FORMAT(d.dataInizioFase,'%Y-%m-%d %H:%i:%S') AS dataInizioFase, d.durata AS duratFase, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso, d.fase AS fase, d.ordine AS ordineFase FROM duratafasi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (d.fase <> 0) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizioFase"
eventDurationQuery = "SELECT DATE_FORMAT(d.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioEvento, d.durata AS durataEvento, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, e.numEvento AS numEvento, p.numProcesso AS numProcesso, et.evento AS tipoEvento, e.codice AS codiceEvento, et.fase AS faseEvento FROM durataeventi AS d, eventi AS e, eventitipo AS et, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((d.numEvento = e.numEvento) AND (e.numProcesso = p.numProcesso) AND (e.numEvento = et.numEvento) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizio"
courtHearingsDurationQuery = "SELECT DATE_FORMAT(d.dataInizioUdienza,'%Y-%m-%d %H:%i:%S') AS dataInizioUdienza, d.durata AS durataUdienza, a.alias AS giudiceProcesso, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, p.numProcesso AS numProcesso FROM durataudienze AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia)) ORDER BY p.numProcesso, d.dataInizioUdienza"
phaseEventsQuery = "SELECT * FROM (SELECT e.numProcesso AS numProcesso, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.descrizione AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, DATE_FORMAT(p.dataInizio,'%Y-%m-%d %H:%i:%S') AS dataInizioProcesso FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice))) AS tuttieventi JOIN duratafasi AS df ON numEvento = numEventoInizioFase ORDER BY df.fase"
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

# get all events.
def getEvents():
    events = connect.getDataFromDatabase(connection, eventsQuery)
    return events

# get important subjects.
def getImportantSubjects():
    subjects = connect.getDataFromDatabase(connection, importantSubjectsQuery)
    subjects = [s for subject in subjects for s in subject]
    return subjects

# get dataframe of events from cache.
# if is not present in cache, get it from database and add to cache.
def getEventsDataframe(filename):
    eventsDataframe = cache.getData(filename)
    if eventsDataframe is None:
        update.refreshData()
        eventsDataframe = cache.getData(filename)
    return getEventsDataframe

# get dataframe of processes duration from cache.
# if is not present in cache, get it from database and add to cache.
def getProcessDurationDataframe(filename):
    processDurationDataframe = cache.getData(filename)
    if processDurationDataframe is None:
        update.refreshData()
        processDurationDataframe = cache.getData(filename)
    return processDurationDataframe

# get dataframe of states duration from cache.
# if is not present in cache, get it from database and add to cache.
def getStateDurationDataframe(filename):
    stateDurationDataframe = cache.getData(filename)
    if stateDurationDataframe is None:
        update.refreshData()
        stateDurationDataframe = cache.getData(filename)
    return stateDurationDataframe

# get dataframe of phases duration from cache.
# if is not present in cache, get it from database and add to cache.
def getPhaseDurationDataframe(filename):
    phaseDurationDataframe = cache.getData(filename)
    if phaseDurationDataframe is None:
        update.refreshData()
        phaseDurationDataframe = cache.getData(filename)
    return phaseDurationDataframe

# get dataframe of events duration from cache.
# if is not present in cache, get it from database and add to cache.
def getEventDurationDataframe(filename):
    eventDurationDataframe = cache.getData(filename)
    if eventDurationDataframe is None:
        update.refreshData()
        eventDurationDataframe = cache.getData(filename)
    return eventDurationDataframe

# get dataframe of court hearings duration from cache.
# if is not present in cache, get it from database and add to cache.
def getCourtHearingsDurationDataframe(filename):
    courtHearingsDurationDataframe = cache.getData(filename)
    if courtHearingsDurationDataframe is None:
        update.refreshData()
        courtHearingsDurationDataframe = cache.getData(filename)
    return courtHearingsDurationDataframe

# get all events from cache file.
def getAllEvents():
    return getEventsDataframe('allEvents.json')

# get important events from cache file.
def getImportantEvents():
    return getEventsDataframe('importantEvents.json')

# get phases events from cache file.
def getPhaseEvents():
    return getEventsDataframe('phaseEvents.json')

# get states events from cache file.
def getStateEvents():
    return getEventsDataframe('stateEvents.json')

# get court hearings events from cache file.
def getCourtHearingsEvents():
    return getEventsDataframe('courtHearingEvents.json')

# get processes events from cache file.
def getProcessesDuration():
    return getProcessDurationDataframe('processesDuration.json')

# get states duration from cache file.
def getStatesDuration():
    return getStateDurationDataframe('statesDuration.json')

# get phases duration from cache file.
def getPhasesDuration():
    return getPhaseDurationDataframe('phasesDuration.json')

# get events duration from cache file.
def getEventsDuration():
    return getEventDurationDataframe('eventsDuration.json')

# get court hearings duration from cache file.
def getCourtHearingsDuration():
    return getCourtHearingsDurationDataframe('courtHearingsDuration.json')

# get states name dataframe.
def getStateNamesDataframe():
    stateDurationDataframe = getStateDurationDataframe('statesDuration.json')
    stateNames = connect.getDataFromDatabase(connection, stateNamesQuery)
    stateNamesDataframe = frame.createStateNameDataframe(stateNames, 'codicestato', 'descrizione', 'etichetta', 'fase_db', 'fase')
    df2 = frame.createStateNameDataframeWithInfo(stateDurationDataframe, stateNamesDataframe, 'codicestato', 'durata', 'conteggio')
    return df2