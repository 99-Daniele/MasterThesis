# this file handles data getters.

import utils.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.DataUpdate as update
import utils.FileOperation as file
import utils.Utilities as utilities

# connection is user database connection.
connection = connect.getDatabaseConnection()

# queries to obtain data from database.
endPhaseQuery = "SELECT FKFASEPROCESSO FROM tipostato WHERE CCODST = 'DF'"
eventsQuery = "SELECT e.numEvento, e.numProcesso, e.codice, te.CDESCR, e.giudice, DATE_FORMAT(e.data,'%Y-%m-%d %H:%i:%S'), e.statofinale, ts.CDESCR, ts.FKFASEPROCESSO, p.codiceMateria, p.materia, p.sezione FROM eventi AS e JOIN (SELECT p.numProcesso AS numProcesso, p.materia AS codiceMateria, tm.DESCCOMPLETA AS materia, p.sezione AS sezione FROM processi AS p JOIN tipomaterie AS tm ON p.materia = tm.codice) AS p ON e.numProcesso = p.numProcesso JOIN tipoeventi AS te ON e.codice = te.CCDOEV JOIN tipostato AS ts ON e.statofinale = ts.CCODST ORDER BY numProcesso, data, numEvento"
eventsInfoQuery = "SELECT CCDOEV, CDESCR FROM tipoeventi"
minDateQuery = "SELECT DATE_FORMAT(MIN(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
maxDateQuery = "SELECT DATE_FORMAT(MAX(data),'%Y-%m-%d %H:%i:%S') FROM eventi"
stallStatesQuery = "SELECT CCODST FROM tipostato WHERE FKFASEPROCESSO IS NULL"
statesInfoQuery = "SELECT CCODST, CDESCR, FKFASEPROCESSO, IFNULL(CAST(FKFASEPROCESSO AS SIGNED), 0) FROM tipostato"
subjectsInfoQuery = "SELECT codice, DESCCOMPLETA, rituale FROM tipomaterie"

# get min date from all events of user database.
def getMinDate():
    minDate = connect.getDataFromDatabase(connection, minDateQuery)
    return minDate[0][0]

# get max date from all events of user database.
def getMaxDate():
    maxDate = connect.getDataFromDatabase(connection, maxDateQuery)
    return maxDate[0][0]

# get end phase.
def getEndPhase():
    endPhase = connect.getDataFromDatabase(connection, endPhaseQuery)
    return endPhase[0][0]

# get stall states.
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
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    events = connect.getDataFromDatabase(connection, eventsQuery)
    keys = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag]
    dictEvents = utilities.fromListOfTuplesToListOfDicts(events, keys)
    return dictEvents

# get all events dataframe.
def getEventsDataframe():
    eventsDataframe = cache.getDataframe('events.json')
    if eventsDataframe is None:
        update.restartData()
        eventsDataframe = cache.getDataframe('events.json')
    return eventsDataframe

# get events info dataframe.
def getEventsInfo():
    codeEventTag = utilities.getTagName("codeEventTag")
    eventTag = utilities.getTagName("eventTag")
    eventsInfoDataframe = cache.getDataframe('eventsInfo.json')
    if eventsInfoDataframe is None:
        eventsInfo = connect.getDataFromDatabase(connection, eventsInfoQuery)
        eventsInfoDataframe = frame.createEventsInfoDataFrame(eventsInfo, codeEventTag, eventTag)
        cache.updateCacheDataframe('eventsInfo.json', eventsInfoDataframe)
    return eventsInfoDataframe

# get states info dataframe.
def getStatesInfo():
    codeStateTag = utilities.getTagName("codeStateTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    stateTag = utilities.getTagName("stateTag")
    statesInfoDataframe = cache.getDataframe('statesInfo.json')
    if statesInfoDataframe is None:
        statesInfo = connect.getDataFromDatabase(connection, statesInfoQuery)
        statesInfoDataframe = frame.createStatesInfoDataFrame(statesInfo, codeStateTag, phaseTag, phaseDBTag, stateTag)
        cache.updateCacheDataframe('statesInfo.json', statesInfoDataframe)
    return statesInfoDataframe

# get subjects info dataframe.
def getSubjectsInfo():
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    ritualTag = utilities.getTagName("ritualTag") 
    subjectTag = utilities.getTagName("subjectTag")
    subjectsInfoDataframe = cache.getDataframe('subjectsInfo.json')
    if subjectsInfoDataframe is None:
        subjectsInfo = connect.getDataFromDatabase(connection, subjectsInfoQuery)
        subjectsInfoDataframe = frame.createSubjectsInfoDataFrame(subjectsInfo, codeSubjectTag, ritualTag, subjectTag)
        cache.updateCacheDataframe('subjectsInfo.json', subjectsInfoDataframe)
    subjectsInfoDataframe[codeSubjectTag] = subjectsInfoDataframe[codeSubjectTag].astype(str)
    return subjectsInfoDataframe

# get processes events.
def getProcessesEvents():
    processEvents = cache.getData('processesEvents.json')
    if processEvents is None:
        update.restartData()
        processEvents = cache.getData('processesEvents.json')
    return processEvents

# get processes info.
def getProcessesInfo():
    processEvents = cache.getDataframe('processesInfo.json')
    if processEvents is None:
        update.restartData()
        processEvents = cache.getDataframe('prrocessesInfo.json')
    return processEvents

# get predicted duration dataframe.
def getPredictedDurationDataframe():
    predictedDurationFataframe = cache.getDataframe('predictions.json')
    if predictedDurationFataframe is None:
        update.predictTest()
        predictedDurationFataframe = cache.getDataframe('predictions.json')
    return predictedDurationFataframe

# get unfinished processes duration.
def getUnfinishedProcessesDuration():
    unfinishedProcesses = cache.getData('unfinishedProcessesDurations.json')
    if unfinishedProcesses is None:
        update.predictDuration()
        unfinishedProcesses = cache.getData('unfinishedProcessesDurations.json')
    return unfinishedProcesses

# get all events dataframe from cache file.
def getAllEvents():
    allEventsDataframe = cache.getDataframe('allEvents.json')
    if allEventsDataframe is None:
        update.refreshData()
        allEventsDataframe = cache.getDataframe('allEvents.json')
    return allEventsDataframe

# get phases events dataframe from cache file.
def getPhaseEvents():
    phaseTag = utilities.getTagName("phaseTag")
    phaseEventsDataframe = cache.getDataframe('phaseEvents.json')
    if phaseEventsDataframe is None:
        update.refreshData()
        phaseEventsDataframe = cache.getDataframe('phaseEvents.json')
    phaseEventsDataframe[phaseTag] = phaseEventsDataframe[phaseTag].astype(str)
    return phaseEventsDataframe

# get states events dataframe from cache file.
def getStateEvents():
    stateEventsDataframe = cache.getDataframe('stateEvents.json')
    if stateEventsDataframe is None:
        update.refreshData()
        stateEventsDataframe = cache.getDataframe('stateEvents.json')
    print(stateEventsDataframe)
    exit()
    return stateEventsDataframe

# get processes duration dataframe from cache file.
def getProcessesDuration():
    processDurationDataframe = cache.getDataframe('processesDuration.json')
    if processDurationDataframe is None:
        update.refreshData()
        processDurationDataframe = cache.getDataframe('processesDuration.json')
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    processDurationDataframe[codeSubjectTag] = processDurationDataframe[codeSubjectTag].astype(str)
    return processDurationDataframe

# get processes duration dataframe from cache file filtered by important process types, sections and subjects.
def getProcessesDurationFiltered():
    processDurationDataframeFiltered = cache.getDataframe('processesDurationFiltered.json')
    if processDurationDataframeFiltered is None:
        update.refreshData()
        processDurationDataframeFiltered = cache.getDataframe('processesDurationFiltered.json')
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    processDurationDataframeFiltered[codeSubjectTag] = processDurationDataframeFiltered[codeSubjectTag].astype(str)
    return processDurationDataframeFiltered

# get states duration from cache file.
def getStatesDuration():
    phaseTag = utilities.getTagName('phaseTag') 
    stateDurationDataframe = cache.getDataframe('statesDuration.json')
    if stateDurationDataframe is None:
        update.refreshData()
        stateDurationDataframe = cache.getDataframe('statesDuration.json')
    stateDurationDataframe[phaseTag] = stateDurationDataframe[phaseTag].astype(str)
    return stateDurationDataframe

# get states duration from cache file filtered by important process types, sections and subjects.
def getStatesDurationFiltered():
    phaseTag = utilities.getTagName('phaseTag') 
    stateDurationDataframeFiltered = cache.getDataframe('statesDurationFiltered.json')
    if stateDurationDataframeFiltered is None:
        update.refreshData()
        stateDurationDataframeFiltered = cache.getDataframe('statesDurationFiltered.json')
    stateDurationDataframeFiltered[phaseTag] = stateDurationDataframeFiltered[phaseTag].astype(str)
    return stateDurationDataframeFiltered

# get phases duration from cache file.
def getPhasesDuration():
    phaseTag = utilities.getTagName('phaseTag') 
    phaseDurationDataframe = cache.getDataframe('phasesDuration.json')
    if phaseDurationDataframe is None:
        update.refreshData()
        phaseDurationDataframe = cache.getDataframe('phasesDuration.json')
    phaseDurationDataframe[phaseTag] = phaseDurationDataframe[phaseTag].astype(str)
    return phaseDurationDataframe

# get phases duration from cache file filtered by important process types, sections and subjects.
def getPhasesDurationFiltered():
    phaseTag = utilities.getTagName('phaseTag') 
    phaseDurationDataframeFiltered = cache.getDataframe('phasesDurationFiltered.json')
    if phaseDurationDataframeFiltered is None:
        update.refreshData()
        phaseDurationDataframeFiltered = cache.getDataframe('phasesDurationFiltered.json')
    phaseDurationDataframeFiltered[phaseTag] = phaseDurationDataframeFiltered[phaseTag].astype(str)
    return phaseDurationDataframeFiltered

# get events duration from cache file.
def getEventsDuration():
    phaseTag = utilities.getTagName("phaseTag")
    eventDurationDataframe = cache.getDataframe('eventsDuration.json')
    if eventDurationDataframe is None:
        update.refreshData()
        eventDurationDataframe = cache.getDataframe('eventsDuration.json')
    eventDurationDataframe[phaseTag] = eventDurationDataframe[phaseTag].astype(str)
    return eventDurationDataframe

# get events duration from cache file filtered by important process types, sections and subjects.
def getEventsDurationFiltered():
    phaseTag = utilities.getTagName("phaseTag")
    eventDurationDataframeFiltered = cache.getDataframe('eventsDurationFiltered.json')
    if eventDurationDataframeFiltered is None:
        update.refreshData()
        eventDurationDataframeFiltered = cache.getDataframe('eventsDurationFiltered.json')
    eventDurationDataframeFiltered[phaseTag] = eventDurationDataframeFiltered[phaseTag].astype(str)
    return eventDurationDataframeFiltered

# get states name dataframe.
def getStateNamesDataframe():
    durationTag = utilities.getTagName("durationTag")
    statesNameDataframe = getStatesInfo()
    stateDurationDataframe = getStatesDurationFiltered()  
    df = frame.createStateNameDataframeWithInfo(stateDurationDataframe, statesNameDataframe) 
    df[durationTag] = df[durationTag].apply(lambda x: float(str(x).replace(',', '')))
    return df

# get events name dataframe.
def getEventNamesDataframe():
    durationTag = utilities.getTagName("durationTag")
    eventNamesDataframe = getEventsInfo()
    eventDurationDataframe = getEventsDurationFiltered()
    df = frame.createEventNameDataframeWithInfo(eventDurationDataframe, eventNamesDataframe)
    df[durationTag] = df[durationTag].apply(lambda x: float(str(x).replace(',', '')))
    return df

# get subject name dataframe.
def getSubjectNamesDataframe():
    durationTag = utilities.getTagName("durationTag")
    subjectNamesDataframe = getSubjectsInfo()
    processDurationDataframe = getProcessesDuration()
    df = frame.createSubjectNameDataframeWithInfo(processDurationDataframe, subjectNamesDataframe)
    df[durationTag] = df[durationTag].apply(lambda x: float(str(x).replace(',', '')))
    return df

# get finished dataframe.
def getFinishedDataframe():
    durationTag = utilities.getTagName("durationTag")
    processDurationDataframe = getProcessesDuration()
    df = frame.creatFinishedDataframeWithInfo(processDurationDataframe)
    df[durationTag] = df[durationTag].apply(lambda x: float(str(x).replace(',', '')))
    return df

# get section dataframe.
def getSectionDataframe():
    durationTag = utilities.getTagName("durationTag")
    processDurationDataframe = getProcessesDuration()
    df = frame.creatSectionDataframeWithInfo(processDurationDataframe)
    df[durationTag] = df[durationTag].apply(lambda x: float(str(x).replace(',', '')))
    return df
