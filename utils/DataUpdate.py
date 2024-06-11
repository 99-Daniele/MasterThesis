# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt
import pandas as pd

import Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Prediction as prediction
import utils.utilities.Utilities as utilities

# restart current database data in case events or process table are changed.
def restartData():
    connection = connect.getDatabaseConnection()
    verifyDatabase(connection)
    file.removeFolder('cache')
    file.createFolder('cache')
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    endPhase = getter.getEndPhase()
    stallStates = getter.getStallStates()
    events = cache.getData('events.json')
    events = getter.getEvents()
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    countTag = utilities.getTagName("countTag")
    dateTag = utilities.getTagName("dateTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    eventDurationSequenceTag = utilities.getTagName("eventDurationSequenceTag")
    eventTag = utilities.getTagName("eventTag")
    eventsTag = utilities.getTagName("eventsTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    phaseDurationSequenceTag = utilities.getTagName("phaseDurationSequenceTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    processDateTag = utilities.getTagName("processDateTag")
    ritualTag = utilities.getTagName("ritualTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    stateDurationSequenceTag = utilities.getTagName("stateDurationSequenceTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    subjectTag = utilities.getTagName("subjectTag")
    getter.getEventsInfo(codeEventTag, eventTag)
    getter.getStatesInfo(codeStateTag, phaseTag, phaseDBTag, stateTag)
    getter.getSubjectsInfo(codeSubjectTag, ritualTag, subjectTag)
    eventsDataframe = frame.createBasicEventsDataFrame(events, dateTag, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, eventTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag)
    processesEvents, processInfo = getProcessEvents(events, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, eventDurationSequenceTag, eventTag, eventsTag, eventSequenceTag, finishedTag, numEventTag, numProcessTag, phaseDBTag, phaseDurationSequenceTag, phaseSequenceTag, processDateTag, sectionTag, stateTag, stateDurationSequenceTag, stateSequenceTag, subjectTag)
    #finishedProcesses = processInfo[processInfo[finishedTag] == utilities.getProcessState('finished')]
    #predictionError = prediction.predictDurationsWithoutLikenessTest(finishedProcesses, codeJudgeTag, codeSubjectTag, countTag, durationFinalTag, finishedTag, numProcessTag, sectionTag)
    #print('Prediction Error: ', predictionError)
    #exit()
    #unfinishedProcessesDurations = prediction.predictDurationsWithoutLikeness(processInfo, codeJudgeTag, codeSubjectTag, durationTag, durationFinalTag, finishedTag, numProcessTag, sectionTag)
    #file.writeOnJsonFile('cache/unfinishedProcessesDurations.json', unfinishedProcessesDurations)
    cache.updateCache('events.json', eventsDataframe)
    file.writeOnJsonFile('cache/processesEvents.json', processesEvents)
    refreshData()

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData():
    import time
    start = time.time()
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    durationTag = utilities.getTagName("durationTag")
    eventTag = utilities.getTagName("eventTag")
    eventsTag = utilities.getTagName("eventsTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    eventPhaseSequenceTag = utilities.getTagName("eventPhaseSequenceTag")
    nextDateTag = utilities.getTagName("nextDateTag")
    nextIdTag = utilities.getTagName("nextIdTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    processEvents = cache.getData('processesEvents.json')
    if processEvents is None:
        restartData()
        processEvents = cache.getData('processesEvents.json')
    eventsDataframe = getter.getEventsDataframe()
    statesInfoDataframe = getter.getStatesInfo(codeStateTag, phaseTag, phaseDBTag, stateTag)
    try:
        courtHearingsEventsType = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    except:
        courtHearingsEventsType = []
    statesInfo = statesInfoDataframe.set_index(codeStateTag).T.to_dict('dict')
    endPhase = frame.getPhaseOfState(statesInfo, "DF", phaseTag)
    processesDuration = updateTypeDurationDataframe(processEvents, statesInfo, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, eventTag, eventsTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    updateProcessDurationDataframe(processesDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag)
    updateEventsDataframe(eventsDataframe, statesInfoDataframe, courtHearingsEventsType, endPhase, codeStateTag, codeEventTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag)
    print(str(time.time() - start) + " seconds")

# group events by process.
def getProcessEvents(events, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, eventDurationSequenceTag, eventTag, eventsTag, eventSequenceTag, finishedTag, numEventTag, numProcessTag, phaseDBTag, phaseDurationSequenceTag, phaseSequenceTag, processDateTag, sectionTag, stateTag, stateDurationSequenceTag, stateSequenceTag, subjectTag):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    allProcessEvents = []
    allProcessDict = []
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag])
    eventsColumns = frame.getGroupBy(df, codeEventTag)
    statesColumns = frame.getGroupBy(df, codeStateTag)
    phasesColumns = frame.getGroupBy(df, phaseDBTag)
    eventsColumns = [eventTag + ": " + e for e in eventsColumns]
    statesColumns = [stateTag + ": " + s for s in statesColumns]
    phasesColumns = [phaseDBTag + ": " + p for p in phasesColumns]
    dfColumns = [numProcessTag, dateTag, codeJudgeTag, codeSubjectTag, sectionTag, finishedTag, durationTag, durationFinalTag, countTag] + eventsColumns + statesColumns + phasesColumns
    processId = events[0][numProcessTag]
    processCodeJudge = events[0][codeJudgeTag]
    processSubjectCode = events[0][codeSubjectTag]
    processSubject = events[0][subjectTag]
    processSection = events[0][sectionTag]
    processStartDate = events[0][dateTag]
    processStartDateDt = dt.datetime.strptime(processStartDate, '%Y-%m-%d %H:%M:%S')
    processFinished = utilities.getProcessState('unfinished')
    processEventSequence = []
    processPhaseSequence = []
    processStateSequence = []
    eventDurationSequence = []
    phaseDurationSequence = []
    stateDurationSequence = []
    processEventSequenceComplete = []
    processPhaseSequenceComplete = []
    processStateSequenceComplete = []
    durationSequenceComplete = []
    processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processSubjectCode, subjectTag: processSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
    end = False
    continuative = False
    i = 0
    with alive_bar(int(len(events))) as bar:
        while i < int(len(events)):
            if events[i][numProcessTag] != processId or end:
                allProcessEvents.append(processEvents)
                if len(durationSequenceComplete) > 0:
                    processDict = dict.fromkeys(dfColumns)
                    processDict = {x: 0 for x in processDict}
                    processDict.update({numProcessTag: processId})
                    processDict.update({dateTag: utilities.distanceAtToday(processStartDateDt)})
                    processDict.update({codeJudgeTag: processCodeJudge})
                    processDict.update({codeSubjectTag: processSubjectCode})
                    processDict.update({sectionTag: processSection})
                    processDict.update({finishedTag: processFinished})
                    processDict.update({durationFinalTag: durationSequenceComplete[-1]})
                    for j in range(len(processEventSequenceComplete)):
                        codeEvent = processEventSequenceComplete[j]
                        phase = processPhaseSequenceComplete[j]
                        if phase == None:
                            phase = '0.0'
                        codeState = processStateSequenceComplete[j]
                        duration = durationSequenceComplete[j]
                        eventCount = processDict.get(eventTag + ": " + codeEvent)
                        phaseCount = processDict.get(phaseDBTag + ": " + phase)
                        stateCount = processDict.get(stateTag + ": " + codeState)
                        processDict.update({eventTag + ": " + codeEvent: eventCount + 1})
                        processDict.update({phaseDBTag + ": " + phase: phaseCount + 1})
                        processDict.update({stateTag + ": " + codeState: stateCount + 1})
                        processDict.update({countTag: j})
                        processDict.update({durationTag: duration})
                        if processFinished == utilities.getProcessState('finished'):
                            allProcessDict.append(processDict.copy())
                    if processFinished == utilities.getProcessState('unfinished'):
                        allProcessDict.append(processDict.copy())
                if events[i][numProcessTag] == processId:
                    while i < len(events) - 1 and events[i][numProcessTag] == processId:
                        bar()
                        i += 1
                processId = events[i][numProcessTag]
                processCodeJudge = events[i][codeJudgeTag]
                processSubjectCode = events[i][codeSubjectTag]
                processSubject = events[i][subjectTag]
                processSection = events[i][sectionTag]
                processFinished = utilities.getProcessState('unfinished')
                processStartDate = events[i][dateTag]
                processStartDateDt = dt.datetime.strptime(processStartDate, '%Y-%m-%d %H:%M:%S')
                processEventSequence = []
                processPhaseSequence = []
                processStateSequence = []
                eventDurationSequence = []
                phaseDurationSequence = []
                stateDurationSequence = []
                processEventSequenceComplete = []
                processPhaseSequenceComplete = []
                processStateSequenceComplete = []
                durationSequenceComplete = []
                processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processSubjectCode, subjectTag: processSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
                if i < len(events) - 1:
                    end = False
                continuative = False
            else:
                if events[i][codeStateTag] in stallStates and not continuative:
                    processFinished = utilities.getProcessState('continuatived')
                    continuative = True
                if events[i][phaseDBTag] == endPhase and not continuative: 
                    processFinished = utilities.getProcessState('finished')
                    processEvents[finishedTag] = processFinished
                    end = True
                if events[i][codeJudgeTag] != processCodeJudge:
                    processCodeJudge = events[i][codeJudgeTag]
                    processEvents[codeJudgeTag] = processCodeJudge
                if events[i][sectionTag] != processSection:
                    processSection = events[i][sectionTag]
                    processEvents[sectionTag] = processSection
                processDate = events[i][dateTag]
                processDateDt = dt.datetime.strptime(processDate, '%Y-%m-%d %H:%M:%S')
                duration = (processDateDt - processStartDateDt).days
                processEvents[eventsTag].append(events[i])
                codeEvent = events[i][codeEventTag]
                phase = events[i][phaseDBTag]
                if phase == None:
                    phase = '0.0'
                codeState = events[i][codeStateTag]
                if len(processEventSequence) == 0 or codeEvent != processEventSequence[-1]:
                    processEventSequence.append(codeEvent)
                    eventDurationSequence.append(duration)
                processEventSequenceComplete.append(codeEvent)
                if len(processPhaseSequence) == 0 or phase != processPhaseSequence[-1]:
                    processPhaseSequence.append(phase)
                    phaseDurationSequence.append(duration)
                processPhaseSequenceComplete.append(phase)
                if len(processStateSequence) == 0 or codeState != processStateSequence[-1]:
                    processStateSequence.append(codeState)
                    stateDurationSequence.append(duration)
                processStateSequenceComplete.append(codeState)
                durationSequenceComplete.append(duration)
            bar()
            i += 1
    if not end:
        allProcessEvents.append(processEvents)
        if len(durationSequenceComplete) > 0:
            processDict = dict.fromkeys(dfColumns)
            processDict = {x: 0 for x in processDict}
            processDict.update({numProcessTag: processId})
            processDict.update({dateTag: utilities.distanceAtToday(processStartDateDt)})
            processDict.update({codeJudgeTag: processCodeJudge})
            processDict.update({codeSubjectTag: processSubjectCode})
            processDict.update({sectionTag: processSection})
            processDict.update({finishedTag: processFinished})
            processDict.update({durationFinalTag: durationSequenceComplete[-1]})
            for i in range(len(processEventSequenceComplete)):
                codeEvent = processEventSequenceComplete[i]
                phase = processPhaseSequenceComplete[i]
                if phase == None:
                    phase = '0.0'
                codeState = processStateSequenceComplete[i]
                duration = durationSequenceComplete[i]
                eventCount = processDict.get(eventTag + ": " + codeEvent)
                phaseCount = processDict.get(phaseDBTag + ": " + phase)
                stateCount = processDict.get(stateTag + ": " + codeState)
                processDict.update({eventTag + ": " + codeEvent: eventCount + 1})
                processDict.update({phaseDBTag + ": " + phase: phaseCount + 1})
                processDict.update({stateTag + ": " + codeState: stateCount + 1})
                processDict.update({durationTag: duration})
                if processFinished == utilities.getProcessState('finished'):
                    allProcessDict.append(processDict.copy())
            if processFinished == utilities.getProcessState('unfinished'):
                allProcessDict.append(processDict.copy())
    processInfoDataframe = pd.DataFrame.from_dict(allProcessDict)
    return allProcessEvents, processInfoDataframe

# update events dataframe.
def updateEventsDataframe(eventsDataframe, statesNameDataframe, courtHearingsEventsType, endPhase, codeStateTag, codeEventTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag):
    eventsDataframeComplete = frame.joinDataframe(eventsDataframe, statesNameDataframe, codeStateTag, phaseDBTag, [phaseDBTag, stateTag])
    allEventsDataframe = frame.createEventsDataFrame(eventsDataframeComplete, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    updateAllEventsDataframe(allEventsDataframe)
    updateCourtHearingEventsDataframe(allEventsDataframe, courtHearingsEventsType, codeEventTag)
    updateStateEventsDataframe(allEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag)
    updatePhaseEventsDataframe(allEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag)

# update all events dataframe.
def updateAllEventsDataframe(allEventsDataframe):
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateCourtHearingEventsDataframe(courtHearingEventsDataframe, courtHearingsEvents, codeEventTag):
    if courtHearingsEvents != None and len(courtHearingsEvents) > 0:
        courtHearingEventsDataframe = courtHearingEventsDataframe[courtHearingEventsDataframe[codeEventTag].isin(courtHearingsEvents)]
    cache.updateCache('courtHearingEvents.json', courtHearingEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(stateEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag):
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, codeStateTag], as_index = False).first()
    try:
        importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
        if importantStates != None and len(importantStates) > 0:
            stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[codeStateTag].isin(importantStates)]
    except:
        pass
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(phaseEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag):
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, statesName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, eventTag, eventsTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    [processesDuration, eventsDuration, phasesDuration, statesDuration, courtHearingsDuration] = calcTypeDuration(processEvents, statesName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    [eventsDurationDataframe, eventsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(eventsDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    [phasesDurationDataframe, phasesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(phasesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    [statesDurationDataframe, statesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(statesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    [courtHearingsDurationDataframe, courtHearingsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(courtHearingsDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)
    cache.updateCache('eventsDurationFiltered.json', eventsDurationDataframeFiltered)
    cache.updateCache('phasesDuration.json', phasesDurationDataframe)
    cache.updateCache('phasesDurationFiltered.json', phasesDurationDataframeFiltered)
    cache.updateCache('statesDuration.json', statesDurationDataframe)
    cache.updateCache('statesDurationFiltered.json', statesDurationDataframeFiltered)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    cache.updateCache('courtHearingsDurationFiltered.json', courtHearingsDurationDataframeFiltered)
    return processesDuration

# calc types durations.
def calcTypeDuration(processEvents, statesName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][numProcessTag]
            processCodeJudge = processEvents[i][codeJudgeTag]
            processSubjectCode = processEvents[i][codeSubjectTag]
            processSubject = processEvents[i][subjectTag]
            processFinished = processEvents[i][finishedTag]
            processSection = processEvents[i][sectionTag]
            [processEventsDuration, eventsSequence, eventPhaseSequence, processPhasesDuration, phasesSequence, processStateDuration, statesSequence, courtHearingDuration, duration, startDate, startEventId, endDate, endId] = getDurations(processEvents[i], processId, processSubjectCode, processSubject, processFinished, statesName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag)
            if duration != None:
                processDuration = (processId, duration, startDate, startEventId, processCodeJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDate, endId)
                eventsDuration.extend(processEventsDuration)
                phasesDuration.extend(processPhasesDuration)
                statesDuration.extend(processStateDuration)
                courtHearingsDuration.extend(courtHearingDuration) 
                processesDuration.append(processDuration)
            bar()
    return [processesDuration, eventsDuration, phasesDuration, statesDuration, courtHearingsDuration]

# return duration.
def getDurations(processEvents, processId, processSubjectCode, processSubject, processFinished, statesName, courtHearingTypes, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag):
    events = processEvents[eventsTag]
    if len(events) == 0:
        return [[], [], [], [], [], [], [], [], None, None, None, None, None]
    eventsDuration = []
    eventsSequence = []
    eventsPhaseSequence = []
    phasesDuration = []
    phasesSequence = []
    statesDuration = []
    statesSequence = []
    courtHearingsDuration = []
    courtHearing = False
    startProcessDate = events[0][dateTag]
    startProcessEventId = events[0][numEventTag]
    endProcessDate = events[-1][dateTag]
    endProcessEventId = events[-1][numEventTag]
    startPhaseEvent = events[0]
    startStateEvent = events[0]
    startProcessDateDt = dt.datetime.strptime(startProcessDate, '%Y-%m-%d %H:%M:%S')
    endProcessDateDt = dt.datetime.strptime(endProcessDate, '%Y-%m-%d %H:%M:%S')
    processDuration = (endProcessDateDt - startProcessDateDt).days
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currEventCode = curr[codeEventTag]
        nextEventCode = next[codeEventTag]
        currStateCode = curr[codeStateTag]
        nextStateCode = next[codeStateTag]
        currPhase = frame.getPhaseOfState(statesName, currStateCode, phaseTag)
        nextPhase = frame.getPhaseOfState(statesName, nextStateCode, phaseTag)
        if curr[codeEventTag] != next[codeEventTag]:
            currEventId = curr[numEventTag]
            nextEventId = next[numEventTag]
            currEventTag = curr[eventTag]
            currJudgeCode = curr[codeJudgeTag]
            currDate = curr[dateTag]
            nextDate = next[dateTag]
            currStateTag = curr[stateTag]
            currSection = curr[sectionTag]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currStateCode, currStateTag, currPhase, processSubjectCode, processSubject, currSection, processFinished, nextDate, nextEventId])
            eventsPhaseSequence.append(currPhase)
            eventsSequence.append(currEventTag)
        if currPhase != nextPhase:
            nextPhaseEvent = next
            startEventId = startPhaseEvent[numEventTag]
            nextEventId = nextPhaseEvent[numEventTag]
            startEventCode = startPhaseEvent[codeEventTag]
            startEventTag = startPhaseEvent[eventTag]
            startJudgeCode = startPhaseEvent[codeJudgeTag]
            startDate = startPhaseEvent[dateTag]
            nextDate = nextPhaseEvent[dateTag]
            startStateCode = startPhaseEvent[codeStateTag]
            startStateTag = startPhaseEvent[stateTag]
            startPhase = frame.getPhaseOfState(statesName, startStateCode, phaseTag)
            startSection = startPhaseEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            phasesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
            if startPhase == '-':
                startPhaseEvent = next
            elif len(phasesSequence) == 0:
                phasesSequence.append(startPhase)
            elif phasesSequence[-1] == "RESTART":
                 if startPhase != '-' and int(startPhase) > int(phasesSequence[-2]):
                    phasesSequence.append(startPhase)
            else:
                if startPhase != '-' and int(startPhase) > int(phasesSequence[-1]):
                    phasesSequence.append(startPhase)
                elif startPhase != '-' and int(startPhase) < int(phasesSequence[-1]):
                    phasesSequence.append("RESTART")
            startPhaseEvent = next
        if currStateCode != nextStateCode:
            nextStateEvent = next
            startEventId = startStateEvent[numEventTag]
            nextEventId = nextStateEvent[numEventTag]
            startEventCode = startStateEvent[codeEventTag]
            startEventTag = startStateEvent[eventTag]
            startJudgeCode = startStateEvent[codeJudgeTag]
            startDate = startStateEvent[dateTag]
            nextDate = nextStateEvent[dateTag]
            startStateCode = startStateEvent[codeStateTag]
            startStateTag = startStateEvent[stateTag]
            startPhase = frame.getPhaseOfState(statesName, startStateCode, phaseTag)
            startSection = startStateEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            statesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
            if startStateTag not in statesSequence and currPhase != '-':
                statesSequence.append(startStateTag)
            startStateEvent = next   
        if currEventCode in courtHearingTypes and not courtHearing:
            startCourtHearingEvent = curr
            courtHearing = True
        if nextEventCode not in courtHearingTypes and courtHearing:
            endCourtHearingEvent = curr
            courtHearing = False
            startEventId = startCourtHearingEvent[numEventTag]
            nextEventId = endCourtHearingEvent[numEventTag]
            startEventCode = startCourtHearingEvent[codeEventTag]
            startEventTag = startCourtHearingEvent[eventTag]
            startJudgeCode = startCourtHearingEvent[codeJudgeTag]
            startDate = startCourtHearingEvent[dateTag]
            nextDate = endCourtHearingEvent[dateTag]
            startStateCode = startCourtHearingEvent[codeStateTag]
            startStateTag = startCourtHearingEvent[stateTag]
            startPhase = frame.getPhaseOfState(statesName, startStateCode, phaseTag)
            startSection = startCourtHearingEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            courtHearingsDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    curr = events[-1]
    currEventCode = curr[codeEventTag]
    currEventTag = curr[eventTag]
    currStateCode = curr[codeStateTag]
    currStateTag = curr[stateTag]
    currDateDt = dt.datetime.strptime(curr[dateTag], '%Y-%m-%d %H:%M:%S')
    currPhase = frame.getPhaseOfState(statesName, currStateCode, phaseTag)
    if currPhase == endPhase:
        currEventCode = curr[codeEventTag]
        currEventId = curr[numEventTag]
        currJudgeCode = curr[codeJudgeTag]
        currDate = curr[dateTag]
        currStateTag = curr[stateTag]
        currSection = curr[sectionTag]
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, 0, currDate, currJudgeCode, currStateCode, currStateTag, currPhase, processSubjectCode, processSubject, currSection, processFinished, currDate, currEventId]) 
        startEventId = startPhaseEvent[numEventTag]
        nextEventId = curr[numEventTag]
        startEventCode = startPhaseEvent[codeEventTag]
        startEventTag = startPhaseEvent[eventTag]
        startJudgeCode = startPhaseEvent[codeJudgeTag]
        startDate = startPhaseEvent[dateTag]
        nextDate = curr[dateTag]
        startStateCode = startPhaseEvent[codeStateTag]
        startStateTag = startPhaseEvent[stateTag]
        startSection = startPhaseEvent[sectionTag]
        startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - startDateDt).days
        phasesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, currPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    if currPhase == endPhase:
        startEventId = startStateEvent[numEventTag]
        nextEventId = curr[numEventTag]
        startEventCode = startStateEvent[codeEventTag]
        startEventTag = startStateEvent[eventTag]
        startJudgeCode = startStateEvent[codeJudgeTag]
        startDate = startStateEvent[dateTag]
        nextDate = curr[dateTag]
        startStateCode = startStateEvent[codeStateTag]
        startStateTag = startStateEvent[stateTag]
        startPhase = frame.getPhaseOfState(statesName, startStateCode, phaseTag)
        startSection = startStateEvent[sectionTag]
        startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - startDateDt).days
        statesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    if currEventCode in courtHearingTypes:
        if not courtHearing:
            startCourtHearingEvent = curr
        endCourtHearingEvent = curr
        startEventId = startCourtHearingEvent[numEventTag]
        nextEventId = endCourtHearingEvent[numEventTag]
        startEventCode = startCourtHearingEvent[codeEventTag]
        startEventTag = startCourtHearingEvent[eventTag]
        startJudgeCode = startCourtHearingEvent[codeJudgeTag]
        startDate = startCourtHearingEvent[dateTag]
        nextDate = endCourtHearingEvent[dateTag]
        startStateCode = startCourtHearingEvent[codeStateTag]
        startStateTag = statesName.get(startStateCode)[stateTag]
        startPhase = frame.getPhaseOfState(statesName, startStateCode, phaseTag)
        startSection = startCourtHearingEvent[sectionTag]
        startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - startDateDt).days
        courtHearingsDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    if currEventCode in courtHearingTypes:
        if not courtHearing:
            startCourtHearingEvent = curr
    if len(eventsSequence) == 0 or currEventTag != eventsSequence[-1]:
        eventsPhaseSequence.append(currPhase)
        eventsSequence.append(currEventTag)
    if len(phasesSequence) > 1 and phasesSequence[-1] == "RESTART":
        if currPhase != '-' and int(currPhase) > int(phasesSequence[-2]):
            phasesSequence.append(currPhase)
    elif len(phasesSequence) > 0:
        if currPhase != '-' and int(currPhase) > int(phasesSequence[-1]):
            phasesSequence.append(currPhase)
        elif currPhase != '-' and int(currPhase) < int(phasesSequence[-1]):
            phasesSequence.append("RESTART")
    else:
        if currPhase != '-':
            phasesSequence.append(currPhase)
    if (len(statesSequence) == 0 or currStateTag not in statesSequence) and currPhase != '-':
        statesSequence.append(currStateTag)
    return [eventsDuration, eventsSequence, eventsPhaseSequence, phasesDuration, phasesSequence, statesDuration, statesSequence, courtHearingsDuration, processDuration, startProcessDate, startProcessEventId, endProcessDate, endProcessEventId]

# update process duration dataframe.
def updateProcessDurationDataframe(processDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag):
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processDuration, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag, codeSubjectTag)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    cache.updateCache('processesDurationFiltered.json', processDurationDataframeFiltered)

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    if not connect.doesATableExist(connection, "eventi"):
        raise Exception("\n'eventi' table is not present or is called differently than 'eventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "eventi", ['numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale'], ['BIGINT', 'BIGINT', 'VARCHAR(4)', 'TEXT', 'DATETIME', 'VARCHAR(5)', 'VARCHAR(5)']):
        raise Exception("\n'eventi' table does not have all requested columns. The requested columns are: 'numEvento'(BIGINT), 'numProcesso'(BIGINT), 'codice'(VARCHAR(4)), 'giudice'(TEXT), 'data'(DATETIME), 'statoiniziale'(VARCHAR(5)), 'statofinale'VARCHAR(5))")
    if not connect.doesATableExist(connection, "processi"):
        raise Exception("\n'processi' table is not present or is called differently than 'processi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "processi", ['numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione'], ['BIGINT', 'DATETIME', 'TEXT', 'VARCHAR(10)', 'VARCHAR(5)']):
        raise Exception("\n'processi' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'dataInizio'(DATETIME), 'giudice'(TEXT), 'materia'(VARCHAR(10)), 'sezione'(VARCHAR(5))")
    if not connect.doesATableExist(connection, "tipoeventi"):
        raise Exception("\n'tipoeventi' table is not present or is called differently than 'tipoeventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipoeventi", ['CCDOEV', 'CDESCR'], ['VARCHAR(10)', 'TEXT']):
        raise Exception("\n'tipoeventi' table does not have all requested columns. The requested columns are: 'CCDOEV'(VARCHAR(10)), 'CDESCR'(TEXT)")
    if not connect.doesATableExist(connection, "tipomaterie"):
        raise Exception("\n'tipomaterie' table is not present or is called differently than 'tipomaterie'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipomaterie", ['codice', 'DESCOGGETTO', 'DESCCOMPLETA', 'rituale'], ['BIGINT', 'TEXT', 'TEXT', 'TEXT']):
        raise Exception("\n'tipomaterie' table does not have all requested columns. The requested columns are: 'codice'(BIGINT), 'DESCOGGETTO'(TEXT), 'DESCCOMPLETA'(TEXT), 'rituale'(TEXT)")
    if not connect.doesATableExist(connection, "tipostato"):
        raise Exception("\n'tipostato' table is not present or is called differently than 'tipostato'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipostato", ['CCODST', 'CDESCR', 'FKFASEPROCESSO'], ['VARCHAR(2)', 'VARCHAR(80)', 'VARCHAR(3)']):
        raise Exception("\n'tipostato' table does not have all requested columns. The requested columns are: 'CCODST'(VARCHAR(2)), 'CDESCR'(VARCHAR(80)), 'FKFASEPROCESSO'(VARCHAR(3))")
