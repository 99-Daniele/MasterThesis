# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData():
    import time
    start = time.time()
    connection = connect.getDatabaseConnection()
    verifyDatabase(connection)
    events = getter.getEvents()
    courtHearingsEventsType = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    endPhase = getter.getEndPhase()
    end = True
    updateEventsDataframe(events, endPhase)
    processEvents = getProcessEvents(events, endPhase, end)
    [eventsSequences, phasesSequences, statesSequences] = updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase)
    updateProcessDurationDataframe(processEvents, eventsSequences, phasesSequences, statesSequences)
    print(time.time() - start)

# group events by process.
def getProcessEvents(events, endPhase, ending):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    allProcessEvents = []
    processId = events[0][1]
    processJudge = events[0][5]
    processSubject = events[0][11]
    processSection = events[0][13]
    processEvents = [processId, processJudge, processSubject, processSection, utilities.getProcessState('unfinished')]
    end = False
    continuative = False
    i = 0
    with alive_bar(int(len(events))) as bar:
        while i < int(len(events)):
            if events[i][1] != processId or (end and ending):
                allProcessEvents.append(processEvents)
                if events[i][1] == processId:
                    while i < len(events) - 1 and events[i][1] == processId:
                        bar()
                        i += 1
                processId = events[i][1]
                processJudge = events[i][5]
                processSubject = events[i][11]
                processSection = events[i][13]
                processEvents = [processId, processJudge, processSubject, processSection, utilities.getProcessState('unfinished')]
                end = False
                continuative = False
            else:
                if events[i][10] == '0' and not continuative:
                    processEvents[4] = utilities.getProcessState('continuatived')
                    continuative = True
                if events[i][10] == endPhase and not continuative: 
                    processEvents[4] = utilities.getProcessState('finished')
                    end = True
                if events[i][5] != processJudge:
                    processJudge = events[i][5]
                    processEvents[1] = processJudge
                processEvents.append(events[i])
            bar()
            i += 1
    return allProcessEvents

# update events dataframe.
def updateEventsDataframe(events, endPhase):
    updateAllEventsDataframe(events, endPhase)
    updateImportantEventsDataframe(events, endPhase)
    updateCourtHearingEventsDataframe(events, endPhase)
    updateStateEventsDataframe(events, endPhase)
    updatePhaseEventsDataframe(events, endPhase)

# update all events dataframe.
def updateAllEventsDataframe(events, endPhase):
    dateTag = utilities.getTagName("dateTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    allEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateImportantEventsDataframe(events, endPhase):
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    importantEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    try:
        importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
        importantEventsDataframe = importantEventsDataframe[importantEventsDataframe[eventTag].isin(importantEvents)]
    except:
        pass
    importantEventsDataframe = importantEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('importantEvents.json', importantEventsDataframe)

# update important events dataframe.
def updateCourtHearingEventsDataframe(events, endPhase):
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    courtHearingEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    try:
        courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
        courtHearingEventsDataframe = courtHearingEventsDataframe[courtHearingEventsDataframe[eventTag].isin(courtHearingsEvents)]
    except:
        pass
    courtHearingEventsDataframe = courtHearingEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('courtHearingEvents.json', courtHearingEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(events, endPhase):
    dateTag = utilities.getTagName("dateTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    stateTag = utilities.getTagName("stateTag")
    stateEventsDataframe = frame.createEventsDataFrame(events, endPhase)
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
def updatePhaseEventsDataframe(events, endPhase):
    dateTag = utilities.getTagName("dateTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase):
    [eventsDuration, eventsSequences, phasesDuration, phasesSequences, statesDuration, statesSequences, courtHearingsDuration] = calcTypeDuration(processEvents, courtHearingsEventsType, endPhase)
    [eventsDurationDataframe, eventsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(eventsDuration)
    [phasesDurationDataframe, phasesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(phasesDuration)
    [statesDurationDataframe, statesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(statesDuration)
    [courtHearingsDurationDataframe, courtHearingsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(courtHearingsDuration)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)
    cache.updateCache('eventsDurationFiltered.json', eventsDurationDataframeFiltered)
    cache.updateCache('phasesDuration.json', phasesDurationDataframe)
    cache.updateCache('phasesDurationFiltered.json', phasesDurationDataframeFiltered)
    cache.updateCache('statesDuration.json', statesDurationDataframe)
    cache.updateCache('statesDurationFiltered.json', statesDurationDataframeFiltered)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    cache.updateCache('courtHearingsDurationFiltered.json', courtHearingsDurationDataframeFiltered)
    return [eventsSequences, phasesSequences, statesSequences]

# calc types durations.
def calcTypeDuration(processEvents, courtHearingsEventsType, endPhase):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    eventsSequences = {}
    phasesSequences = {}
    statesSequences = {}
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][0]
            [processEventsDuration, eventsSequence] = getEventInfo(processEvents[i], endPhase)
            [processPhasesDuration, phasesSequence] = getPhaseInfo(processEvents[i], endPhase)
            [processStateDuration, statesSequence] = getStateInfo(processEvents[i], endPhase)
            courtHearingDuration = getCourtHearingDuration(processEvents[i], courtHearingsEventsType)
            eventsDuration.extend(processEventsDuration)
            phasesDuration.extend(processPhasesDuration)
            statesDuration.extend(processStateDuration)
            courtHearingsDuration.extend(courtHearingDuration) 
            eventsSequences.update({processId: eventsSequence})
            phasesSequences.update({processId: phasesSequence})
            statesSequences.update({processId: statesSequence})
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
        currEventId = curr[0]
        nextEventId = next[0]
        currEventCode = curr[2]
        currEventTag = curr[3]
        nextEventTag = next[3]
        currJudgeCode = curr[4]
        currJudge = curr[5]
        currDate = curr[6]
        nextDate = next[6]
        currStateCode = curr[8]
        currStateTag = curr[9]
        currPhase = curr[10]
        currSubjectCode = curr[11]
        currSubjectTag = curr[12]
        currSection = curr[13]
        currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
        if currEventTag != nextEventTag:
            eventsSequence.append(currEventTag)
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[6], '%Y-%m-%d %H:%M:%S')
    if curr[10] == endPhase:
        currEventId = curr[0]
        currEventCode = curr[2]
        currEventTag = curr[3]
        currJudgeCode = curr[4]
        currJudge = curr[5]
        currDate = curr[6]
        nextDate = curr[6]
        currStateCode = curr[8]
        currStateTag = curr[9]
        currPhase = curr[10]
        currSubjectCode = curr[11]
        currSubjectTag = curr[12]
        currSection = curr[13]
        duration = 0
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, currDate, currEventId])
    if len(eventsSequence) == 0 or curr[3] != eventsSequence[-1]:
        eventsSequence.append(curr[3])
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
        if curr[10] != next[10]:
            lastPhase = curr
            currEventId = startPhase[0]
            nextEventId = lastPhase[0]
            currEventCode = startPhase[2]
            currEventTag = startPhase[3]
            currJudgeCode = startPhase[4]
            currJudge = startPhase[5]
            currDate = startPhase[6]
            nextDate = lastPhase[6]
            currStateCode = startPhase[8]
            currStateTag = startPhase[9]
            currPhase = startPhase[10]
            currSubjectCode = startPhase[11]
            currSubjectTag = startPhase[12]
            currSection = startPhase[13]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            phasesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
            if currPhase != '-':
                phasesSequence.append(currPhase)
            startPhase = next
    curr = events[-1]
    if curr[10] == endPhase:
        currEventId = startPhase[0]
        nextEventId = curr[0]
        currEventCode = startPhase[2]
        currEventTag = startPhase[3]
        currJudgeCode = startPhase[4]
        currJudge = startPhase[5]
        currDate = startPhase[6]
        nextDate = curr[6]
        currStateCode = startPhase[8]
        currStateTag = startPhase[9]
        currPhase = startPhase[10]
        currSubjectCode = startPhase[11]
        currSubjectTag = startPhase[12]
        currSection = startPhase[13]
        duration = 0
        phasesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
    if len(phasesSequence) == 0 or curr[10] != phasesSequence[-1]:
        phasesSequence.append(curr[10])
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
        if curr[8] != next[8]:
            endState = curr
            currEventId = startState[0]
            nextEventId = endState[0]
            currEventCode = startState[2]
            currEventTag = startState[3]
            currJudgeCode = startState[4]
            currJudge = startState[5]
            currDate = startState[6]
            nextDate = endState[6]
            currStateCode = startState[8]
            currStateTag = startState[9]
            currPhase = startState[10]
            currSubjectCode = startState[11]
            currSubjectTag = startState[12]
            currSection = startState[13]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            statesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
            if curr[9] != next[9] and curr[10] != '-':
                statesSequence.append(curr[9])
            startState = next
    curr = events[-1]
    if curr[10] == endPhase:
        currEventId = startState[0]
        nextEventId = curr[0]
        currEventCode = startState[2]
        currEventTag = startState[3]
        currJudgeCode = startState[4]
        currJudge = startState[5]
        currDate = startState[6]
        nextDate = curr[6]
        currStateCode = startState[8]
        currStateTag = startState[9]
        currPhase = startState[10]
        currSubjectCode = startState[11]
        currSubjectTag = startState[12]
        currSection = startState[13]
        duration = 0
        statesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
    if len(statesSequence) == 0 or curr[9] != statesSequence[-1]:
        statesSequence.append(curr[9])
    return [statesDuration, statesSequence]

# return court hearing duration.
def getCourtHearingDuration(events, courtHearingTypes):
    processId = events[0]
    judge = events[1]
    subject = events[2]
    section = events[3]
    finished = events[4]
    if len(events) == 5:
        return []
    events = events[5:]
    courtHearingsDuration = []
    courtHearing = False
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[3] in courtHearingTypes and not courtHearing:
            startCourtHearing = curr
            courtHearing = True
        if next[3] not in courtHearingTypes and courtHearing:
            endCourtHearing = curr
            courtHearing = False
            currEventId = startCourtHearing[0]
            nextEventId = endCourtHearing[0]
            currEventCode = startCourtHearing[2]
            currEventTag = startCourtHearing[3]
            currJudgeCode = startCourtHearing[4]
            currJudge = startCourtHearing[5]
            currDate = startCourtHearing[6]
            nextDate = endCourtHearing[6]
            currStateCode = startCourtHearing[7]
            currStateTag = startCourtHearing[8]
            currPhase = startCourtHearing[9]
            currSubjectCode = startCourtHearing[10]
            currSubjectTag = startCourtHearing[11]
            currSection = startCourtHearing[12]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            courtHearingsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
    curr = events[-1]
    if curr[3] in courtHearingTypes:
        if not courtHearing:
            startCourtHearing = curr
        endCourtHearing = curr
        currEventId = startCourtHearing[0]
        nextEventId = endCourtHearing[0]
        currEventCode = startCourtHearing[2]
        currEventTag = startCourtHearing[3]
        currJudgeCode = startCourtHearing[4]
        currJudge = startCourtHearing[5]
        currDate = startCourtHearing[6]
        nextDate = endCourtHearing[6]
        currStateCode = startCourtHearing[7]
        currStateTag = startCourtHearing[8]
        currPhase = startCourtHearing[9]
        currSubjectCode = startCourtHearing[10]
        currSubjectTag = startCourtHearing[11]
        currSection = startCourtHearing[12]
        currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        courtHearingsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, currSubjectCode, currSubjectTag, currSection, finished, nextDate, nextEventId])
    return courtHearingsDuration

# update process duration dataframe.
def updateProcessDurationDataframe(processEvents, eventSequence, phaseSequence, stateSequence):
    processDuration = calcProcessDuration(processEvents, eventSequence, phaseSequence, stateSequence)
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processDuration)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    cache.updateCache('processesDurationFiltered.json', processDurationDataframeFiltered)

# calc types durations.
def calcProcessDuration(processEvents, eventsSequence, phasesSequence, statesSequence):
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][0]
            processDuration = getProcessDuration(processEvents[i], eventsSequence.get(processId), phasesSequence.get(processId), statesSequence.get(processId))
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
    currEventId = start[0]
    nextEventId = end[0]
    currDate = start[6]
    nextDate = end[6]
    currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
    nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
    duration = (nextDateDt - currDateDt).days
    return (processId, duration, currDate, currEventId, judge, subject, section, finished, utilities.fromListToString(stateSequence), utilities.fromListToString(phaseSequence), utilities.fromListToString(eventSequence), nextDate, nextEventId)

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    try:
        eventsName = file.getDataFromTextFile('preferences/eventsName.txt')
        eventsName = list(eventsName[0])
    except:
        raise Exception("\n'eventsName.txt' file is not present or is called differently than 'eventsName.txt")
    try:
        subjectsName = file.getDataFromTextFile('preferences/subjectsName.txt')
        subjectsName = list(subjectsName[0])
    except:
        raise Exception("\n'subjectsName.txt' file is not present or is called differently than 'subjectsName.txt")
    try:
        statesName = file.getDataFromTextFile('preferences/statesName.txt')
        statesName = list(statesName[0])
    except:
        raise Exception("\n'statesName.txt' file is not present or is called differently than 'statesName.txt")
    try:
        judgesName = file.getDataFromTextFile('preferences/judgesName.txt')
        judgesName = list(judgesName[0])
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
        connect.createTable(connection, 'eventinome', ['codice', 'etichetta', 'fase'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(5)'], [0], [])
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    else:
        if not connect.doesATableHaveColumns(connection, "eventinome", ['codice', 'etichetta', 'fase'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'eventinome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'abbreviazione'(TEXT), 'fase'(VARCHAR(5))")
        connect.clearTable(connection, "eventinome")
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    if not connect.doesATableExist(connection, "materienome"):
        connect.createTable(connection, 'materienome', ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT'], [0], [])
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    else:
        if not connect.doesATableHaveColumns(connection, "materienome", ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT']):
            raise Exception("\n'materienome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'descrizione'(TEXT), 'rituale'(VARCHAR(4)), 'etichetta'(TEXT)")
        connect.clearTable(connection, "materienome")
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    if not connect.doesATableExist(connection, "statinome"):
        connect.createTable(connection, 'statinome', ['stato', 'etichetta', 'fase'], ['VARCHAR(5)', 'TEXT', 'VARCHAR(5)'], [0], [])
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    else:
        if not connect.doesATableHaveColumns(connection, "statinome", ['stato', 'etichetta', 'fase'], ['VARCHAR(5)', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'statinome' table does not have all requested columns. The requested columns are: 'stato'(VARCHAR(5)), 'etichetta'(TEXT), 'fase'(VARCHAR(5))")
        connect.clearTable(connection, "statinome")
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    if not connect.doesATableExist(connection, "giudicinome"):
        connect.createTable(connection, 'giudicinome', ['giudice', 'alias'], ['VARCHAR(50)', 'TEXT'], [0], [])
        connect.insertIntoDatabase(connection, 'giudicinome', judgesName)
    else:
        if not connect.doesATableHaveColumns(connection, "giudicinome", ['giudice', 'alias'], ['VARCHAR(50)', 'TEXT']):
            raise Exception("\n'giudicinome' table does not have all requested columns. The requested columns are: 'giudice'(VARCHAR(50)), 'alias'(TEXT)")
        connect.clearTable(connection, "giudicinome")
        connect.insertIntoDatabase(connection, 'giudicinome', judgesName)  
