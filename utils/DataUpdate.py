# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt
import pandas as pd

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData(connection):
    verifyDatabase(connection)
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    events = getter.getEvents()
    courtHearingsEventsType = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    numEventTag = 'numEvento'
    numProcessTag = 'numProcesso'
    eventTag = 'evento'
    durationTag = 'durata'
    judgeTag = 'giudice'
    dateTag = 'data'
    stateTag = 'stato'
    phaseTag = 'fase'
    subjectTag = 'materia'
    sectionTag = 'sezione'
    finishedTag = 'finito'
    stateSequenceTag = 'sequenza'
    phaseSequenceTag = 'fasi'
    eventSequenceTag = 'eventi'
    endDateTag = 'endData'
    endIdTag = 'endId'
    countTag = 'conteggio'
    endPhase = '4'
    end = True
    updateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    processEvents = getProcessEvents(events, endPhase, end)
    [eventsSequences, phasesSequences, statesSequences] = updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag, endDateTag, endIdTag, countTag)
    updateProcessDurationDataframe(processEvents, eventsSequences, phasesSequences, statesSequences, numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag)

# update events dataframe.
def updateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    updateAllEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updateImportantEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updateCourtHearingEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updateStateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updatePhaseEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)

# update all events dataframe.
def updateAllEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    allEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateImportantEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    importantEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    try:
        importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
        importantEventsDataframe = importantEventsDataframe[importantEventsDataframe[eventTag].isin(importantEvents)]
    except:
        pass
    importantEventsDataframe = importantEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('importantEvents.json', importantEventsDataframe)

# update important events dataframe.
def updateCourtHearingEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    courtHearingEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    try:
        courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
        courtHearingEventsDataframe = courtHearingEventsDataframe[courtHearingEventsDataframe[eventTag].isin(courtHearingsEvents)]
    except:
        pass
    courtHearingEventsDataframe = courtHearingEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('courtHearingEvents.json', courtHearingEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    stateEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, stateTag], as_index = False).first()
    try:
        importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[stateTag].isin(importantStates)]
    except:
        pass
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    phaseEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# group events by process.
def getProcessEvents(events, endPhase, ending):
    allProcessEvents = []
    processId = events[0][1]
    processJudge = events[0][3]
    processSubject = events[0][7]
    processSection = events[0][8]
    finished = utilities.getAllProcessState()
    processEvents = [processId, processJudge, processSubject, processSection, finished[-1]]
    end = False
    with alive_bar(int(len(events))) as bar:
        for i in range(int(len(events))):
            if events[i][1] != processId or (end and ending):
                allProcessEvents.append(processEvents)
                processId = events[i][1]
                processJudge = events[i][3]
                processSubject = events[i][7]
                processSection = events[i][8]
                processEvents = [processId, processJudge, processSubject, processSection, finished[-1]]
                end = False
            else:
                if events[i][6] != '0':
                    processEvents[4] = finished[0]
                if events[i][6] == endPhase:
                    if events[i][5] == 'FINE': 
                        processEvents[4] = finished[1]
                    else:
                        processEvents[4] = finished[2]
                    end = True
                if events[i][3] != processJudge:
                    processEvents[1] = events[i][3]
                    processJudge = events[i][3]
                processEvents.append(events[i])
            bar()
    return allProcessEvents

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag, endDateTag, endIdTag, countTag):
    [eventsDuration, eventsSequences, phasesDuration, phasesSequences, statesDuration, statesSequences, courtHearingsDuration] = calcTypeDuration(processEvents, courtHearingsEventsType, endPhase)
    eventsDurationDataframe = frame.createTypeDurationsDataFrame(eventsDuration, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag,  endDateTag, endIdTag)
    eventsDurationDataframe = frame.keepOnlyRelevant(eventsDurationDataframe, 0.005, eventTag, countTag)
    phasesDurationDataframe = frame.createTypeDurationsDataFrame(phasesDuration, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag,  endDateTag, endIdTag)
    statesDurationDataframe = frame.createTypeDurationsDataFrame(statesDuration, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag,  endDateTag, endIdTag)
    courtHearingsDurationDataframe = frame.createTypeDurationsDataFrame(courtHearingsDuration, numEventTag, numProcessTag, eventTag, durationTag, dateTag, judgeTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag, endDateTag, endIdTag)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)
    cache.updateCache('phasesDuration.json', phasesDurationDataframe)
    cache.updateCache('statesDuration.json', statesDurationDataframe)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    return [eventsSequences, phasesSequences, statesSequences]

# calc types durations.
def calcTypeDuration(processEvents, courtHearingsEventsType, endPhase):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    eventsSequences = []
    phasesSequences = []
    statesSequences = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            [processEventsDuration, eventsSequence] = getEventInfo(processEvents[i], endPhase)
            [processPhasesDuration, phasesSequence] = getPhaseInfo(processEvents[i], endPhase)
            [processStateDuration, statesSequence] = getStateInfo(processEvents[i], endPhase)
            courtHearingDuration = getCourtHearingDuration(processEvents[i], courtHearingsEventsType)
            eventsDuration.extend(processEventsDuration)
            phasesDuration.extend(processPhasesDuration)
            statesDuration.extend(processStateDuration)
            courtHearingsDuration.extend(courtHearingDuration)
            eventsSequences.extend([eventsSequence])
            phasesSequences.extend([phasesSequence])
            statesSequences.extend([statesSequence])
            bar()
    return [eventsDuration, eventsSequences, phasesDuration, phasesSequences, statesDuration, statesSequences, courtHearingsDuration]

# return events duration.
def getEventInfo(events, endPhase):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return [[], []]
    events = events[5:]
    eventsDuration = []
    eventsSequence = []
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(next[4], '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        eventsDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, next[4], next[0]])
        if curr[2] != next[2]:
            eventsSequence.append(curr[2])
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
    if curr[6] == endPhase:
        duration = 0
        eventsDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, curr[4], curr[0]])
    if len(eventsSequence) == 0 or curr[2] != eventsSequence[-1]:
        eventsSequence.append(curr[2])
    if len(eventsDuration) == 1:
        eventsDuration = [eventsDuration]
    return [eventsDuration, eventsSequence]

# return phases duration.
def getPhaseInfo(events, endPhase):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return [[], []]
    events = events[5:]
    phasesDuration = []
    phasesSequence = []
    startPhase = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[6] != next[6]:
            endPhase = curr
            startDateDt = dt.datetime.strptime(startPhase[4], '%Y-%m-%d %H:%M:%S')
            endDateDt = dt.datetime.strptime(endPhase[4], '%Y-%m-%d %H:%M:%S')
            duration = (endDateDt - startDateDt).days
            phasesDuration.append([startPhase[0], processId, startPhase[2], duration, startPhase[4], startPhase[3], startPhase[5], startPhase[6], subject, section, finished, endPhase[4], endPhase[0]])
            phasesSequence.append(curr[6])
            startPhase = next
    curr = events[-1]
    if curr[6] == endPhase:
        duration = 0
        phasesDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, curr[4], curr[0]])
    if len(phasesSequence) == 0 or curr[6] != phasesSequence[-1]:
        phasesSequence.append(curr[6])
    if len(phasesDuration) == 1:
        phasesDuration = [phasesDuration]
    return [phasesDuration, phasesSequence]

# return states duration.
def getStateInfo(events, endPhase):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return [[], []]
    events = events[5:]
    statesDuration = []
    statesSequence = []
    startState = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[5] != next[5]:
            endState = curr
            startDateDt = dt.datetime.strptime(startState[4], '%Y-%m-%d %H:%M:%S')
            endDateDt = dt.datetime.strptime(endState[4], '%Y-%m-%d %H:%M:%S')
            duration = (endDateDt - startDateDt).days
            statesDuration.append([startState[0], processId, startState[2], duration, startState[4], startState[3], startState[5], startState[6], subject, section, finished, endState[4], endState[0]])
            statesSequence.append(curr[5])
            startState = next
    curr = events[-1]
    if curr[6] == endPhase:
        duration = 0
        statesDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, curr[4], curr[0]])
    if len(statesSequence) == 0 or curr[5] != statesSequence[-1]:
        statesSequence.append(curr[5])
    if len(statesDuration) == 1:
        statesDuration = [statesDuration]
    return [statesDuration, statesSequence]

# return court hearing duration.
def getCourtHearingDuration(events, courtHearingTypes):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return [[]]
    events = events[5:]
    courtHearingsDuration = []
    courtHearing = False
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[2] in courtHearingTypes and not courtHearing:
            startCourtHearing = curr
            courtHearing = True
        if next[2] not in courtHearingTypes and courtHearing:
            endCourtHearing = curr
            courtHearing = False
            startDateDt = dt.datetime.strptime(startCourtHearing[4], '%Y-%m-%d %H:%M:%S')
            endDateDt = dt.datetime.strptime(endCourtHearing[4], '%Y-%m-%d %H:%M:%S')
            duration = (endDateDt - startDateDt).days
            courtHearingsDuration.append([startCourtHearing[0], processId, startCourtHearing[2], duration, startCourtHearing[4], startCourtHearing[3], startCourtHearing[5], startCourtHearing[6], subject, section, finished, endCourtHearing[4], endCourtHearing[0]])
    curr = events[-1]
    if curr[2] in courtHearingTypes:
        if not courtHearing:
            startCourtHearing = curr
        endCourtHearing = curr
        startDateDt = dt.datetime.strptime(startCourtHearing[4], '%Y-%m-%d %H:%M:%S')
        endDateDt = dt.datetime.strptime(endCourtHearing[4], '%Y-%m-%d %H:%M:%S')
        duration = (endDateDt - startDateDt).days
        courtHearingsDuration.append([startCourtHearing[0], processId, startCourtHearing[2], duration, startCourtHearing[4], startCourtHearing[3], startCourtHearing[5], startCourtHearing[6], subject, section, finished, endCourtHearing[4], endCourtHearing[0]])
    if len(courtHearingsDuration) == 1:
        courtHearingsDuration = [courtHearingsDuration]
    return courtHearingsDuration

# update process duration dataframe.
def updateProcessDurationDataframe(processEvents, eventSequence, phaseSequence, stateSequence, numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag):
    processDuration = calcProcessDuration(processEvents, eventSequence, phaseSequence, stateSequence)
    processDurationDataframe = frame.createProcessDurationsDataFrame(processDuration, numProcessTag, durationTag, dateTag, numEventTag, judgeTag, subjectTag, sectionTag, finishedTag, stateSequenceTag, phaseSequenceTag, eventSequenceTag, endDateTag, endIdTag)
    cache.updateCache('processesDuration.json', processDurationDataframe)

# calc types durations.
def calcProcessDuration(processEvents, eventSequence, phaseSequence, stateSequence):
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processDuration = getProcessDuration(processEvents[i], eventSequence[i], phaseSequence[i], stateSequence[i])
            processesDuration.append(processDuration)
            bar()
    return processesDuration

# return events duration.
def getProcessDuration(events, eventSequence, phaseSequence, stateSequence):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return ()
    events = events[5:]
    start = events[0]
    end = events[-1]
    startDateDt = dt.datetime.strptime(start[4], '%Y-%m-%d %H:%M:%S')
    endDateDt = dt.datetime.strptime(end[4], '%Y-%m-%d %H:%M:%S')
    duration = (endDateDt - startDateDt).days
    return (processId, duration, start[4], start[0], judge, subject, section, finished, stateSequence, phaseSequence, eventSequence, end[4], end[0])

    eventsDuration = []
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(next[4], '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        nextDate = next[4]
        nextId = next[0]
        eventsDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, nextDate, nextId])
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
    if curr[6] == endPhase:
        duration = 0
        nextDate = curr[4]
        nextId = curr[0]
        eventsDuration.append((curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, nextDate, nextId))
    return eventsDuration

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    try:
        eventsName = file.getDataFromTextFile('preferences/eventsName.txt')
    except:
        raise Exception("\n'eventsName.txt' file is not present or is called differently than 'eventsName.txt")
    try:
        subjectsName = file.getDataFromTextFile('preferences/subjectsName.txt')
    except:
        raise Exception("\n'subjectsName.txt' file is not present or is called differently than 'subjectsName.txt")
    try:
        statesName = file.getDataFromTextFile('preferences/statesName.txt')
    except:
        raise Exception("\n'statesName.txt' file is not present or is called differently than 'statesName.txt")
    try:
        judgesName = file.getDataFromTextFile('preferences/judgesName.txt')
    except:
        raise Exception("\n'judgesName.txt' file is not present or is called differently than 'judgesName.txt")
    if not connect.doesATableExist(connection, "eventi"):
        raise Exception("\n'eventi' table is not present or is called differently than 'eventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "eventi", ['numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale'], ['BIGINT', 'BIGINT', 'VARCHAR(4)', 'TEXT', 'DATETIME', 'VARCHAR(5)', 'VARCHAR(5)']):
        raise Exception("\n'eventi' table does not have all requested columns. The requested columns are: 'numEvento'(BIGINT), 'numProcesso'(BIGINT), 'codice'(VARCHAR(4)), 'giudice'(TEXT), 'data'(DATETIME), 'statoiniziale'(VARCHAR(5)), 'statofinale'VARCHAR(5))")
    if not connect.doesATableExist(connection, "processi"):
        raise Exception("\n'processi' table is not present or is called differently than 'processi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "processi", ['numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione'], ['BIGINT', 'DATETIME', 'TEXT', 'VARCHAR(10)', 'VARCHAR(5)']):
        raise Exception("\n'processi' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'dataInizio'(DATETIME), 'giudice'(TEXT), 'materia'(VARCHAR(10)), 'sezione'(VARCHAR(5))")
    if not connect.doesATableExist(connection, "eventinome"):
        connect.createTable(connection, 'eventinome', ['codice', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(10)', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    else:
        if not connect.doesATableHaveColumns(connection, "eventinome", ['codice', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(10)', 'TEXT', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'eventinome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'etichetta'(TEXT), 'abbreviazione'(TEXT), 'fase'(VARCHAR(5))")
        eventsNameInfo = compareData(eventsName, connection, "SELECT * FROM eventinome ORDER BY codice")
        connect.updateTable(connection, 'eventinome', eventsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "materienome"):
        connect.createTable(connection, 'materienome', ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT'], [0], [])
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    else:
        if not connect.doesATableHaveColumns(connection, "materienome", ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT']):
            raise Exception("\n'materienome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'descrizione'(TEXT), 'rituale'(VARCHAR(4)), 'etichetta'(TEXT)")
        subjectsNameInfo = compareData(subjectsName, connection, "SELECT * FROM materienome ORDER BY codice")
        connect.updateTable(connection, 'materienome', subjectsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "statinome"):
        connect.createTable(connection, 'statinome', ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    else:
        if not connect.doesATableHaveColumns(connection, "statinome", ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'statinome' table does not have all requested columns. The requested columns are: 'stato'(VARCHAR(5)), 'etichetta'(TEXT), 'abbreviazione'(TEXT), 'fase'(VARCHAR(5))")
        statesNameInfo = compareData(statesName, connection, "SELECT * FROM statinome ORDER BY stato")
        connect.updateTable(connection, 'statinome', statesNameInfo, 'stato') 
    if not connect.doesATableExist(connection, "giudicinome"):
        connect.createTable(connection, 'giudicinome', ['giudice', 'alias'], ['VARCHAR(100)', 'TEXT'], [0], [])
        connect.insertIntoDatabase(connection, 'giudicinome', judgesName)
    else:
        if not connect.doesATableHaveColumns(connection, "giudicinome", ['giudice', 'alias'], ['VARCHAR(100)', 'TEXT']):
            raise Exception("\n'giudicinome' table does not have all requested columns. The requested columns are: 'giudice'(VARCHAR(100)), 'alias'(TEXT)")
        judgesNameInfo = compareData(judgesName, connection, "SELECT * FROM giudicinome ORDER BY giudice")
        connect.updateTable(connection, 'giudicinome', judgesNameInfo, 'giudice')    

# compare data with database data and return info about what has to be eliminated from or added to database.
def compareData(data, connection, query):
    databaseData = connect.getDataFromDatabase(connection, query)
    i = 0
    j = 0
    dataInfo = [[], []]
    data.sort(key = lambda a: a[0])
    databaseData.sort(key = lambda a: a[0])
    while i < len(data) and j < len(databaseData):
        if data[i][0] == databaseData[j][0]:
            if data[i] != databaseData[j]:
                dataInfo[0].append(data[i])
                dataInfo[1].append(data[i][0])
            i = i + 1
            j = j + 1
        elif data[i][0] > databaseData[j][0]:
            dataInfo[1].append(databaseData[j][0])
            j = j + 1
        else:
            dataInfo[0].append(data[i])
            i = i + 1
    while i < len(data):
        dataInfo[0].append(data[i])
        i = i + 1
    while j < len(databaseData):
        dataInfo[1].append(databaseData[j][0])
        j = j + 1
    return dataInfo
