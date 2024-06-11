# this file handles data getters.

import pandas as pd

import Cache as cache
import utils.database.DatabaseConnection as connect
import utils.DataUpdate as update
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.utilities.Utilities as utilities

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
endPhaseQuery = "SELECT FKFASEPROCESSO FROM tipostato WHERE CCODST = 'DF'"
eventsQuery = "SELECT e.numEvento, e.numProcesso, e.codice, te.CDESCR, e.giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S'), DATE_FORMAT((SELECT MIN(data) FROM eventi AS ev WHERE e.numProcesso = ev.numProcesso), '%Y-%m-%d %H:%i:%S'), e.statofinale, ts.CDESCR, ts.FKFASEPROCESSO, p.codiceMateria, p.materia, p.sezione FROM eventi AS e JOIN (SELECT p.numProcesso AS numProcesso, p.materia AS codiceMateria, tm.DESCCOMPLETA AS materia, p.sezione AS sezione FROM processi AS p JOIN tipomaterie AS tm ON p.materia = tm.codice) AS p ON e.numProcesso = p.numProcesso JOIN tipoeventi AS te ON e.codice = te.CCDOEV JOIN tipostato AS ts ON e.statofinale = ts.CCODST ORDER BY numProcesso, data, numEvento"
eventsInfoQuery = "SELECT CCDOEV, CDESCR FROM tipoeventi"
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
stallStatesQuery = "SELECT CCODST FROM tipostato WHERE FKFASEPROCESSO IS NULL"
statesInfoQuery = "SELECT CCODST, CDESCR, FKFASEPROCESSO, IFNULL(CAST(FKFASEPROCESSO AS SIGNED), '-') FROM tipostato"
subjectsInfoQuery = "SELECT codice, DESCCOMPLETA, rituale FROM tipomaterie"

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
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    processDateTag = utilities.getTagName("processDateTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    events = connect.getDataFromDatabase(connection, eventsQuery)
    keys = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag]
    dictEvents = utilities.fromListOfTuplesToListOfDicts(events, keys)
    return dictEvents

# get all events dataframe.
def getEventsDataframe():
    eventsDataframe = cache.getDataframe('events.json')
    if eventsDataframe is None:
        update.restartData()
        eventsDataframe = cache.getDataframe('events.json')
    return eventsDataframe

# get events info.
def getEventsInfo(codeEventTag, eventTag):
    eventsInfoDataframe = cache.getDataframe('eventsInfo.json')
    if eventsInfoDataframe is None:
        eventsInfo = connect.getDataFromDatabase(connection, eventsInfoQuery)
        eventsInfoDataframe = frame.createEventsInfoDataFrame(eventsInfo, codeEventTag, eventTag)
        cache.updateCache('eventsInfo.json', eventsInfoDataframe)
    return eventsInfoDataframe

# get states info.
def getStatesInfo(codeStateTag, phaseTag, phaseDBTag, stateTag):
    statesInfoDataframe = cache.getDataframe('statesInfo.json')
    if statesInfoDataframe is None:
        statesInfo = connect.getDataFromDatabase(connection, statesInfoQuery)
        statesInfoDataframe = frame.createStatesInfoDataFrame(statesInfo, codeStateTag, phaseTag, phaseDBTag, stateTag)
        cache.updateCache('statesInfo.json', statesInfoDataframe)
    return statesInfoDataframe

# get subjects info.
def getSubjectsInfo(codeSubjectTag, ritualTag, subjectTag):
    subjectsInfoDataframe = cache.getDataframe('subjectsInfo.json')
    if subjectsInfoDataframe is None:
        subjectsInfo = connect.getDataFromDatabase(connection, subjectsInfoQuery)
        subjectsInfoDataframe = frame.createSubjectsInfoDataFrame(subjectsInfo, codeSubjectTag, ritualTag, subjectTag)
        cache.updateCache('subjectsInfo.json', subjectsInfoDataframe)
    return subjectsInfoDataframe

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
    phaseTag = utilities.getTagName("phaseTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    stateTag = utilities.getTagName("codeStateTag")
    statesNameDataframe = getStatesInfo(codeStateTag, phaseTag, phaseDBTag, stateTag)
    stateDurationDataframe = getStatesDuration()  
    df = frame.createStateNameDataframeWithInfo(stateDurationDataframe, statesNameDataframe) 
    return df

# get events name dataframe.
def getEventNamesDataframe():
    codeEventTag = utilities.getTagName("codeEventTag")
    eventTag = utilities.getTagName("eventTag")
    eventNamesDataframe = getEventsInfo(codeEventTag, eventTag)
    eventDurationDataframe = getEventsDuration()
    df = frame.createEventNameDataframeWithInfo(eventDurationDataframe, eventNamesDataframe)
    return df

# get subject name dataframe.
def getSubjectNamesDataframe():
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    ritualTag = utilities.getTagName("ritualTag")
    subjectTag = utilities.getTagName("subjectTag")
    subjectNamesDataframe = getSubjectsInfo(codeSubjectTag, ritualTag, subjectTag)
    processDurationDataframe = getProcessesDuration()
    df = frame.createSubjectNameDataframeWithInfo(processDurationDataframe, subjectNamesDataframe)
    return df
