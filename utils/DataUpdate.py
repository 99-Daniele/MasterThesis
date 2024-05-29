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
    exit()
    events = getter.getEvents()
    courtHearingsEventsType = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    endPhase = getter.getEndPhase()
    stallPhase = getter.getStallPhase()
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    judgeTag = utilities.getTagName("judgeTag")
    eventTag = utilities.getTagName("eventTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    end = True
    updateEventsDataframe(events, endPhase, codeEventTag, dateTag, eventTag, numEventTag, numProcessTag, phaseTag, stateTag)
    processEvents = getProcessEvents(events, stallPhase, endPhase, end, codeSubjectTag, judgeTag, numProcessTag, phaseTag, sectionTag, subjectTag)
    [eventsSequences, phasesSequences, statesSequences] = updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
    updateProcessDurationDataframe(processEvents, eventsSequences, phasesSequences, statesSequences, dateTag, numEventTag)
    print(str(time.time() - start) + " seconds")

# update events dataframe.
def updateEventsDataframe(events, endPhase, codeEventTag, dateTag, eventTag, numEventTag, numProcessTag, phaseTag, stateTag):
    updateAllEventsDataframe(events, endPhase, codeEventTag, eventTag, phaseTag)
    updateImportantEventsDataframe(events, endPhase, codeEventTag, eventTag, phaseTag)
    updateCourtHearingEventsDataframe(events, endPhase, eventTag)
    updateStateEventsDataframe(events, endPhase, dateTag, numEventTag, numProcessTag, stateTag)
    updatePhaseEventsDataframe(events, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)

# update all events dataframe.
def updateAllEventsDataframe(events, endPhase, codeEventTag, eventTag, phaseTag):
    allEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    #allEventsDataframe = utilities.changePhaseDataframe(allEventsDataframe, 'preferences/eventsName.txt', [codeEventTag, eventTag, phaseTag], codeEventTag, eventTag)
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateImportantEventsDataframe(events, endPhase, codeEventTag, eventTag, phaseTag):
    importantEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    try:
        importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
        importantEventsDataframe = importantEventsDataframe[importantEventsDataframe[eventTag].isin(importantEvents)]
    except:
        pass
    #importantEventsDataframe = utilities.changePhaseDataframe(importantEventsDataframe, 'preferences/eventsName.txt', [codeEventTag, eventTag, phaseTag], codeEventTag, eventTag)
    cache.updateCache('importantEvents.json', importantEventsDataframe)

# update important events dataframe.
def updateCourtHearingEventsDataframe(events, endPhase, eventTag):
    courtHearingEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    try:
        courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
        courtHearingEventsDataframe = courtHearingEventsDataframe[courtHearingEventsDataframe[eventTag].isin(courtHearingsEvents)]
    except:
        pass
    cache.updateCache('courtHearingEvents.json', courtHearingEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(events, endPhase, dateTag, numEventTag, numProcessTag, stateTag):
    stateEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, stateTag], as_index = False).first()
    try:
        importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[stateTag].isin(importantStates)]
    except:
        pass
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(events, endPhase, dateTag, numEventTag, numProcessTag, phaseTag):
    phaseEventsDataframe = frame.createEventsDataFrame(events, endPhase)
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# group events by process.
def getProcessEvents(events, stallPhase, endPhase, ending, codeSubjectTag, judgeTag, numProcessTag, phaseTag, sectionTag, subjectTag):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    allProcessEvents = []
    processId = events[0][numProcessTag]
    processJudge = events[0][judgeTag]
    processCodeSubject = events[0][codeSubjectTag]
    processSubject = events[0][subjectTag]
    processSection = events[0][sectionTag]
    processEvents = [processId, processJudge, processCodeSubject, processSubject, processSection, utilities.getProcessState('unfinished')]
    end = False
    continuative = False
    i = 0
    with alive_bar(int(len(events))) as bar:
        while i < int(len(events)):
            if events[i][numProcessTag] != processId or (end and ending):
                allProcessEvents.append(processEvents)
                if events[i][numProcessTag] == processId:
                    while i < len(events) - 1 and events[i][numProcessTag] == processId:
                        bar()
                        i += 1
                processId = events[i][numProcessTag]
                processJudge = events[i][judgeTag]
                processCodeSubject = events[i][codeSubjectTag]
                processSubject = events[0][subjectTag]
                processSection = events[i][sectionTag]
                processEvents = [processId, processJudge, processCodeSubject, processSubject, processSection, utilities.getProcessState('unfinished')]
                end = False
                continuative = False
            else:
                if events[i][phaseTag] == stallPhase and not continuative:
                    processEvents[5] = utilities.getProcessState('continuatived')
                    continuative = True
                if events[i][phaseTag] == endPhase and not continuative: 
                    processEvents[5] = utilities.getProcessState('finished')
                    end = True
                if events[i][judgeTag] != processJudge:
                    processJudge = events[i][judgeTag]
                    processEvents[1] = processJudge
                if events[i][sectionTag] != processSection:
                    processSection = events[i][sectionTag]
                    processEvents[4] = processSection
                processEvents.append(events[i])
            bar()
            i += 1
    return allProcessEvents

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
    [eventsDuration, eventsSequences, phasesDuration, phasesSequences, statesDuration, statesSequences, courtHearingsDuration] = calcTypeDuration(processEvents, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
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
def calcTypeDuration(processEvents, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
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
            [processEventsDuration, eventsSequence] = getEventInfo(processEvents[i], endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
            [processPhasesDuration, phasesSequence] = getPhaseInfo(processEvents[i], endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
            [processStateDuration, statesSequence] = getStateInfo(processEvents[i], endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
            courtHearingDuration = getCourtHearingDuration(processEvents[i], courtHearingsEventsType, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag)
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
def getEventInfo(events, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
    processId = events[0]
    subjectCode = events[2]
    subjectTag = events[3]
    finished = events[5]
    if len(events) == 6:
        return [[], []]
    events = events[6:]
    eventsDuration = []
    eventsSequence = []
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currEventId = curr[numEventTag]
        nextEventId = next[numEventTag]
        currEventCode = curr[codeEventTag]
        currEventTag = curr[eventTag]
        nextEventTag = next[eventTag]
        currJudgeCode = curr[codeJudgeTag]
        currJudge = curr[judgeTag]
        currDate = curr[dateTag]
        nextDate = next[dateTag]
        currStateCode = curr[codeStateTag]
        currStateTag = curr[stateTag]
        currPhase = curr[phaseTag]
        currSection = curr[sectionTag]
        currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
        if currEventTag != nextEventTag:
            eventsSequence.append(currEventTag)
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[dateTag], '%Y-%m-%d %H:%M:%S')
    if curr[phaseTag] == endPhase:
        currEventId = curr[numEventTag]
        currEventCode = curr[codeEventTag]
        currEventTag = curr[eventTag]
        currJudgeCode = curr[codeJudgeTag]
        currJudge = curr[judgeTag]
        currDate = curr[dateTag]
        nextDate = curr[dateTag]
        currStateCode = curr[codeStateTag]
        currStateTag = curr[stateTag]
        currPhase = curr[phaseTag]
        currSection = curr[sectionTag]
        duration = 0
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, currDate, currEventId])
    if len(eventsSequence) == 0 or curr[eventTag] != eventsSequence[-1]:
        eventsSequence.append(curr[eventTag])
    return [eventsDuration, eventsSequence]

# return phases duration.
def getPhaseInfo(events, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
    processId = events[0]
    subjectCode = events[2]
    subjectTag = events[3]
    finished = events[5]
    if len(events) == 6:
        return [[], []]
    events = events[6:]
    phasesDuration = []
    phasesSequence = []
    startPhase = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[phaseTag] != next[phaseTag]:
            nextPhase = next
            currEventId = startPhase[numEventTag]
            nextEventId = nextPhase[numEventTag]
            currEventCode = startPhase[codeEventTag]
            currEventTag = startPhase[eventTag]
            currJudgeCode = startPhase[codeJudgeTag]
            currJudge = startPhase[judgeTag]
            currDate = startPhase[dateTag]
            nextDate = nextPhase[dateTag]
            currStateCode = startPhase[codeStateTag]
            currStateTag = startPhase[stateTag]
            currPhase = startPhase[phaseTag]
            currSection = startPhase[sectionTag]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            phasesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
            if currPhase != '-':
                phasesSequence.append(currPhase)
            startPhase = next
    curr = events[-1]
    if curr[phaseTag] == endPhase:
        currEventId = startPhase[numEventTag]
        nextEventId = curr[numEventTag]
        currEventCode = startPhase[codeEventTag]
        currEventTag = startPhase[eventTag]
        currJudgeCode = startPhase[codeJudgeTag]
        currJudge = startPhase[judgeTag]
        currDate = startPhase[dateTag]
        nextDate = curr[dateTag]
        currStateCode = startPhase[codeStateTag]
        currStateTag = startPhase[stateTag]
        currPhase = startPhase[phaseTag]
        currSection = startPhase[sectionTag]
        duration = 0
        phasesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
    if len(phasesSequence) == 0 or curr[phaseTag] != phasesSequence[-1]:
        phasesSequence.append(curr[phaseTag])
    return [phasesDuration, phasesSequence]

# return states duration.
def getStateInfo(events, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
    processId = events[0]
    subjectCode = events[2]
    subjectTag = events[3]
    finished = events[5]
    if len(events) == 6:
        return [[], []]
    events = events[6:]
    statesDuration = []
    statesSequence = []
    startState = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[codeStateTag] != next[codeStateTag]:
            nextState = next
            currEventId = startState[numEventTag]
            nextEventId = nextState[numEventTag]
            currEventCode = startState[codeEventTag]
            currEventTag = startState[eventTag]
            currJudgeCode = startState[codeJudgeTag]
            currJudge = startState[judgeTag]
            currDate = startState[dateTag]
            nextDate = nextState[dateTag]
            currStateCode = startState[codeStateTag]
            currStateTag = startState[stateTag]
            currPhase = startState[phaseTag]
            currSection = startState[sectionTag]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            statesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
            if curr[stateTag] != next[stateTag] and curr[phaseTag] != '-':
                statesSequence.append(curr[stateTag])
            startState = next
    curr = events[-1]
    if curr[phaseTag] == endPhase:
        currEventId = startState[numEventTag]
        nextEventId = curr[numEventTag]
        currEventCode = startState[codeEventTag]
        currEventTag = startState[eventTag]
        currJudgeCode = startState[codeJudgeTag]
        currJudge = startState[judgeTag]
        currDate = startState[dateTag]
        nextDate = curr[dateTag]
        currStateCode = startState[codeStateTag]
        currStateTag = startState[stateTag]
        currPhase = startState[phaseTag]
        currSection = startState[sectionTag]
        duration = 0
        statesDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
    if len(statesSequence) == 0 or curr[stateTag] != statesSequence[-1]:
        statesSequence.append(curr[stateTag])
    return [statesDuration, statesSequence]

# return court hearing duration.
def getCourtHearingDuration(events, courtHearingTypes, codeEventTag, codeJudgeTag, codeStateTag, dateTag, judgeTag, eventTag, numEventTag, phaseTag, sectionTag, stateTag):
    processId = events[0]
    subjectCode = events[2]
    subjectTag = events[3]
    finished = events[5]
    if len(events) == 6:
        return []
    events = events[6:]
    courtHearingsDuration = []
    courtHearing = False
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[eventTag] in courtHearingTypes and not courtHearing:
            startCourtHearing = curr
            courtHearing = True
        if next[eventTag] not in courtHearingTypes and courtHearing:
            endCourtHearing = curr
            courtHearing = False
            currEventId = startCourtHearing[numEventTag]
            nextEventId = endCourtHearing[numEventTag]
            currEventCode = startCourtHearing[codeEventTag]
            currEventTag = startCourtHearing[eventTag]
            currJudgeCode = startCourtHearing[codeJudgeTag]
            currJudge = startCourtHearing[judgeTag]
            currDate = startCourtHearing[dateTag]
            nextDate = endCourtHearing[dateTag]
            currStateCode = startCourtHearing[codeStateTag]
            currStateTag = startCourtHearing[stateTag]
            currPhase = startCourtHearing[phaseTag]
            currSection = startCourtHearing[sectionTag]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            courtHearingsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
    curr = events[-1]
    if curr[eventTag] in courtHearingTypes:
        if not courtHearing:
            startCourtHearing = curr
        endCourtHearing = curr
        currEventId = startCourtHearing[numEventTag]
        nextEventId = endCourtHearing[numEventTag]
        currEventCode = startCourtHearing[codeEventTag]
        currEventTag = startCourtHearing[eventTag]
        currJudgeCode = startCourtHearing[codeJudgeTag]
        currJudge = startCourtHearing[judgeTag]
        currDate = startCourtHearing[dateTag]
        nextDate = endCourtHearing[dateTag]
        currStateCode = startCourtHearing[codeStateTag]
        currStateTag = startCourtHearing[stateTag]
        currPhase = startCourtHearing[phaseTag]
        currSection = startCourtHearing[sectionTag]
        currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - currDateDt).days
        courtHearingsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, subjectCode, subjectTag, currSection, finished, nextDate, nextEventId])
    return courtHearingsDuration

# update process duration dataframe.
def updateProcessDurationDataframe(processEvents, eventSequence, phaseSequence, stateSequence, dateTag, numEventTag):
    processDuration = calcProcessDuration(processEvents, eventSequence, phaseSequence, stateSequence, dateTag, numEventTag)
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processDuration)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    cache.updateCache('processesDurationFiltered.json', processDurationDataframeFiltered)

# calc types durations.
def calcProcessDuration(processEvents, eventsSequence, phasesSequence, statesSequence, dateTag, numEventTag):
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][0]
            processDuration = getProcessDuration(processEvents[i], eventsSequence.get(processId), phasesSequence.get(processId), statesSequence.get(processId), dateTag, numEventTag)
            processesDuration.append(processDuration)
            bar()
    return processesDuration

# return events duration.
def getProcessDuration(events, eventSequence, phaseSequence, stateSequence, dateTag, numEventTag):
    processId = events[0]
    judge = events[1]
    subjectCode = events[2]
    subjectTag = events[3]
    section = events[4]
    finished = events[5]
    if len(events) == 6:
        return ()
    events = events[6:]
    start = events[0]
    end = events[-1]
    currEventId = start[numEventTag]
    nextEventId = end[numEventTag]
    currDate = start[dateTag]
    nextDate = end[dateTag]
    currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
    nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
    duration = (nextDateDt - currDateDt).days
    return (processId, duration, currDate, currEventId, judge, subjectCode, subjectTag, section, finished, utilities.fromListToString(stateSequence), utilities.fromListToString(phaseSequence), utilities.fromListToString(eventSequence), nextDate, nextEventId)

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    try:
        eventsName = file.getDataFromTextFile('preferences/eventsName.txt')
        eventsName = list(eventsName[0])
        eventsName = [tuple(f.values()) for f in eventsName]
    except:
        raise Exception("\n'eventsName.txt' file is not present or is called differently than 'eventsName.txt")
    try:
        subjectsName = file.getDataFromTextFile('preferences/subjectsName.txt')
        subjectsName = list(subjectsName[0])
        subjectsName = [tuple(f.values()) for f in subjectsName]
    except:
        raise Exception("\n'subjectsName.txt' file is not present or is called differently than 'subjectsName.txt")
    try:
        statesName = file.getDataFromTextFile('preferences/statesName.txt')
        statesName = list(statesName[0])
        statesName = [tuple(f.values()) for f in statesName]
    except:
        raise Exception("\n'statesName.txt' file is not present or is called differently than 'statesName.txt")
    try:
        judgesName = file.getDataFromTextFile('preferences/judgesName.txt')
        judgesName = list(judgesName[0])
        judgesName = [tuple(f.values()) for f in judgesName]
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
