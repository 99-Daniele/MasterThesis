# this file handles data getters.

import pandas as pd

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.utilities.Utilities as utilities

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
endPhaseQuery = "SELECT FKFASEPROCESSO FROM tipostato WHERE CCODST = 'DF'"
eventsNamesQuery = "SELECT en.codice AS codice, te.CDESCR AS descrizione, en.etichetta AS etichetta, en.fase AS fase FROM eventinome AS en, tipoeventi AS te WHERE en.codice = te.CCDOEV"
eventsQuery = "SELECT e.numEvento AS numEvento, e.numProcesso AS numProcesso, e.codice AS codiceEvento, p.giudice AS giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S') AS dataEvento, DATE_FORMAT((SELECT MIN(data) FROM eventi AS ev WHERE e.numProcesso = ev.numProcesso), '%Y-%m-%d %H:%i:%S') AS dataInizioProcesso, e.statofinale AS codiceStato, s.FKFASEPROCESSO AS faseStato, p.materia AS codiceMateria, p.sezione AS sezioneProcesso FROM eventi AS e, processi AS p, tipostato AS s WHERE e.numProcesso = p.numProcesso AND e.statofinale = s.CCODST ORDER BY e.numProcesso, e.data, e.numEvento"
judgeNamesQuery = "SELECT * FROM giudicinome ORDER BY alias"
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
stallStatesQuery = "SELECT CCODST FROM tipostato WHERE FKFASEPROCESSO IS NULL"
stateNamesQuery = "SELECT sn.stato AS codice, ts.CDESCR AS descrizione, sn.etichetta AS etichetta, ts.FKFASEPROCESSO AS fase_db, sn.fase AS fase FROM statinome AS sn, tipostato AS ts WHERE sn.stato = ts.CCODST"
subjectNamesQuery = "SELECT * FROM materienome ORDER BY codice"

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

# get stall phase from all events of user database.
def getStallStates():
    stallStateTuples = connect.getDataFromDatabase(connection, stallStatesQuery)
    stallStates = utilities.fromListOfTuplesToList(stallStateTuples)
    return stallStates

# get all events.
def getEvents():
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    processDateTag = utilities.getTagName("processDateTag")
    sectionTag = utilities.getTagName("sectionTag")
    events = connect.getDataFromDatabase(connection, eventsQuery)
    keys = [numEventTag, numProcessTag, codeEventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, phaseDBTag, codeSubjectTag, sectionTag]
    dictEvents = utilities.fromListOfTuplesToListOfDicts(events, keys)
    return dictEvents

# get all events from cache file.
def getAllEvents():
    allEventsDataframe = cache.getDataframe('allEvents.json')
    if allEventsDataframe is None:
        update.refreshData()
        allEventsDataframe = cache.getDataframe('allEvents.json')
    return allEventsDataframe

# get important events from cache file.
def getImportantEvents():
    importantEventsDataframe = cache.getDataframe('importantEvents.json')
    if importantEventsDataframe is None:
        update.refreshData()
        importantEventsDataframe = cache.getDataframe('importantEvents.json')
    return importantEventsDataframe

# get phases events from cache file.
def getPhaseEvents():
    phaseEventsDataframe = cache.getDataframe('phaseEvents.json')
    if phaseEventsDataframe is None:
        update.refreshData()
        phaseEventsDataframe = cache.getDataframe('phaseEvents.json')
    return phaseEventsDataframe

# get states events from cache file.
def getStateEvents():
    stateEventsDataframe = cache.getDataframe('stateEvents.json')
    if stateEventsDataframe is None:
        update.refreshData()
        stateEventsDataframe = cache.getDataframe('stateEvents.json')
    return stateEventsDataframe

# get court hearings events from cache file.
def getCourtHearingsEvents():
    courtHearingsEventsDataframe = cache.getDataframe('courtHearingEvents.json')
    if courtHearingsEventsDataframe is None:
        update.refreshData()
        courtHearingsEventsDataframe = cache.getDataframe('courtHearingEvents.json')
    return courtHearingsEventsDataframe

# get processes events from cache file.
def getProcessesDuration():
    processDurationDataframe = cache.getDataframe('processesDuration.json')
    if processDurationDataframe is None:
        update.refreshData()
        processDurationDataframe = cache.getDataframe('processesDuration.json')
    return processDurationDataframe

# get processes events from cache file filtered by important process types, sections and subjects.
def getProcessesDurationFiltered():
    processDurationDataframeFiltered = cache.getDataframe('processesDurationFiltered.json')
    if processDurationDataframeFiltered is None:
        update.refreshData()
        processDurationDataframeFiltered = cache.getDataframe('processesDurationFiltered.json')
    return processDurationDataframeFiltered

# get states duration from cache file.
def getStatesDuration():
    stateDurationDataframe = cache.getDataframe('statesDuration.json')
    if stateDurationDataframe is None:
        update.refreshData()
        stateDurationDataframe = cache.getDataframe('statesDuration.json')
    return stateDurationDataframe

# get states duration from cache file filtered by important process types, sections and subjects.
def getStatesDurationFiltered():
    stateDurationDataframeFiltered = cache.getDataframe('statesDurationFiltered.json')
    if stateDurationDataframeFiltered is None:
        update.refreshData()
        stateDurationDataframeFiltered = cache.getDataframe('statesDurationFiltered.json')
    return stateDurationDataframeFiltered

# get phases duration from cache file.
def getPhasesDuration():
    phaseDurationDataframe = cache.getDataframe('phasesDuration.json')
    if phaseDurationDataframe is None:
        update.refreshData()
        phaseDurationDataframe = cache.getDataframe('phasesDuration.json')
    return phaseDurationDataframe

# get phases duration from cache file filtered by important process types, sections and subjects.
def getPhasesDurationFiltered():
    phaseDurationDataframeFiltered = cache.getDataframe('phasesDurationFiltered.json')
    if phaseDurationDataframeFiltered is None:
        update.refreshData()
        phaseDurationDataframeFiltered = cache.getDataframe('phasesDurationFiltered.json')
    return phaseDurationDataframeFiltered

# get events duration from cache file.
def getEventsDuration():
    eventDurationDataframe = cache.getDataframe('eventsDuration.json')
    if eventDurationDataframe is None:
        update.refreshData()
        eventDurationDataframe = cache.getDataframe('eventsDuration.json')
    return eventDurationDataframe

# get events duration from cache file filtered by important process types, sections and subjects.
def getEventsDurationFiltered():
    eventDurationDataframeFiltered = cache.getDataframe('eventsDurationFiltered.json')
    if eventDurationDataframeFiltered is None:
        update.refreshData()
        eventDurationDataframeFiltered = cache.getDataframe('eventsDurationFiltered.json')
    return eventDurationDataframeFiltered

# get court hearings duration from cache file.
def getCourtHearingsDuration():
    courtHearingsDurationDataframe = cache.getDataframe('courtHearingsDuration.json')
    if courtHearingsDurationDataframe is None:
        update.refreshData()
        courtHearingsDurationDataframe = cache.getDataframe('courtHearingsDuration.json')
    return courtHearingsDurationDataframe

# get court hearings duration from cache file filtered by important process types, sections and subjects.
def getCourtHearingsDurationFiltered():
    courtHearingsDurationFiltered = cache.getDataframe('courtHearingsDurationFiltered.json')
    if courtHearingsDurationFiltered is None:
        update.refreshData()
        courtHearingsDurationFiltered = cache.getDataframe('courtHearingsDurationFiltered.json')
    return courtHearingsDurationFiltered

# get states name dataframe.
def getStateNamesDataframe():
    codeStateTag = utilities.getTagName("codeStateTag")
    stateDurationDataframe = getStatesDuration()    
    statesName = file.getDataFromJsonFile('preferences/statesName.json')
    statesNameDataframe = pd.DataFrame.from_dict(statesName, orient = 'index').reset_index().rename(columns = {'index': codeStateTag})
    df = frame.createStateNameDataframeWithInfo(stateDurationDataframe, statesNameDataframe)
    return df

# get events name dataframe.
def getEventNamesDataframe():
    codeEventTag = utilities.getTagName("codeEventTag")
    eventDurationDataframe = getEventsDuration()
    eventsName = file.getDataFromJsonFile('preferences/eventsName.json')
    eventNamesDataframe = pd.DataFrame.from_dict(eventsName, orient = 'index').reset_index().rename(columns = {'index': codeEventTag})
    df = frame.createEventNameDataframeWithInfo(eventDurationDataframe, eventNamesDataframe)
    return df

# get judge name dataframe.
def getJudgeNamesDataframe():
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    processDurationDataframe = getProcessesDuration()
    judgesName = file.getDataFromJsonFile('preferences/judgesName.json')
    judgesNameDataframe = pd.DataFrame.from_dict(judgesName, orient = 'index').reset_index().rename(columns = {'index': codeJudgeTag})
    df = frame.createJudgeNameDataframeWithInfo(processDurationDataframe, judgesNameDataframe)
    return df

# get subject name dataframe.
def getSubjectNamesDataframe():
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    processDurationDataframe = getProcessesDuration()
    subjectsName = file.getDataFromJsonFile('preferences/subjectsName.json')
    subjectsNameDataframe = pd.DataFrame.from_dict(subjectsName, orient = 'index').reset_index().rename(columns = {'index': codeSubjectTag})
    df = frame.createSubjectNameDataframeWithInfo(processDurationDataframe, subjectsNameDataframe)
    return df
